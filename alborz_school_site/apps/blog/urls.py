from django.urls import path,include
from .views import BlogsView

app_name='blog'
urlpatterns = [
    path("",BlogsView.as_view(),name='blogs' ),
    # path("blog/",BlogsView.as_view(),name='blogs' ),
]