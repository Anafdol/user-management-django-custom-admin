from django.db import models
from utils.cep.check_cep import check_cep
from utils.city.check_city import check_city
from utils.cpf.check_cpf import check_cpf
from utils.phone.check_phone import check_phone
from simple_history.models import HistoricalRecords
from .base import BaseModel

class Person(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nome')
    mother_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome da mãe'
    )
    born_date = models.DateField(
        blank=True,
        null=True,
        help_text="Exemplo: 03/12/2015",
        verbose_name='Dt. nascimento'
    )
    death_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Dt. óbito'
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name='E-mail'
    )
    
    # NOVOS CAMPOS - MELHORIA 3
    companion_name = models.CharField(
        max_length=100,
        verbose_name='Nome do acompanhante',
        blank=True,
        null=True
    )
    companion_phone = models.CharField(
        max_length=20,
        verbose_name='Telefone do acompanhante',
        blank=True,
        null=True
    )
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name='Gênero'
    )
    cpf = models.CharField(
        max_length=14,
        blank=True,
        null=True, # Corrigido de 'ull' para 'null'
        unique=True,
        help_text='Exemplo: 00000000000',
        verbose_name='CPF',
        validators=[check_cpf]
    )
    
    STATE_CHOICES = [
        ("SP", "São Paulo"), ("PR", "Paraná"), ("SC", "Santa Catarina"), 
        ("RS", "Rio Grande do Sul"), ("MS", "Mato Grosso do Sul"), ("RO", "Rondônia"),
        ("AC", "Acre"), ("AM", "Amazonas"), ("RR", "Roraima"), ("PA", "Pará"), 
        ("AP", "Amapá"), ("TO", "Tocantins"), ("MA", "Maranhão"), 
        ("RN", "Rio Grande do Norte"), ("PB", "Paraíba"), ("PE", "Pernambuco"),
        ("AL", "Alagoas"), ("SE", "Sergipe"), ("BA", "Bahia"), ("MG", "Minas Gerais"), 
        ("RJ", "Rio de Janeiro"), ("MT", "Mato Grosso"), ("GO", "Goiás"),
        ("DF", "Distrito Federal"), ("PI", "Piauí"), ("CE", "Ceará"), ("ES", "Espírito Santo")
    ]
    
    rg = models.CharField(max_length=14, blank=True, null=True, verbose_name='RG')
    rg_ssp = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True, verbose_name='SSP')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True, verbose_name='Estado')
    
    address_line_1 = models.CharField(
        max_length=100, blank=True, null=True, 
        help_text='Rua e número da residência', verbose_name='Endereço (linha 1)'
    )
    address_line_2 = models.CharField(
        max_length=100, blank=True, null=True, 
        help_text='Complemento (apartamento, bloco,...)', verbose_name='Endereço (linha 2)'
    )
    neighbourhood = models.CharField(max_length=60, blank=True, null=True, verbose_name='Bairro')
    city = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Cidade", #validators=[check_city]
    )
    postal_code = models.CharField(
        max_length=15, blank=True, null=True, help_text='Exemplo: 00000000', 
        verbose_name="CEP", #validators=[check_cep]
    )
    
    RESIDENCE_TYPE_CHOICES = [('urban', 'Urbano'), ('rural', 'Rural')]
    residence_type = models.CharField(
        max_length=6, choices=RESIDENCE_TYPE_CHOICES, blank=True, null=True, verbose_name='Distrito'
    )
    
    DDD_CHOICES = [(str(i), str(i)) for i in range(11, 100)] # Simplificado para o exemplo

    ddd_private_phone = models.CharField(
        max_length=2, blank=True, null=True, choices=DDD_CHOICES, 
        help_text="Apenas 2 dígitos", verbose_name="DDD"
    )
    private_phone = models.CharField(
        max_length=10, blank=True, null=True, help_text='Exemplo: 999999999', 
        verbose_name='Tel. p/ contato', validators=[check_phone]
    )
    ddd_message_phone = models.CharField(
        max_length=2, blank=True, null=True, choices=DDD_CHOICES, 
        help_text="Apenas 2 dígitos", verbose_name="DDD"
    )
    message_phone = models.CharField(
        max_length=10, blank=True, null=True, help_text='Exemplo: 999999999', 
        verbose_name='Tel. p/ mensagem', validators=[check_phone]
    )
    observation = models.TextField(max_length=600, blank=True, null=True, verbose_name='Observação')

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    @property
    def formatted_born_date(self):
        if self.born_date:
            return self.born_date.strftime("%d/%m/%Y")

    @property
    def formatted_death_date(self):
        if self.death_date:
            return self.death_date.strftime("%d/%m/%Y")

    @property
    def formatted_cpf(self):
        if self.cpf:
            return "{}.{}.{}-{}".format(self.cpf[:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:11])

    @property
    def formatted_postal_code(self):
        if self.postal_code:
            return "{}-{}".format(self.postal_code[:5], self.postal_code[5:9])

    def __str__(self):
        return self.name