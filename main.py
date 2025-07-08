from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fitz  # PyMuPDF
from openai_chat import formatar_com_gpt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile, velocidade: float = Form(...)):
    conteudo_pdf = await file.read()
    texto_extraido = extrair_texto_pdf(conteudo_pdf)
    resposta = formatar_com_gpt(texto_extraido)

    return templates.TemplateResponse("presentation.html", {
        "request": request,
        "titulo": resposta.get("titulo", "Sem título"),
        "autor": resposta.get("autor", "Desconhecido"),
        "cifra": resposta.get("cifra", ""),
        "velocidade": velocidade
    })

def extrair_texto_pdf(pdf_bytes):
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        texto = "\n".join(page.get_text() for page in doc)
    return texto
