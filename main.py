from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fitz  # PyMuPDF
from openai_chat import formatar_com_gpt
from db import salvar_cifra  # ✅ Importa a função do banco
from db import listar_cifras

from db import buscar_cifra_por_titulo

from db import criar_tabela_se_nao_existir
criar_tabela_se_nao_existir()


from fastapi import Path

app = FastAPI()

@app.get("/historico", response_class=HTMLResponse)
def historico(request: Request):
    cifras = listar_cifras()
    return templates.TemplateResponse("historico.html", {
        "request": request,
        "cifras": cifras
    })

@app.get("/cifra/{id}", response_class=HTMLResponse)
def ver_cifra(request: Request, id: int = Path(...)):
    resultado = buscar_cifra_por_id(id)
    if not resultado:
        return HTMLResponse(content="Cifra não encontrada", status_code=404)

    _, titulo, autor, cifra = resultado
    linhas = separar_cifras_letra(cifra)

    return templates.TemplateResponse("presentation.html", {
        "request": request,
        "titulo": titulo,
        "autor": autor,
        "linhas": linhas
    })


@app.get("/cifra/titulo/{titulo}", response_class=HTMLResponse)
def exibir_cifra_por_titulo(request: Request, titulo: str = Path(...)):
    cifra = buscar_cifra_por_titulo(titulo)

    if cifra is None:
        return HTMLResponse(content="Cifra não encontrada", status_code=404)

    return templates.TemplateResponse("presentation.html", {
        "request": request,
        "titulo": cifra["titulo"],
        "autor": cifra["autor"],
        "cifra": cifra["cifra"]
    })

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile):
    conteudo_pdf = await file.read()
    texto_extraido = extrair_texto_pdf(conteudo_pdf)
    resposta = formatar_com_gpt(texto_extraido)

    # ✅ Salva no banco de dados
    salvar_cifra(
        resposta.get("titulo", "Sem título"),
        resposta.get("autor", "Desconhecido"),
        resposta.get("cifra", "")
    )

    # Converte para linhas alinhadas estilo Cifra Club
    linhas = separar_cifras_letra(resposta.get("cifra", ""))

    return templates.TemplateResponse("presentation.html", {
        "request": request,
        "titulo": resposta.get("titulo", "Sem título"),
        "autor": resposta.get("autor", "Desconhecido"),
        "linhas": linhas
    })

def extrair_texto_pdf(pdf_bytes):
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        texto = "\n".join(page.get_text() for page in doc)
    return texto

def separar_cifras_letra(cifra: str):
    linhas_processadas = []
    for linha in cifra.split('\n'):
        cifra_linha = ""
        letra_linha = ""
        i = 0
        while i < len(linha):
            if linha[i] == '[':
                j = linha.find(']', i)
                if j != -1:
                    acorde = linha[i:j+1]
                    cifra_linha += acorde
                    letra_linha += ' ' * (j + 1 - i)
                    i = j + 1
                else:
                    cifra_linha += linha[i]
                    letra_linha += ' '
                    i += 1
            else:
                cifra_linha += ' '
                letra_linha += linha[i]
                i += 1
        linhas_processadas.append({"cifra": cifra_linha, "letra": letra_linha})
    return linhas_processadas
