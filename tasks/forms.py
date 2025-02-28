from django import forms
from tasks.models import Task


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border-2 border-solid border-slate-800 px-2 py-1',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border-2 border-solid border-slate-800 px-2 py-1',
                'placeholder': 'Enter task description'
            }),
            'due_date': forms.SelectDateWidget(attrs={
                'class': 'border-2 border-solid border-slate-800 px-2 py-1',
            }),
            'assigned_to': forms.CheckboxSelectMultiple(attrs={
                'class': 'px-2 py-1',
            }),
        }
