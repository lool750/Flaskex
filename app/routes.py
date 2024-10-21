from app import app

from flask import render_template
from flask import request
import requests
import json
link = "https://flasktintcarlos-default-rtdb.firebaseio.com/"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',titulo="Bem-Vindo(a)")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo ="Entre em contato conosco")

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo ="Cadastro")

@app.route('/consultar')
def consultar():
    return render_template('consultar.html', titulo ="")

@app.route('/atualizacao')
def atualizacao():
    return render_template('atualizacao.html', titulo ="Atualização")

@app.route('/exclusao')
def exclusao():
    return render_template('exclusao.html', titulo ="Exclusão")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    try:
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        dados = {"cpf":cpf,"nome":nome,"telefone":telefone,"endereco":endereco}
        requisicao = requests.post(f'{link}/cadastro/.json', data = json.dumps(dados))
        return 'Cadastrado com sucesso!'
    except Exception as e:
        return f'Ocorreu um erro\n +{e}'

@app.route('/listar')
def listarTudo():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        return  dicionario
    except Exception as e:
        return f'Algo deu errado \n {e}'

@app.route('/listarIndividual')
def listarIndividual(cpf): #consultar CPF
    try:
        requisicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requisicao.json()
        cpfCadastro = "" #coletar o id
        for codigo in dicionario:
            chaveCpf = dicionario[codigo]['cpf']
            if chaveCpf == cpf:
                return codigo
    except Exception as e:
        return f'Algo deu errado\n {e}'


@app.route('/excluir', methods=['POST'])
def excluir():
    try:
        cpf = request.form.get("cpf")
        idCadastro = listarIndividual(cpf)
        requisicao = requests.delete(f'{link}/cadastro/{idCadastro}/.json')
        return "Excluido com sucesso"

    except Exception as e:
        return f'Algo deu errado\n{e}'


@app.route('/atualizarCpf', methods=['POST'])
def atualizarCpf():
    try:
        cpf = request.form.get("cpf")
        idCadastro = listarIndividual(cpf)
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        dados = {"nome":nome,"telefone":telefone,"endereco":endereco}
        requisicao = requests.patch(f'{link}/cadastro/{idCadastro}/.json', data=json.dumps(dados))
        return "Atualizado com sucesso"

    except Exception as e:
        return f'Algo deu errado\n{e}'


@app.route('/consultarGeral', methods=['POST'])
def consultarGeral():
    try:
        cpf = request.form.get("cpf")
        idCadastro = listarIndividual(cpf)
        requisicao = requests.get(f'{link}/cadastro/{idCadastro}/.json')
        dicionario = requisicao.json()
        nome = dicionario["nome"]
        telefone = dicionario["telefone"]
        endereco = dicionario["endereco"]
        resposta = f'CPF: {cpf}\n Nome: {nome}\n Telefone: {telefone}\n Endereço: {endereco}'
        return resposta
    except Exception as e:
        return f'Algo deu errado\n {e}'






