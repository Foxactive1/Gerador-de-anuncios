from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# OpenRouter configuration from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gerar_anuncio_openrouter(produto, estilo, modelo_escolhido):
    if not OPENROUTER_API_KEY:
        return "⚠️ Chave API não configurada. Verifique o arquivo .env"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": request.host_url,
        "X-Title": "Gerador de Anúncios",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Crie um texto de anúncio para o produto '{produto}' com as seguintes características:
    - Estilo: {estilo}
    - Linguagem: Dinâmica e persuasiva
    - Elementos obrigatórios: Emojis relacionados, chamada para ação
    - Tamanho: Máximo 2 frases
    """

    data = {
        "model": modelo_escolhido,
        "messages": [
            {"role": "system", "content": "Você é um especialista em marketing persuasivo."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 220,
        "temperature": 0.9,
        "stream": False,
        "stop": ["[", " ["],
        "logit_bias": {}
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        resposta = response.json()
        return resposta['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
        if response.status_code == 401:
            return "⚠️ Erro de autenticação com a API. Verifique sua chave API."
        elif response.status_code == 429:
            return "⚠️ Limite de requisições excedido. Tente novamente mais tarde."
        else:
            return f"⚠️ Erro ao conectar com o serviço: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Não foi possível conectar ao serviço. Verifique sua conexão."
    except Exception as e:
        print(f"Erro ao gerar anúncio: {e}")
        return "⚠️ Não foi possível gerar o anúncio no momento."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto', '').strip()
        estilo = request.form.get('estilo', '')
        modelo = request.form.get('modelo', 'anthropic/claude-3-haiku')
        imagem = request.files.get('imagem')
        path_imagem = None

        if not nome_produto:
            flash("Por favor, insira um nome para o produto", "danger")
            return render_template('index.html')

        # Handle image upload
        if imagem and imagem.filename != '':
            if not allowed_file(imagem.filename):
                flash("Formato de arquivo não permitido. Use PNG, JPG, JPEG ou GIF.", "danger")
                return render_template('index.html')
            
            try:
                filename = secure_filename(imagem.filename)
                imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path_imagem = filename
            except Exception as e:
                print(f"Erro ao salvar imagem: {e}")
                flash("Erro ao enviar imagem. Tente novamente.", "warning")

        anuncio = gerar_anuncio_openrouter(nome_produto, estilo, modelo)
        return render_template('resultado.html', anuncio=anuncio, imagem=path_imagem, produto=nome_produto)

    return render_template('index.html', modelos=get_available_models())

def get_available_models():
    """Return a dictionary of available models"""
    return {
        "anthropic/claude-3-haiku": "Claude 3 Haiku (Rápido)",
        "anthropic/claude-3-sonnet": "Claude 3 Sonnet (Balanceado)",
        "anthropic/claude-3-opus": "Claude 3 Opus (Avançado)",
        "google/gemini-pro": "Google Gemini Pro",
        "meta-llama/llama-3-70b-instruct": "Meta Llama 3 70B"
    }

if __name__ == '__main__':
    app.run(debug=True)