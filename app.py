import streamlit as st
import os
import configparser
import openai
import scipy.io.wavfile
from transformers import pipeline

# Read configuration
config_ini_location = 'config_new.ini'
config = configparser.ConfigParser()
config.read(config_ini_location)
open_AI_key = config['OpenAI']['API_KEY']

# Streamlit App
def main():
    st.title("Bruce Almighty - Fitness Activity Audio Generator")

    # User Inputs
    st.subheader("Activity Information")
    activity_date = st.text_input("Activity Date", value='2023-10-29')
    start_time = st.text_input("Start Time", value='12:00:00')
    end_time = st.text_input("End Time", value='12:10:00')
    activity_type = st.text_input("Type", value='Walking')
    duration = st.text_input("Duration (seconds)", value='600')
    distance = st.text_input("Distance (meters)", value='300')
    calories_burned = st.text_input("Calories Burned", value='20')
    avg_heart_rate = st.text_input("Average Heart Rate", value='80')
    peak_heart_rate = st.text_input("Peak Heart Rate", value='90')
    steps = st.text_input("Steps", value='400')
    notes = st.text_area("Notes", value='I feel tired and unmotivated.')

    # New Feature: Choice between MusicGen and Spotify Suggestion
    choice = st.selectbox("Choose an option", ["Generate a New Song", "Get a Song Suggestion from Spotify"])

    # Action Button
    if st.button("Proceed"):
        user_input = f"""
        Activity Date: {activity_date}
        Start Time: {start_time}
        End Time: {end_time}
        Type: {activity_type}
        Duration: {duration}
        Distance: {distance}
        Calories Burned: {calories_burned}
        Average Heart Rate: {avg_heart_rate}
        Peak Heart Rate: {peak_heart_rate}
        Steps: {steps}
        Notes: {notes}
        """ 

        if choice == "Generate a New Song":
            generate_new_song(user_input)
        elif choice == "Get a Song Suggestion from Spotify":
            st.info("Feature under development")

def generate_new_song(user_input):
    # Set OpenAI API key
    openai.api_key = open_AI_key

    # OpenAI API Call
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                "Generate a text based on what this person's activity shows. "
                "If it has a negative implication, suggest a positive statement "
                "to help and encourage them to recover from the negative situation.\n"
                f"Response: {user_input}"
            ),
            max_tokens=50
        )
        result_text = response.choices[0].text.strip()
    except Exception as e:
        st.error("Error in OpenAI API call: " + str(e))
        return

    # Initialize the MusicGen model
    synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

    # Generate audio from the result text
    try:
        music = synthesiser(result_text, forward_params={"do_sample": True, "max_length": 100, "min_length": 50})
        scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])
        st.audio("musicgen_out.wav", format='audio/wav')
    except Exception as e:
        st.error("Error in audio generation: " + str(e))

# Running the Streamlit app
if __name__ == "__main__":
    main()
