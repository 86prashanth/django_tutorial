from django import forms 
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.forms.widgets import NumberInput,SelectDateWidget
from django.core import validators
from django.utils.translation import gettext_lazy as _

class EmpForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'

class StudentForm(forms.Form):
    name=forms.CharField(max_length=100,label="Enter your Name")
    email=forms.CharField(max_length=50,label="Enter your Email")        


#file upload form
class UploadForm(forms.Form):
    firstname=forms.CharField(label="Enter Your name",max_length=50,initial='prashanth')
    lastname=forms.CharField(label="Enter your last name",max_length=100)
    email=forms.EmailField(label="Enter Email")
    file=forms.FileField()    
    key=forms.CharField(widget=forms.HiddenInput())

#upload image form







class uploadimage(forms.ModelForm):
    class Meta:
        model=UploadImage   
        exclude=('figure',)
        # fields="__all__"

# crud operation 
class CrudForm(forms.ModelForm):
    class Meta:
        model=Crud
        fields=['eid','ename','eemail','econtact']
        widgets={
            'eid':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your id'}),
            'ename':forms.TextInput(attrs={'class':'form-control','placeholder':"Enter your name"}),
            'eemail':forms.EmailInput(attrs={'class':'form-control','placeholder':"Enter your email"}),
            'econtact':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your Econtact'}),
        }    
        labels={'eid':'Enter your Eid','ename':'Enter your ename','eemail':'Enter your Email','econtact':'Enter your Contact'}
        error_messages={
            'eid':{'required':'pleasse Enter your Id'},
            'ename':{'required':'pleasse Enter your name'},
            'eemail':{'required':'pleasse Enter your email'},
            'econtact':{'required':'please ENter your contact'}
        }
     
# contact form
class ContactForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    mobile=forms.CharField()
    message=forms.CharField(widget=forms.Textarea)
            

class MirrorForm(forms.ModelForm):
    model=Mirror
    fields='__all__'

# user creation form
class CustomUserCreationForm(UserCreationForm):
    username=forms.CharField(max_length=150,min_length=5,label='Username')
    email=forms.EmailField(label='email')
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='ConfirmPassword',widget=forms.PasswordInput)
    def username_clean(self):
        username=self.cleaned_data['username'].lower()
        new=User.objects.filter(username=username)
        if new.count():
            raise ValidationError('User alredy Exist')
        return username    
    def email_clean(self):
        email=self.cleaned_data['email'].lower()
        new=User.objects.filter(email=email)
        if new.count():
            raise ValidationError('Email alredy Exist')
        return email
    def clean_password2(self):
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        if password1 and password2 and password1 !=password2:
            raise ValidationError('password does not match') 
        return password2
    def save(self,commit=True):
        user=User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user    
class Contactform(forms.Form):
    BIRTH_YEAR_CHOICES=['1991','1992','1993','1994','1995','1996','1997']
    choice_value=[('1','First'),('2','second'),('3','Third'),]
    gender=[('1','male'),('2','Female'),('3','Others'),] 
    first_name=forms.CharField(initial='prashanth',required=False)
    last_name=forms.CharField(required=True)
    comment=forms.CharField(initial='prashanth@gmail.com',widget=forms.Textarea(attrs={'rows':3}))
    email=forms.EmailField()
    agree=forms.BooleanField()
    # date_birth=forms.DateField(widget=NumberInput(attrs={'type':'date'}))
    date_of_birth=forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    value=forms.DecimalField()
    rank=forms.ChoiceField(choices=choice_value)
    Gender=forms.ChoiceField(widget=forms.RadioSelect,choices=gender)
    message=forms.CharField(max_length=100,label='please write a message for us')

class DynamicForm(forms.Form):
    name=forms.CharField(validators=['start_with_s'],label='Enter your name',label_suffix='',required=False,help_text='it contain 300 characters')
    email=forms.CharField(label="Enter your email",label_suffix='',help_text='it contain 300 characaters ')
    password=forms.CharField(error_messages={'required':'Enter your Password'},widget=forms.PasswordInput())
    repassword=forms.CharField(error_messages={'required':'Enter your password'},label='Confirm Password',widget=forms.PasswordInput())
    def clean(self):
        cleaned_data=super().clean()
        name=self.cleaned_data['name']
        if len(name)<4:
            raise forms.ValidationError('enter more than 4 or equal characaters...') 
        email=self.cleaned_data['email']
        if len(email)<13:
            raise forms.ValidationError('email should be more than or equal 13')
        valpwd=self.cleaned_data['password']
        valrpwd=self.cleaned_data['repassword']
        if valpwd!=valrpwd:
            raise forms.ValidationError('password does not match')    

# model inheritance      
class Brand(forms.ModelForm):
    class Meta:
        model=Phone
        fields=['name','phone_name','phone_model']

# inheritance
class Color(Brand):
    class Meta(Brand.Meta):
        fields=['price','phone_name','phone_model']       

#message frame work
class Message(forms.ModelForm):
    class Meta:
        model=Message
        fields=['name','email','password']

# authenication
class AuthForm(forms.ModelForm):
    class Meta:
        model=Auth
        fields=['name','email','password']

# signup form
class Signup(UserCreationForm):
    password2=forms.CharField(label='confirm password(again)',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}      
        

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','date_joined','last_login','is_active']
        labels=['email','Email']

class EditAdminProfileForm(UserChangeForm):
    password=None
    model=User
    fields='__all__'
    labels={'email':'Email'}
# contact form
class ContactForm(forms.Form):
    name=forms.CharField(max_length=100)


# crud class form   
class CrudForm(forms.ModelForm):
    class Meta:
        model=Crud_class
        fields={'name','email','password'}
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True,attrs={'class':'form-control'})
        }   
        labels={
            'name':'Enter the name',
            'email':'Enter the email',
            'password':'Enter the password'
            }
        name=forms.CharField(error_messages={'required':'Enter your name'})   
# form view
class Filling(forms.Form):
    name=forms.CharField(max_length=100)        
    email=forms.EmailField(max_length=100)        
    message=forms.CharField(max_length=100)        


# create view
class ApplicationForm(forms.ModelForm):
    class Meta:
        model=Camera
        fields=['name','email','password']
        widgets={
            'name':forms.TextInput(attrs={'class':'myclass'}),
            'password':forms.PasswordInput(attrs={'class':'mypass'}),
            'email':forms.TextInput(attrs={'class':'myemail'}),       
                 }

# class Login form
class Login_Form(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus':True,'class':'myuser'}))
    password=forms.CharField(label=_('password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password'}))

# class Empdetails


select_mode_of_contact=(
            ("email",'E_mail'),
            ("phone","phone"),)
select_question_categories=(
    ("certification","certification"),
    ("interview","interview"),
    ("material","material"),
    ("access_duration","Acess and Duration"),
    ("other","Others"),
)

class Contact_Form(forms.ModelForm):
    phone=models.CharField(max_length=100)
    mode_of_contact=forms.CharField(required=False,widget=forms.RadioSelect(choices=select_mode_of_contact))
    question_categories=forms.CharField(required=False,widget=forms.Select(choices=select_question_categories))
    class Meta:
        model=Contact_1
        fields='__all__'