from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime

class FriendshipSchema(ma.Schema):
    user1 = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])
    user2 = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])

    requester = fields.Integer(required=True, validate=Range(min=1, max=2, error='Not a valid option.'))
    status = fields.Integer(required=True, validate=Range(min=0, max=1, error='Not a valid option.'))
    date_time = fields.DateTime(load_default=datetime.now())
    user1_id = fields.Integer(required=True)
    user2_id = fields.Integer(required=True)

    @validates('date_time')
    def validate_date_time(self, value):
        if value >= datetime.now():
            raise ValidationError('You cannot set a future time and date.')

    class Meta:
        fields = ('id', 'date_time', 'user1_id', 'user2_id', 'requester', 'status')