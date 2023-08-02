from datetime import *
from django.shortcuts import render
from datetime import *
from django.shortcuts import render, redirect
from .models import Suggestion_Data,Login
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q

def send_email_to_solve(request,emaill):
    template = render_to_string('email_solve.html')
    email =  EmailMultiAlternatives(
        'Testing Email of Suggestion System',
        template,
        [emaill],
    )
    email.attach_alternative(template, "text/html")
    email.fail_silently=False
    email.send()

def send_email_to_check(request,emaill):
    template = render_to_string('email_check.html')
    email =  EmailMultiAlternatives(
        'Testing Email of Suggestion System',
        template,
        settings.EMAIL_HOST_USER,
        [emaill],
    )
    email.attach_alternative(template, "text/html")
    email.fail_silently=False
    email.send()

def user(request):

    user_info = {
        'username': request.session.get('username'),
        'mail': request.session.get('mail'),
        'role': request.session.get('role')
    }

    return user_info

def check(request):
    try:
        if request.session['login'] == False or request.session['login'] == None:
            return False
        else:
            return True
    except:
        return False


def index(request):

    if check(request):
        notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
        emp=list(Suggestion_Data.objects.all().filter(Status_A='Accepted').filter(Status_M='Accepted').reverse())[::-1]
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        paginator = Paginator(emp, per_page=5)  # Show 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages
        context1={
            'q': page_obj.object_list,
            'u' : user(request),
            'totalpagelist': [n+1 for n in range(totalpage)],
            'page_obj': page_obj,
            'notification':notification,
            'notification_manager':notification_manager,
            'notification_issue':notification_issue,
               
        
        }
        return render(request,'home.html',context1)
    else:
        return redirect('/mains/login')

def showmyquestions(request):
    if check(request):    
        mail=request.session.get('mail')
        emp=list(Suggestion_Data.objects.all().filter(Mail=mail).reverse())[::-1]
        notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        paginator = Paginator(emp, per_page=3)  # Show 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages
            
        context1={
            'notification':notification,
            'notification_manager':notification_manager,
            'notification_issue':notification_issue,
            'q' : page_obj.object_list,
            'u' : user(request),
            'totalpagelist': [n+1 for n in range(totalpage)],
            'page_obj': page_obj  
            }
        

        return render(request,'myquestions.html',context1)  
    else:
        return redirect('/mains/login')  

def askquestions(request):
    if check(request) and request.session.get('role')=='user':
        notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
        context1={
            'u' : user(request),
            'notification_issue':notification_issue
        }
        return render(request,'askquestions.html',context1)
    else:
        return redirect('/mains/login')

def addq(request):
    if check(request) and request.session.get('role')=='user':
        if request.method == "POST":
            qtitle=request.POST.get('title')
            qdesc=request.POST.get('description')
            qatt=request.POST.get('attachment')
            if request.POST.get('qusername') is None:
                qusername="off"
            else:
                qusername=request.POST.get('qusername')
            print(qusername)
            print(qtitle)
            print(qdesc)
            sug_data= Suggestion_Data(Title=qtitle, Mail=request.session.get('mail'), Description=qdesc, Attachment=qatt, Entry_Time=datetime.now().date(), Anonymous=qusername)
            sug_data.save()
            return redirect('../')
        else:
            pass
    else:
        return redirect('/mains/login')

def addq2(request):
    if check(request) and request.session.get('role')=='admin':
        if request.method == "POST":
            qtitle=request.POST.get('title')
            qdesc=request.POST.get('description')
            qmanager=request.POST.get('mail_list')
            qatt=request.POST.get('attachment')
            print(qtitle)
            print(qdesc)
            sug_data= Suggestion_Data(Title=qtitle, Mail=request.session.get('mail'), Description=qdesc,Manager_mail=qmanager,Attachment=qatt, Entry_Time=datetime.now().date(),Status_A='Accepted')
            sug_data.save()  
            send_email_to_solve(request,qmanager)
            return redirect('../')
        else:
            pass
    else:
        return redirect('/mains/login')

