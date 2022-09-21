from django.forms import ModelForm
from courses.models import Course,Content,Module



class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','subject','overview','picture','price']


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title','description']



class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title','video']