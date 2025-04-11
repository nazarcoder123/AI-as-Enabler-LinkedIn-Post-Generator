import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyB97KS2QgzC95-UNXz9nFBX7_F1UxOFcag")  # Replace with your actual API key or use st.secrets

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

# Generate a summary using Gemini with a perspective
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

# Generate LinkedIn post based on the summary and AI as enabler philosophy
def generate_linkedin_post(summary):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "Generates a LinkedIn post (200-250 words) reflecting the client's 'AI as enabler'' philosophy. "
            "The post should be insightful, thought-provoking, and based on the following summary of an article. "
            "Include a light call-to-action at the end, and write in a human, conversational tone suitable for professionals.\n\n"
            f"Summary:\n{summary}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating LinkedIn post: {str(e)}"

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="AI-Powered LinkedIn Post Generator", layout="centered")
st.title("💼 AI-Powered LinkedIn Post Generator (AI as Enabler)")

st.markdown("Paste a blog/article URL or content below. Choose a tone and we’ll generate a professional LinkedIn post that reflects the **'AI as an enabler'** mindset.")

# Input fields
url = st.text_input("🔗 Enter URL (optional):")
pasted_content = st.text_area("📝 Or paste the article content here:", height=300)

# Perspective options
perspectives = [
    "Beginner-friendly",
    "Technical expert",
    "Product/Marketing focus",
    "Critical analysis",
    "Neutral/Objective",
    "Business executive",
    "Academic style"
]
selected_perspective = st.selectbox("🎯 Choose your summary perspective:", perspectives)

# Button to trigger processing
if st.button("Generate LinkedIn Post"):
    if not url and not pasted_content.strip():
        st.warning("Please provide a URL or paste article content.")
    else:
        with st.spinner("Generating your LinkedIn post..."):
            if pasted_content.strip():
                article_text = pasted_content.strip()
            else:
                article_text = scrape_text_from_url(url)
                if article_text.startswith("Error"):
                    st.error(article_text)
                    st.stop()

            summary = summarize_with_gemini(article_text[:6000], selected_perspective)
            linkedin_post = generate_linkedin_post(summary)

            st.subheader("💡 Your LinkedIn Post:")
            st.write(linkedin_post)