def reviewmanager(request,sid):
    if check(request) and request.session.get('role')=='admin':
        if sid=='Pending':
            emp = Suggestion_Data.objects.filter(Status_M='Accepted').filter(Status_A='Pending')[::-1]
            pagestatus='Pending'
        elif sid=='Accepted':
            emp = Suggestion_Data.objects.filter(Status_M='Accepted').filter(Status_A='Accepted')[::-1]
            pagestatus='Accepted'
        else:
            emp = Suggestion_Data.objects.filter(Status_M='Accepted')[::-1]
            pagestatus='Review'

        paginator = Paginator(emp, per_page=5)  # Show 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages
        notification = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        context1 = {
            'q': page_obj.object_list,
            'status': sid,
            'page_obj': page_obj,
            'notification':notification,
            'notification_manager':notification_manager,
            'pagestatus':pagestatus,
            'totalpagelist': [n+1 for n in range(totalpage)],
            'u':user(request)
        }
        return render(request, 'reviewmanager.html', context1)
    else:
        return redirect('/mains/login')




def reviewemployee(request, sid):
    if check(request) and request.session.get('role')=='admin':
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()

        if sid=='Pending':
            emp = Suggestion_Data.objects.filter(Status_M='Pending').filter(Status_A='Pending')[::-1]
            pagestatus='Pending'
        elif sid=='Accepted':
            emp = Suggestion_Data.objects.filter(Status_M='Pending').filter(Status_A='Accepted')[::-1]
            pagestatus='Accepted'
        else:
            emp = Suggestion_Data.objects.filter(Status_M='Pending')[::-1]
            pagestatus='Review'


        paginator = Paginator(emp, per_page=5)  # Show 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages
        context1 = {
            'q': page_obj.object_list,
            'status': sid,
            'notification': notification,
            'notification_manager':notification_manager,
            'page_obj': page_obj,
            'pagestatus':pagestatus,
            'totalpagelist': [n+1 for n in range(totalpage)],
            'u':user(request)
        }
        return render(request, 'reviewemployee.html', context1)
    else:
        return redirect('/mains/login')
  
def romyquestions(request,fid):
    if check(request):
        q = Suggestion_Data.objects.get(Form_id=fid)

        context1={
            'i' : q,
            'u' : user(request) 
        }

        return render(request,'romyquestions.html',context1)
    else:
        return redirect('/mains/login')

def rcreviewemployee(request,fid) :
    if check(request) and request.session.get('role')=='admin':
        notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        q = Suggestion_Data.objects.get(Form_id=fid)
        r = list(Login.objects.all().values())
        context1={
            'notification': notification,
            'notification_manager':notification_manager,
            'notification_issue':notification_issue,
            'i' : q,
            'r' : r,
            'u' : user(request)
        }
        return render(request,'rcreviewemployee.html',context1)
    else:
        return redirect('/mains/login')

def solveissues(request,sid):
        if check(request) and request.session.get('role')=='user':
            notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
            
            if sid=='Pending':
                emp = Suggestion_Data.objects.all().filter(Manager_mail=request.session.get('mail')).filter(Status_M='Pending').reverse()[::-1]
                pagestatus='Pending'
            elif sid=='Accepted':
                emp = Suggestion_Data.objects.all().filter(Manager_mail=request.session.get('mail')).filter(Status_M='Accepted').reverse()[::-1]
                pagestatus='Accepted'
            else:
                emp = Suggestion_Data.objects.all().filter(Manager_mail=request.session.get('mail')).reverse()[::-1]
                pagestatus='Solve'

           

            paginator = Paginator(emp, per_page=5)  # Show 5 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            totalpage = page_obj.paginator.num_pages
            
            context1={
                'notification_issue':notification_issue,
                'q': page_obj.object_list, 
                'status' : sid,
                'u' : user(request),
                'page_obj': page_obj,
                'pagestatus':pagestatus,
                'totalpagelist': [n+1 for n in range(totalpage)]
                }
            print(emp)
            print(page_obj)
            return render(request,'solveissues.html',context1)
        else:
            return redirect('/mains/login')

def repsolveissues(request,fid):
    if check(request):
        q = Suggestion_Data.objects.get(Form_id=fid)
        notification_issue = Suggestion_Data.objects.filter(Status_M='Pending').filter(Manager_mail=request.session.get('mail')).count()
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        context1={
            'i' : q,
            'notification':notification,
            'notification_manager':notification_manager,
            'notification_issue':notification_issue,
            'u' : user(request) 
        }
        return render(request,'repsolveissues.html',context1)
    else:
        return redirect('/mains/login')

