from django.shortcuts import render,redirect
from datetime import datetime,timedelta
import datetime
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import forms,authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm,UserCreationForm,AuthenticationForm
import csv
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView,TemplateView
from django.views import View
from django.conf import settings
from django.core.cache import cache
from reportlab.pdfgen import canvas
from .forms import *
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Mobile
from django.core.mail import send_mail,BadHeaderError
from app.fun import handle_upload_file
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,Http404
import datetime
from django.db.models import Avg,Sum,Min,Max,Count
from app import signals
# Create your views here.
def index(request):
    now=datetime.datetime.now()
    html="<html><body><h3>Now time is %s.</h3></body></html>"% now
    return HttpResponse(html) 
# page not found    
def notfound(request):
    a=1
    if a:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>') #rendering the template in HttpResponse 
# http decorator
@require_http_methods(['GET'])
def show(request):
    return HttpResponse('<h1>This is Http Get request</h1>')
# static files 
def static(request):
    return render(request,'app/static.html')

#java script
def js(request):
    return render(request,'app/js.html')     

# loading template
def temp(request):
    name={'name':'prashanth'}
    template=loader.get_template('app/temp.html')
    return HttpResponse(template.render(name))

# modelform
def form(request):
    stu=StudentForm()
    stu.order_fields(field_order=['name','email'])
    return render(request,'app/form.html',{'form':stu})

# student form
def modelform(request):
    stu=EmpForm()
    return render(request,'app/modelform.html',{'stu':stu})

# form validation
def validate(request):
    if request.method=='POST':
        form=EmpForm(request.POST)
        if form.is_valid():
            try:
                return HttpResponse('Form submitted')
            except:
                pass
    else:
        form=EmpForm()
    return render(request,'app/validate.html',{'form':form})            

# file upload
def upload(request):
    if request.method=='POST':
        upload=UploadForm(request.POST,request.FILES)
        if upload.is_valid():
            handle_upload_file(request.FILES['file'])
            return HttpResponse('file uploaded successfully')
    else:
        upload=UploadForm()
    return render(request,'app/upload.html',{'form':upload})            

# connect new database display
def condb(request):
    user=Mobile.objects.all()
    context={'user':user}
    return render(request,'app/condb.html',context)

# django request and response

def request(request):
    return HttpResponse("Http request is " +request.method)

# django exception
def exception(request):
    try:
        data=Mobile.objects.get(id=2)
    except ObjectDoesNotExist:
        return HttpResponse("Exception:Data not found")
    return HttpResponse(data)        

# set session
def setsession(request):
    request.session['first_name']='prashanth'
    # request.session.set_expiry(10)
    return render(request,'app/setsession.html')
    # request.session['last_name']='nanda'
    # return HttpResponse('session is set')  
# cache
def chome(request):
    return render(request,'app/cache_home.html')
# contact cache
def ccontact(request):
    return render(request,'app/cache_contact.html')
# signal 
def ssignal(request):
    return HttpResponse('<h1>This is prashanth</h1>')
# page count
def count(request):
    ct=request.session.get('count', 0)
    newcount=ct + 1
    request.session['count']=newcount
    return render(request,'app/pagecount.html',{'c':newcount})
# get session
def getsession(request):
    if 'name' in request.session:
        name=request.session['first_name']
        request.session.modified=True
        return render(request,'app/getsession.html',{'name':name})     
    else:
        return HttpResponse('your session has been expired..')   
    # semail=request.session['last_name']
# del session
def delsession(request):
    request.session.flush()
    request.session.clear_expired()
    return render(request,'app/delsession.html')

# set cookies
def setcookie(request):
    response=render(request,'app/setcookie.html')
    response.set_signed_cookie('name','Chiranjeevi',salt='nm',expires=datetime.datetime.utcnow()+timedelta(days=2))
    return response

# get cookie
def getcookie(request):
    name=request.get_signed_cookie('name',default='Guest',salt='nm')
    return render(request,'app/getcookie.html',{'name':name})     
