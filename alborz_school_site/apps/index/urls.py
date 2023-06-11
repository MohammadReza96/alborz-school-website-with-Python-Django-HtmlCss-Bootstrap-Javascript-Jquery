from django.urls import path,include
from .views import IndexView,ContactUsView,AboutUsView,TeacherListView

app_name='index'
urlpatterns = [
    path("",IndexView.as_view(),name='home' ),
    path("contact-us/",ContactUsView.as_view(),name='contact' ),
    path("about-us/",AboutUsView.as_view(),name='about_us' ),
    path("teacher-list/",TeacherListView.as_view(),name='teacher_list' ),
]