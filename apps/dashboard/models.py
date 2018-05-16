from __future__ import unicode_literals
from django.db import models
from apps.login.models import User, UserManager
from apps.user.models import Description, DescriptionManager



class MessageManager(models.Manager):
    def validateMessage(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = 'Cannot create an empty message'
        return errors

    def createMessage(self, request):
        errors = self.validateMessage(request.POST)
        if errors:
            return errors
        Message.objects.create(content=request.POST['content'],sender=request.session['userid'],receiver=request.session['receiver'])

    def deleteMessage(self, messageID):
        Message.objects.get(id=messageID).delete()
        context = {
            'messageDeleted' : 'Successfully deleted message'
        }
        return context
        

class CommentManager(models.Manager):
    def validateComment(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['content'] = 'Cannot create an empty comment'
        return errors

    def createComment(self, request):
        errors = self.validateComment(request.POST)
        if errors:
            return errors
        Comment.objects.create(content=request.POST['content'],sender=request.session['userid'],message=request.POST['messageid'])

    def deleteComment(self, commentID):
        Comment.objects.get(id=commentID).delete()
        context = {
            'commentDeleted' : 'Successfully deleted comment'
        }
        return context



class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(Message, related_name="comments")
    sender = models.ForeignKey(User, related_name="comments")