#delte cookie
def delcookie(requst):
    response=render(request,'app/delcookie.html')
    response.delete_cookie('name')
    return response
# csv files
def getcsvfile(request):
    response=HttpResponse(content_type='text/csv')
    response['content-disposition']='attachement;firlname="file.csv"'
    s=Employee.objects.all()
    writer=csv.writer(response)
    for employee in s:
        writer.writerow([employee.first_name,employee.last_name,employee.contact,employee.email,employee.age,])
    return response      

#Pdf genrator
def getpdffile(request):
    response=HttpResponse(content_type='application/pdf')     
    response['content-Disposition']='attachement;"file.pdf"'
    p=canvas.Canvas(response)
    p.setFont('Times-Roman',55)
    p.drawString(10,700,"prashanth nanda")
    p.showPage()
    p.save()
    return response      

# image upload and show
def image_request(request):
    if request.method=='POST':
        form=uploadimage(request.PO/ST,request.FILES)
        if form.is_valid():
            form.save()
            img_object=form.instance
        return render(request,'app/imageform.html',{'form':form,'img':img_object})
    else:
        form=uploadimage()
    return render(request,'app/imageform.html',{'form':form})    

#add and show views here..
def create(request):
    if request.method=='POST':
        form=CrudForm(request.POST)
        if form.is_valid():
            eid=form.cleaned_data['eid']
            ename=form.cleaned_data['ename']
            eemail=form.cleaned_data['eemail']
            econtact=form.cleaned_data['econtact']
            reg=Crud(eid=eid,ename=ename,eemail=eemail,econtact=econtact)
            reg.save()
            form=CrudForm()
    else:
        form=CrudForm()
    curd=Crud.objects.all()
    return render(request,'app/index.html',{'form':form,'curd':curd})             

# update
def update(request,id):
    if request.method=='POST':
        pi=Crud.objects.get(pk=id)
        form=CrudForm(request.POST,instance=pi)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create/')
    else:     
        pi=Crud.objects.get(pk=id)
        form=CrudForm(instance=pi)
    return render(request,'app/update.html',{"pi":pi,'form':form})       

# delete
def delete(request,id):
    if request.method=='POST':
        pi=Crud.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/create/')
class NewView(View):
    def get(self,request):
        return HttpResponse('response')

class MirrorCreate(CreateView):
    model=Mirror
    fields='__all__'  
    def re(request):
        return redirect('/create/')  
    
    

# retrive
class MirrorRetrive(ListView):
    model=Mirror
# detail
class MirrorDetail(DetailView):
    model=Mirror
#update view
class MirrorUpdate(UpdateView):
    model=Mirror
# delete    
class MirrorDelete(UpdateView):
    model=Mirror
    success_url='/'



# user creation form
def register(request):
    if request.POST=='POST':
        form=CustomUserCreationForm()
        if form.is_valid():
            form.save()
    else:
        form=CustomUserCreationForm()
        context={'form':form}
    return render(request,'app/register.html',context)

# def contact(request):
#     if request.method=='POST':
#         form=Contactform(request.POST)
#         if form.is_valid():
#             subject="contact"
#             body={
#                 'first_name':form.cleaned_data['first_name'],
#                 'last_name':form.cleaned_data['last_name'],
#                 'email':form.cleaned_data['email'],
#                 'comment':form.cleaned_data['comment'],
#                 'email':form.cleaned_data['email'],
#                 'agree':form.cleaned_data['agree'],
#                 'value':form.cleaned_data['value'],
#                 'gender':form.cleaned_data['Gender'],
#                 'rank':form.cleaned_data['rank'],
#                 'message':form.cleaned_data['message'],
#                 'date_of_birth':form.cleaned_data['date_of_birth']
#             }
#             message="\n".join(body.values())
#             try:
#                 send_mail(subject,message,'admin@example.com',['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('invalid header found')
#             return redirect("main:homepage")
#     form=Contactform()            
#     return render(request,'app/contactform.html',{'form':form})   
#home
def home(request,check):
    return render(request,'app/home.html',{'ch':check})
