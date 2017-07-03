from django import forms
# Não esqueçam de dar o import do .models da classe a ser implementado o forms
from .models import Medico
from .models import Area, Area_Classe_Social
from .models import Medico, Classe_Social

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

# Forms para Area
class Area_Form(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'col-xs-12'}),

        }
        error_messages = {
            'nome': {'max_length': "O campo Nome deve conter no máximo 200 caracteres.",
                     'required': "O campo Nome deve ser preenchido.",
                     },
        }

# Forms para Area_ClasseSocial TODO
# na verdade e so tirar o comentario apos inserir a classe social

class Area_Classe_Social_Form(forms.ModelForm):
    class Meta:
        model = Area_Classe_Social
        fields = ['entrada','desvios']
        widgets = {
            'entrada': forms.TextInput(attrs={'class': 'col-xs-12'}),
            'desvios': forms.TextInput(attrs={'class': 'col-xs-12'}),

        }
        error_messages = {
            'entrada': {'invalid': "O campo Entrada deve conter um número inteiro ou decimal.",
                      'required': "O campo Entrada deve ser preenchido.",
                      'max_value': "O campo Entrada não deve conter um número inteiro maior que 2147483647.0.",
                      'min_value': "O campo Entrada deve conter um número inteiro maior ou igual a zero.",
                      },
            'desvios': {'invalid': "O campo Desvio deve conter um número inteiro ou decimal.",
                        'required': "O campo Desvio deve ser preenchido.",
                        'max_value': "O campo Desvio não deve conter um número inteiro maior que 2147483647.0.",
                        'min_value': "O campo Desvio deve conter um número inteiro maior ou igual a zero.",
                        },
        }

class Classe_Social_Form(forms.ModelForm):
    class Meta:
        model = Classe_Social
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(),
            'preco_atendimento': forms.TextInput(),
            'nivel_especialidade': forms.TextInput(),
            'nivel_tecnologia': forms.TextInput(),
            'media_conforto': forms.TextInput(),
            'velocidade_atendimento': forms.TextInput(),
        }
        error_messages = {
            'nome': {'max_length': "O campo Nome deve conter no máximo 200 caracteres.",
                     'required': "O campo Nome deve ser preenchido.",
                     },
            'preco_atendimento': {
                'min_value': 'O campo Preço de atendimento deve conter um número maior que zero.',
                'invalid': 'O campo Preço de atendimento deve conter um número inteiro ou decimal.',
                'max_value': "O campo Preço de atendimento não deve conter um número maior que 3.0.",
                'required': "O campo Preço de atendimento deve ser preenchido.",
            },
            'nivel_especialidade': {
                'invalid': "O campo Nível de Especialidade deve conter um número inteiro ou decimal.",
                'required': "O campo Nível de Especialidade deve ser preenchido.",
                'max_value': "O campo Nível de Especialidade não deve conter um número maior que 3.0.",
                'min_value': "O campo Nível de Especialidade deve conter um número maior que zero.",
                },
            'nivel_tecnologia': {
                'invalid': "O campo Nível de tecnologia deve conter um número inteiro ou decimal.",
                'required': "O campo Nível de tecnologia deve ser preenchido.",
                'max_value': "O campo Nível de tecnologia não deve conter um número maior que 3.0.",
                'min_value': "O campo Nível de tecnologia deve conter um número maior que zero.",
                },
            'media_conforto': {'invalid': "O campo Media de conforto deve conter um número inteiro ou decimal.",
                               'required': "O campo Media de conforto deve ser preenchido.",
                               'max_value': "O campo Media de conforto não deve conter um número inteiro maior que 3.0.",
                               'min_value': "O campo Media de conforto deve conter um número inteiro maior que zero.",
                               },
            'velocidade_atendimento': {
                'invalid': "O campo Velocidade de atendimento deve conter um número inteiro ou decimal.",
                'required': "O campo Velocidade de atendimento deve ser preenchido.",
                'max_value': "O campo Velocidade de atendimento não deve conter um número maior que 3.0.",
                'min_value': "O campo Velocidade de atendimento deve conter um número maior que zero.",
                },

        }

