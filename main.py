##  OpenAI's Text-Davinci-003 Model based Voice Assistant
##  Author: Ryan 
##  API Key left intentionally blank. Fill in your own private API key. 
##  Ensure appropriate drivers are installed
##  If facing "AttributeError: 'super' object has no attribute 'init'", then: https://stackoverflow.com/questions/76434535/attributeerror-super-object-has-no-attribute-init

import openai
import pyttsx3 
import speech_recognition

#OpenAI API key is private. You can retrieve your own on the website. 
openai.api_key = ""

system = pyttsx3.init()
def transcribe(filename):
    detector = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(filename) as source:
        audio = detector.record(source)
    try:
        return detector.recognize_google(audio)
    except:
        print('Transcribing Error')

def response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens = 2500,
        n=1,
        stop = None,
        temperature = 1.25, 
    )
    return response["choices"][0]["text"]

def speech(text):
    system.say(text)
    system.runAndWait()

def main():
    while True:
        print("Hi, say 'System' to begin...")
        with speech_recognition.Microphone() as source:
            detector = speech_recognition.Recognizer()
            audio = detector.listen(source)
        try:
            transcription = detector.recognize_google(audio)
            if transcription.lower() == "system":

                filename = "input.wav"
                print("How may I help you today?")
                with speech_recognition.Microphone() as source:
                    detector = speech_recognition.Recognizer()
                    source.pause_threshold = 1
                    audio = detector.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as z:
                        z.write(audio.get_wave_data())

                text = transcribe(filename)
                if text:
                    response = response(text)
                    print(f"System says: {response}")

                    speech(response)
        except Exception as a:
            print("Error: {}".format(a))

if __name__ == "__main__":
    main()