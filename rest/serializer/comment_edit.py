from rest_framework import serializers

from users.models.comment import Comment
import datetime

class CommentEdit(serializers.Serializer):

    object_id = serializers.IntegerField(min_value=1)
    edit_comment = serializers.CharField(max_length=200)

    def comment_edit(self, request):
        validated_data = self.validated_data
        comment_object = Comment.objects.get(id=validated_data['object_id'])
        print(comment_object.date_create.time())
        print(datetime.datetime.now(tz=None).time())
        time_difference = datetime.datetime.now() - datetime.timedelta(minutes=15)
        print(time_difference)
        if request.user == comment_object.user and comment_object.date_create.time() > time_difference.time():
            comment_object.comment = validated_data['edit_comment']
            comment_object.save()
            return {'status': 'comment was edited'}
        else:
            return {'status': 'it is not your comment'}