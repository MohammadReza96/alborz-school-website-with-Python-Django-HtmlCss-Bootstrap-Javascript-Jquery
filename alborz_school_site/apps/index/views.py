from django.shortcuts import render
from django.views import View
from django.conf import settings
from apps.blog.models import Blog

#----------------------------------------- media loader in each page 
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}
#----------------------------------------- -------------------------

#----------------------------------------- index View
class IndexView(View):
    def get(self,request,*args,**kwargs):
        get_blogs=Blog.objects.filter(blog_is_active=True).order_by('blog_publish_date')
        return render(request,'index.html',{'blogs':get_blogs})
#----------------------------------------- media loader in each page 
class ContactUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'contactus_app/contact-us.html')
#----------------------------------------- media loader in each page 
class AboutUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'aboutus_app/about-us.html')