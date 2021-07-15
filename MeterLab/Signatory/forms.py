from django import forms
from .models import *


class signatoryForm(forms.ModelForm):
    class Meta:
        model = signatory
        fields = ['id', 'calibratedby', 'calibratedby_position', 'checkedby',
                  'checkedby_position', 'notedby', 'notedby_position', 'preparedby', 'preparedby_position', 'receivedby', 'receivedby_position']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(signatoryForm, self).__init__(*args, **kwargs)
        # self.fields['rrnumber'].required = False
