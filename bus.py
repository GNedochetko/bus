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
    def __init__(self, nomeDoErro, detalheDoErro):
        self.nomeoErro = nomeDoErro
        self.detalheDoErro = detalheDoErro

    def toString(self):
        return f"{self.nomeoErro}: {self.detalheDoErro}"

class ErroCaractereInvalido(Erro):
    def __init__(self, detalheDoErro):
        super().__init__('Erro de caractere inválido', detalheDoErro)

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
        self.pos = -1
        self.atual = None
        self.avancar()
    
    def avancar(self):
        self.pos += 1
        if(self.pos < len(self.text)):
            self.atual = self.text[self.pos]
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
                self.avancar()
                return [], ErroCaractereInvalido(char)
            
        return tokens, None
    
def run(text):
    lexer = Lexer(text)
    tokens, erro = lexer.make_Tokens()
    return tokens, erro



    

