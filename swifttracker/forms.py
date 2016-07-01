import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from .models import Profile, Project

class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30, placeholder="Username")), label=_(""), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30, placeholder="Email")), label=_(""))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False, placeholder="Password")), label=_(""))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False, placeholder="Confirm Password")), label=_(""))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("Username already exists."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Unmatch password."))
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['position', 'birthdate', 'phone', 'address']


class EditForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100, placeholder="Firstname")), label=_(""))
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100, placeholder="Lastname")), label=_(""))
    position = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100, placeholder="Position")), label=_(""))
    birthdate = forms.DateField(widget=forms.TextInput(attrs={
            'id':'datepicker',
            'type':'date'
            }),input_formats=['%Y-%m-%d'], label=_(""))
    phone = forms.IntegerField(widget=forms.TextInput(attrs=dict(required=True, max_length=11, placeholder="Phone")), label=_(""))
    address =forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100, placeholder="Address")), label=_(""))

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        return birthdate


class WeeklyReportForm(forms.Form):
    title = forms.CharField(max_length = 2000)
    date_track = forms.DateField(label='Date', widget=forms.TextInput(attrs={
        'id':'datepicker',
        'type':'date'
        }),input_formats=['%Y-%m-%d'])
    question1 = forms.CharField(label='What I did?:', widget=forms.Textarea)
    question2 = forms.CharField(label='What to do?:', widget=forms.Textarea)
    question3 = forms.CharField(label='Issues/Blocker:', widget=forms.Textarea)
    time_track = forms.FloatField(label='Weekly hours')