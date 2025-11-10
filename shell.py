import bus

while True:
    text = input('bus>>')
    tokens, erro = bus.run(text)
    if erro is not None:
        print(erro.toString())
    else:
        print(tokens)