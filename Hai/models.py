from django.db import models


class AuthUserT(models.Model):
    authId = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    token  = models.CharField(max_length=255, blank=True)


class ContactUserT(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    adress = models.CharField(max_length=255, blank=True)
    userEmail = models.EmailField(max_length=255, blank=True)
    authId = models.ForeignKey(AuthUserT, on_delete=models.CASCADE)
    is_valid = models.IntegerField(default=1)


    def __unicode__(self):
        return '%d: %d' % (self.userId, self.authId)
