from django import forms
from .models import meters, meterserials, meterserials_details


class meterForm(forms.ModelForm):
    class Meta:
        model = meters
        fields = ['id', 'dateforwarded', 'rrnumber', 'brand',
                  'metertype', 'serialnos', 'units', 'active', 'userid']
        labels = {
            'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        }
        widgets = {
            'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        }

    def __init__(self, *args, **kwargs):
        super(meterForm, self).__init__(*args, **kwargs)
        self.fields['rrnumber'].required = False


class meterserialsForm(forms.ModelForm):
    class Meta:
        model = meterserials
        fields = ['id', 'idmeters', 'serialno', 'ampheres',
                  'accuracy', 'wms_status', 'status', 'active', 'userid']
        readonly_fields = ['created_at', 'updated_at']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(meterserialsForm, self).__init__(*args, **kwargs)
        self.fields['serialno'].required = True


class serialsdetailsForm(forms.ModelForm):
    class Meta:
        model = meterserials_details
        fields = ['id', 'idmeterserials', 'testdate', 'gen_average',
                  'fullload_average', 'fl1', 'fl2', 'fl3',
                  'lightload_average','ll1', 'll2', 'll3',
                  'reading', 'type', 'volts', 'phase', 'kh', 'ta', 'remarks',
                  'active', 'isdamage', 'userid']
        readonly_fields = ['created_at', 'updated_at']
        # labels = {
        #     'dateforwarded': 'Date Forwarded', 'rrnumber': 'RR# ', 'brand': 'Brand Name', 'metertype': 'Meter Type', 'units': 'Unit'
        # }
        # widgets = {
        #     'dateforwarded': forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'dateforwarded', 'placeholder': 'Select a date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(serialsdetailsForm, self).__init__(*args, **kwargs)
        self.fields['idmeterserials'].required = True

