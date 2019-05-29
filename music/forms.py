from django import forms
from django.contrib.auth.models import User

from .models import Problemset, Problem ,Submission


class ProblemsetForm(forms.ModelForm):

    class Meta:
        model = Problemset
        fields = ['curator', 'problemset_title', 'problemset_type', 'problemset_logo']


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ['problem_title', 'problem_file','problem_expected_output']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['user', 'problem','code']