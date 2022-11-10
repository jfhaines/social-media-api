from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime, date

class UserSchema(ma.Schema):
    posts = fields.List(fields.Nested('PostSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))
    post_reacts = fields.List(fields.Nested('PostReactSchema', exclude=['user']))
    comment_reacts = fields.List(fields.Nested('CommentReactSchema', exclude=['user']))
    friendships1 = fields.List(fields.Nested('FriendSchema', exclude=['user']))
    friendships2 = fields.List(fields.Nested('FriendSchema', exclude=['user']))

    username = fields.String(required=True, validate=And(
        Regexp('[a-zA-Z0-9!?]*', error='Invalid input for username'),
        Length(min=1, max=100, error='Username has the wrong number of characters')
        ))
    email = fields.Email(required=True)
    dob = fields.Date(required=True)
    password = fields.String(required=True, validate=Length(min=7, error='Password is not long enough'))
    is_admin = fields.Boolean(required=True, load_default=False)

    @validates('dob')
    def validate_dob(self, value):
        if value >= date.today():
            raise ValidationError('You cannot be born in the future')

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'dob', 'is_admin')