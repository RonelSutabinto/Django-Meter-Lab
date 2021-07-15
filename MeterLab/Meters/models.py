import datetime
from decimal import Decimal
from django.db import models
from datetime import date
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class meters(models.Model):
    id = models.AutoField(primary_key=True)
    dateforwarded = models.DateField(("Date"), default=date.today)
    rrnumber = models.CharField(max_length=145, db_index=True)
    brand = models.CharField(max_length=145)
    metertype = models.CharField(max_length=145, null=True)
    serialnos = models.CharField(max_length=145, null=True)
    units = models.IntegerField(default=0)              # meter count
    active = models.PositiveSmallIntegerField(
        default=0, null=False)        # active, deleted

    userid = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "meters"

class meterserials(models.Model):
    id = models.AutoField(primary_key=True)
    idmeters = models.ForeignKey(
        meters, db_column='idmeters', related_name="meters", on_delete=models.CASCADE)
    serialno = models.CharField(max_length=45, null=False)
    ampheres = models.CharField(max_length=45, null=True)
    accuracy = models.CharField(max_length=45, null=True)
    wms_status = models.PositiveSmallIntegerField(
        default=0, null=True)    # 0=forwarded, 1=pending, 2=returned
    status  = models.PositiveSmallIntegerField(
        default=0, null=True)    # pending, passed, failed
    active = models.PositiveSmallIntegerField(
        default=0, null=True)        # active, deleted

    userid = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "meter_serials"

class meterserials_details(models.Model):
    id = models.AutoField(primary_key=True)
    idmeterserials = models.ForeignKey(meters, db_column='idmeterserials', related_name="meter_serials", on_delete=models.CASCADE)
    testdate = models.DateField(("Date"), default=date.today)
    gen_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fullload_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fl1 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fl2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    fl3 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    lightload_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    ll1 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    ll2 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    ll3 = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    reading = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    type = models.PositiveSmallIntegerField(default=0, null=True)        # type, class
    volts = models.CharField(max_length=45)
    phase = models.CharField(max_length=45)
    kh = models.CharField(max_length=45)
    ta = models.CharField(max_length=45)
    remarks = models.CharField(max_length=245)

    active = models.PositiveSmallIntegerField(default=0, null=True)        # active, deleted
    isdamage = models.BooleanField(default=False)
    userid = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "meter_serials_details"
        # abstract = True




