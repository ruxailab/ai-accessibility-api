from gtts import gTTS
import os

def text_to_speech(text_list, filename="output.mp3"):
    """
    Converts a list of words to an MP3 file.

    Args:
        text_list (list): A list of words to convert to speech.
        filename (str): The name of the output MP3 file.
    """
    text = " ".join(text_list)
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Audio saved to {filename}")

# Example usage:
words = ["Home", "about", "contact", "rest"]
text_to_speech(words)