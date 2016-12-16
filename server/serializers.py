from marshmallow import Schema, fields

class PostSerializer(Schema):
    id = fields.Str();
    title = fields.Str();
    body = fields.Str();
    created_at = fields.LocalDateTime("%Y-%m-%d %H:%M:%S");