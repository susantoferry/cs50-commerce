from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe

from .models import Comment, Auction


class CommentsForm(forms.Form):
    comentarios = forms.CharField(label="",
        widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '4',
            'placeholder': 'Place your comment here'
        })
    )

class CommentForm(forms.ModelForm):

    comment = forms.CharField(label=mark_safe("<strong>Type your comment below</strong>"),
                            widget = forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': '4',
                            'placeholder': 'Place your comment here'
                        })
        )
                            
    class Meta:
        model = Comment
        exclude = ["auction", "author", "date"]

class SellForm(forms.ModelForm):

    title = forms.CharField(label=mark_safe("<strong>Type your title below</strong>"),
                            min_length=1,
                            max_length=100,
                            widget=forms.TextInput
                            (attrs={'class':'form-control mb-2',
				            'placeholder':'Title'
                            }))

    description = forms.CharField(label=mark_safe("<strong>Type your description below</strong>"),
                            widget = forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': '7',
                            'placeholder': 'Description item'
                        }))

    price = forms.CharField(label=mark_safe("<strong>Type your price below</strong>"),
                            min_length=1,
                            max_length=100,
                            widget=forms.NumberInput
                            (attrs={'class':'form-control mb-2',
				            'placeholder':'Price'
                            })) 

    image = forms.CharField(label=mark_safe("<strong>Type your url image below</strong>"),
                            min_length=1,
                            max_length=255,
                            widget=forms.TextInput
                            (attrs={'class':'form-control mb-2',
				            'placeholder':'Url image'
                            }))

    class Meta:
        model = Auction
        exclude = ["auction", "author", "date"]
                              