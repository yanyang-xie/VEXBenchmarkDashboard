from django import forms
from django.forms.models import ModelForm

from dashboard.models import VEXGolbalSettings


class VEXGolbalSettingsFrom(ModelForm):
    class Meta:
        model = VEXGolbalSettings
        fields = '__all__'
    
    kubectl_ip_address = forms.GenericIPAddressField(max_length=128, help_text=u'Internal IP Address of Kubernete master',
                                                     error_messages={'max_length': u'Grafana http address is too long(<128)'})
    grafana_http_address = forms.CharField(max_length=128, help_text=u'Http address of Grafana dashboard',
                                           error_messages={'max_length': u'Grafana http address is too long(<128)'})
    
    def clean_grafana_http_address(self):
        grafana_http_address = self.cleaned_data.get('grafana_http_address')
        if grafana_http_address.find('http') != 0:
            raise forms.ValidationError(u'Grafana address should be a http URL')
        return grafana_http_address
    
