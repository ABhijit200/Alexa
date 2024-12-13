import speech_recognition as sr
import pyttsx3
import openai
import time
from datetime import datetime

# Set your OpenAI API key
openai.api_key = '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'  # Replace with your actual OpenAI API key

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak_text(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking text: {e}")

# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio)
                print(f"You said: {query}")
                return query
            except sr.UnknownValueError:
                print("Sorry, could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
    except Exception as e:
        print(f"Error recognizing speech: {e}")
        return None

# Function to process the query using OpenAI API
def process_query(query):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-1106",  # Use 'model' instead of 'engine'
            prompt=query,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error processing query: {e}")
        return "I couldn't find an answer to that."

# Function to generate a call summary
def generate_summary(transcript):
    try:
        summary = f"Call Summary - {datetime.now()}\n\nTranscript:\n{transcript}"
        with open("call_summary.txt", "w") as file:
            file.write(summary)
        print("Call summary saved as call_summary.txt")
    except Exception as e:
        print(f"Error generating summary: {e}")

# Main function to handle the call
def main():
    print("Starting call...")
    transcript = ""
    start_time = time.time()
    max_duration = 40 * 60  # 40 minutes in seconds

    while time.time() - start_time < max_duration:
        query = recognize_speech_from_mic()
        if query:
            transcript += f"You: {query}\n"
            response = process_query(query)
            speak_text(response)
            transcript += f"Alexa: {response}\n"
        else:
            time.sleep(1)  # Wait for 1 second before trying again

    print("Call ended.")
    generate_summary(transcript)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main function: {e}")