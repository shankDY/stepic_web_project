from django import forms
from django.shortcuts import get_object_or_404

from qa.models import Question, Answer

#form for user question
class AskForm(forms.Form):
    title = forms.CharField(max_length=60)
    text = forms.CharField(widget=forms.Textarea)

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
        ask.save()
        return ask

#form for answer
class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == '':
            raise forms.ValidationError('Text question is empty', code='empty_body_question')
        elif len(text) >= 512: 
            raise forms.ValidationError('Text question is too big', code='big_question')
        return text

    def clean_question(self):
        question_id =self.cleaned_data.get('question')
        question = get_object_or_404(Question, pk=question_id)
        return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

