from django.forms import ModelForm
from courses.models import Course,Content,Module



class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','subject','overview','picture','price']
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['title','description']

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title','video']
    def __init__(self, *args, **kwargs):
        super(ContentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'