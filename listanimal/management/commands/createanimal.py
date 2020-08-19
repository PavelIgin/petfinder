from django.core.management.base import BaseCommand
from listanimal.models import AnimalInfo,AnimalColor,AnimalType
import json,requests
from django.core.mail import send_mail
from django.conf import settings
from listanimal.models import NewestLogFileContent
import vk_api
import logging
from django.utils import timezone
logger = logging.getLogger('commands.createanimal')


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.createanimal()


    def createanimal(self):
        data = {'grant_type': 'client_credentials', 'client_id': settings.CLIENT_ID, 'client_secret': settings.CLIENT_SECRET}
        r = requests.post('https://api.petfinder.com/v2/oauth2/token', data=json.dumps(data), verify=False)
        token_petfinder = json.loads(r.text)['access_token']
        headers = {'Authorization': 'Bearer ' + token_petfinder}
        r = requests.get('https://api.petfinder.com/v2/animals?page=1', headers=headers, verify=False)
        j = json.loads(r.text)
        dict_animal = j.get('animals')
        summ_new_animals = ''
        for one_animal in dict_animal:
            animal_type = AnimalType.objects.get_or_create(animal_type=one_animal['type'])[0]
            animal_color = None
            if one_animal['colors']['primary'] is not None:
                animal_color = AnimalColor.objects.get_or_create(primary=one_animal['colors']['primary'])[0]
            url_animals = []
            for i in one_animal['photos']:
                url_animals.append(i['full'])
            defaults = {'animal_type': animal_type, 'color': animal_color,
                        'age': one_animal['age'], 'gender': one_animal['gender'],
                        'size': one_animal['size'], 'photos': url_animals,
                        'name': one_animal['name'], 'status': one_animal['status']}
            create_object, is_created = AnimalInfo.objects.update_or_create(number=one_animal['id'], defaults=defaults)
            if is_created:
                summ_new_animals += '\n' + 'Новое объявление:' + str(animal_type) + '' + defaults['name']
                self.vk_wall_post(one_animal,animal_type)
        self.send_massage(summ_new_animals,one_animal)

    def vk_wall_post(self,one_animal,animal_type):
        vk_session = vk_api.VkApi(settings.LOGIN, settings.PASSWORD, token=settings.ACESS_TOKEN_ATTACHEMENT)
        try:
            vk_session.method('wall.post', {'owner_id': -settings.GROUP_ID,
                                        'from_group': 1,
                                        'message': 'Номер животного:{}\nТип животного:{}'
                                                   '\nВозраст:{}\nПол:{}\nГабариты:{}\nИмя:{}\nСтатус поиска:{}\n'
                                                   'Цвет:{}\nФотографии{}'.format(
                                            one_animal.get('number', None),
                                            animal_type,
                                            one_animal['age'],
                                            one_animal['gender'],
                                            one_animal['size'],
                                            one_animal['name'],
                                            one_animal['status'],
                                            one_animal.get('color', None),
                                            one_animal.get('photos', None)
                                        )})

        except vk_api.VkApiError:
            logger.error(msg='Ошибка отправки объявления в вк:{},{}'.format(one_animal['name'],timezone.now()))
            log_db = open('listanimal/logger/advertisement.log', 'r')
            NewestLogFileContent.objects.update_or_create(log_filename='commands.advertisement',defaults={'content':log_db.readlines()[-100:-1]})
            log_db.close()

    def send_massage(self,summ_new_animals,one_animal):
        if summ_new_animals != '':
            send_mail('новое объявление епта', summ_new_animals, 'dkdjjdkd@gmail.com', ['paveligin1861@gmail.com'],
                      fail_silently=False)
        elif summ_new_animals == '':
            send_mail('нет объявленией', 'объявлений нет', 'dkdjjdkd@gmail.com', ['paveligin1861@gmail.com'],
                      fail_silently=False)
        return one_animal








