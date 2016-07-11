import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from .models import Profile, Project, WeeklyReport

class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(
        attrs=dict(required=True, 
                    max_length=30, 
                    placeholder="Username")), 
                    label=_(""), 
                    error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") }
        )
    email = forms.EmailField(widget=forms.TextInput(
        attrs=dict(required=True, 
                    max_length=30, 
                    placeholder="Email")), 
                    label=_(""))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs=dict(required=True, 
                    max_length=30, 
                    render_value=False, 
                    placeholder="Password")), 
                    label=_(""))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs=dict(required=True, 
                    max_length=30, 
                    render_value=False, 
                    placeholder="Confirm Password")), 
                    label=_(""))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super (RegistrationForm, self).__init__(*args, **kwargs)

    class Meta:

        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users.exists():
            raise forms.ValidationError('Email already exist!')

        return email

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password2']:
            self._errors["password"] = ["Passwords did not match!"]
            del form_data['password']
        return form_data

    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(RegistrationForm, self).save(commit=False)

        if commit:
            instance.set_password(self.cleaned_data['password'])
            instance.save()
            Profile.objects.create(user=instance, phone='', address='')
        
        return instance


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['position', 'birthdate', 'phone', 'address']


class EditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)))
    birthdate = forms.DateField(widget=forms.TextInput(attrs={
            'id':'datepicker',
            'type':'date'
            }),input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = Profile
        fields =('first_name',
                'last_name',
                'position',
                'birthdate',
                'phone',
                'address'
            )


class WeeklyReportForm(forms.ModelForm):
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'type':'date'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.FloatField(label='Time Comsumed:')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.project = kwargs.pop('project', None)
        return super(WeeklyReportForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WeeklyReport
        fields = ('title',
                'date_track',
                'question1',
                'question2',
                'question3',
                'time_track'
            )

    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(WeeklyReportForm, self).save(commit=False)
        if commit:
            instance.user = self.user
            instance.project_name = self.project
            instance.save()
        return instance


class EditWeeklyReportForm(forms.ModelForm):
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'type':'date'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.FloatField(label='Time Comsumed:')

    def clean_date_track(self):
        date_track = self.cleaned_data.get('date_track')
        return date_track

    class Meta:
        model = WeeklyReport
        fields = ('title',
                'date_track',
                'question1',
                'question2',
                'question3',
                'time_track'
            )