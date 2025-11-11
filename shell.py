import bus

while True:
    text = input('bus>>')
    tokens, erro, arvOp = bus.run("file.bus", text)
    if erro is not None:
        print(erro.toString())
    else:
        print(tokens)
        print(arvOp)