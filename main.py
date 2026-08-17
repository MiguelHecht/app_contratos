from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from docxtpl import DocxTemplate
import os
import re

app = FastAPI(title="Gerador de Contratos - Curso Albert")

# Serve a página inicial com o formulário HTML
@app.get("/", response_class=HTMLResponse)
async def carregar_formulario():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/gerar-contrato/")
async def gerar_contrato(
    # Dados do Contratante
    nome_contratante: str = Form(...),
    cpf_contratante: str = Form(...),
    nascimento_contratante: str = Form(""),
    estado_civil: str = Form(""),
    profissao: str = Form(""),
    email_contratante: str = Form(""),
    endereco: str = Form(""),
    cep: str = Form(""),
    telefone_contratante: str = Form(""),
    
    # Dados do Aluno
    nome_aluno: str = Form(...),
    nascimento_aluno: str = Form(""),
    telefone_aluno: str = Form(""),
    email_aluno: str = Form(""),
    escola: str = Form(""),
    serie: str = Form(""),
    
    # Vigência
    mes_inicio: str = Form(""),
    ano_inicio: str = Form("2026"),
    mes_fim: str = Form(""),
    ano_fim: str = Form("2026"),
    
    # Pagamento e Pacote
    forma_pagamento: str = Form(...),
    descricao_pacote: str = Form(...),
    valor_total: str = Form(...),
    num_parcelas: str = Form(""),
    valor_parcela: str = Form(""),
    data_primeira_parcela: str = Form(""),
    data_ultima_parcela: str = Form(""),
    detalhe_isencao: str = Form("")
):
    # 1. Abre o arquivo do modelo (.docx)
    nome_template = "template_contrato.docx"
    if not os.path.exists(nome_template):
        return {"erro": f"Arquivo '{nome_template}' não encontrado na pasta do projeto."}

    doc = DocxTemplate(nome_template)

    # 2. Monta o mapa de variáveis a serem substituídas
    contexto = {
        'nome_contratante': nome_contratante,
        'cpf_contratante': cpf_contratante,
        'nascimento_contratante': nascimento_contratante,
        'estado_civil': estado_civil,
        'profissao': profissao,
        'email_contratante': email_contratante,
        'endereco': endereco,
        'cep': cep,
        'telefone_contratante': telefone_contratante,
        
        'nome_aluno': nome_aluno,
        'nascimento_aluno': nascimento_aluno,
        'telefone_aluno': telefone_aluno,
        'email_aluno': email_aluno,
        'escola': escola,
        'serie': serie,
        
        'mes_inicio': mes_inicio,
        'ano_inicio': ano_inicio,
        'mes_fim': mes_fim,
        'ano_fim': ano_fim,
        
        'forma_pagamento': forma_pagamento,
        'descricao_pacote': descricao_pacote,
        'valor_total': valor_total,
        'num_parcelas': num_parcelas,
        'valor_parcela': valor_parcela,
        'data_primeira_parcela': data_primeira_parcela,
        'data_ultima_parcela': data_ultima_parcela,
        'detalhe_isencao': detalhe_isencao
    }

    # 3. Processa a substituição das tags
    doc.render(contexto)

    # 4. Cria um nome limpo para o arquivo de saída
    nome_limpo = re.sub(r'[^\w\s-]', '', nome_aluno).strip().replace(' ', '_')
    arquivo_saida = f"Contrato_{nome_limpo}.docx"
    doc.save(arquivo_saida)

    # 5. Entrega o arquivo Word para download
    return FileResponse(
        path=arquivo_saida,
        filename=arquivo_saida,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )