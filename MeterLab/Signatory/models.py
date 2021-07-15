from django.db import models

# Create your models here.


class signatory(models.Model):
    id = models.AutoField(primary_key=True)
    calibratedby = models.CharField(max_length=45)
    calibratedby_position = models.CharField(max_length=45)
    checkedby = models.CharField(max_length=45)
    checkedby_position = models.CharField(max_length=45)
    notedby = models.CharField(max_length=45)
    notedby_position = models.CharField(max_length=45)

    preparedby = models.CharField(max_length=45)
    preparedby_position = models.CharField(max_length=45)
    receivedby = models.CharField(max_length=45)
    receivedby_position = models.CharField(max_length=45)

    class Meta:
        db_table = "signatory"
