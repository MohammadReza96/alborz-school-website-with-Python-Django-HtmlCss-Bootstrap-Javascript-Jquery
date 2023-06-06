from django.shortcuts import render

#------------------------------------------------------------- run error 404handler View
def handler404(request,exception=None):
    return render(request,'errorhandlers_app/handler404.html')