from __future__ import unicode_literals
from django.db import models #pylint: disable = E0401
from apps.login.models import User, UserManager

class DescriptionManager(models.Manager):
    def validateDescription(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = 'Cannot create an empty description'
        return errors

    def createDescription(self, userID):
        Description.objects.create(content = "", user = User.objects.get(id=userID))
        return Description.objects.last()

    def updateDescription(self, content, userID):
        errors = self.validateDescription(content)
        if errors:
            return errors
        desc = Description.object.get(user=User.objects.get(id=userID))
        desc.content = content
        desc.save()
        return desc

class Description(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, related_name="description")
    objects = DescriptionManager()

