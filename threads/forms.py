from typing import Any
from datetime import timedelta
from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
from threads.models import Report, Reply, Thread

class ReportCreateForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = ['reason']

    def __init__(self, *args, **kwargs) -> None:
        self.reporter = kwargs.pop('reporter')
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        time_delay = timezone.now() - timedelta(minutes=5)
        report_count = Report.objects.filter(reporter=self.reporter, created_at__gte=time_delay).count()
        if report_count >= 3:
            raise forms.ValidationError('You are reporting too fast!')
        return cleaned_data


class ThreadCreateForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['title', 'raw_content', 'tags', 'tagged_courses', 'tagged_documents']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'raw_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs) -> None:
        self.author = kwargs.pop('author')
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        time_delay = timezone.now() - timedelta(minutes=2)
        count = Thread.objects.filter(author=self.author, created_at__gte=time_delay).count()
        if count >= 2:
            raise forms.ValidationError('You are creating threads too fast!')
        return cleaned_data


class ReplyCreateForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = ['raw_content']
        widgets = {
            'raw_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs) -> None:
        self.author = kwargs.pop('author')
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        time_delay = timezone.now() - timedelta(minutes=2)
        count = Reply.objects.filter(author=self.author, created_at__gte=time_delay).count()
        if count >= 2:
            raise forms.ValidationError('You are creating replies too fast!')
        return cleaned_data


class TagCreateForm(forms.Form):
    tag_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9 ]+$',
        message='Enter the tags separated by whitespaces, they cannot include special characters!'
    )
    tags = forms.CharField(
        required=True, 
        validators=[tag_validator], 
        strip=True,
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. physics chemistry maths thermodynamics'
        })
    )

