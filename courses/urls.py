from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('<slug:slug>',views.course_detail,name='course_detail'),
    path('courses/comment/<int:pk>',views.post_comment,name='postcomment'),
    path('courses/feedback/<int:pk>',views.post_feedback,name='feedback'),
]
