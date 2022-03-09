
from urllib import request
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from register.models import profile
from .forms import EmployeeForm



#write backend code here
#frontend stored in templates
def home(request):
    #use render for load html page
    return render(request,"register/home.html")
def register(request):
    # to read input from fields
    if(request.method=="POST"):
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if(password1==password2):
            if(User.objects.filter(username=username).exists()):
                #show messages
                messages.info(request,"username Exist")
                return redirect('/register/')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request,"email exist")
                return redirect('/register/')
            else:
                # create new instance of User model
                user= User.objects.create_user(username=username,password=password1,email=email)
                user.save()# save form
                return redirect('/employee_form/')
        else:
            messages.info(request,"password mismatch")
            return redirect('/register/')
        
        
    else:
        return render(request,"register/register.html")
def login(request):
    if(request.method=="POST"):
        username=request.POST['username']
        password=request.POST['password']
        #for checking if user present in database and it return username
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            #for login
            auth.login(request,user)
            return redirect('/show/')
        else:
            messages.info(request,"invalid credentials")
            return redirect('/login/')
    else:
        return render(request,"register/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')# take to current app homepage

def employee_form(request):
    
    if request.method =='POST':
        form=EmployeeForm(request.POST)
        #to access form.cleaned_data
        form.is_valid()
        temp=form.cleaned_data.get('incharge')
        #check incharge field
        if(profile.objects.all().filter(user=temp).filter(position="manager") or  temp==None):
            
    
            if(form.is_valid):
                form.save()
                return redirect('/login/')
            else:
                messages.info(request,"invalid  field")
                return redirect('/employee_form/')
        
        else:

            messages.info(request,"invalid incharge field")
            return redirect('/employee_form/')
            
        
        
    else:
        form=EmployeeForm()
        return render(request,"register/employee_form.html",{'form':form})

    
def show(request):
    current_user=request.user
    
    #test
    #b=User.objects.get(username=current_user)
   # print(b)
   # print(b.profile.all())
    ##end test
    userdetail=profile.objects.filter(user=current_user).values
    #check for admin
    if profile.objects.filter(user=current_user).filter(position="admin"):
        val=profile.objects.all().exclude(user=current_user).values
    #check for manager
    elif profile.objects.filter(user=current_user).filter(position="manager"):
        val=profile.objects.all().filter(position="employee").filter(incharge=current_user).exclude(user=current_user).values
    #to pass elif if next to each other error
    else:
        pass
    #to seperate context cause only manager & admin has employees details
    if(profile.objects.all().filter(user=current_user).filter(position="employee")):
        context={'userdetail':userdetail}
    else:
        context={'val':val,'userdetail':userdetail,'current_user':current_user}
    return render(request,"register/show.html",context)

def update(request):
    
    usr=request.user
    id=usr.id
    ob=profile.objects.get(id=id)
    print('id',ob)
    if request.method =='POST':
        #for update use instance if u used to in render line:148
        form=EmployeeForm(request.POST,instance=ob)
        #to access form.cleaned_data
        form.is_valid()
        temp=form.cleaned_data.get('incharge')
        print("usrt",temp)
        #check incharge field
        if(profile.objects.all().filter(user=temp).filter(position="manager") or temp==None):
            
    
            if(form.is_valid):
                form.save()
                return redirect('/login/')
            else:
                messages.info(request,"invalid  field")
                return redirect('/update/')
        
        else:

            messages.info(request,"invalid incharge field")
            return redirect('/update/')
            
        
        
    else:
        form1=EmployeeForm(instance=ob)# instance to show older details in forms

        return render(request,"register/employee_form.html",{'form':form1})

def delete(request):
    current_user=request.user
    context={'current_user':current_user}
    return render(request,"register/delete.html",context)
def real_delete(request):
    current_user= request.user
    u=User.objects.get(username=current_user)
    u.delete()
    return redirect('/') 
