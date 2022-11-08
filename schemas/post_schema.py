from init import ma
from marshmallow import fields

class PostSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])

    class Meta:
        fields = ('id', 'title', 'text', 'datetime', 'user_id')