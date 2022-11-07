from init import ma
from marshmallow import fields

class FriendRequestSchema(ma.Schema):
    sender_id = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])
    receiver_id = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friend_requests_sent', 'friend_requests_received', 'friends1', 'friends2'])


    class Meta:
        fields = ('id', 'datetime', 'sender_id', 'receiver_id')