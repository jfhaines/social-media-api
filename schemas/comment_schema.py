from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])
    post = fields.Nested('PostSchema')

    text = fields.String(required=True, validate=And(
        Regexp('[a-zA-Z0-9!?]*', error='Invalid input for comment text'),
        Length(min=1, max=400, error='Text has the wrong number of characters')
        ))
    date_time = fields.DateTime(required=True, load_default=datetime.now())
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)

    @validates('date_time')
    def validate_date_time(self, value):
        if value >= datetime.now():
            raise ValidationError('You cannot set a future time and date')


    class Meta:
        fields = ('id', 'text', 'datetime', 'user_id', 'post_id')