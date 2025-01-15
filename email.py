import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("OPENAI_ENDPOINT")
api_version = os.getenv("OPENAI_API_VERSION")

engine="gpt-4o-mini"

client = AzureOpenAI(
  azure_endpoint = endpoint,
  api_key=api_key,
  api_version=api_version
)

# Function to generate a summary of the email
def generate_summary(email_text):
    prompt=f"Summarize the following email:\n{email_text}\n\nSummary:"
    return send_prompt(prompt)

# Function to generate an answer to the email
def generate_answer(email_text):
    prompt=f"Provide a professional response to the following email:\n{email_text}\n\nResponse:"
    return send_prompt(prompt)
    
def send_prompt(prompt):
    try:
        response = client.chat.completions.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are a helpfull assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit App UI
st.title("Email Summarization and Answering App")
st.write("Enter your email below and choose to generate a summary or a response.")

# Text area for email input
email_text = st.text_area("Your Email", height=200)

# Buttons for actions
if st.button("Generate Summary"):
    if email_text.strip():
        summary = generate_summary(email_text)
        st.subheader("Generated Summary")
        st.write(summary)
    else:
        st.warning("Please enter an email to summarize.")

if st.button("Generate Answer"):
    if email_text.strip():
        answer = generate_answer(email_text)
        st.subheader("Generated Answer")
        st.write(answer)
    else:
        st.warning("Please enter an email to generate an answer.")

# Instructions for running the app
st.write("---")
st.write("Run this app using `streamlit run email_app.py`. Ensure your Azure OpenAI Service is configured.")
