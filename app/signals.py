from code import interact
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache
from django.dispatch import Signal
from django.db.models.signals import pre_migrate,post_migrate,pre_init,pre_save,pre_delete,post_init,post_save,post_delete
from django.core.signals import request_started,request_finished,got_request_exception
from django.db.backends.signals import connection_created

@receiver(user_logged_in,sender=User)
def login_succes(sender,request,user, **kwargs):
    print("--------------------------------")
    print("logged-in signal... run intro..")
    print("sender",sender)
    print("request",request)
    print("user",user)
    print("user password",user.password)
    print(f'kwargs: {kwargs}')
    
    # user_logged_in.connect(login_succes,sender=User)
    
@receiver(user_logged_out,sender=User)
def login_out(sender,request,user, **kwargs):
    print("--------------------------------")
    print("logged-out signal... run intro..")
    print("sender",sender)
    print("request",request)
    print("user",user)
    print(f'kwargs: {kwargs}')
    
    # user_logged_out.connect(login_out,sender=User)
    
    
@receiver(user_login_failed)
def login_failed(sender,credentials,request, **kwargs):
    print("--------------------------------")
    print("logged-failed signal... ")
    print("sender",sender)
    print("credentials",credentials)
    print("request",request)
    print(f'kwargs: {kwargs}')
    
    # user_login_failed.connect(login_failed,sender=User)
 
@receiver(pre_save,sender=User)   
def at_beginning_save(sender,instance,**kwargs):
    print("------------------")
    print("pre save signal...")
    print("sender",sender)
    print("instance",instance)
    print(f'kwargs,{kwargs}')
    # pre_save.connect(at_beginning_save,sender=User)

@receiver(post_save,sender=User)
def at_ending_save(sender,instance,created,**kwargs):
    if created:
        print("-----------------------")
        print("post save signals..")
        print("New recored..")
        print("sender",sender)
        print("instance",instance)
        print("created",created)
        print(f'kwargs:{kwargs}')
    else:
        print("----------------------------")
        print("post save signal...")
        print("Update")
        print("sender",sender)
        print("instance",instance)
        print("created",created)
        print(f'kwargs:{kwargs}')
        # post_save.connect(at_ending_save,sender=User)
        
@receiver(pre_delete,sender=User)
def at_begining_delete(sender,instance,**kwargs):
    print("----------------------------")
    print("pre delete signal..")
    print("sender",sender)
    print("instacne",instance)
    print(f'kwargs:{kwargs}')
    # pre_delete.connect(at_begining_delete,sender=User)
    
@receiver(post_delete,sender=User)
def at_ending_delete(sender,instance,**kwargs):
    print("------------------------")
    print("post delete signal..")
    print("sender",sender)
    print("instance",instance)
    print(f'kwargs:{kwargs}')
    # post_delete.connect(at_ending_delete,sender=User)
    
    
@receiver(pre_init,sender=User)
def at_begining_init(sender,*args,**kwargs):
    print("------------------------")
    print("pre init signal....")
    print("sender",sender)
    print(f'args:{args}')
    print(f'kwargs:{kwargs}')
    # pre_init.connect(at_begining_init,sender=User)
    
@receiver(post_init,sender=User)
def at_ending_init(sender, *args,**kwargs):
    print('-----------------')
    print("post init signal....")
    print("sender",sender)
    print(f'Args:{args}')
    print(f'kwargs:{kwargs}')
    # post_init.connect(at_ending_init,sender=User)
    
@receiver(request_started)
def at_begining_request(sender,environ,**kwargs):
    print('-----------------')
    print("begining request signal....")
    print("sender",sender)
    print("environ",environ)
    print(f'kwargs:{kwargs}')
    # request_started.connect(at_ending_init,sender=User)
    
@receiver(request_finished)
def at_ending_request(sender,**kwargs):
    print('-----------------')
    print("ending request signal....")
    print("sender",sender)
    print(f'kwargs:{kwargs}')
    # request_finished.connect(at_ending_init,sender=User)
    
    
@receiver(got_request_exception)
def at_req_exception(sender,request,**kwargs):
    print('-----------------')
    print("got request exception..")
    print("sender",sender)
    print("request",request)
    print(f'kwargs:{kwargs}')
    # get_request_exception.connect(at_ending_init,sender=User)
    
@receiver(pre_migrate)
def before_install_app(sender,app_config,verbosity,interactive,using,plan,apps,**kwargs):
    print('-------------------------')
    print("before install")
    print("sender",sender)
    print("app_config",app_config)
    print('verbosity',verbosity)
    print('interactive',interactive)
    print('using',using)
    print('plane',plan)
    print('apps',apps)
    print(f'kwargs:{kwargs}')
    #pre_migrate.connect(before_install_app)
    
@receiver(post_migrate)
def at_end_migrate_flush(sender,app_config,verbosity,interactive,using,plan,apps,**kwargs):
    print('-----------------------------------')
    print("post installed")
    print("sender",sender)
    print("app_config",app_config)
    print("verbosity",verbosity)
    print("interactive",interactive)
    print("using",using)
    print("plan",plan)
    print("apps",apps)
    print(f'kwargs:{kwargs}')
    #post_migrate.connect(at_end_migrate_flush)
    
@receiver(connection_created)
def conn_db(sender,connection,**kwargs):
    print("---------------------------")
    print("Initial connection to the database")
    print("sender",sender)
    print("connection",connection)
    print(f'kwargs:{kwargs}')
    #connection_created.connect(conn_db)

@receiver(user_logged_in,sender=User)
def login_success(sender,request,user,**kwargs):
    print("________________________")
    print("logged-in signal... run intro...") 
    ip=request.META.get('REMOTE_ADDR')
    print('client IP',ip)
    request.session['ip']=ip   

@receiver(user_logged_out,sender=User)
def login_success(sender,request,user,**kwargs):
    ct=cache.get('count',0,version=user.pk)
    newcount=ct+1
    cache.set('count',newcount,60*60*24,version=user.pk)
notification=Signal()
@receiver(notification)
def show_notification(sender,**kwargs):
    print("sender",sender)
    print("kwargs",f'{kwargs}')
    print("notification...")