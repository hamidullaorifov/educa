from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from datetime import datetime
# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(null=True,blank=True,upload_to='images')
    role = models.CharField(max_length=30,choices=(('student','Student'),('teacher','teacher')))


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(CustomUser,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images',null=True,blank=True)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})
    
    @property
    def picture_url(self):
        try:
            url=self.picture.url
        except:
            url=''
        return url
    def average_rating(self):
        ratings = self.ratings.all()
        total_rating = sum(r.star for r in ratings)
        count = ratings.count()
        if not count==0:
            return total_rating/count
        else:
            return ""

    

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='contents')
    content_type = models.ForeignKey(ContentType,
    on_delete=models.CASCADE,
    limit_choices_to={'model__in':(
                            'text',
                            'video',
                            'image',
                            'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(CustomUser,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class Image(ItemBase):
    content = models.FileField(upload_to='images')

class File(ItemBase):
    content = models.FileField(upload_to='files')


class Video(ItemBase):
    content = models.URLField()


class Comment(models.Model):
    course = models.ForeignKey(Course,related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    

class Rating(models.Model):
    course = models.ForeignKey(Course,related_name='ratings',on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    star = models.IntegerField(blank=True,null=True)
    feedback = models.TextField(null=True,blank=True)