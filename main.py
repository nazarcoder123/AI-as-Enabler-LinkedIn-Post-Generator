from fastapi import FastAPI, HTTPException, Body
import requests, os
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY is required.")
genai.configure(api_key=api_key)
app = FastAPI(title="AI as Enabler")

def scrape_text(url): 
    r = requests.get(url, timeout=10); r.raise_for_status()
    return " ".join([p.text for p in BeautifulSoup(r.content, "html.parser").find_all("p")])

def generate_post(text, perspective): 
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""You are a professional LinkedIn strategist. Write a 200–250 word post from a {perspective}'s view on 'AI as an enabler', based on this article:\n{text}\nAvoid fluff. Be insightful, persuasive, and include a call-to-action."""
    post = model.generate_content(prompt).text.strip()
    score_prompt = f"""Rate this post (1–100) on how well it aligns with 'AI as an enabler':\n{post}\nReturn only a number."""
    score = model.generate_content(score_prompt).text.strip()
    return post, score

@app.post("/generate-post")
async def create_post(
    url: str = Body(default=None),
    content: str = Body(default=None),
    perspective: str = Body(...),
):
    if not content and not url:
        raise HTTPException(status_code=400, detail="Provide URL or content.")
    text = content.strip() if content else scrape_text(url)
    if not text:
        raise HTTPException(status_code=400, detail="No content retrieved.")
    text = text[:10000]

    post, score = generate_post(text, perspective)
    return {
        "linkedin_post": post,
        "confidence_score": score
    }
