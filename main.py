import base64
import vertexai
from vertexai.generative_models import GenerativeModel
import vertexai.generative_models as generative_models
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
import json

def multiturn_generate_content():
  # Initialize the Vertex AI model
  vertexai.init(project="poised-defender-426800-h6", location="us-central1")
  model = GenerativeModel(
      "projects/936854510592/locations/us-central1/endpoints/3851138432331939840",
  )
  chat = model.start_chat()

  # Read the analysis_results.json file
  try:
      with open('analysis_results.json', 'r') as json_file:
          analysis_results = json.load(json_file)
          sentiment_results = json.dumps(analysis_results, indent=4)
  except FileNotFoundError:
      print("JSON file not found.")
      return

  # Get the topic from user input
  topic = input("What topic would you like to write a newsletter about? ")

  # Construct the message for the chat
  message = (
      f"""Here is the sentiment and style that I want you to base your newsletters around:
      {sentiment_results}
      Do not mention the sentiment and style in the output.
      Write a very intriguing article about '{topic}' for a weekly news marketing article based on this data."""
  )

  # Send the message and get the response
  response = chat.send_message(
      message,
      generation_config=generation_config,
      safety_settings=safety_settings
  )

  # Extract and print the generated newsletter
  newsletter = response.candidates[0].content.parts[0].text
  show_popup(newsletter)
  return

from tkinter import font

def show_popup(newsletter):
  # Create the main window
  window = tk.Tk()
  window.title("Generated Newsletter")
  window.geometry("1000x600")
  # Create a scrolled text widget to display the content
  text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=120, height=30)
  text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

  # Set a monospace font for better formatting
  monospace_font = font.Font(family="Courier", size=10)
  text_area.configure(font=monospace_font)

  # Insert the newsletter content with proper formatting
  formatted_newsletter = newsletter.replace("\n", "\n\n")
  text_area.insert(tk.END, formatted_newsletter)

  # Make the text area read-only
  text_area.config(state=tk.DISABLED)

  # Run the tkinter main loop
  window.mainloop()
  
# Load sentiment data and configure generation settings
try:
  with open('analysis_results.json', 'r') as json_file:
    analysis_results = json.load(json_file)
    sentiment_results = json.dumps(analysis_results, indent=4)
except FileNotFoundError:
  print("JSON file not found.")
  sentiment_results = "{}"

# Extract values from the sentiment analysis results
avg_output_tokens = analysis_results['writing_style']['avg_num_tokens']
subjectivity = analysis_results['sentiment']['subjectivity']

# Define generation configuration and safety settings
generation_config = {
  "max_output_tokens": int(min(max(avg_output_tokens * 1.1, 0), 8192)),
  "temperature": min(max(subjectivity * 0.01, 0), 1),
  "top_p": 0.95,
}

safety_settings = {
  generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Run the content generation function
multiturn_generate_content()