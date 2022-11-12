from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime

class PostReactSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])
    post = fields.Nested('PostSchema')

    type = fields.Integer(required=True, validate=Range(1, 5, error='Not a valid option.'))
    date_time = fields.DateTime(load_default=datetime.now())
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'type','date_time', 'user_id', 'post_id')