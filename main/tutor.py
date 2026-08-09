import ollama 
import sounddevice as sd 
import soundfile as sf 
import whisper

whisper_model = whisper.load_model('base') 
messages = [{'role': 'system', 'content': 'Act as a friendly, patient Hungarian tutor.'}]

while True:
    input('Press Enter to record for 5 seconds...')
    fs = 16000 
    audio = sd.rec(int(5 * fs), samplerate=fs, channels=1) 
    sd.wait() 
    sf.write('temp.wav', audio, fs) 
    text = whisper_model.transcribe('temp.wav')['text'] 
    print('You:', text)
    enough= 'quit' in text.lower() or 'exit' in text.lower() or 'stop' in text.lower() 
    if enough:
        break
    messages.append({'role': 'user', 'content': text}) 
    res = ollama.chat(model='mistral', messages=messages) 
    print('Tutor:', res['message']['content']) 
    messages.append(res['message'])