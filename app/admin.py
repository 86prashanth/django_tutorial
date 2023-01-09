from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Employee)
admin.site.register(Mobile)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Dynamic)
admin.site.register(Mirror)
@admin.register(UploadImage)
class UploadImageAdmin(admin.ModelAdmin):
    list_display=['id','figure','image']
@admin.register(Crud)
class Crud(admin.ModelAdmin):
    list_display=['eid','ename','eemail','econtact']
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display=['name','phone_name','phone_model']    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password')    
@admin.register(Auth)
class AuthAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password')    
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password')    
@admin.register(Queryset_model)
class Queryset_modelAdmin(admin.ModelAdmin):
    list_display=['id','name','roll','city','marks','pass_date']
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=['id','name','empnum','city','salary'] 

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display=['id','name','age','fees']  

@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display=['id','name','age','date','salary']

@admin.register(Contractor)
class Contractoradmin(admin.ModelAdmin):
    list_display=['id','name','age','date','payment']
    
@admin.register(Examcenter)
class Examcenteradmin(admin.ModelAdmin):
    list_display=['id','cname','city']
    
@admin.register(Invigilator)
class Invigilatoradmin(admin.ModelAdmin):
    list_display=['id','name','cname','city','roll']  
  
@admin.register(Begin)
class Beginadmin(admin.ModelAdmin):
    list_display=['id','cname','city']
    
@admin.register(Meraexamcenter)
class Meraexamcenteradmin(admin.ModelAdmin):
    list_display=['id','cname','city']  
@admin.register(Cpu)
class CpuAdmin(admin.ModelAdmin):
    list_display=['id','name','roll']
    ordering=['id']
@admin.register(ProxyStudent)
class ProxyStudentAdmin(admin.ModelAdmin):
    list_display=['id','name','roll']
    ordering=['id']   
@admin.register(One2one)    
class One2oneAdmin(admin.ModelAdmin):
    list_display=['page_name','page_cat','page_publish_date','user']
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=['page','likes','page_name','page_cat','page_publish_date','user']    

@admin.register(Hellomany2one)
class Hellomany2oneAdmin(admin.ModelAdmin):
    list_display=['post_title','post_cat','post_publish_date','user']

@admin.register(Many2manysong)
class  Many2manysongAdmin(admin.ModelAdmin):
        list_display=['song_name','song_duration','written_by']

@admin.register(Crud_class)
class Crud_classAdmin(admin.ModelAdmin):
        list_display=['name','email','password']

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
        list_display=['id','name','roll','course']
@admin.register(Detail)
class ListAdmin(admin.ModelAdmin):
        list_display=['id','name','roll','course']
@admin.register(Camera)
class Cameraadmin(admin.ModelAdmin):
    list_display=['id','name','email','password']


@admin.register(Remove)
class Removeadmin(admin.ModelAdmin):
    list_display=['id','name','email','password']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display=['id','title','desc','publish_date']

admin.site.register(Contact_1)