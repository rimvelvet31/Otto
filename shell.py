import otto

while True:
    text = input("Otto > ")
    tokens, error = otto.run("<stdin>", text)

    if error:
        print(error.error_message())
    else:
        print(tokens)
