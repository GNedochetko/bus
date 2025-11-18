import sys
import bus

def executarArquivo(pathArquivo):
    if not pathArquivo.endswith('.bus'):
        print("A extensão do arquivo está errada.")
        return
    
    try:
        with open(pathArquivo, 'r') as arquivo:
            texto = arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo {pathArquivo} não encontrado")

    for numero, linha in enumerate(texto.split('\n'), start=1):
        if linha.strip() == '':
            continue

        resultado, erro = bus.run(pathArquivo, linha)
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python shel.py <nomeArquivo>.bus")
    else:
        executarArquivo(sys.argv[1])
