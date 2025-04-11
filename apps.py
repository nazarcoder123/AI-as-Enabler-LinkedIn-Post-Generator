import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyB97KS2QgzC95-UNXz9nFBX7_F1UxOFcag")

# Function to scrape article from URL
def scrape_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# Summarize with Gemini using a specified perspective
def summarize_with_gemini(text, perspective):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            f"You are an expert summarizer. Your job is to generate a summary of the following article "
            f"from the perspective of **{perspective}**. "
            f"Ensure the tone and style are consistent with this viewpoint, and the summary remains concise and insightful.\n\n"
            f"Article:\n{text}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Streamlit UI
st.title("📰 Perspective-Based Blog / News Summarizer with Gemini")

st.write("Paste a blog/article URL or directly paste the content below to get a perspective-based summary.")

url = st.text_input("Enter the URL (optional):")
pasted_content = st.text_area("Or paste the article content here (optional):", height=300)

# Perspective selection
perspectives = [
    "Beginner-friendly",
    "Technical expert",
    "Product/Marketing focus",
    "Critical analysis",
    "Neutral/Objective",
    "Business executive",
    "Academic style"
]
selected_perspective = st.selectbox("Choose your perspective for the summary:", perspectives)

if st.button("Generate Summary"):
    if not url and not pasted_content.strip():
        st.warning("Please provide a URL or paste article content.")
    else:
        with st.spinner("Generating summary..."):
            if pasted_content.strip():
                article_text = pasted_content.strip()
            else:
                article_text = scrape_text_from_url(url)
                if article_text.startswith("Error"):
                    st.error(article_text)
                    st.stop()

            summary = summarize_with_gemini(article_text[:6000], selected_perspective)
            st.subheader(f"📝 Summary ({selected_perspective}):")
            st.write(summary)
