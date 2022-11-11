from init import ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime

class CommentReactSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])
    comment = fields.Nested('CommentSchema')

    type = fields.Integer(required=True, validate=Range(1, 5, error='Not a valid option.'))
    date_time = fields.DateTime(load_default=datetime.now())
    user_id = fields.Integer(required=True)
    comment_id = fields.Integer(required=True)

    @validates('date_time')
    def validate_date_time(self, value):
        if value >= datetime.now():
            raise ValidationError('You cannot set a future time and date.')

    class Meta:
        fields = ('id', 'type','datetime', 'user_id', 'post_id')