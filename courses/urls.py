from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('courses/',views.paginate_courses,name='paginate_courses'),
    path('courses/comment/<int:pk>',views.post_comment,name='postcomment'),
    path('courses/feedback/<int:pk>',views.post_feedback,name='feedback'),
    path('courses/content/<int:pk>',views.course_content,name='course_content'),
    path('courses/addstudent/',views.add_user_to_students,name='entroll_course'),
    path('courses/module-details/<int:pk>',views.module_details,name='module_details'),
    path('courses/<slug:slug>',views.course_detail,name='course_detail'),

]
