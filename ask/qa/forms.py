from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from qa.models import Question, Answer

#form add user question
class AskForm(forms.Form):
    title = forms.CharField(max_length=60)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(AskForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == '':
            raise forms.ValidationError('Title is empty', code='empty_title')
        elif len(title) >= 60:
            raise forms.ValidationError('Title is too big', code='big_title')
        return title
    

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == '':
            raise forms.ValidationError('Text question is empty', code='empty_body_question')
        elif len(text) >= 512: 
            raise forms.ValidationError('Text question is too big', code='big_question')
        return text

    #save data
    def save(self):
        ask = Question(**self.cleaned_data)
        ask.author = self._user
        ask.save()
        return ask

#form add answer
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    #verification text
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == '':
            raise forms.ValidationError('Text question is empty', code='empty_body_question')
        elif len(text) >= 512: 
            raise forms.ValidationError('Text question is too big', code='big_question')
        return text
    
    #verification question
    def clean_question(self):
        question_id =self.cleaned_data.get('question')
        question = get_object_or_404(Question, pk=question_id)
        return question

    #save data
    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author = self._user
        answer.save()
        return answer

#form add signup
class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    #verification username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('username not set')
        try:
            _ = User.objects.get(username=username)
            raise forms.ValidationError('This user already exists')
        except User.DoesNotExist:
            pass
        return username
        
    #verification email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_email = User.objects.filter(email=email)
        if not email:
            raise forms.ValidationError('email address not set', code='empty_email')
        if len(existing_email) > 0:
            raise forms.ValidationError('That email address already exists', code='mail_exist')
        return email

    #verification password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('password not set')
        return make_password(password)

    #save data
    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user

#form add login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)


    #validation of the entire form
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username:
            raise forms.ValidationError('username is empty')
        elif not password:
            raise forms.ValidationError('password is empty')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid username and password')
        if not user.check_password(password):
            raise forms.ValidationError('Invalid username and password')
    
    def save(self):
        user = authenticate(**self.cleaned_data)
        return user
