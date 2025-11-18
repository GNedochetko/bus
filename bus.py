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

class Erro(Exception):
    def __init__(self, posInicio, posFinal, nomeDoErro, detalheDoErro):
        super().__init__('f{nomeDoErro}: {detalheDoErro}')
        self.posInicio = posInicio
        self.posFinal = posFinal
        self.nomeDoErro = nomeDoErro
        self.detalheDoErro = detalheDoErro

    def toString(self):
        resultado = f"{self.nomeDoErro}: {self.detalheDoErro} \n"
        resultado += f"Posição do erro -> Linha: {self.posInicio.linha}, Coluna: {self.posInicio.coluna} \n"
        resultado += f"Arquivo: {self.posInicio.nomeArquivo}"
        return resultado

class ErroCaractereInvalido(Erro):
    def __init__(self, posInicio, posFinal, detalheDoErro):
        super().__init__(posInicio, posFinal, 'Erro de caractere inválido', detalheDoErro)

class ErroSintaxeInvalida(Erro):
    def __init__(self, detalheDoErro, posErro=None):
        if posErro is None:
            posErro = Posicao(0, 0, 0, 'Desconhecido')
        super().__init__(posErro, posErro, 'Erro de caractere inválido', detalheDoErro)

class ErroDesconhecido(Erro):
    def __init__(self, detalheDoErro, posErro=None):
        if posErro is None:
            posErro = Posicao(0, 0, 0, 'Execução')
        super().__init__(posErro, posErro, 'Erro desconhecido', detalheDoErro)

