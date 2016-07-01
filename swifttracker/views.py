from django.shortcuts import render

# Create your views here.
from swifttracker.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import Profile, Project, WeeklyReport
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            info = request.POST

            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )

            #name = User.objects.get(username=info['username'])
            profile = Profile.objects.create(user=name, position='', phone='', address='')

            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success_view(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page_view(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home_view(request):
    if request.user.is_authenticated():
        prof = Profile.objects.get(user=request.user)
        proj = Project.objects.filter(username=request.user)

        if prof.birthdate:
             now = datetime.datetime.now()    
             profilebd = prof.birthdate.year
             age = int((datetime.date.today() - prof.birthdate).days / 365.25  )

             context = {'prof':prof,'proj':proj,'age':age}  
             return render(request,'home.html', context)
        else:
            context = {'prof':prof,'proj':proj}
        
            return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))
    # prof = Profile.objects.get(user=request.user)
    # proj = Project.objects.filter(username=request.user)
    
    # if info.birthdate:
    #          now = datetime.datetime.now()    
    #          profilebd = info.birthdate.year
    #          age = int((datetime.date.today() - info.birthdate).days / 365.25  )

    #          context = {'info':info,'proj':proj,'age':age}  
    # return render(request,'pages/dashboard.html', context)
    # else:
    #     context = {'prof':prof,'proj':proj}

    #     return render(request,'home.html',context)

def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)
   

    form = EditForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'position':profile.position,
        'birthdate': profile.birthdate,
        'phone':profile.phone,
        'address':profile.address})
    if request.method == 'POST':
        
        form = EditForm(request.POST)
        if form.is_valid():
            
            info = request.POST
            user = User.objects.filter(username=request.user)
            user.update(first_name = info['first_name'])
            user.update(last_name = info['last_name'])
                    
            profile = Profile.objects.filter(user=request.user)
            profile.update(
                position = info['position'],
                birthdate = info['birthdate'],
                phone = info['phone'],
                address = info['address']) 
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'edit.html', {'form':form})

    return render(request, 'edit.html', {'form':form})

def project_view(request, project_id): 
    data = Project.objects.get(id = project_id)

    reports = WeeklyReport.objects.filter(project_name = data, user = request.user)
    
    return render(request ,'projects.html',{'data':data, 'reports':reports })

def  add_report_view(request, project_id):
    form = WeeklyReportForm()
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            info = request.POST
            projects = Project.objects.get(id=project_id)
            reports = WeeklyReport.objects.create(
                project_name = projects, 
                user = request.user,
                title = info['title'],
                date_track = info['date_track'],
                question1 = info['question1'],
                question2 = info['question2'],
                question3 = info['question3'],
                time_track = info['time_track']
                )
            return HttpResponseRedirect(reverse('project_detail', kwargs={'project_id':project_id}))
        else:
            return render(request, 'add_report.html', {'form':form})
            
    return render(request, 'add_report.html',{'form':form})