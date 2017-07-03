from django import forms
# Não esqueçam de dar o import do .models da classe a ser implementado o forms
from .models import Medico
from .models import Evento
from .models import Emprestimo

# Forms para Médicos:
class Medico_Form(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
        widgets = {
                'perfil': forms.TextInput(),
                'salario': forms.TextInput(),
                'expertise': forms.RadioSelect(),
                'atendimento': forms.RadioSelect(),
                'pontualidade': forms.RadioSelect(),
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

class Evento_Form(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(),
            'multiplicador_classeA': forms.TextInput(),
            'multiplicador_classeB': forms.TextInput(),
            'multiplicador_classeC': forms.TextInput(),
            'multiplicador_classeD': forms.TextInput(),
            'multiplicador_classeE': forms.TextInput(),
        }
        error_messages = {
            'multiplicador_classeA': {'min_value': 'O campo precisa de um número maior que zero',
                                      'invalid': 'O campo deve conter um número inteiro ou decimal',
                                      'required': 'O campo Multiplicador para Classe A deve ser preenchido'},
            'multiplicador_classeB': {'min_value': 'O campo precisa de um número maior que zero',
                                      'invalid': 'O campo deve conter um número inteiro ou decimal',
                                      'required': 'O campo Multiplicador para Classe B deve ser preenchido',},
            'multiplicador_classeC': {'min_value': 'O campo precisa de um número maior que zero',
                                      'invalid': 'O campo deve conter um número inteiro ou decimal',
                                      'required': 'O campo Multiplicador para Classe C deve ser preenchido',},
            'multiplicador_classeD': {'min_value': 'O campo precisa de um número maior que zero',
                                      'invalid': 'O campo deve conter um número inteiro ou decimal',
                                      'required': 'O campo Multiplicador para Classe D deve ser preenchido',},
            'multiplicador_classeE': {'min_value': 'O campo precisa de um número maior que zero',
                                      'invalid': 'O campo deve conter um número inteiro ou decimal',
                                      'required': 'O campo Multiplicador para Classe E deve ser preenchido',},

            'nome': {'required': 'O campo Nome deve ser preenchido',}

        }

class Emprestimo_Form(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        widgets = {
            'valor': forms.TextInput(attrs={'class': 'col-xs-6'}),
        }
        error_messages = {
            'valor': {'invalid': "O campo Valor deve conter um número inteiro ou decimal.",
                      'required': "O campo Valor deve ser preenchido.",
                      'max_value': "O campo Valor não deve conter um número inteiro maior que 2147483647.0.",
                      'min_value': "O campo Valor deve conter um número inteiro maior que zero.",
                      },
        }