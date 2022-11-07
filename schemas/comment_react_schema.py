from init import ma
from marshmallow import fields

class CommentReactSchema(ma.Schema):
    user_id = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])
    post_id = fields.Nested('PostSchema')

    class Meta:
        fields = ('id', 'type','datetime', 'user_id', 'post_id')