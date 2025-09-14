import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

class VoiceAssistant:
    def __init__(self):
        # Initialize recognizer and speech engine
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Choose default voice
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[0].id)  # change index for male/female

    def speak(self, text):
        """Speak out the given text"""
        print("Assistant:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen from microphone and return recognized text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio, language="en-in")
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return ""
            except sr.RequestError:
                self.speak("Network error, please check your connection.")
                return ""

    def greet(self):
        """Greet the user according to the time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good morning!")
        elif 12 <= hour < 18:
            self.speak("Good afternoon!")
        else:
            self.speak("Good evening!")
        self.speak("I am your assistant. How can I help you?")

    def play_music(self):
        """Play the first song from default music folder"""
        music_dir = "C:\\Users\\Public\\Music"
        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                self.speak("Playing music")
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                self.speak("No music files found.")
        else:
            self.speak("Music folder not found.")

    def run(self):
        """Main loop for the assistant"""
        self.greet()
        while True:
            command = self.listen()
            print("Command received:", repr(command))

            if "time" in command:
                now = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"The time is {now}")

            elif "open youtube" in command:
                self.speak("Opening YouTube")
                webbrowser.open("https://youtube.com")

            elif "open google" in command:
                self.speak("Opening Google")
                webbrowser.open("https://google.com")

            elif "play music" in command:
                self.play_music()

            elif "weather" in command:
                self.speak("Please tell me the city name")
                city = self.listen()
                if city:
                    self.speak(f"Showing weather in {city}")
                    webbrowser.open(f"https://www.google.com/search?q=weather+in+{city}")
                else:
                    self.speak("City name not recognized.")

            elif "exit" in command or "quit" in command or "stop" in command:
                self.speak("Goodbye! Have a nice day.")
                break

            elif command:
                self.speak("Let me search that for you.")
                webbrowser.open(f"https://www.google.com/search?q={command}")


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()