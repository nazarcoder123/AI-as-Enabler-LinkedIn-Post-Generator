# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# from bs4 import BeautifulSoup
# import google.generativeai as genai
# import os
# from typing import Optional
# import logging
# import sys # Import sys for exiting if API key is missing
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Configure basic logging settings (level, format)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# # Get a logger instance for this module
# logger = logging.getLogger(__name__)

# # Configure Gemini API
# # Retrieve the API key from environment variables for security

# google_api_key = os.getenv("GOOGLE_API_KEY")

# api_key = google_api_key
# if not api_key:
#     # Log a critical error if the API key is missing, as the app cannot function
#     logger.critical("CRITICAL: GOOGLE_API_KEY environment variable not set. Application cannot start.")
#     # Exit the application if the key is missing
#     sys.exit("GOOGLE_API_KEY environment variable is required.")

# # Configure the Gemini client with the retrieved API key
# genai.configure(api_key=api_key)
# # Log successful API configuration
# logger.info("Gemini API configured successfully.")

# # Initialize FastAPI app
# app = FastAPI(title="AI as Enabler API", description="API for LinkedIn post generation with AI as enabler philosophy")
# # Log app initialization
# logger.info("FastAPI application initialized.")

# class ArticleInput(BaseModel):
#     url: Optional[str] = None
#     content: Optional[str] = None
#     perspective: str

# class PostResponse(BaseModel):
#     linkedin_post: str
#     confidence_score: str
#     word_count: int

# @app.get("/")
# def read_root():
#     # Log access to the root endpoint
#     logger.info("Root endpoint '/' accessed.")
#     return {"message": "Welcome to AI as Enabler API"}

# # Function to scrape article from URL
# def scrape_text_from_url(url):
#     # Log the attempt to scrape a specific URL
#     logger.info(f"Attempting to scrape content from URL: {url}")
#     try:
#         response = requests.get(url, timeout=10)
#         # Raise an exception for bad status codes (4xx or 5xx)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")
#         paragraphs = soup.find_all("p")
#         text = " ".join([para.get_text() for para in paragraphs]).strip()
#         if not text:
#             # Log a warning if no paragraph text was found
#             logger.warning(f"No paragraph text found at URL: {url}")
#             # Consider raising HTTPException(status_code=404) if empty content is an error
#         else:
#             # Log successful scraping
#             logger.info(f"Successfully scraped content from URL: {url}")
#         return text
#     except requests.exceptions.RequestException as e:
#         # Log HTTP-related errors during scraping
#         logger.error(f"HTTP error scraping URL {url}: {e}", exc_info=True)
#         raise HTTPException(status_code=400, detail=f"Error fetching content from URL: {str(e)}")
#     except Exception as e:
#         # Log any other unexpected errors during scraping
#         logger.error(f"Unexpected error scraping URL {url}: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Unexpected error processing URL: {str(e)}")


# def generate_linkedin_post(article_text, perspective):
#     logger.info(f"Generating LinkedIn post for perspective: {perspective}")
#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")

#         # Retry logic
#         max_retries = 3
#         for attempt in range(max_retries):
#             logger.debug(f"Attempt {attempt + 1} of {max_retries} for post generation.")
#             prompt_post = (
#                 f"You are a professional content strategist. Write a LinkedIn post "
#                 f"based on the following article. The post MUST be between 200 and 250 words. "
#                 f"The post should reflect the philosophy of 'AI as an enabler', "
#                 f"from the viewpoint of a {perspective}. Avoid generalizations and fluff. "
#                 f"Be concise, professional, and engaging. End with a light call-to-action.\n\n"
#                 f"Article Content:\n{article_text}"
#             )

#             logger.info("Calling Gemini API for post generation.")
#             post_response = model.generate_content(prompt_post)
#             linkedin_post = post_response.text.strip()
#             word_count = len(linkedin_post.split())

#             logger.info(f"Generated post word count: {word_count}")

