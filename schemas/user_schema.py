from init import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    posts = fields.List(fields.Nested('PostSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))
    post_reacts = fields.List(fields.Nested('PostReactSchema', exclude=['user']))
    comment_reacts = fields.List(fields.Nested('CommentReactSchema', exclude=['user']))
    friend_requests_sent = fields.List(fields.Nested('FriendRequestSchema', exclude=['user']))
    friend_requests_received = fields.List(fields.Nested('FriendRequestSchema', exclude=['user']))
    friends1 = fields.List(fields.Nested('FriendSchema', exclude=['user']))
    friends2 = fields.List(fields.Nested('FriendSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'dob', 'is_admin')