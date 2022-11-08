from init import ma
from marshmallow import fields

class FriendRequestSchema(ma.Schema):
    friend1 = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])
    friend2 = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])

    class Meta:
        fields = ('id', 'datetime', 'friend1_id', 'friend2_id')