import asyncio
import ctypes

import edge_tts
import ollama
import sounddevice as sd
import soundfile as sf
import whisper


whisper_model = whisper.load_model("tiny")
messages = [
	{"role": "system", "content": ": Act as a patient Hungarian tutor. Always format your responses by grouping English explanations under an EN label and Hungarian speech under a HU label, like this: EN: Here is how you greet someone. HU: Szia!"}
]


def play_audio(file_path):
	ctypes.windll.winmm.mciSendStringA(
		f'open "{file_path}" type mpegvideo alias mp3'.encode(), None, 0, 0
	)
	ctypes.windll.winmm.mciSendStringA(b"play mp3 wait", None, 0, 0)
	ctypes.windll.winmm.mciSendStringA(b"close mp3", None, 0, 0)


async def speak(text):
	for line in text.split("\n"):
		if line.startswith("EN:"):
			clean_text = line.replace("EN:", "").strip()
			if clean_text:
				communicate = edge_tts.Communicate(clean_text, "en-US-AriaNeural")
				await communicate.save("tutor_output.mp3")
				play_audio("tutor_output.mp3")
		elif line.startswith("HU:"):
			clean_text = line.replace("HU:", "").strip()
			if clean_text:
				communicate = edge_tts.Communicate(clean_text, "hu-HU-NoemiNeural")
				await communicate.save("tutor_output.mp3")
				play_audio("tutor_output.mp3")


async def main_loop():
	while True:
		input("Press Enter to record for 5 seconds...")
		fs = 16000
		audio = sd.rec(int(5 * fs), samplerate=fs, channels=1)
		sd.wait()
		sf.write("temp.wav", audio, fs)
		text = whisper_model.transcribe("temp.wav")["text"]
		print("You:", text)

		if "quit" in text.lower() or "exit" in text.lower():
			break

		messages.append({"role": "user", "content": text})
		res = ollama.chat(model="mistral", messages=messages)
		tutor_response = res["message"]["content"]
		print("Tutor:", tutor_response)
		await speak(tutor_response)
		messages.append(res["message"])


if __name__ == "__main__":
	asyncio.run(main_loop())