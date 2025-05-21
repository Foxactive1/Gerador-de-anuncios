# Gerador de Anúncios com IA

Uma aplicação Flask que utiliza a API do OpenRouter para gerar textos persuasivos para anúncios de produtos utilizando modelos de IA como Claude e outros.

## Recursos

- Geração de textos persuasivos para anúncios
- Suporte a múltiplos modelos de IA (Claude, Gemini, Llama)
- Upload de imagens de produtos
- Interface amigável construída com Bootstrap
- Compartilhamento fácil dos anúncios gerados

## Instalação

1. Clone este repositório:
```bash
git clone https://seu-repositorio/gerador-anuncios-ia.git
cd gerador-anuncios-ia
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure suas variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto (ou edite o existente)
   - Adicione sua chave API do OpenRouter:
   ```
   OPENROUTER_API_KEY=sua-chave-api-aqui
   SECRET_KEY=uma-chave-secreta-aleatoria
   ```

5. Execute a aplicação:
```bash
flask run
```

6. Acesse a aplicação em seu navegador:
```
http://localhost:5000
```

## Como Usar

1. Preencha o nome do produto
2. Selecione o estilo do anúncio
3. Escolha o modelo de IA desejado
4. Faça upload de uma imagem do produto (opcional)
5. Clique em "Gerar Anúncio"
6. Copie o texto gerado ou compartilhe nas redes sociais

## Modelos Disponíveis

- Claude 3 Haiku (Rápido)
- Claude 3 Sonnet (Balanceado)
- Claude 3 Opus (Avançado)
- Google Gemini Pro
- Meta Llama 3 70B

## Segurança

- Nunca compartilhe seu arquivo `.env` ou exponha suas chaves API
- Esta aplicação valida e sanitiza os uploads de arquivos
- Em ambiente de produção, considere medidas adicionais de segurança

## Licença

MIT
