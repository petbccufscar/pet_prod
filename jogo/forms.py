from django import forms
# Não esqueçam de dar o import do .models da classe a ser implementado o forms
from .models import Medico
from .models import Evento
from .models import Emprestimo
from .models import Time

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

