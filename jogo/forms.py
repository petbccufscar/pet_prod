from django import forms
from .models import Evento
from .models import Emprestimo
from .models import Time
from .models import Area, Area_Classe_Social
from .models import Medico, Classe_Social
from .models import Rodada, Modulo, Multiplicador


class MedicoForm(forms.ModelForm):
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


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgetsAux = {}
        error_messages = {
            'nome': {
                'required': 'O campo Nome deve ser preenchido'
            }
        }

        widgets = {
            'nome': forms.TextInput(),
        }


class MultiplicadorForm(forms.ModelForm):
    class Meta:
        model = Multiplicador
        fields = '__all__'
        widgets = {
            'valor': forms.TextInput(),
        }


class EmprestimoForm(forms.ModelForm):
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


class TimeForm(forms.ModelForm):
    repetesenha = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'col-xs-6'}))
    error_messages = {
        'repetesenha': {'invalid': "O campo Repita a Senha deve conter uma palavra .",
                        'required': "O campo Repita a Senha  deve ser preenchido.",
                        'iguais': "As senhas são diferentes."},
    }

    def clean(self):
        cleaned_data = super(TimeForm, self).clean()
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


# Forms para Area
class AreaForm(forms.ModelForm):
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


class AreaClasseSocialForm(forms.ModelForm):
    class Meta:
        model = Area_Classe_Social
        fields = ['entrada', 'desvios']
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


class ClasseSocialForm(forms.ModelForm):
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


class RodadaForm(forms.ModelForm):
    class Meta:
        model = Rodada
        fields = '__all__'
        widgets = {
            'duracao': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'numeroRodada': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'evento': forms.Select(attrs={'class': 'col-xs-6'})

        }
        error_messages = {
            'duracao': {'invalid': "O campo Duração deve conter um número inteiro ou decimal.",
                        'required': "O campo Duração deve ser preenchido.",
                        'max_value': "O campo Duração não deve conter um número maior que 2147483647.0.",
                        'min_value': "O campo Duração deve conter um número maior que zero.",
                        },
            'numeroRodada': {'invalid': "O campo Duração deve conter um número inteiro ou decimal.",
                             'required': "O campo Duração deve ser preenchido.",
                             'max_value': "O campo Duração não deve conter um número maior que 2147483647.0.",
                             'min_value': "O campo Duração deve conter um número maior que zero.",
                             },
            'evento': {'max_length': "O campo Evento deve conter no máximo 200 caracteres.",
                       'required': "O campo Evento deve ser preenchido.",
                       },
        }


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'area': forms.Select(attrs={'class': 'col-xs-6'}),
            'custo_de_aquisicao': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'custo_mensal': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'tecnologia': forms.RadioSelect(attrs={'name': 'optradio', 'class': 'radio-inline'}),
            'conforto': forms.RadioSelect(attrs={'name': 'optradio', 'class': 'radio-inline'}),
            'capacidade': forms.TextInput(attrs={'class': 'col-xs-6'}),
            'preco_do_tratamento': forms.TextInput(attrs={'class': 'col-xs-6'}),
        }
        error_messages = {
            'area': {'max_length': "O campo Área deve conter no máximo 200 caracteres.",
                     'required': "O campo Área deve ser preenchido.",
                     },
            'codigo': {
                'min_value': 'O campo Código deve conter um número maior que zero.',
                'invalid': 'O campo Custo de Aquisição deve conter um número inteiro ou decimal.',
                'max_value': "O campo Custo de Aquisição não deve conter um número maior que 2147483647.0.",
                'required': "O campo Custo Mensal deve ser preenchido.",
            },
            'custo_de_aquisicao': {'invalid': "O campo Custo de Aquisição deve conter um número inteiro ou decimal.",
                                   'required': "O campo Custo de Aquisição deve ser preenchido.",
                                   'max_value': "O campo Custo de Aquisição não deve conter um número maior que 2147483647.0.",
                                   'min_value': "O campo Custo de Aquisição deve conter um número maior que zero.",
                                   },
            'custo_mensal': {'invalid': "O campo Custo Mensal deve conter um número inteiro ou decimal.",
                             'required': "O campo Custo Mensal deve ser preenchido.",
                             'max_value': "O campo Custo Mensal não deve conter um número maior que 2147483647.0.",
                             'min_value': "O campo Custo Mensal deve conter um número maior que zero.",
                             },
            'capacidade': {'invalid': "O campo Capacidade deve conter um número inteiro.",
                           'required': "O campo Capacidade deve ser preenchido.",
                           'max_value': "O campo Capacidade não deve conter um número inteiro maior que 2147483647.",
                           'min_value': "O campo Capacidade deve conter um número inteiro maior que zero.",
                           },
            'preco_do_tratamento': {'invalid': "O campo Preço do Tratamento deve conter um número inteiro ou decimal.",
                                    'required': "O campo Preço do Tratamento deve ser preenchido.",
                                    'max_value': "O campo Preço do Tratamento não deve conter um número maior que 2147483647.0.",
                                    'min_value': "O campo Preço do Tratamento deve conter um número maior que zero.",
                                    },

        }
