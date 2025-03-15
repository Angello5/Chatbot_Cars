import ollama

while True:

    user_prompt = input('Pibinho: ')
    if user_prompt.lower() == 'gudbai':
        print("Chau")
        break


    response = ollama.generate(model = 'llama3.2-vision', prompt = user_prompt)
    print(response['response'])

