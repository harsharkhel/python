import speech_recognition as sr
import pyttsx3
import time

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            # Listen from microphone
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")

            # Google Speech Recognition
            command = r.recognize_google(audio)
            print(f"You said: {command}")

        except sr.WaitTimeoutError:
            print("No speech detected.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")

        except sr.RequestError as e:
            print(f"Google Speech Recognition error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")