from tortoise import fields, models


class UserModel(models.Model):
    """
    The User model
    """

    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=64)
    name = fields.CharField(max_length=64, null=True)
    last_name = fields.CharField(max_length=64, null=True)
    is_active = fields.BooleanField(null=False, default=True)
    is_staff = fields.BooleanField(null=False, default=False)
    is_superuser = fields.BooleanField(null=False, default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table: str = 'users'
