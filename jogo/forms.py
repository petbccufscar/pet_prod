from django import forms
# Não esqueçam de dar o import do .models da classe a ser implementado o forms
from .models import Medico

# Forms para Médicos:
class Medico_Form(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
        widgets = {
            'perfil': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'salario': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'expertise': forms.RadioSelect(attrs={'name': 'optradio'}),
            'atendimento': forms.RadioSelect(attrs={'name': 'optradio'}),
            'pontualidade': forms.RadioSelect(attrs={'name': 'optradio', 'class': 'radio-inline'}),
        }
        error_messages = {
            'perfil': {'invalid': "O campo Perfil deve conter um número inteiro.",
                       'required': "O campo Perfil deve ser preenchido.",
                       'max_value': "O campo Perfil não deve conter um número inteiro maior que 2147483647.",
                       'min_value': "O campo Perfil deve conter um número inteiro maior que zero.",
                       },
            'salario': {'invalid': "O campo Salário deve conter um número inteiro ou decimal.",
                        'required': "O campo Salário deve ser preenchido.",
                        'max_value': "O campo Salário não deve conter um número maior que 2147483647.0.",
                        'min_value': "O campo Salário deve conter um número maior que zero.",
                        },
        }
