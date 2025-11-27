TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_EQ = 'EQ'
TT_VAR = 'VAR'

def criar_erro(posInicio, posFinal, nomeDoErro, detalheDoErro):
    return {
        'posInicio': posInicio,
        'posFinal': posFinal,
        'nomeDoErro': nomeDoErro,
        'detalheDoErro': detalheDoErro
    }

def erro_caractere_invalido(posInicio, posFinal, detalhe):
    return criar_erro(posInicio, posFinal, 'Erro de caractere inválido', detalhe)

def erro_sintaxe_invalida(detalhe, posErro=None):
    if posErro is None:
        posErro = criar_posicao(0, 0, 0, 'Desconhecido')
    return criar_erro(posErro, posErro, 'Erro de caractere inválido', detalhe)

def erro_desconhecido(detalhe, posErro=None):
    if posErro is None:
        posErro = criar_posicao(0, 0, 0, 'Execução')
    return criar_erro(posErro, posErro, 'Erro desconhecido', detalhe)

def erro_para_string(erro):
    resultado = f"{erro['nomeDoErro']}: {erro['detalheDoErro']} \n"
    resultado += f"Posição do erro -> Linha: {erro['posInicio']['linha']}, Coluna: {erro['posInicio']['coluna']} \n"
    resultado += f"Arquivo: {erro['posInicio']['nomeArquivo']}"
    return resultado

def criar_posicao(indice, linha, coluna, nomeArquivo):
    return {
        'indice': indice,
        'linha': linha,
        'coluna': coluna,
        'nomeArquivo': nomeArquivo
    }

def avancar_posicao(posicao, atual=None):
    posicao['indice'] += 1
    posicao['coluna'] += 1
    if atual == '\n':
        posicao['linha'] += 1
        posicao['coluna'] = 0
    return posicao

def copiar_posicao(posicao):
    return {
        'indice': posicao['indice'],
        'linha': posicao['linha'],
        'coluna': posicao['coluna'],
        'nomeArquivo': posicao['nomeArquivo']
    }

def criar_token(tipo, valor=None):
    return {
        'tipo': tipo,
        'valor': valor
    }


def criar_lexer(nomeArquivo, text):
    posicao = criar_posicao(-1, 0, -1, nomeArquivo)
    lexer = {
        'nomeArquivo': nomeArquivo,
        'text': text,
        'pos': posicao,
        'atual': None
    }
    lexer_avancar(lexer)
    return lexer

def lexer_avancar(lexer):
    avancar_posicao(lexer['pos'], lexer['atual'])
    if lexer['pos']['indice'] < len(lexer['text']):
        lexer['atual'] = lexer['text'][lexer['pos']['indice']]
    else:
        lexer['atual'] = None

def lexer_float_or_int(lexer):
    contadorDePontos = 0
    numStr = ''
    while lexer['atual'] is not None and (lexer['atual'].isdigit() or lexer['atual'] == '.'):
        if lexer['atual'] == '.':
            if contadorDePontos == 1:
                break
            contadorDePontos += 1
        numStr += lexer['atual']
        lexer_avancar(lexer)
    if contadorDePontos == 1:
        return criar_token(TT_FLOAT, float(numStr))
    return criar_token(TT_INT, int(numStr))

def lexer_make_var(lexer):
    varStr = ''
    while lexer['atual'] is not None and (lexer['atual'] == '_' or lexer['atual'].isalpha()):
        varStr += lexer['atual']
        lexer_avancar(lexer)
    return criar_token(TT_VAR, varStr)

def lexer_make_tokens(lexer):
    tokens = []
    while True:
        atual = lexer['atual']
        if atual is None:
            tokens.append(criar_token(TT_EOF))
            break
        elif atual.isspace():
            lexer_avancar(lexer)
        elif atual == '+':
            tokens.append(criar_token(TT_PLUS))
            lexer_avancar(lexer)
        elif atual == '-':
            tokens.append(criar_token(TT_MINUS))
            lexer_avancar(lexer)
        elif atual == '*':
            tokens.append(criar_token(TT_MUL))
            lexer_avancar(lexer)
        elif atual == '/':
            tokens.append(criar_token(TT_DIV))
            lexer_avancar(lexer)
        elif atual == '(':
            tokens.append(criar_token(TT_LPAREN))
            lexer_avancar(lexer)
        elif atual == ')':
            tokens.append(criar_token(TT_RPAREN))
            lexer_avancar(lexer)
        elif atual.isdigit():
            tokens.append(lexer_float_or_int(lexer))
        elif atual == '=':
            tokens.append(criar_token(TT_EQ))
            lexer_avancar(lexer)
        elif atual.isalpha() or atual == '_':
            tokens.append(lexer_make_var(lexer))
        else:
            posInicio = copiar_posicao(lexer['pos'])
            char = atual
            lexer_avancar(lexer)
            return [], erro_caractere_invalido(posInicio, lexer['pos'], char)
    return tokens, None

def criar_node(tipo, **kwargs):
    node = {'tipo': tipo}
    node.update(kwargs)
    return node

