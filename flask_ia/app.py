from flask import Flask, render_template, request
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

#Para rodar o app no Windows digite no terminal set FLASK_ENV=development e depois flask run
#Para rodar o app no Linux digite no terminal export FLASK_ENV=development e depois flask run

#aplicativo principal
app = Flask(__name__)

#rota default
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    #Realiza a leitura dos valores do formulário
    original_text = request.form['text']
    target_language = request.form['language']

    #Carrega os valores de .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    #Indica o que queremos traduzir, a versão da API (3.0) e o idioma de destino
    path = 'translate?api-version=3.0'
    #Adiciona o parâmetro de idioma de destino
    target_language_parameter = '&to=' + target_language
    #Cria o URL completo
    constructed_url = endpoint + path + target_language_parameter

    #Configura as informações do cabeçalho, que inclui a chave de assinatura  
    headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }

    # Cria o corpo do pedido com o texto a ser traduzido
    body = [{ 'text': original_text }]

    #realiza a chamada usando post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    #Recupera a reposta JSON
    translator_response = translator_request.json()
    #Recupera a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    #chama o render template, passando o texto traduzido,
    #o texto original, e o idioma de destino para o template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )