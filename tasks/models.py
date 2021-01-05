from django.db import models

# Create your models here.
class Task(models.Model):
    name=models.CharField(max_length=120)
    body=models.TextField()
    customer=models.ForeignKey('auth.User',related_name='customer',on_delete=models.CASCADE)
    executor=models.ForeignKey('auth.User',related_name='executor',on_delete=models.CASCADE,blank=True,default=None,null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    completed=models.DateTimeField(blank=True,default=None,null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Comment(models.Model):
    task=models.ForeignKey('Task',on_delete=models.CASCADE)
    text=models.TextField()
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    answer=models.TextField(blank=True,default=None,null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} {} {}'.format(self.task,self.created,self.author)


class File(models.Model):
    file=models.FileField()
    name=models.CharField(max_length=45,blank=True,default=None,null=True)
    type=models.CharField(max_length=15,blank=True,default=None,null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE,blank=True,default=None,null=True)
    comment =  models.ForeignKey('Comment', on_delete=models.CASCADE,blank=True,default=None,null=True)

    def __str__(self):
        return '{}.{}'.format(self.name,self.type)