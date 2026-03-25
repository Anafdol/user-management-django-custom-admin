from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets, filters 
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django_filters.rest_framework import DjangoFilterBackend

from people.models import Person
from people.serializers import PersonSerializer

# 1. ViewSet para a API (Swagger)
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    
    filter_backends = [
        DjangoFilterBackend,    
        filters.SearchFilter,   
        filters.OrderingFilter 
    ]
    
    filterset_fields = ['cpf', 'gender'] 
    search_fields = ['name']
    ordering_fields = ['name']
    # permission_classes = [IsAuthenticated]

# 2. View para o Dashboard (MELHORIA 3: COM FILTROS)
def dashboard_view(request):
    # Captura o que o usuário digitou na busca no template
    busca_nome = request.GET.get('nome', '')
    filtro_genero = request.GET.get('genero', '')

    queryset = Person.objects.all()

    # Aplica os filtros lógicos se o usuário preencher os campos
    if busca_nome:
        queryset = queryset.filter(name__icontains=busca_nome)
    if filtro_genero:
        queryset = queryset.filter(gender=filtro_genero)

    total = queryset.count()
    # A contagem de gêneros também respeita o filtro agora!
    generos = queryset.values('gender').annotate(total=Count('gender'))
    
    context = {
        'total_pacientes': total,
        'generos': generos,
        'query_nome': busca_nome, 
        'query_genero': filtro_genero,
    }
    return render(request, 'people/dashboard.html', context)

# 3. View para Exportar PDF (MELHORIA 1)
def exportar_pacientes_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_casa_danielle.pdf"'
    
    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, altura - 50, "CASA DANIELLE - RELATÓRIO DE GESTÃO")
    p.setFont("Helvetica", 12)
    p.drawString(100, altura - 70, "Parceiro: Irrigação Sem Fronteira")
    p.line(100, altura - 80, 500, altura - 80)

    y = altura - 120
    p.setFont("Helvetica", 10)
    
    pessoas = Person.objects.all()
    
    for pessoa in pessoas:
        if y < 50:
            p.showPage()
            y = altura - 50
        
        data_str = pessoa.created_at.strftime('%d/%m/%Y') if hasattr(pessoa, 'created_at') and pessoa.created_at else 'N/A'
        texto = f"- {pessoa.name} | Cadastro: {data_str}"
        p.drawString(100, y, texto)
        y -= 20

    p.showPage()
    p.save()
    return response