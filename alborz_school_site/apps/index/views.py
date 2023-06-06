from django.shortcuts import render
from django.views import View
from django.conf import settings


#----------------------------------------- media loader in each page 
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}
#----------------------------------------- -------------------------

#----------------------------------------- media loader in each page 
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'index.html')
#----------------------------------------- media loader in each page 
class ContactUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'contactus_app/contact-us.html')
#----------------------------------------- media loader in each page 
class BlogsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'blog_app/blogs.html')
#----------------------------------------- media loader in each page 
class AboutUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'aboutus_app/about-us.html')