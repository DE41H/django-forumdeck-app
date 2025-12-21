from typing import Any
from datetime import timedelta
from django import forms
from django.utils import timezone
from threads.models import *

class ReportCreateForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = []

    reason = forms.CharField(
        label='Enter Reason',
        required=True,
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        time_delay = timezone.now() - timedelta(minutes=5)
        report_count = Report.objects.filter(reporter=self.user, created_at__gte=time_delay).count()
        if report_count >= 3:
            raise forms.ValidationError('You are reporting too fast!')
        return cleaned_data
