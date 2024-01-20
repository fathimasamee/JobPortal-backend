from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class JobSeeker(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),

    ]
    phnNo_validator = RegexValidator(
        regex=r'^(?:7|0|(?:\+94))[0-9]{9,10}$',
        message='Enter a valid Sri Lankan phone number.'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(validators=[phnNo_validator],max_length=12)
    address = models.TextField()
    education = models.CharField(max_length=100)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobseeker')
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker')





