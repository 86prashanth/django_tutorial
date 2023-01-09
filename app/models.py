from django.db import models
from django.contrib.auth.models import User
from .managers import CustomManager
from django.urls import reverse
from django.utils.safestring import mark_safe
# Create your models here.
class Employee(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    contact=models.IntegerField()
    email=models.EmailField(max_length=50)
    age=models.IntegerField()
# creating new connecting database
class Mobile(models.Model):
    mid=models.CharField(max_length=100)
    mname=models.CharField(max_length=100)
    mconn=models.CharField(max_length=100)
    class Meta:
        db_table="mobile"

# image upload 
class UploadImage(models.Model):
    figure=models.CharField(max_length=300)
    image=models.ImageField(upload_to='images')
    def admin_photo(self):
        return mark_safe('<img src="{}" width="100"/>' .format(self.image.url))
        

# crud operations
class Crud(models.Model):
    eid=models.CharField(max_length=100)
    ename=models.CharField(max_length=100)
    eemail=models.EmailField()
    econtact=models.CharField(max_length=100)
    class Meta:
        db_table="Crud"        

class Author(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)

    def __str__(self):
        return "%s %s" %(self.first_name,self.last_name)

class Post(models.Model):
    title=models.CharField(max_length=50)     
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    # author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title   

class Mirror(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)

    def __str__(self):
        return "%s %s"%(self.first_name,self.last_name)

class Dynamic(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=254)
    repassword=models.CharField(max_length=254)


class Phone(models.Model):
    name=models.CharField(max_length=100)
    phone_name=models.CharField(max_length=100)
    phone_model=models.CharField(max_length=100)
    price=models.FloatField()

# Message 
class Message(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    
class Auth(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)

# Registration    
class Register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)

class Queryset_model(models.Model):
    name=models.CharField(max_length=100)
    roll=models.CharField(max_length=100,unique=True,null=False)
    city=models.CharField(max_length=50)
    marks=models.IntegerField()
    pass_date=models.DateField()

class Teacher(models.Model):
    name=models.CharField(max_length=100)
    empnum=models.IntegerField(unique=True,null=False)
    city=models.CharField(max_length=70)
    salary=models.IntegerField()
    join_date=models.DateField()

# model inheritance
class Commoninfo(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    date=models.DateField()
    class Meta:
        abstract=True

class Person(Commoninfo):
    fees=models.IntegerField()
    data=None

class Human(Commoninfo):
    salary=models.IntegerField()

class Contractor(Commoninfo):
    date=models.DateTimeField()
    payment=models.IntegerField()

class Examcenter(models.Model):
    cname=models.CharField(max_length=75)
    city=models.CharField(max_length=50)
# model inheritance
class Invigilator(Examcenter):
    name=models.CharField(max_length=100)
    roll=models.IntegerField()

# proxy model
class Begin(models.Model):
    cname=models.CharField(max_length=50)
    city=models.CharField(max_length=150)

class Meraexamcenter(Begin):
    class Meta:
        proxy=True
        ordering=['id']

# custom manager
class Cpu(models.Model):
    name=models.CharField(max_length=50)
    roll=models.IntegerField()
    objects=models.Manager()
    students=CustomManager()

class ProxyStudent(Cpu):    
    barking=CustomManager()
    class Meta:
        proxy=True
        ordering=['id']

class One2one(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,limit_choices_to={'is_staff':True})
    # user=models.OneToOneField(User,on_delete=models.PROTECT,primary_key=True)
    page_name=models.CharField(max_length=100)
    page_cat=models.CharField(max_length=100)
    page_publish_date=models.DateField()

class Like(One2one):
    page=models.OneToOneField(One2one,on_delete=models.CASCADE,primary_key=True,parent_link=True)
    likes=models.IntegerField()    

#many to one fields
class Hellomany2one(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    post_title=models.CharField(max_length=100)
    post_cat=models.CharField(max_length=50)
    post_publish_date=models.DateField()

# many to many fields
class Many2manysong(models.Model):
    user=models.ManyToManyField(User)
    song_name=models.CharField(max_length=70)
    song_duration=models.IntegerField()
    def written_by(self):
        return ",".join([str(q) for q in self.user.all()])

# classbesed view crud
class Crud_class(models.Model):
      name=models.CharField(max_length=50)      
      email=models.EmailField(max_length=50)      
      password=models.CharField(max_length=50)      

# listview
class List(models.Model):
    name=models.CharField(max_length=100)
    roll=models.IntegerField()
    course=models.CharField(max_length=100)

    def __str__(self):
        return self.name      

# details view
class Detail(models.Model):
    name=models.CharField(max_length=100)
    roll=models.IntegerField()
    course=models.CharField(max_length=100)

    def __str__(self):
        return self.name   

# class Camera
class Camera(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('thanks')   

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

# remove
class Remove(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)  

# page
class Page(models.Model):
    title=models.CharField(max_length=50)
    desc=models.TextField(max_length=250)
    publish_date=models.DateTimeField()



# contact form
class Contact_1(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    question_categories=models.CharField('how can we help you?',max_length=100)
    message=models.TextField(max_length=300)
    def __str__(self):
        return self.email