<!-- cSpell:disable -->
# API Casa Danielle — Desafio Técnico

API para gerenciamento de pessoas em casa de apoio, com recursos de consulta, dashboard visual, exportação de relatórios em PDF e documentação interativa da API.
<!-- cSpell:enable -->

---

## Objetivo

Oferecer uma API REST e um painel de monitoramento para apoiar a operação da Casa Danielle, permitindo cadastro e consulta de pessoas, análise por gênero e geração de relatório em PDF.

---

##   Technologies

- Python
- Django 4.2.29
- Django REST Framework 3.15.1
- drf-yasg (Swagger)
- django-filter
- django-cors-headers
- django-simple-history
- reportlab
- pillow
- python-dotenv
- SQLite (local)

---

## Execute local

### 1. Clonar projeto
```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

### 2. Ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Criar `.env`
```env
SECRET_KEY=sua_chave
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Banco e execução
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

##  Rotas principais

- Admin: `http://127.0.0.1:8000/admin/`
- Swagger: `http://127.0.0.1:8000/swagger/`
- Dashboard: `http://127.0.0.1:8000/dashboard`
- Exportação PDF: rota nomeada `exportar_pdf`

---

## API — Pessoas (`PersonViewSet`)

A API de pessoas permite operações CRUD e suporta filtros:

### Recursos suportados
- **Filtro**: `cpf`, `gender`
- **Busca**: `name`
- **Ordenação**: `name`

### Exemplos
```http
GET /people/?search=maria
GET /people/?gender=F
GET /people/?ordering=name
GET /people/?cpf=12345678900
```

---

##  Dashboard (MVT)

Rota pública: `/dashboard` (sem login).

### Funcionalidades implementadas
- Filtro por nome (`nome`)
- Filtro por gênero (`genero`)
- Indicador de total de pacientes filtrados
- Tabela de distribuição por gênero
- Link rápido para documentação
- Botão para baixar relatório em PDF

---

##  Exportação de PDF

Foi implementada a view `exportar_pacientes_pdf` que:

- gera o arquivo `relatorio_casa_danielle.pdf`
- lista pessoas com nome e data de cadastro
- realiza quebra de página automática quando necessário

---

## Melhorias propostas e implementadas

## 1) User Story
**Como gestor da casa de apoio, eu quero exportar um relatório em PDF, para que eu compartilhe dados de atendimento de forma rápida.**

### 5W2H
- **O quê:** Exportação de relatório PDF com lista de pessoas.
- **Por quê:** Facilitar prestação de contas e acompanhamento.
- **Onde:** Dashboard (`exportar_pdf`).
- **Quando:** Sob demanda do usuário.
- **Quem:** Coordenação e equipe administrativa.
- **Como:** `reportlab` em view Django.
- **Quanto:** Baixo custo de implementação.

### Critérios de aceitação
- [ ] PDF baixado com sucesso ao clicar no botão.
- [ ] Arquivo contém título institucional e listagem.
- [ ] Suporta paginação automática no documento.

---

## 2) User Story
**Como operador da casa, eu quero filtrar pacientes no dashboard por nome e gênero, para que eu encontre informações com mais agilidade.**

### 5W2H
- **O quê:** Filtros no dashboard.
- **Por quê:** Melhorar produtividade operacional.
- **Onde:** Página `/dashboard`.
- **Quando:** Durante consultas diárias.
- **Quem:** Recepção e coordenação.
- **Como:** Query params + filtro ORM.
- **Quanto:** Baixo.

### Critérios de aceitação
- [ ] Filtro por nome funciona com busca parcial.
- [ ] Filtro por gênero retorna resultados corretos.
- [ ] Indicadores respeitam os filtros aplicados.

---

## 3) User Story
**Como desenvolvedor consumidor da API, eu quero endpoints pesquisáveis e ordenáveis com documentação Swagger, para que a integração com front-end seja mais rápida e previsível.**

### 5W2H
- **O quê:** Filtro, busca, ordenação e docs interativas.
- **Por quê:** Reduzir erros e tempo de integração.
- **Onde:** Endpoints REST da app `people`.
- **Quando:** Desenvolvimento e testes.
- **Quem:** Backend, frontend e QA.
- **Como:** DRF + `django-filter` + `drf-yasg`.
- **Quanto:** Baixo a médio.

### Critérios de aceitação
- [ ] Endpoint de pessoas aparece no Swagger.
- [ ] Busca por nome funciona.
- [ ] Filtro por `cpf` e `gender` funciona.
- [ ] Ordenação por `name` funciona.

---

## Observações técnicas

- Em produção, **não usar `DEBUG=True`**.
- Restringir `ALLOWED_HOSTS` e CORS em ambiente produtivo.
- Remover arquivos `__pycache__` e `*.pyc` do versionamento.
- Se o requisito exigir, migrar docs de `drf-yasg` para `drf-spectacular`.

---

## Próximos passos recomendados

1. Migrar `/swagger/` para `drf-spectacular` (`/api/schema/` e `/api/docs/`).
2. Reativar `permission_classes = [IsAuthenticated]` na API, se regra de negócio exigir segurança.
3. Padronizar nomenclatura “pacientes” x “pessoas” em telas e documentação.