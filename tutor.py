import ollama 
messages = [{'role': 'system', 'content': 'Act as a friendly Hungarian tutor for beginners. Be patient take the student in step by step and explain everything in detail. Use simple words and short sentences. Ask questions to the student and wait for their answer before continuing.'}] 
while True: 
    text = input('You: ') 
    if text == 'quit': break 
    messages.append({'role': 'user', 'content': text}) 
    res = ollama.chat(model='mistral', messages=messages) 
    print('Tutor:', res['message']['content']) 
    messages.append(res['message'])