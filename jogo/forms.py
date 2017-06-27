from django import forms
# Não esqueçam de dar o import do .models da classe a ser implementado o forms
from .models import Medico
from .models import Time

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

class Time_Form(forms.ModelForm):
    repetesenha = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'col-xs-6'}))
    error_messages = {
        'repetesenha': {'invalid': "O campo Repita a Senha deve conter uma palavra .",
                        'required': "O campo Repita a Senha  deve ser preenchido.",
                        'iguais': "As senhas são diferentes."},
    }
    def clean(self):
        cleaned_data = super(Time_Form, self).clean()
        repetesenha = cleaned_data.get('repetesenha')
        senha = cleaned_data.get('senha')

        if repetesenha != senha:
            self.add_error("repetesenha", "As senhas devem ser iguais.")
        return cleaned_data



    class Meta:
        model = Time
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'login': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'senha': forms.PasswordInput(attrs={'class': 'col-xs-6'}),
            'caixa': forms.NumberInput(attrs={'step': 0.25, 'class': 'col-xs-6'})
        ,
        }

        error_messages = {
            'nome': {'invalid': "O campo Nome deve conter uma palavra .",
                       'required': "O campo Nome deve ser preenchido.",
                       },
            'login': {'invalid': "O campo Login deve conter uma palavra .",
                       'required': "O campo Login deve ser preenchido.",
                       },
            'senha': {'invalid': "O campo Senha deve conter uma palavra .",
                       'required': "O campo Senha deve ser preenchido.",
                       },


        }