def askquestions2(request):
    if check(request) and request.session.get('role')=='admin':
        r = list(Login.objects.all().values())
        notification = Suggestion_Data.objects.filter(Status_A='Pending').count()
        notification_manager = Suggestion_Data.objects.filter(Status_A='Pending').filter(Status_M='Accepted').count()
        context1={
            'r' : r,
            'notification':notification,
            'notification_manager':notification_manager,
            'u' : user(request),
        }
        return render(request,'askquestions2.html',context1)
    else:
        return redirect('/mains/login')

def admin_accept(request,fid):
    if check(request) and request.session.get('role')=='admin':   
        if request.method == "POST":
            q = Suggestion_Data.objects.get(Form_id=fid)
            a_answer=request.POST.get('a_answer')
            m_mail=request.POST.get('m_mail')
            q.Admin_answer=a_answer
            q.Manager_mail=m_mail
            q.Status_A="Accepted"
            print(q.Status_A)
            q.save()
            send_email_to_solve(request,m_mail)
            return redirect('/mains/reviewemployee/review')
        else:
            pass
    else:
        return redirect('/mains/login')

def admin_reject(request,fid):
    if check(request) and request.session.get('role')=='admin':
        if request.method == "POST":
            q = Suggestion_Data.objects.get(Form_id=fid)
            a_answer=request.POST.get('A_answer')
            m_mail=request.POST.get('m_mail')
            q.Admin_answer=a_answer
            q.Manager_mail=m_mail
            q.Status_A="Rejected"
            q.Status_M="Rejected"
            q.save()
            return redirect('/mains/reviewemployee/review')
        else:
            pass
    else:
        return redirect('/mains/login')
     
def manageraccept(request,fid):
    if check(request) and request.session.get('role')=='user':
        if request.method == "POST":
            q = Suggestion_Data.objects.get(Form_id=fid)
            m_answer=request.POST.get('Manager_answer')
            q.Manager_answer=m_answer
            q.Status_M="Accepted"
            q.Status_A="Pending"
            q.save()
            return redirect('/mains/solveissues/solve')
        else:
            pass
    else:
        return redirect('/mains/login')
     
def managercancel(request,fid):
    if check(request) and request.session.get('role')=='user':
        if request.method == "POST":
            return redirect('/mains/solveissues/solve')
        else:
            pass
    else:
        return redirect('/mains/login')

def publish(request,fid):
    if check(request) and request.session.get('role')=='admin':
        if request.method == "POST":
            q = Suggestion_Data.objects.get(Form_id=fid)
            q.Status_A="Accepted"
            q.save()
            send_email_to_check(request,q.Mail)
            return redirect('/mains/reviewmanager/review')
        else:
            pass
    else:
        return redirect('/mains/login')

    
def authenticate(request, email=None,password=None):

    try:
        user = Login.objects.all().get(Password=password, Mail=email)
        return user
    except Login.DoesNotExist:
        return None

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        password=request.POST.get('password')
        user = authenticate(request, password=password, email=email )
        username=user.Mail.split("@")[0].capitalize()


        
        print(username)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # Redirect authenticated user to a desired page
            request.session['username'] = username
            request.session['mail'] = user.Mail
            print(user,"--------------------")
            request.session['role'] = user.Role
            request.session['login'] = True
            request.session['password']=user.Password
        
    
            if user.Role=="user":
                return redirect('/mains/') 
            elif user.Role=="admin":


                return redirect('/mains/admin/')
        else:
            # Display an error message for failed authentication
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def logout(request):
            request.session['username'] = None
            request.session['mail'] = None
            request.session['role'] = None
            request.session['login'] = False
            return redirect('/mains/login/')

def search(request):
    if check(request):
        query = request.GET.get('search')

        results = Suggestion_Data.objects.filter(
            Q(Title__icontains=query) | 
            Q(Description__icontains=query) |
            Q(Admin_answer__icontains=query) |
            Q(Manager_answer__icontains=query)
        )
        paginator = Paginator(results, per_page=5)  # Show 5 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        totalpage = page_obj.paginator.num_pages

        context1={
                'q': page_obj.object_list,
                'u' : user(request),
                'totalpagelist': [n+1 for n in range(totalpage)],
                'page_obj': page_obj,
        }

        return render(request, 'home.html', context1)
    else:
        return redirect('/mains/login')


