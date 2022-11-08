from init import ma
from marshmallow import fields

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])
    post = fields.Nested('PostSchema')

    class Meta:
        fields = ('id', 'text', 'datetime', 'user_id', 'post_id')