from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'employee_code',
            'job_title',
            'location',
            'date_of_joining',
            'date_of_birth',
            'marital_status',
            'contact_number',
            'permanent_address',
            'emergency_number',
            'blood_group',
            'aadhar_number',
            'pan_number',
            'esi_number',
            'pf_number',
            'uan_number',
            'communication_address',
        ]
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'communication_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('placeholder', field.label)




