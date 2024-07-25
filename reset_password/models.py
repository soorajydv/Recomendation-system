from django.db import models
from recomendation.models import User

# Create your models here.
class Otp(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    token = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'OTP'