from django import forms
from blog.models import Comment

class SendMailForm(forms.Form):
    Name=forms.CharField()
    Email=forms.EmailField()
    To=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')
