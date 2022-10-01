from django.urls import path
from . import views


urlpatterns = [
    # path('forbidden',views.forbidden,name='forbidden'),
    path('sort-modules/<int:pk>/<int:module_pk>',views.sort_modules,name='sort_modules'),
    path('sort-contents/<int:pk>/<int:module_pk>',views.sort_contents,name='sort_contents'),
    path('mycourses/',views.my_courses,name='mycourses'),
    path('create/',views.create_coure,name='create_course'),
    path('edit/<int:pk>',views.edit_course,name='edit_course'),
    path('delete/<int:pk>',views.delete_course,name='delete_course'),
    path('modules/<int:pk>',views.course_modules_details,name='course-modules'),
    path('modules/<int:pk>/<int:module_pk>',views.course_modules_details,name='course-modules'),
    path('get_module_contents/<int:pk>',views.get_module_contents,name='get_module_contents'),

    path('course/module/update/<int:id>',views.update_module,name='update_module'),
    path('course/module/delete/<int:id>',views.delete_module,name='delete_module'),
    path('course/<slug:slug>/module/create/',views.create_module,name='create_module'),


    path('course/content/update/<int:id>',views.update_content,name='update_content'),
    path('course/content/delete/<int:id>',views.delete_content,name='delete_content'),
    path('course/<int:pk>/content/create/',views.create_content,name='create_content'),
]
