from django.http import HttpResponse
from urllib import response
from django.shortcuts import render

# def mymiddleware(get_response):
#     print("one time my_middleware initialized...")
#     def my_function(request):
#         print("this is my_middleware before view...")
#         response=get_response(request)
#         print("This is my_middleware after view")
#         return response
#     return my_function    

# class Mymiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print('one time mymiddleware initialized..')
#     def __call__(self,request):
#         print("this is mymiddleware before  classview")  
#         response=self.get_response(request)
#         print("This is mymiddleware after classview")
#         return response   
      
# class Brothermiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print("one time brother initialized..")
#     def __call__(self,request):
#         print("This is Brother before view..")
#         response=self.get_response(request)
#         print("This is Brother after Brother view")
#         return response    

# class Fathermiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print("one time father initialized")
#     def __call__(self,request):
#         print("This is father before view..")
#         response=self.get_response(request)
#         # return HttpResponse('leave it')
#         print("This is father after view") 
#         return response   

# class Mothermiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print("one time mother initialized..")
        
#     def __call__(self,request):
#             print("This is mother before view")
#             response=self.get_response(request)
#             print("This is mother after view")
#             return response        
class Myprocessmiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        response=self.get_response(request)
        return response
    def process_view(request,*args,**kwargs):
        print("This is process view before view")
        return None

class MyExceptionmiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        response=self.get_response(request)
        return response
    def process_exception(self,request,exception):
        print("Exception occured..")           
        msg=exception
        class_name=exception.__class__.__name__
        print(class_name)
        print(msg)
        return HttpResponse(msg)

        
class MyTemplateresponsemiddleware:
    def __init__(self,get_response):
        self.get_response=get_response       

    def __call__(self,request):
        response=self.get_response(request)
        return response
    def process_template_response(self,request,response):
        print("process templates response from middlware...")
        response.context_data['name']='prashanth'
        return response         



# site under contstruction
# class UnderConstructionMiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#     def __call__(self,request):
#         print("call from before middleware view...")
#         # response=self.get_response(request)
#         # response=HttpResponse('our website is under construction...')
#         response=render(request,'app/siteuc.html')
#         print("call from after middleware view..")
#         return response