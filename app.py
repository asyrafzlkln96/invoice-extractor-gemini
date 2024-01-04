from dotenv import load_dotenv

load_dotenv() ##load all env variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

# Input- what you want the AI to do
# Prompt - What you want to ask the AI
def get_gemini_response(input, image, prompt):
	response = model.generate_content([input, image[0], prompt])
	return response.text

def input_image_details(uploaded_file):
	if uploaded_file is not None:
		 #Read the file into bytes
		 bytes_data = uploaded_file.getvalue()
		 image_parts = [
		 {
		 	"mime_type": uploaded_file.type,
		 	"data": bytes_data
		 }

		 ]
		 return image_parts
	else:
		raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multilanguage Invoice Extractor App")
st.header("Multilanguage Invoice Extractor using Gemini")
st.markdown("INFO: This app extracts the details in invoice image by using Gemini Pro AI")

input = st.text_input("Input prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Invoice image...", type=["jpg","jpeg","png"])

image= ""
if uploaded_file is not None:
	image=Image.open(uploaded_file)
	st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")
input_prompt = """
You are an expet in understanding invoices. We will upload an image as invoices
and you will have to answer any questions based on the uploaded invoice image
"""

# If submit button is clicked
if submit:
	image_data = input_image_details(uploaded_file)

	response= get_gemini_response(input_prompt, image_data,input)
	st.subheader("The Response is:")
	st.write(response)