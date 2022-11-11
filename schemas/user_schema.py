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
        Regexp('[a-zA-Z0-9!?]*', error='Invalid characters.'),
        Length(min=1, max=100, error='Invalid number of characters.')
        ))
    email = fields.Email(required=True)
    dob = fields.String(required=True)
    password = fields.String(required=True, validate=Length(min=7, error='Invalid number of characters.'))
    is_admin = fields.Boolean(load_default=False)

    @validates('dob')
    def validate_dob(self, value):
        try:
            date_data = value.split('/')
            day = int(date_data[0])
            month = int(date_data[1])
            year = int(date_data[2])
            date(year, month, day)
        except:
            raise ValidationError('Must be a valid date represented as a string in the "DD/MM/YYYY" format.')

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'dob', 'is_admin')