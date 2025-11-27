import sys
import time
import busSemPOO
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

    linhas = [linha for linha in texto.split('\n') if linha.strip() != '']

    def executar(modulo, descricao):
        print(f"\n=== {descricao} ===")
        inicio_total = time.perf_counter()
        for numero, linha in enumerate(linhas, start=1):
            try:
                resultado, erro = modulo.run(pathArquivo, linha)
            except Exception as exc:
                resultado, erro = None, exc
        tempo_total = time.perf_counter() - inicio_total
        print(f"Tempo total: {tempo_total:.6f}s\n")

    executar(bus, "Com OO")
    executar(busSemPOO, "Sem OO")
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python shel.py <nomeArquivo>.bus")
    else:
        executarArquivo(sys.argv[1])