def convert(request,year):
    student={'id':year}
    return render(request,'app/convert.html',student)
# dynamic url
def dynamic(request):
    if request.method=='POST':
        form=DynamicForm(request.POST)
        if form.is_valid():
            print('form is valid')
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            repassword=form.cleaned_data['repassword']
            reg=Dynamic(name=name,email=email,password=password,repassword=repassword)
            reg.save()
            fm=Dynamic()
            return HttpResponseRedirect('/home/')
            
    else:
        form=DynamicForm()
    return render(request,'app/dy.html',{'form':form})            

# id 
def id(request,my_id):
    print(my_id)
    if my_id==1:
        student={'id':my_id,'name':'prashanth'}
    if my_id==2:
        student={'id':my_id,'name':'praveen'}
    if my_id==3:
        student={'id':my_id,'name':'pradeep'}
    return render(request,'app/id.html',student)    

# sub_id
def sub_id(request,my_id,my_subid):
    if my_id==1 and my_subid==5:
        student={'id':my_id,'name':'yakanna','my_subid':my_subid}
    if my_id==2 and my_subid==6:
        student={'id':my_id,'name':'manikanth','my_subid':my_subid}
    if my_id==3 and my_subid==7:
        student={'id':my_id,'name':'Rajinikanth','my_subid':my_subid}
    return render(request,'app/id.html',student)


