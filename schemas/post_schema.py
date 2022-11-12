from init import ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp, Range
from marshmallow.exceptions import ValidationError
from datetime import datetime

class PostSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude = ['posts', 'comments', 'post_reacts', 'comment_reacts', 'friendships1', 'friendships2'])

    title = fields.String(required=True, validate=Length(min=1, max=150, error='Invalid number of characters.'))
    text = fields.String(required=True, validate=Length(min=1, max=400, error='Invalid number of characters.'))
    date_time = fields.DateTime(load_default=datetime.now())
    user_id = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'title', 'text', 'date_time', 'user_id')