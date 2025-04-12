import streamlit as st
import requests
from typing import Optional, Dict, Any, Tuple

# Define the API endpoint
API_BASE_URL = "http://localhost:8000"

def call_api(endpoint: str, payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Make a POST request to the API and return the response"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return False, {"error": f"Connection Error: {str(e)}"}

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="AI as Enabler – LinkedIn Post Generator", layout="centered")
st.title("💼 AI as Enabler – LinkedIn Post Generator")

st.markdown("Provide a blog/news/article URL or paste content directly below. We'll generate a 200–250 word LinkedIn post from your selected perspective, reflecting the **AI as enabler** philosophy. You'll also receive a confidence score on how well it aligns with this vision.")

# Input fields
url = st.text_input("🔗 Enter URL (optional):")
pasted_content = st.text_area("📝 Or paste the article content here:", height=300)

# Perspective options
perspectives = [
    "Primary care physician",
    "Specialist/Surgeon",
    "Healthcare administrator",
    "Medical researcher/scientist",
    "Patient-centered clinician",
    "Technology-skeptical physician",
    "Technology-enthusiastic physician",
    "Rural/underserved healthcare provider",
    "Medical educator",
    "Public health focused"
]
selected_perspective = st.selectbox("🎯 Choose your perspective:", perspectives)

# Button to trigger post generation
if st.button("Generate LinkedIn Post"):
    if not url and not pasted_content.strip():
        st.warning("Please provide a URL or paste article content.")
    else:
        with st.spinner("Creating your post..."):
            # Prepare payload for API call
            payload = {
                "url": url if url else None,
                "content": pasted_content.strip() if pasted_content.strip() else None,
                "perspective": selected_perspective
            }
            
            # Call API
            success, response = call_api("generate-post", payload)
            
            if not success:
                st.error(response.get("error", "Unknown error occurred"))
            else:
                st.subheader("📢 LinkedIn Post")
                st.write(response["linkedin_post"])

                st.markdown("---")
                st.subheader("📊 Alignment Confidence Score:")
                st.metric(label="Confidence (AI as Enabler)", value=f"{response['confidence_score']}/100")

