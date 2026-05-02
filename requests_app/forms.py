from django import forms
from .models import MaintenanceRequest
from django.utils import timezone
from datetime import datetime, time

class MaintenanceRequestForm(forms.ModelForm):
    request_subcategory = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_request_subcategory'}),
        required=True,
    )

    class Meta:
        model = MaintenanceRequest
        fields = ['request_category', 'request_subcategory', 'title', 'description', 'office_location', 'destination_location', 'priority', 'availability_start', 'availability_end', 'attachment']
        widgets = {
            'request_category': forms.Select(attrs={'class': 'form-control', 'id': 'id_request_category'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of the request', 'data-en-placeholder': 'Brief summary of the request', 'data-fr-placeholder': 'Résumé bref de la demande'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description of what needs to be done', 'data-en-placeholder': 'Detailed description of what needs to be done', 'data-fr-placeholder': 'Description détaillée de ce qui doit être fait'}),
            'office_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Building A, Room 122', 'data-en-placeholder': 'e.g. Building A, Room 122', 'data-fr-placeholder': 'ex. Bâtiment A, Salle 122', 'id': 'id_office_location'}),
            'destination_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Building B, Room 205', 'data-en-placeholder': 'e.g. Building B, Room 205', 'data-fr-placeholder': 'ex. Bâtiment B, Salle 205', 'id': 'id_destination_location'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'availability_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'availability_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_category'].initial = ''
        self.fields['request_category'].widget.choices = [
            ('', '---------'),
            ('deplacement', 'Déplacement'),
            ('nettoyage', 'Nettoyage'),
            ('desinsectisation', 'Désinsectisation'),
            ('maintenance', 'Maintenance'),
        ]
        self.fields['request_subcategory'].choices = [('', '---------')] + list(MaintenanceRequest.SUBCATEGORY_CHOICES)
        self.fields['priority'].widget.choices = [
            ('', '---------'),
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ]
        if not self.instance.pk:
            now = timezone.localtime(timezone.now())
            today = now.date()
            self.fields['availability_start'].initial = datetime.combine(today, time(8, 0))
            self.fields['availability_end'].initial = datetime.combine(today, time(17, 0))

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('request_category')
        subcategory = cleaned_data.get('request_subcategory')
        if category and not subcategory:
            self.add_error('request_subcategory', 'Please select a sub-category.')
        if category == 'deplacement':
            dest = cleaned_data.get('destination_location')
            if not dest:
                self.add_error('destination_location', 'Destination is required for Déplacement requests.')
        return cleaned_data

class AdminRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'scheduled_date', 'admin_notes', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal notes for the service team', 'data-en-placeholder': 'Internal notes for the service team', 'data-fr-placeholder': 'Notes internes pour l\'équipe de service'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for rejection', 'data-en-placeholder': 'Reason for rejection', 'data-fr-placeholder': 'Raison du rejet'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.choices = [
            ('', '---------'),
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('rejected', 'Rejected'),
        ]
