from django import forms

class RestructuredTextAreaField(forms.CharField):

    widget = forms.Textarea(attrs={'cols': '80', 'rows': '10', 'wrap': 'off'})

