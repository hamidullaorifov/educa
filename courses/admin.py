from django.contrib import admin
from .models import CustomUser, Subject, Course, Module,Comment,Content
# Register your models here.


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display= ['title','slug']
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk','slug','title','subject','created','price','owner']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['course','title']
    
    # class Meta:
    #     ordering = ('course',)  


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['course','author']
    
    


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['module']
    class Meta:
        ordering = ('module',)  

