from .models import Emprestimos, Lojas
from django import forms
from django.forms import widgets


class FormLoja(forms.Form):
    nome = forms.CharField(max_length=64)

class LancarEmprestimo(forms.Form):
    data = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}))
    credor = forms.ModelChoiceField(queryset=Lojas.objects.all(), required=True, label='Credor')
    devedor = forms.ModelChoiceField(queryset=Lojas.objects.all(), required=True, label='Devedor')
    valor = forms.DecimalField(required=True, label='Valor')
    
    def clean(self):
        cleaned_data = super().clean()
        credor = cleaned_data.get('credor')
        devedor = cleaned_data.get('devedor')
        if credor == devedor:
            raise forms.ValidationError("O credor não pode ser igual ao devedor.")