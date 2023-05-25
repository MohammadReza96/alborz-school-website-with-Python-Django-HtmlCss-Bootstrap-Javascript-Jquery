from django.shortcuts import render
from django.views import View

#----------------------------------------- media loader in each page 
#----------------------------------------- -------------------------

#----------------------------------------- media loader in each page 
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'base.html')