from django.db import models
from datetime import datetime


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    heading0 = models.CharField(max_length=140)
    post0 = models.TextField()
    heading1 = models.CharField(max_length=140)
    post1 = models.TextField()
    pub_date = models.DateField()
    file_name = models.FileField(upload_to='image',default=0)

    def __str__(self):
        return str(self.news_id) + '-' + self.title + ' - - - ' + self.heading0

    def get_absolute_url(self):
     return f"/{self.title.replace(' ', '-')}/"

class Comment(models.Model):
    post_id = models.ForeignKey(News, on_delete=models.CASCADE, default=0, related_name='comments')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE,null=True,related_name='replies')
    user_name =models.CharField(max_length=20, default=0)
    msg = models.TextField()
    com_date = models.DateTimeField(default=datetime.now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.msg

class Contact(models.Model):
    Contact_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=120)
    Password = models.CharField(max_length=15,default=0)
    Re_Password = models.CharField(max_length=15,default=0)
    Phone = models.IntegerField()
    com_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.Contact_id) + '-' + self.Name

class Message(models.Model):
    mess_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=500)
    mes_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name