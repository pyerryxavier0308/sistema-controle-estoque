from flask import request, render_template, url_for, redirect, flash
from app import app

from models.Produto import Produto
from views.auth import login_required

CATEGORIAS_VALIDAS = [
    'Informática',
    'Telefonia',
    'Moda',
    'Eletrodomésticos',
    'Automotivo',
    'Pet Shop',
]

TEMPLATE_PRODUTO_INSERT = 'produtos/insert.html'
TEMPLATE_PRODUTO_EDIT = 'produtos/edit.html'
ROTA_PRODUTO_LIST = 'produto.list'
MSG_IDPRODUTO_INVALIDO = "Campo 'idproduto' é obrigatório e deve ser numérico."
MSG_NOME_INVALIDO = "Campo 'nome' é obrigatório e deve ter no máximo 40 caracteres."
MSG_QUANTIDADE_INVALIDA = "Campo 'quantidade' é obrigatório e deve ser numérico."
MSG_CATEGORIA_INVALIDA = "Campo 'categoria' é obrigatório ou é inválido."
MSG_PRODUTO_NAO_ENCONTRADO = 'Produto não encontrado.'
MSG_PRODUTO_INSERIDO = 'Produto inserido com sucesso.'
MSG_PRODUTO_ALTERADO = 'Produto alterado com sucesso.'
MSG_PRODUTO_EXCLUIDO = 'Produto excluído com sucesso.'


def idproduto_valido(idproduto):
    return bool(idproduto and idproduto.isdigit() and int(idproduto) > 0)


def validar_dados_produto(nome, quantidade, categoria):
    if not nome or len(nome) > 40:
        return MSG_NOME_INVALIDO

    if not quantidade or not quantidade.isdigit() or int(quantidade) < 0:
        return MSG_QUANTIDADE_INVALIDA

    if not categoria or categoria not in CATEGORIAS_VALIDAS:
        return MSG_CATEGORIA_INVALIDA

    return None


@app.route('/main/produtos/insert', methods=['GET', 'POST'], endpoint='produto.insert')
@login_required
def insert():
    if request.method == 'GET':
        return render_template(TEMPLATE_PRODUTO_INSERT)

    nome = request.form.get('nome', '')
    quantidade = request.form.get('quantidade', '')
    categoria = request.form.get('categoria', '')

    erro = validar_dados_produto(nome, quantidade, categoria)

    if erro:
        flash(erro)
        return render_template(TEMPLATE_PRODUTO_INSERT)

    model = Produto()
    model.insert(request)
    flash(MSG_PRODUTO_INSERIDO)

    return render_template(TEMPLATE_PRODUTO_INSERT)


@app.route('/main/produtos/delete', methods=['POST'], endpoint='produto.delete')
@login_required
def delete():
    idproduto = request.values.get('idproduto', '')

    if not idproduto_valido(idproduto):
        flash(MSG_IDPRODUTO_INVALIDO)
        return redirect(url_for(ROTA_PRODUTO_LIST))

    model = Produto()
    produto = model.view(request)

    if produto is None:
        flash(MSG_PRODUTO_NAO_ENCONTRADO)
        return redirect(url_for(ROTA_PRODUTO_LIST))

    model.delete(request)
    flash(MSG_PRODUTO_EXCLUIDO)

    return redirect(url_for(ROTA_PRODUTO_LIST))


@app.route('/main/produtos', methods=['GET'], endpoint='produto.list')
@login_required
def list():
    model = Produto()
    produtos = model.list(request)
    return render_template('produtos/list.html', produtos=produtos)


@app.route('/main/produtos/edit', methods=['GET', 'POST'], endpoint='produto.edit')
@login_required
def edit():
    if request.method == 'GET':
        idproduto = request.values.get('idproduto', '')

        if not idproduto_valido(idproduto):
            flash(MSG_IDPRODUTO_INVALIDO)
            return redirect(url_for(ROTA_PRODUTO_LIST))

        model = Produto()
        produto = model.view(request)

        if produto is None:
            flash(MSG_PRODUTO_NAO_ENCONTRADO)
            return redirect(url_for(ROTA_PRODUTO_LIST))

        return render_template(TEMPLATE_PRODUTO_EDIT, produto=produto)

    idproduto = request.form.get('idproduto', '')
    nome = request.form.get('nome', '')
    quantidade = request.form.get('quantidade', '')
    categoria = request.form.get('categoria', '')

    if not idproduto_valido(idproduto):
        flash(MSG_IDPRODUTO_INVALIDO)
        return redirect(url_for(ROTA_PRODUTO_LIST))

    erro = validar_dados_produto(nome, quantidade, categoria)

    if erro:
        flash(erro)
        return render_template(TEMPLATE_PRODUTO_EDIT, produto=request.form)

    model = Produto()

    if model.view(request) is None:
        flash(MSG_PRODUTO_NAO_ENCONTRADO)
        return redirect(url_for(ROTA_PRODUTO_LIST))

    model.edit(request)
    flash(MSG_PRODUTO_ALTERADO)

    return render_template(TEMPLATE_PRODUTO_EDIT, produto=request.form)
