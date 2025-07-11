# 🎵 CifraMusic

**CifraMusic** é uma aplicação web que permite enviar cifras de músicas gospel em PDF, extrair e organizar automaticamente a letra e os acordes em formato estruturado, exibindo-os de forma legível e responsiva.

---

## ✨ Funcionalidades

- Upload de PDFs com letras cifradas de músicas gospel
- Extração automática de texto do PDF
- Estruturação com ajuda da API OpenAI (GPT)
- Visualização limpa com formatação de acordes
- Histórico das cifras enviadas
- Interface leve e responsiva (Jinja2 + CSS customizado)

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [OpenAI API](https://platform.openai.com/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Uvicorn](https://www.uvicorn.org/)
- PostgreSQL (via `psycopg2`)
- HTML/CSS

---

## 📦 Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ciframusic.git
   cd ciframusic
Crie e ative um ambiente virtual:

2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
Instale as dependências:

3. Instale as dependências:
pip install -r requirements.txt
Configure a variável de ambiente no arquivo .env:

4. Configure a variável de ambiente no arquivo .env:
OPENAI_API_KEY=sua_chave_aqui
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco


5. Execute a aplicação:

uvicorn main:app --reload
🌐 Deploy
A aplicação está pronta para ser hospedada em algum servidor ou Render utilizando o arquivo Procfile.

