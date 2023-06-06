from django.urls import path,include
from .views import IndexView,ContactUsView,BlogsView,AboutUsView

app_name='index'
urlpatterns = [
    path("",IndexView.as_view(),name='home' ),
    path("contact-us/",ContactUsView.as_view(),name='contact' ),
    path("blogs/",BlogsView.as_view(),name='blogs' ),
    path("about-us/",AboutUsView.as_view(),name='about_us' ),
]