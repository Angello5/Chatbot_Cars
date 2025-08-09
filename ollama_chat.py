import ollama

while True:

    user_prompt = input('Pibinho: ')
    if user_prompt.lower() == 'gudbai':
        print("Chau")
        break

    response = ollama.generate(model = 'deepseek-r1:7b', prompt = user_prompt)
    print(response['response'])

