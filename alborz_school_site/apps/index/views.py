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
        return render(request,'base.html')