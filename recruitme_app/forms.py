from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import UserProfile, WorkerProfile, JobProfile, Apply, SkillTag, Requirements


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'user_type', 'first_name', 'last_name', 'company_name', 'password1', 'password2',)


    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['company_name'].required = False

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None # Remooving comments


class WorkerProfileForm(ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ('introduction', 'resume',)
        widgets = {
            'introduction': forms.Textarea(attrs={'rows': 10, 'style': 'font-size: medium',}),

        }

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class JobProfileForm(ModelForm):
    class Meta:
        model = JobProfile
        fields = ('offer_name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 20, 'style': 'font-size: medium'}),
        }


class JobApplyForm(forms.ModelForm):

    class Meta:
        model = Apply
        fields = ('coverletter', 'resume',)
        widgets = {
            'coverletter': forms.Textarea(attrs={'class': 'form-control','rows': 10}),
        }

class ResponseForm(forms.ModelForm):

    class Meta:
        model = Apply
        fields = ('employer_comment', 'state',)
        widgets = {
            'employer_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class SkillsForm(forms.ModelForm):

    class Meta:
        model = SkillTag
        fields = ('tagname',)


class RequirementsForm(forms.ModelForm):

    class Meta:
        model = Requirements
        fields = ('rname',)
