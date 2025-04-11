import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# Set up Gemini API key
genai.configure(api_key="AIzaSyB97KS2QgzC95-UNXz9nFBX7_F1UxOFcag")  # Use environment variable in production

def scrape_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract only meaningful text from paragraphs
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error fetching content: {str(e)}"

def summarize_with_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize the following article in a concise and clear way:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Streamlit UI
st.title("📰 Blog / News Summarizer with Gemini")
st.write("Paste a blog/article URL or directly paste the content below to get a summary.")

url = st.text_input("Enter the URL (optional):")
pasted_content = st.text_area("Or paste the article content here (optional):", height=300)

if st.button("Generate Summary"):
    if not url and not pasted_content.strip():
        st.warning("Please provide a URL or paste article content.")
    else:
        with st.spinner("Summarizing..."):
            if pasted_content.strip():
                article_text = pasted_content.strip()
            else:
                article_text = scrape_text_from_url(url)
                if article_text.startswith("Error"):
                    st.error(article_text)
                    st.stop()

            summary = summarize_with_gemini(article_text[:6000])
            st.subheader("📝 Summary:")
            st.write(summary)
