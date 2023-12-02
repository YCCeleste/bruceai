import streamlit as st
import os
import io
import openai
import numpy as np
import soundfile as sf
from transformers import pipeline

# Fetch the OpenAI API Key securely
open_AI_key = os.environ.get('OPENAI_API_KEY')
if not open_AI_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

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

    # Action Button
    if st.button("Generate Audio"):
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

        # OpenAI API Call
        openai.api_key = open_AI_key
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

        # Initialize the text-to-audio (TTA) pipeline with the MusicGen model
        synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

        # Generate audio from the result text
        try:
            music = synthesiser(result_text, forward_params={"do_sample": True})
            
            # Save the generated music as a .wav file
            audio_data_2d = np.squeeze(music["audio"])
            sf.write("musicgen_out.wav", audio_data_2d.T, music["sampling_rate"], format='WAV')

            # Display the audio
            st.audio("musicgen_out.wav", format='audio/wav')
        except Exception as e:
            st.error("Error in audio generation: " + str(e))

# Running the Streamlit app
if __name__ == "__main__":
    main()
