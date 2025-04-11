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

# Generate LinkedIn post + confidence score
def generate_linkedin_post(article_text, perspective):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash") 

        # First, generate the LinkedIn post
        prompt_post = (
            f"You are a professional content strategist. Write a short LinkedIn post "
            f"short LinkedIn post based on the following article. The post should reflect the philosophy of 'AI as an enabler', "
            f"from the viewpoint of a {perspective}. Avoid generalizations and fluff. Be concise, professional, and engaging. "
            f"End with a light call-to-action.\n\n"
            f"Article Content:\n{article_text}"
        )
        post_response = model.generate_content(prompt_post)
        linkedin_post = post_response.text.strip()

        # Now, evaluate confidence of alignment with "AI as enabler"
        prompt_confidence = (
            f"Rate how well the following LinkedIn post aligns with the philosophy of 'AI as an enabler'. "
            f"Give a confidence score from 1 to 100, where 100 means perfect alignment. "
            f"Just return a number without explanation.\n\nPost:\n{linkedin_post}"
        )
        confidence_response = model.generate_content(prompt_confidence)
        score = confidence_response.text.strip()

        return linkedin_post, score

    except Exception as e:
        return f"Error generating content: {str(e)}", None

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="AI as Enabler – LinkedIn Post Generator", layout="centered")
st.title("💼 AI as Enabler – LinkedIn Post Generator")

st.markdown("Provide a blog/news/article URL or paste content directly below. We'll generate a 200–250 word LinkedIn post from your selected perspective, reflecting the **AI as enabler** philosophy. You’ll also receive a confidence score on how well it aligns with this vision.")

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
selected_perspective = st.selectbox("🎯 Choose your perspective:", perspectives)

# Button to trigger post generation
if st.button("Generate LinkedIn Post"):
    if not url and not pasted_content.strip():
        st.warning("Please provide a URL or paste article content.")
    else:
        with st.spinner("Creating your post..."):
            if pasted_content.strip():
                article_text = pasted_content.strip()
            else:
                article_text = scrape_text_from_url(url)
                if article_text.startswith("Error"):
                    st.error(article_text)
                    st.stop()

            linkedin_post, score = generate_linkedin_post(article_text[:200], selected_perspective)
            
            if score is None:
                st.error(linkedin_post)
            else:
                st.subheader("📢LinkedIn Post")
                st.write(linkedin_post)

                st.markdown("---")
                st.subheader("📊 Alignment Confidence Score:")
                st.metric(label="Confidence (AI as Enabler)", value=f"{score}/100")