def criar_parser(tokens):
    parser = {
        'tokens': tokens,
        'tokenIndex': -1,
        'tokenAtual': None
    }
    parser_avancar(parser)
    return parser

def parser_avancar(parser):
    parser['tokenIndex'] += 1
    if parser['tokenIndex'] < len(parser['tokens']):
        parser['tokenAtual'] = parser['tokens'][parser['tokenIndex']]
    else:
        parser['tokenAtual'] = criar_token(TT_EOF)
    return parser['tokenAtual']

def parser_voltar(parser):
    parser['tokenIndex'] -= 1
    parser['tokenAtual'] = parser['tokens'][parser['tokenIndex']]

def parser_factor(parser):
    token = parser['tokenAtual']
    if token['tipo'] in (TT_INT, TT_FLOAT):
        node = criar_node('number', token=token)
        parser_avancar(parser)
        return node, None
    if token['tipo'] == TT_VAR:
        parser_avancar(parser)
        return criar_node('var_acess', token=token), None
    if token['tipo'] == TT_LPAREN:
        parser_avancar(parser)
        exprNode, erro = parser_expr(parser)
        if erro:
            return None, erro
        if parser['tokenAtual']['tipo'] == TT_RPAREN:
            parser_avancar(parser)
            return exprNode, None
        return None, erro_sintaxe_invalida("Esperava encontrar ')'")
    return None, erro_sintaxe_invalida("Esperava número, variável ou '('")

def parser_term(parser):
    left, erro = parser_factor(parser)
    if erro:
        return None, erro
    while parser['tokenAtual']['tipo'] in (TT_DIV, TT_MUL):
        operador = parser['tokenAtual']
        parser_avancar(parser)
        right, erro = parser_factor(parser)
        if erro:
            return None, erro
        left = criar_node('op_binario', left=left, operadorToken=operador, right=right)
    return left, None

def parser_expr(parser):
    left, erro = parser_term(parser)
    if erro:
        return None, erro
    while parser['tokenAtual']['tipo'] in (TT_PLUS, TT_MINUS):
        operador = parser['tokenAtual']
        parser_avancar(parser)
        right, erro = parser_term(parser)
        if erro:
            return None, erro
        left = criar_node('op_binario', left=left, operadorToken=operador, right=right)
    return left, None

def parser_statment(parser):
    tok = parser['tokenAtual']
    if tok['tipo'] == TT_VAR and tok['valor'] == "PRINT":
        parser_avancar(parser)
        exprNode, erro = parser_expr(parser)
        if erro:
            return None, erro
        return criar_node('print', valorNode=exprNode), None
    if tok['tipo'] == TT_VAR:
        varAux = tok
        parser_avancar(parser)
        if parser['tokenAtual']['tipo'] == TT_EQ:
            parser_avancar(parser)
            valorNode, erro = parser_expr(parser)
            if erro:
                return None, erro
            return criar_node('var_assign', token=varAux, valorNode=valorNode), None
        parser_voltar(parser)
    return parser_expr(parser)

def parser_parse(parser):
    resultado, erro = parser_statment(parser)
    if erro:
        return None, erro
    if parser['tokenAtual']['tipo'] != TT_EOF:
        return None, erro_sintaxe_invalida("Simbolos extras após o fim da digitação.")
    return resultado, None

nomeVariaveis = {}

def avaliador(node):
    if node is None:
        return None, erro_desconhecido("Nenhum nó para avaliar")
    tipoNode = node['tipo']
    if tipoNode == 'number':
        return node['token']['valor'], None
    if tipoNode == 'var_acess':
        nome = node['token']['valor']
        if nome not in nomeVariaveis:
            return None, erro_sintaxe_invalida(f'Variavel {nome} não declarada')
        return nomeVariaveis[nome], None
    if tipoNode == 'var_assign':
        nome = node['token']['valor']
        valor, erro = avaliador(node['valorNode'])
        if erro:
            return None, erro
        nomeVariaveis[nome] = valor
        return valor, None
    if tipoNode == 'print':
        valor, erro = avaliador(node['valorNode'])
        if erro:
            return None, erro
        print(valor)
        return valor, None
    if tipoNode == 'op_binario':
        left, erro = avaliador(node['left'])
        if erro:
            return None, erro
        right, erro = avaliador(node['right'])
        if erro:
            return None, erro
        tipo = node['operadorToken']['tipo']
        if tipo == TT_PLUS:
            return left + right, None
        if tipo == TT_MINUS:
            return left - right, None
        if tipo == TT_DIV:
            return left / right, None
        if tipo == TT_MUL:
            return left * right, None
        return None, erro_desconhecido("Operador desconhecido")
    return None, erro_desconhecido("Tipo de nó desconhecido")

def run(nomeArquivo, text):
    lexer = criar_lexer(nomeArquivo, text)
    tokens, erro = lexer_make_tokens(lexer)
    if erro is not None:
        return None, erro
    parser = criar_parser(tokens)
    arvOp, erro = parser_parse(parser)
    if erro is not None:
        return None, erro
    resultado, erro = avaliador(arvOp)
    if erro is not None:
        return None, erro
    return resultado, None
