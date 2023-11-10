from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tittle', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Escribe un titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Escribe una descripción'}),
            'description': forms.Textarea(attrs={'class': 'form-control text-center'}),
        }