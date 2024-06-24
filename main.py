from datetime import time
import time
import nltk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pydub import AudioSegment
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from nltk.tokenize import sent_tokenize

# Use an existing Chrome Profile
options = webdriver.ChromeOptions()
# Replace 'C:\Users\hamza\AppData\Local\Google\Chrome\User Data\Profile 3' with your actual profile path
options.add_argument("user-data-dir=C:\\Users\\hamza\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")

# Initialize the Chrome web driver with the specified options
driver = webdriver.Chrome(options=options)

# Open the Google Cloud Console URL
driver.get('https://console.cloud.google.com/vertex-ai/generative/speech/text-to-speech?project=winged-pen-153321')

# You should already be logged in using your existing Chrome Profile
time.sleep(3)
radio_button = driver.find_element("id", "_0rif_mat-radio-3-input")

# Check the radio button
radio_button.click()


def divide_text_into_sentences(text, max_sentence_length=200):
    # Remove newlines and replace them with spaces
    text = text.replace('\n', ' ')
    sentences = sent_tokenize(text)
    new_sentences = []

    for sentence in sentences:
        if len(sentence) > max_sentence_length:
            split_sentences = sentence.split('.')
            current_sentence = split_sentences[0]
            for part in split_sentences[1:]:
                if len(current_sentence) + len(part) + 1 <= max_sentence_length:
                    current_sentence += '.' + part
                else:
                    new_sentences.append(current_sentence)
                    current_sentence = part

            new_sentences.append(current_sentence)
        else:
            new_sentences.append(sentence)

    return new_sentences





# Start over and ask for new text
while True:
    text = input("Enter the text: ")
    sentences = divide_text_into_sentences(text)

    for i, sentence in enumerate(sentences):
        print(f"Sentence {i + 1}: {sentence}")



    for sentence in sentences:
        # Navigate to the text area and input your text
        textarea = driver.find_element("id", "_0rif_p6ntest-ai-llm-text-to-speech-text-area")



        # Input your sentence
        textarea.clear()  # Clear any existing text
        textarea.send_keys(sentence)

        submit_button = driver.find_element("id", "_0rif_p6ntest-ai-llm-text-to-speech-submit-button")
        submit_button.click()

        wait = WebDriverWait(driver, 10)
        submit_button = wait.until(EC.presence_of_element_located((By.ID, "_0rif_p6ntest-ai-llm-text-to-speech-submit-button")))
        wait.until(EC.element_to_be_clickable((By.ID, "_0rif_p6ntest-ai-llm-text-to-speech-submit-button")))

        # You can optionally submit the form or take further actions on the page as needed

        download_button = driver.find_element("id", "_0rif_p6ntest-ai-llm-text-to-speech-download-button")
        download_button.click()

        # Print the sentence


 #   time.sleep(2)

    from pydub import AudioSegment
    import os
    import shutil

    # Directory where your audio files are located
    source_directory = 'C:\\Users\\hamza\\Downloads'

    # Directory where you want to move the merged audio file
    destination_directory = 'C:\\Users\\hamza\\OneDrive\\Desktop\\audio for the project'

    # Initialize an empty audio segment
    merged_audio = AudioSegment.empty()

    # Create a base filename
    base_filename = "synthesis.wav"

    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)


    # Function to find the next available filename
    def find_available_filename(base_filename, destination_directory):
        i = 0
        while True:
            new_filename = base_filename if i == 0 else f"{base_filename[:-4]} ({i}).wav"
            full_path = os.path.join(destination_directory, new_filename)
            if not os.path.exists(full_path):
                return new_filename
            i += 1


    # Iterate through the expected filenames and merge them
    i = 0
    while True:
        expected_filename = base_filename if i == 0 else f"{base_filename[:-4]} ({i}).wav"
        full_path = os.path.join(source_directory, expected_filename)

        if not os.path.exists(full_path):
            break

        audio_segment = AudioSegment.from_file(full_path)
        merged_audio += audio_segment

        i += 1

    # Determine the new filename with a unique number suffix in the destination directory
    new_filename = find_available_filename(base_filename, destination_directory)

    # Export the merged audio to the new filename
    merged_audio.export(os.path.join(destination_directory, new_filename), format="wav")

    # Delete the original audio files
    i = 0
    while True:
        expected_filename = base_filename if i == 0 else f"{base_filename[:-4]} ({i}).wav"
        full_path = os.path.join(source_directory, expected_filename)

        if not os.path.exists(full_path):
            break

        try:
            os.remove(full_path)
        except Exception as e:
            print(f"Error deleting file {full_path}: {e}")

        i += 1

