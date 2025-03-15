import ollama

user_prompt = input('Pibinho: ')
response = ollama.generate(model = 'mistral', prompt = user_prompt)
print(response['response'])