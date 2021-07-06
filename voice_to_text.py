import speech_recognition as sr
def read():
    filename = "predictions/demo.wav"
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        f= open("voice.txt","w+")
        f.write(text)
        f.close()
        print(text)