#             # If valid length, proceed
#             if 200 <= word_count <= 250:
#                 break
#             else:
#                 logger.warning(f"Post word count {word_count} not in range 200–250.")
#         else:
#             logger.error("Failed to generate post within word count range after multiple attempts.")
#             raise HTTPException(status_code=422, detail="Could not generate a valid post between 200 and 250 words.")

#         # Generate confidence score
#         prompt_confidence = (
#             f"Rate how well the following LinkedIn post aligns with the philosophy of 'AI as an enabler'. "
#             f"Give a confidence score from 1 to 100. Just return a number without explanation.\n\nPost:\n{linkedin_post}"
#         )
#         logger.info("Calling Gemini API for confidence score.")
#         confidence_response = model.generate_content(prompt_confidence)
#         score = confidence_response.text.strip()

#         logger.info(f"Successfully generated confidence score: {score}")

#         return linkedin_post, score, word_count

#     except Exception as e:
#         logger.error(f"Error during Gemini API call or processing: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Error generating content via AI model: {str(e)}")



# @app.post("/generate-post", response_model=PostResponse)
# def create_linkedin_post(article_input: ArticleInput):
#     # Log the reception of a request to this endpoint, including input details
#     logger.info(f"Received request for /generate-post. URL provided: {bool(article_input.url)}, Content provided: {bool(article_input.content)}, Perspective: {article_input.perspective}")

#     # Validate that at least one input source is provided
#     if not article_input.url and not article_input.content:
#         # Log validation failure
#         logger.warning("Validation failed: Neither URL nor content provided in the request.")
#         raise HTTPException(status_code=400, detail="Please provide either URL or article content")

#     article_text = ""
#     # Determine the source of the article text (content or URL)
#     if article_input.content and article_input.content.strip():
#         # Log that provided content is being used
#         logger.info("Using provided content for article text.")
#         article_text = article_input.content.strip()
#     elif article_input.url:
#         # Log that URL scraping is being initiated
#         logger.info("Using provided URL. Attempting to scrape article text.")
#         article_text = scrape_text_from_url(article_input.url)
#     # Note: The case where both are None is handled by the validation above

#     # Ensure we don't exceed input limits for the Gemini API (truncate if needed)
#     # TODO: Make the limit configurable or based on model requirements
#     max_input_len = 10000 # Define max input length
#     if len(article_text) > max_input_len:
#         # Log that input text is being truncated
#         logger.warning(f"Input article text length ({len(article_text)}) exceeds limit ({max_input_len}). Truncating.")
#         article_text = article_text[:max_input_len]
#     elif not article_text:
#          # Log a warning if the article text is empty after processing input
#          logger.warning("Article text is empty after processing input source (URL scrape or direct content).")
#          # Decide how to handle empty text - raise error or return default?
#          raise HTTPException(status_code=400, detail="Could not retrieve or process article content.")

#     # Generate the post using the processed article text
#     # Log initiation of the generation process
#     logger.info("Proceeding to generate LinkedIn post, score, and word count.")
#     linkedin_post, score, word_count = generate_linkedin_post(article_text, article_input.perspective)

#     # Prepare the response object
#     response_data = PostResponse(
#         linkedin_post=linkedin_post,
#         confidence_score=score,
#         word_count=word_count
#     )
#     # Log successful completion of the request with key details
#     logger.info(f"Successfully generated response for perspective '{article_input.perspective}'. Score: {score}, Word Count: {word_count}")
#     return response_data











from fastapi import FastAPI, HTTPException, Request
import requests, os, json
from typing import Optional
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
    return post, score, len(post.split())

@app.post("/generate-post")
async def create_post(request: Request):
    data = await request.json()
    url = data.get("url")
    content = data.get("content")
    perspective = data.get("perspective")
    if not perspective:
        raise HTTPException(400, "Perspective is required.")
    if not content and not url:
        raise HTTPException(400, "Provide URL or content.")
    text = content.strip() if content else scrape_text(url)
    if not text:
        raise HTTPException(400, "No content retrieved.")
    text = text[:10000]
    post, score, count = generate_post(text, perspective)
    return {"linkedin_post": post, "confidence_score": score, "word_count": count}
