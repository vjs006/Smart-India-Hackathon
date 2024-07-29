# Initialize the recognizer
import pymongo, datetime, calendar, math, speech_recognition as sr, numpy as np, nltk
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize
from nltk import pos_tag 
class Speech:
    def __init__(self) -> None:
        self.translation = None
        self.nouns, self.gerunds,self.keywords = None, None, None
    def speak(self):
        recognizer = sr.Recognizer()

        # Capture voice input from the microphone
        with sr.Microphone() as source:
            print("Please speak something...")
            try:
                audio = recognizer.listen(source)
                print("Recording finished.")
            except:
                print("No voice heard. Kindly speak.")
                audio = recognizer.listen(source)
                print("Recording finished.")

        # Recognize the speech (convert audio to text)
        try:
            spoken_text = recognizer.recognize_google(
                audio, language="en"
            )  # Specify the language for recognition
            print(f"Recognized text: {spoken_text}")

            # Translate the recognized text to English
            self.translation = GoogleTranslator(source="hi", target="en").translate(
                spoken_text
            )

            print(f"Translation to English: {self.translation}")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )
        except Exception as e:
            print(f"An error occurred: {e}")

        #self.identify_keywords()

    def identify_keywords(self):
        tokens = word_tokenize(self.translation)

        # Perform part-of-speech tagging
        pos_tags = pos_tag(tokens)

        # Extract nouns and gerunds
        self.nouns = [word for word, tag in pos_tags if tag.startswith("N")]
        self.gerunds = [word for word, tag in pos_tags if tag == "VBG"] 

        self.keywords = self.nouns + self.gerunds 

        self.keywords = [i.capitalize() for i in self.keywords]
