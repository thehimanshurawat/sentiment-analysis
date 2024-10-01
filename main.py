import tkinter as tk
import azure.cognitiveservices.speech as speechsdk
import requests

# Azure credentials
speech_key = "b32f134094a2432fa1293380952bfa61"
speech_region = "eastus"
language_key = "d59c070ceefa417687e0b85ddf37a7c8"
language_endpoint = "https://lang097867575.cognitiveservices.azure.com/"

# Function to get sentiment
def get_sentiment(text):
    endpoint = f"{language_endpoint}/text/analytics/v3.0/sentiment"
    headers = {"Ocp-Apim-Subscription-Key": language_key, "Content-Type": "application/json"}
    body = {
        "documents": [{"id": "1", "language": "en", "text": text}]
    }
    response = requests.post(endpoint, headers=headers, json=body)
    sentiment_result = response.json()
    sentiment = sentiment_result['documents'][0]['sentiment']
    return sentiment

# Function to speak sentiment type
def speak_sentiment(sentiment):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    synthesizer.speak_text(f"The sentiment is {sentiment}")

# Function to start speech recognition
def start_listening():
    label_listening.config(text="Listening...")
    entry_text.delete(0, tk.END)  # Clear previous text
    root.update()  # Update the GUI to show the change

    # Speech recognition setup
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # Start recognition
    result = speech_recognizer.recognize_once()
    
    # Print information messages to terminal
    print(f"Result Reason: {result.reason}")

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = result.text
        print(f"Recognized: {recognized_text}")

        # Get sentiment
        sentiment = get_sentiment(recognized_text)
        print(f"Sentiment: {sentiment}")  # Print sentiment type
        speak_sentiment(sentiment)

        # Update GUI with sentiment and recognized text
        label_result.config(text=f"Sentiment: {sentiment}")
        entry_text.delete(0, tk.END)  # Clear the entry
        entry_text.insert(0, recognized_text)  # Display recognized text

    elif result.reason == speechsdk.ResultReason.NoMatch:
        label_result.config(text="No speech could be recognized")
        entry_text.delete(0, tk.END)  # Clear the entry
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        label_result.config(text=f"Speech Recognition canceled: {cancellation_details.reason}")
        print(f"Cancellation Reason: {cancellation_details.reason}")

    # Reset the listening label after processing
    label_listening.config(text="")

# Create the main GUI window
root = tk.Tk()
root.title("Sentiment Analysis")
root.geometry("250x350")  # Set the window size
root.configure(bg="#000")  # Set background color

# Create a frame for the main content
frame = tk.Frame(root, bg="#000", padx=20, pady=20)
frame.pack(pady=20)

# Title label
label_title = tk.Label(frame, text="Sentiment Analysis", font=("Helvetica", 20), fg="white", bg="black")
label_title.pack(pady=10)

# Listening status label
label_listening = tk.Label(frame, text="", font=("Helvetica", 12), fg="red", bg="black")
label_listening.pack(pady=5)

# Create a button to start listening
button_listen = tk.Button(frame, text="Start Listening", command=start_listening, font=("Helvetica", 14), bg="#000", fg="black")
button_listen.pack(pady=20)

# Entry to display recognized text
entry_text = tk.Entry(frame, font=("Helvetica", 14), width=40,bg="#000",fg="white",justify="center")
entry_text.pack(pady=10)

# Label to display the result
label_result = tk.Label(frame, text="Sentiment: ", font=("Helvetica", 16), bg="#000",fg="white")
label_result.pack(pady=20)



# Run the GUI main loop
root.mainloop()
