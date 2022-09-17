from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('courses/comment/<int:pk>',views.post_comment,name='postcomment'),
    path('courses/feedback/<int:pk>',views.post_feedback,name='feedback'),
    path('courses/content/<int:pk>',views.course_content,name='course_content'),
    path('courses/addstudent/',views.add_user_to_students,name='entroll_course'),
    path('<slug:slug>',views.course_detail,name='course_detail'),

]