# form field
def phone(request):
    if request.method=='POST':
        form=Brand(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=Brand()
    return render(request,'app/convert.html',{'form':form})    
# phone_info
def phone_info(request):
    if request.method=='POST':
        form=Color(request.POST)
        if form.is_valid():
            form.save()
    else:
        form=Color()
    return render(request,'app/info.html',{"form":form})            

# message 
def message(request):
    if request.method=='POST':
        form=Message(request.POST)
        form.save()
        messages.info(request,'now you can login')
        print(messages.get_level(request))
        messages.debug(request,'This is debug')
        messages.set_level(request,messages.DEBUG)
        messages.debug(request,'This is new debug')
        print(messages.get_level(request))
        form=Message()
    else:
        form=Message()
    return render(request,'app/message.html',{'form':form})         

# auth
def auth(request):
    if request.method=='POST':
        form=AuthForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            print('name',name)
            print('email',email)
            print('password',password)
            reg=Auth(name=name,email=email,password=password)
            reg.save()
            form=Auth()
    else:
        form=AuthForm()
    return render(request,'app/auth.html',{'form':form})           

# signup
def signup(request):
    if request.method=='POST':
        form=Signup(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created successfully')
            form.save()
            form=Signup()
    else:
        form=Signup()
    return render(request,'app/signup.html',{'form':form})           
#login view
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                pswd=form.cleaned_data['password']
                user=authenticate(username=uname,password=pswd)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully')
                    return HttpResponseRedirect('/profile/')
        else: 
            form=AuthenticationForm()
        return render(request,'app/login.html',{"form":form})   
    else:
        return HttpResponseRedirect('/profile/')

# profile
def user_profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            if request.user.is_superuser==True:
                form=EditAdminProfileForm(request.POST,instance=request.user)
            else:
                form=EditUserProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                messages.success(request,'profile has been updated') 
                form.save()
        else:
            if request.user.is_superuser==True:
                form=EditAdminProfileForm(instance=request.user) 
                users=User.objects.all()   
            else:
                form=EditAdminProfileForm(instance=request.user)
                users=None        
        return render(request,'app/profile.html',{'name':request.user,'form':form,'users':users})
    else:
        return HttpResponseRedirect('/login/')    

# change password with oldpassword
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                messages.success(request,'password changed successfully')
                return HttpResponseRedirect('/profile/')
        else:
            form=PasswordChangeForm(user=request.user)
        return render(request,'app/changepass.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')       

# use change password
def user_change_pass1(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=SetPasswordForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                messages.success(request,'password changed successfully')
                return HttpResponseRedirect('/profile/')
        else:
            form=SetPasswordForm(user=request.user)
        return render(request,'app/changepass1.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')    
            
# logout  
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')  

# user detail
def user_detail(request,id):
    if request.user.is_authenticated:
        pi=User.objects.get(pk=id)
        form=EditAdminProfileForm(instance=pi)
        return render(request,'app/detail.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')    
# dashboard
def user_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        full_name=user.get_full_name()
        groups=user.groups.all()
        ct=cache.get('count',0,version=user.pk)
        ip=request.session.get('ip',0)
        return render(request,'app/dashboard.html',{'ct':ct,'name':request.user.username,'ip':ip,'full_name':full_name,'groups':groups,})
    else:
        return HttpResponseRedirect('/login/')    
# custome signal
def customsignal(request):
    signals.notification.send(sender=None,request=request,user={'yakanna','anna'})
    return HttpResponse('this is custom signal...')
# Exception
def exception(request):
    print("i am exception view...")
    a=10/0
    return HttpResponse('this is exception page...')
# user_info
def user_info(request):
    print("i am user info view")
    context={'name':'prashanth'}
    return TemplateResponse(request,'app/user_info.html',context)

# queryset model
def queryset(request):
    # wallet=Queryset_model.objects.get(id=1)
    # wallet=Queryset_model.objects.first()
    # wallet=Queryset_model.objects.order_by('name').first()
    # wallet=Queryset_model.objects.latest('pass_date')
    # wallet=Queryset_model.objects.earliest('pass_date')
    # wallet=Queryset_model.objects.create(name='mobile',roll='talking',city='tamilnadu',marks=40,pass_date='2023-03-04')
    # wallet=Queryset_model.objects.get_or_create(name='mobile',roll='talking',city='tamilnadu',marks=40,pass_date='2023-03-04')
    # wallet=Queryset_model.objects.filter(id=1).update(name='Ramana',marks=100)
    # wallet=Queryset_model.objects.filter(marks=79).update(city='hyderabad')
    # wallet=Queryset_model.objects.update_or_create(id=1,name='vasantha',defaults={'name':'sameer'})
    # objs=[
    #     Queryset_model(name='ramana',roll='fa',city='hanamajipet',marks=80,date='2020-02-20'),
    #     Queryset_model(name='mallesh',roll='fa',city='dubai',marks=80,date='2020-02-22'),
    #     Queryset_model(name='laxminaryana',roll='fa',city='hanamajipet',marks=80,date='2020-02-21'),
    # ]
    # wallet=Queryset_model.objects.bulk_create(objs)
    # wallet_=Queryset_model.objects.all()
    # for stu in wallet:
    #     stu.city='laknavaram'
    # wallet=Queryset_model.objects.bulk_update(wallet_)    
    # wallet=Queryset_model.objects.in_bulk([1,2])    
    # print("name",wallet[1].name)
    # print('name',wallet[2].name)
    # print(wallet.exists())
    # wallet=Queryset_model.objects.in_bulk([])
    # wallet=Queryset_model.objects.in_bulk()
    # wallet=Queryset_model.objects.get(pk=5).delete()
    # wallet=Queryset_model.objects.get(marks=55).delete()
    # wallet=Queryset_model.objects.all().delete()
    # wallet=Queryset_model.objects.all().delete()
    # wallet=Queryset_model.objects.all().get(pk=1)
    # wallet=Queryset_model.objects.filter(marks=78).update(marks=100)
    # wallet=Queryset_model.objects.all()
    # wallet=Queryset_model.objects.filter(name__exact='prashanth')
    # wallet=Queryset_model.objects.filter(name__iexact='pradeep')
    # wallet=Queryset_model.objects.filter(name__contains='x')
    # wallet=Queryset_model.objects.filter(name__contains='x')
    # wallet=Queryset_model.objects.filter(id__in=[1,3])
    # wallet=Queryset_model.objects.filter(marks__in=[65,45])
    # wallet=Queryset_model.objects.filter(marks__gt=60)
    # wallet=Queryset_model.objects.filter(marks__gte=60)
    # wallet=Queryset_model.objects.filter(marks__lt=60)
    # wallet=Queryset_model.objects.filter(marks__lte=60)
    # wallet=Queryset_model.objects.filter(name__startswith='s')
    # wallet=Queryset_model.objects.filter(name__istartswith='b')
    # wallet=Queryset_model.objects.filter(name__endswith='h')
    # wallet=Queryset_model.objects.filter(name__iendswith='H')
    # wallet=Queryset_model.objects.filter(marks__lte=60)
    # wallet=Queryset_model.objects.filter(passdate__range=('2022-09-03' ,'2022-09-05'))
    # wallet=Queryset_model.objects.filter(admdatetime__date=date(2022,9,5))
    # wallet=Queryset_model.objects.filter(admdatetime__date__gt=date(2022,9,4))
    # wallet=Queryset_model.objects.filter(admdatetime__date__lt=date(2022,9,6))
    # wallet=Queryset_model.objects.filter(passdate__year=2019)
    # wallet=Queryset_model.objects.filter(passdate__year__gt=2019)
    # wallet=Queryset_model.objects.filter(passdate__year__lt=2022)
    # wallet=Queryset_model.objects.filter(passdate__month=9)
    # wallet=Queryset_model.objects.filter(passdate__month__gt=9)
    # wallet=Queryset_model.objects.filter(passdate__month__lt=9)
    # wallet=Queryset_model.objects.filter(passdate__day__gt=2)
    # wallet=Queryset_model.objects.filter(passdate__day__lt=5)
    # wallet=Queryset_model.objects.filter(passdate__week=30)
    # wallet=Queryset_model.objects.filter(passdate__week__gt=30)
    # wallet=Queryset_model.objects.filter(passdate__week_day=2)
    # wallet=Queryset_model.objects.filter(passdate__week_day__gt=1)
    # wallet=Queryset_model.objects.filter(passdate__quarter=3)
    # wallet=Queryset_model.objects.filter(admdatetime__time__gt=time(7,00))
    # wallet=Queryset_model.objects.filter(admdatetime__hour__gt=5)
    # wallet=Queryset_model.objects.filter(admdatetime__minute__gt=20)
    # wallet=Queryset_model.objects.filter(roll__isnull=True)
    # wallet=Queryset_model.objects.filter(roll__isnull=False)
    # wallet=Queryset_model.objects.aggregate(Avg('marks'))
    # wallet=Queryset_model.objects.filter(marks=65)
    # wallet=Queryset_model.objects.filter(city='hyderabad')
    # wallet=Queryset_model.objects.exclude(city='hyderabad')
    # wallet=Queryset_model.objects.order_by('name')
    # one_data=Queryset_model.objects.get(pk=1)
    # print(student_data.filter(pk=one_data.pk).exists())
    # wallet=Queryset_model.objects.order_by('?')
    # wallet=Queryset_model.objects.order_by('id')
    # wallet=Queryset_model.objects.order_by('id').reverse()[0:3]
    # wallet=Queryset_model.objects.values()
    # wallet=Queryset_model.objects.values('name','city')
    # wallet=Queryset_model.objects.values_list()
    # wallet=Queryset_model.objects.values_list('id','name',named=True)
    # wallet=Queryset_model.objects.values_list('pass_date','year')
    # wallet=Queryset_model.objects.values_list('pass_date','month')
    # wallet=Queryset_model.objects.values_list(id=1)& Queryset_model.objects.filter(roll='software')
    # wallet=Queryset_model.objects.filter(id=1,city='hyderabad')
    # wallet=Queryset_model.objects.filter(Q(id=1)&Q(city='hyderabad'))
    # wallet=Queryset_model.objects.filter(id=1) | wallet.objects.filter(roll='software developer')
    # wallet=Queryset_model.objects.filter(roll__isnull=False)
    # wallet=Queryset_model.objects.filter(~Q(id=2))
    # wallet=Queryset_model.objects.filter(Q(id=2))
    # wallet=Queryset_model.objects.filter(Q(id=3))
    # wallet=Queryset_model.objects.all()[2:5]#limting queryset
    # context={'wallet':wallet}
    # print("student data",wallet)
    # print("-----------------------")
    # print("sql query",wallet.query)
    # wallet=Queryset_model.objects.all()
    # average=wallet.aggregate(Avg('marks'))
    # total=wallet.aggregate(Sum('marks'))
    # minimum=wallet.aggregate(Min('marks'))
    # maximum=wallet.aggregate(Max('marks'))
    # totalcount=wallet.aggregate(Count('marks'))
    # context={'wallet':wallet,'average':average,'total':total,'minimum':minimum,'maximum':maximum,'totalcount':totalcount}
    # print(average)
    # print(minimum)
    # print(maximum)
    # print(totalcount)
    # print("return",wallet)
    # print("-----------------------")
    # print("sql query",wallet.query)
    return render(request,'app/queryset.html',{'wallet':wallet})
def teacher_info(request):
    teacher_data=Teacher.objects.all()
    # q1=Teacher.objects.values_list('id','name',named=True)
    q1=Teacher.objects.values_list('id','name',named=True)
    q2=Queryset_model.objects.values_list('id','name',named=True)
    # teacher_data=q2.union(q1)
    # q1=Teacher.objects.values_list('id','name',named=True)
    # q2=Queryset_model.objects.values_list('id','name',named=True)
    # teacher_data=q2.union(q1,all=True)
    # teacher_data=q2.intersection(q2)
    teacher_data=q2.difference(q2)
    print("teacher",teacher_data)
    print('----------------')
    print("sql query",teacher_data.query)
    return render(request,'app/teacher_info.html',{'teacher_data':teacher_data})

# Inheritance 
def inheritance(request):
    person=Person.objects.all()
    human=Human.objects.all()
    contractor=Contractor.objects.all()
    examcenter=Examcenter.objects.all()
    inivigilator=Invigilator.objects.all()
    begin=Begin.objects.all()
    meraexamcenter=Meraexamcenter.objects.all()
    return render(request,'app/inheritance.html',{'person':person,
                                                'human':human,
                                                'contractor':contractor,                                                'examcenter':examcenter,
                                                'inivigilator':inivigilator,
                                                'begin':begin,
                                                'meraexamcenter':meraexamcenter
                                                    })    


# model manager
def manager(request):
    # wallet=Cpu.objects.all()
    # wallet=ProxyStudent.objects.all()
    # wallet=Cpu.barking.all()
    wallet=ProxyStudent.barking.all()
    # wallet=ProxyStudent.barking.get_stu_roll_range(101,104)
    # wallet=Cpu.barking.get_stu_roll_range(101,104)
    return render(request,'app/manager.html',{'wallet':wallet})                                                    
# One to one fields
def one2one(request):
    data=One2one.objects.all()
    return render(request,'app/one2one.html',{"data":data})

# many to one fields
def many2one(request):
    data=Hellomany2one.objects.all()
    return render(request,'app/many2one.html',{'data':data})


# many to many fields
def many2many(request):
    data=Many2manysong.objects.all()
    return render(request,'app/many2many.html',{'data':data})
#class based view
class Myview(View):
    name='prashanth'
    # name=''
    def get(self,request):
        context={'msg':'welcome to mycity'}
        return render(request,'app/home.html',context)
        # return HttpResponse("<h1>This is class based view -Get</h1> ")
        # return HttpResponse(self.name)

class MyChild(Myview):
    def get(self,request):
        return HttpResponse(self.name)               

# contact
class ContactClassView(View):
    template_name='app/news.html'
    def get(self,request):
        # template_name=''
        form=ContactForm()
        # context={'info':'The site underconstruction'}
        # return render(request,self.template_name,context)
        return render(request,'app/contactform.html',{'form':form})
    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            print("name",form.cleaned_data['name'])
            return HttpResponse("Thank you for submitted")
            
def news(request,template_name):
    template_name=template_name
    context={"info":"CBI enquiry why google earns less money"}
    return render(request,template_name,context)    
# template view
class HomeTemplateView(TemplateView):
    template_name='app/home.html'

class ContextTemplateView(TemplateView):
    template_name='app/contemp.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        # context['name']='prashanth'
        context={'name':'yakbro','roll':101}
        print(context)
        print(kwargs)
        return context

# redirectview
class GoogleRedirect(RedirectView):
    # url='https://www.google.com'
    pattern_name='prashanth'
    permanent=True
    query_string=True
    # query_string=False # by default false

    def get_redirect_url(self, *args, **kwargs): 
        print(kwargs)
        return super().get_redirect_url(*args,**kwargs)

# Class Crud operation

class UserCrud(TemplateView):
    template_name='app/classcrud.html'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        form=CrudForm()
        data=Crud_class.objects.all()
        context={'form':form,'data':data}
        return context
    
    def post(self,request):
        form=CrudForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            reg=Crud_class(name=name,email=email,password=password)
            reg.save()
            form=CrudForm()
        return HttpResponseRedirect('/usercrud/')
        # else:c
        #     form=CrudForm()
        # return render(request,'app/classcrud.html',{'forms':form})    

class ClsUpdate(View):
    def get(self,request,id):
        pi=Crud_class.objects.get(pk=id)
        form=CrudForm(instance=pi)
        return render(request,'app/clsupdate.html',{'form':form})
        
    def post(self,request,id):
        pi=Crud_class.objects.get(pk=id)
        form=CrudForm(request.POST,instance=pi)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/usercrud/')       

# class delete view
class ClsDeleteview(RedirectView):
    url='/usercrud/'
    def get_redirect_url(self,*args,**kwargs):
        print(kwargs['id'])
        del_id=kwargs['id']
        Crud_class.objects.get(pk=del_id).delete()
        return super().get_redirect_url(*args,**kwargs)
# class list view
class list(ListView):
    model=List
    template_name='app/list.html'
    # template_name_suffix='_list'# for using templatesuffix name
    # ordering=['name']# for ordering
    context_object_name='lists'
    # data=List.objects.all()
    # context={"data":data}
    # return render(request,'app/List_list.html',context)

    def get_queryset(self):
        return List.objects.filter(course='django')
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['freshers']=List.objects.all().order_by('name')
        return context
    # def get_template_names(self):
    #     if self.request.COOKIES['user']:
    #         template_name='geeks/user.html'
    #     else:
    #         template_name=self.template_name
    #     return[template_name]    
# list detail view 
class ListDetailview(DetailView):
    model=Detail
    template_name='app/details.html'
    # context_object_name='list'
    # pk_url_kwarg='id'
    # pk_url_kwarg='hi'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['all_details']=self.model.objects.all().order_by('name')
        return context


class Listlistview(ListView):
    model=Detail

# class form view
class Base(FormView):
    form_class=Filling
    template_name='app/formview.html'
    success_url='/thankyou/'
    def form_valid(self,form):
        print(form)
        print("name",form.cleaned_data['name'])
        print("email",form.cleaned_data['email'])
        print("message",form.cleaned_data['message'])
        form=Filling()
        return super().form_valid(form)

class Thankyou(TemplateView):
    template_name='app/thankyou.html'        

# create view class 
class Create(CreateView):
    form_class=ApplicationForm
    template_name='app/camera_form.html'
    success_url='/thankyou/'
# updateview
class Update(UpdateView):
    model=Camera
    form_class=ApplicationForm
    template_name='app/camera_form.html'
    success_url='/thanks/'
# thank you
class ThankyouUpdate(TemplateView):
    template_name='app/thanks.html'
# delete
class Cameradelete(DetailView):
    model=Remove
    success_url='/clscreate/' 

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['all_removes']=self.model.objects.all().order_by('name')
        return context
# xlass authentication
class ProfileTemplateView(TemplateView):
    template_name='registration/profile.html'
    @method_decorator(login_required)
    def dispatch(self,*args,**kwargs):
        return super().dispatch(*args,**kwargs)

class AboutTemplateView(TemplateView):
    template_name='app/about.html'
    @method_decorator(staff_member_required)
    def dispatch(self,*args,**kwargs):
        return super().dispathc(*args,**kwargs)
# func authentication
@login_required
def profile(request):
    return render(request,'registration/profile.html')

def logout(request):
    return render(request,'registration/logout.html')

@staff_member_required
def about(request):
    return render(request,'app/about.html')    

#customize authentication
class TemplateView(TemplateView):
    template_name='registration/home.html'

class Login_view(TemplateView):
    template_name='registration/login.html'
    # authententication_form=Login_Form

class LogoutView(TemplateView):
    template_name='registration/loggedout.html'

class PasswordChangeView(TemplateView):
    template_name='registration/changepass.html'
    success_url='/changepass/'
# pagination
def page_list(request):
    all_page=Page.objects.all().order_by('id')
    paginator=Paginator(all_page,3,orphans=1)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    print("all_page=",all_page)
    print('-----------------')
    print("paginator= ",paginator)
    print("--------------")
    print("page_number= ",page_number)
    print("----------")
    print("page_obj= ",page_obj)
    return render(request,'app/page.html',{'page_obj':page_obj})

#class pagelist view
class PageListview(ListView):
    model=Page
    template_name='app/page_list.html'
    ordering=['id']
    paginate_by=3
    paginate_orphans=1


    # def get_context_data(self,*args,**kwargs):
    #     try:
    #         return super(PageListview,self).get_context_data(*args,**kwargs)
    #     except Http404:
    #         self.kwargs['page']=1
    #     return super(PageListview,self).get_context_data(*args,**kwargs)

    def paginate_queryset(self,queryset,page_size):
        try:
            return super(PageListview,self).paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page']=1
            return super(PageListview,self).paginate_queryset(queryset,page_size)

class PageDetail(DetailView):
    model=Page
    template_name='app/page_detail.html'   

# datetime
def date_time(request):
    x=datetime.date(2023,1,9)
    current_time=timezone.now().strftime("%H:%M:%S")
    currentdate=datetime.date.today()
    formatDate=currentdate.strftime("%d-%b-%y")
    format_Date1=currentdate.strftime("%d/%b/%Y")
    format_Date2=currentdate.strftime("%d/%B/%Y")
    format_Date3=currentdate.strftime("%m/%d/%Y")
    format_date_1=currentdate.strftime("%a")
    format_date_2=currentdate.strftime("%j")
    format_date_3=currentdate.strftime("%W")
    format_date_4=currentdate.strftime("%m")        
    return render(request,'app/date_time.html',
                    {'current_date':currentdate,
                    'format_date':formatDate,
                    'format_Date1':format_Date1,
                    'format_Date2':format_Date2,
                    'format_Date3':format_Date3,
                    'format_date_1':format_date_1,
                    'format_date_2':format_date_2,
                    'format_date_3':format_date_3,
                    'format_date_4':format_date_4,
                    'my_date':x,
                    'current_time':current_time,
                    })

# get user ip address 
def ipaddress(request):
    user_ip=request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        ip=user_ip.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return HttpResponse('Welcome user !<br> You are visiting from: {}'.format(ip))


