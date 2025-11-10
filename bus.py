TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

class Erro:
    def __init__(self, posInicio, posFinal, nomeDoErro, detalheDoErro):
        self.posInicio = posInicio
        self.posFinal = posFinal
        self.nomeDoErro = nomeDoErro
        self.detalheDoErro = detalheDoErro

    def toString(self):
        resultado = f"{self.nomeDoErro}: {self.detalheDoErro} \n"
        resultado += f"Posição do erro -> Linha: {self.posInicio.linha}, Coluna: {self.posInicio.coluna}"
        return resultado

class ErroCaractereInvalido(Erro):
    def __init__(self, posInicio, posFinal, detalheDoErro):
        super().__init__(posInicio, posFinal, 'Erro de caractere inválido', detalheDoErro)

class Posicao:
    def __init__(self, indice, linha, coluna):
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
        return Posicao(self.indice, self.linha, self.coluna)
    

class Token:
    def __init__(self, tipo, valor = None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        if self.valor is not None:
            return f'{self.tipo} : {self.valor}'
        return f'{self.tipo}'
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Posicao(-1, 0, -1)
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
    
    def make_Tokens(self):
        tokens = []

        while True:
            if self.atual is None:
                tokens.append(TT_EOF)
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
                self.avancar()
            else:
                char = self.atual
                posInicio = self.pos.copia()
                self.avancar()
                return [], ErroCaractereInvalido(posInicio, self.pos, char)
            
        return tokens, None
    
def run(text):
    lexer = Lexer(text)
    tokens, erro = lexer.make_Tokens()
    return tokens, erro



    

