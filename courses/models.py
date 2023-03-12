from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.db.models.signals import pre_save,post_delete,pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
from moviepy.editor import VideoFileClip
from .utils import duration_formatting




# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(null=True,blank=True,upload_to='images')
    # role = models.CharField(max_length=30,choices=(('student','Student'),('teacher','teacher')))


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
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images',null=True,blank=True)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    students = models.ManyToManyField(CustomUser,related_name='courses',blank=True)
    # course_duration_seconds = models.FloatField(null=True,blank=True)
    is_ready = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})
    
    @property
    def picture_url(self):
        if self.picture:
            url=self.picture.url
        else:
            url='https://images.unsplash.com/photo-1571260899304-425eee4c7efc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8dW5pdmVyc2l0eSUyMHN0dWRlbnR8ZW58MHx8MHx8&w=1000&q=80'
        return url
    def average_rating(self):
        ratings = self.ratings.all()
        total_rating = sum(r.star for r in ratings)
        count = ratings.count()
        if not count==0:
            return total_rating/count
        else:
            return "No"
    

    @property
    def course_duration_seconds(self):
      return sum([m.module_duration_seconds for m in self.modules.all()])
      pass


    @property
    def duration(self):
        return duration_formatting(self.course_duration_seconds)

@receiver(pre_save,sender=Course)
def slugify_title(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    # if not instance.course_duration_seconds:
    #     instance.course_duration_seconds = sum([m.module_duration_seconds for m in instance.modules.all()])


    








class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # module_duration_seconds = models.FloatField(null=True,blank=True)
    order = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title


    @property
    def owner(self):
        return self.course.owner
    
    @property
    def module_duration_seconds(self):
      return sum([c.duration_seconds for c in self.contents.all()])
      
    @property
    def duration(self):
        return duration_formatting(self.module_duration_seconds)


@receiver(pre_save,sender=Module)
def set_additional_fields(sender,instance,*args,**kwargs):
    # if not instance.module_duration_seconds:
    #     instance.module_duration_seconds = sum([c.duration_seconds for c in instance.contents.all()])
    if not instance.order:
        instance.order = instance.course.modules.count()+1



@receiver(post_delete,sender=Module)
def update_module_orders(sender,instance,*args,**kwargs):
    for module in instance.course.modules.filter(order__gt=instance.order):
        module.order = module.order-1
        module.save()

class Content(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='contents')
    video = models.FileField(upload_to='videos',blank=True,null=True)
    title = models.CharField(blank=True,null=True,max_length=250)
    order = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        ordering = ('order',)
    @property
    def video_url(self):
        url = ''
        try:
            url = self.video.url
        except:
            pass
        return url
    @property
    def owner(self):
        return self.module.course.owner

    @property
    def duration_seconds(self):
        if self.video_url:
            file = VideoFileClip(self.video.path)
            return int(file.duration)
        else:
            return 0

    @property
    def duration(self):
        print("DS",self.duration_seconds)
        return duration_formatting(self.duration_seconds)


@receiver(post_delete,sender=Content)
def update_content_orders(sender,instance,*args,**kwargs):
    for content in instance.module.contents.filter(order__gt=instance.order):
        content.order = content.order-1
        content.save()

@receiver(pre_delete,sender=Module)
def update_status_module_course(sender,instance,*args,**kwargs):
    instance.course.is_ready = False
    instance.course.save()



@receiver(pre_delete,sender=Content)
def update_status_module_course(sender,instance,*args,**kwargs):
    instance.module.course.is_ready = False
    instance.module.course.save()

@receiver(pre_save,sender=Content)
def set_order(sender,instance,*args,**kwargs):
    if not instance.order:
        instance.order = instance.module.contents.count()+1



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