class Posicao:
    def __init__(self, indice, linha, coluna, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.indice = indice
        self.linha = linha
        self.coluna = coluna

    def avancar(self, atual = None):
        self.indice += 1
        self.coluna += 1

        if atual == '/n':
            self.coluna = 0
            self.linha += 1

        return self

    def copia(self):
        return Posicao(self.indice, self.linha, self.coluna, self.nomeArquivo)
    

class Token:
    def __init__(self, tipo, valor = None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if self.valor is not None:
            return f'{self.tipo} : {self.valor}'
        return f'{self.tipo}'
    
class Lexer:
    def __init__(self, nomeArquivo, text):
        self.text = text
        self.pos = Posicao(-1, 0, -1, nomeArquivo)
        self.atual = None
        self.avancar()
    
    def avancar(self):
        self.pos.avancar()
        if(self.pos.indice < len(self.text)):
            self.atual = self.text[self.pos.indice]
        else:
            self.atual = None
    
    def floatOrInt(self):
        contadorDePontos = 0
        numStr = ''

        while(self.atual != None and (self.atual.isdigit() or self.atual == '.')):
            if self.atual == '.':
                if contadorDePontos == 1:
                    break
                contadorDePontos += 1
                numStr += self.atual
            else:
                numStr += self.atual
            self.avancar()
        
        if contadorDePontos == 1:
            return Token(TT_FLOAT, float(numStr))
        else:
            return Token(TT_INT, int(numStr))
        
    def makeVar(self):
        varStr = ''

        while self.atual is not None and (self.atual == '_' or self.atual.isalpha()):
            varStr += self.atual
            self.avancar()

        return Token(TT_VAR, varStr)
    
    def makeTokens(self):
        tokens = []

        while True:
            if self.atual is None:
                tokens.append(Token(TT_EOF))
                break
            elif self.atual.isspace():
                self.avancar()
            elif self.atual == '+':
                tokens.append(Token(TT_PLUS))
                self.avancar()
            elif self.atual == '-':
                tokens.append(Token(TT_MINUS))
                self.avancar()
            elif self.atual == '*':
                tokens.append(Token(TT_MUL))
                self.avancar()
            elif self.atual == '/':
                tokens.append(Token(TT_DIV))
                self.avancar()
            elif self.atual == '(':
                tokens.append(Token(TT_LPAREN))
                self.avancar()
            elif self.atual == ')':
                tokens.append(Token(TT_RPAREN))
                self.avancar()
            elif self.atual.isdigit():
                tokens.append(self.floatOrInt())
            elif self.atual == '=':
                tokens.append(Token(TT_EQ))
                self.avancar()
            elif self.atual.isalpha() or self.atual == '_':
                tokens.append(self.makeVar())
            else:
                char = self.atual
                posInicio = self.pos.copia()
                self.avancar()
                return [], ErroCaractereInvalido(posInicio, self.pos, char)
            
        return tokens, None

class NumberNode:
    def __init__(self, token):
        self.token = token
    
    def __repr__(self):
        return f"{self.token}"
    
class opBinario:
    def __init__(self, left, operadorToken, right):
        self.left = left
        self.operadorToken = operadorToken
        self.right = right
    
    def __repr__(self):
        return f"({self.left}, {self.operadorToken}, {self.right})"
    
class VarAcessNode:
    def __init__(self, token):
        self.token = token

class VarAssignNode:
    def __init__(self, token, valorNode):
        self.token = token
        self.valorNode = valorNode

class PrintNode:
    def __init__(self, valorNode):
        self.valorNode = valorNode
        
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = -1
        self.avancar()

    def avancar(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.tokenAtual = self.tokens[self.tokenIndex]
        else:
            self.tokenAtual = Token(TT_EOF)
        
        return self.tokenAtual
    
    def voltar(self):
        self.tokenIndex -= 1
        self.tokenAtual = self.tokens[self.tokenIndex]
    
    def factor(self):
        token = self.tokenAtual

        if token.tipo in (TT_INT, TT_FLOAT):
            node = NumberNode(token)
            self.avancar()
            return node
        
        if token.tipo == TT_VAR:
            self.avancar()
            return VarAcessNode(token)
        
        if token.tipo == TT_LPAREN:
            self.avancar()
            exprNode = self.expr()
            if self.tokenAtual.tipo == TT_RPAREN:
                self.avancar()
                return exprNode
            raise ErroSintaxeInvalida("Esperava encontrar ')'")
        
        raise ErroSintaxeInvalida("Esperava número, variável ou '('")
        
    def term(self):
        left = self.factor()
        while self.tokenAtual.tipo in (TT_DIV, TT_MUL):
            operador = self.tokenAtual
            self.avancar()
            right = self.factor()
            left = opBinario(left, operador, right)
        
        return left

    def expr(self):
        left = self.term()

        while self.tokenAtual.tipo in (TT_PLUS, TT_MINUS):
            operador = self.tokenAtual
            self.avancar()
            right = self.term()
            left = opBinario(left, operador, right)
        
        return left
    
    def statment(self):
        tok = self.tokenAtual

        if tok.tipo == TT_VAR and tok.valor == "PRINT":
            self.avancar()
            expr = self.expr()
            return PrintNode(expr)
        
        if tok.tipo == TT_VAR:
            varAux = tok
            self.avancar()

            if self.tokenAtual.tipo == TT_EQ:
                self.avancar()
                valorNode = self.expr()
                return VarAssignNode(varAux, valorNode)
            else:
                self.voltar()

        return self.expr()

    
    def parse(self):
        resultado = self.statment()
        if self.tokenAtual.tipo != TT_EOF:
            raise ErroSintaxeInvalida("Simbolos extras após o fim da digitação.")
        
        return resultado
    
nomeVariaveis = {}

def avaliador(node):
    if isinstance(node, NumberNode):
        return node.token.valor
    
    if isinstance(node, VarAcessNode):
        nome = node.token.valor
        if nome not in nomeVariaveis:
            raise ErroSintaxeInvalida('Variavel {nome} não declarada')
        
        return nomeVariaveis[nome]
    
    if isinstance(node, VarAssignNode):
        nome = node.token.valor
        valor = avaliador(node.valorNode)
        nomeVariaveis[nome] = valor

        return valor
    
    if isinstance(node, PrintNode):
        valor = avaliador(node.valorNode)
        print(valor)
        return valor
    
    if isinstance(node, opBinario):
        left = avaliador(node.left)
        right = avaliador(node.right)
        tipo = node.operadorToken.tipo

        if tipo == TT_PLUS:
            return left + right
        if tipo == TT_MINUS:
            return left - right
        if tipo == TT_DIV:
            return left / right
        if tipo == TT_MUL:
            return left * right
        
        return ErroDesconhecido("Erro desconhecido")

def run(nomeArquivo, text):
    lexer = Lexer(nomeArquivo, text)
    tokens, erro = lexer.makeTokens()

    if erro is not None:
        return None, erro
    
    parser = Parser(tokens)
    arvOp = parser.parse()

    resultado = avaliador(arvOp)
    return resultado, None
