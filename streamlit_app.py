import streamlit as st
import pandas as pd
from recommender import SHLRecommender
import json
import re

# MUST be the first Streamlit command
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for glassmorphism vibes - using a single cleaner block
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
    /* Main Background */
    .stApp {
        background: #050510 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(112, 0, 255, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(0, 229, 255, 0.15) 0%, transparent 40%) !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* Hide Streamlit elements */
    header, footer, #MainMenu {
        visibility: hidden !important;
    }

    /* Title Styling */
    .title-container {
        padding: 2rem 0;
        text-align: center;
    }
    .title-text {
        font-family: 'Outfit', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 600 !important;
        background: linear-gradient(90deg, #00e5ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        color: #a0a0c0 !important;
        font-size: 1.2rem !important;
    }

    /* Input Container (Glassmorphism) */
    div.stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: white !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
    }
    div.stTextArea textarea:focus {
        border-color: #00e5ff !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2) !important;
    }

    /* Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00e5ff, #7000ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 10px 20px rgba(112, 0, 255, 0.3) !important;
        width: 100% !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(112, 0, 255, 0.4) !important;
        background: linear-gradient(45deg, #7000ff, #00e5ff) !important;
    }

    /* Result Card Styling */
    .result-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        margin-bottom: 1.5rem !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        transition: all 0.3s ease !important;
    }
    .result-card:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.01) !important;
    }
    .result-info h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #00e5ff !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 1.3rem !important;
    }
    .result-info a {
        color: #a0a0c0 !important;
        text-decoration: none !important;
        font-size: 0.9rem !important;
        word-break: break-all !important;
    }
    .result-info a:hover {
        color: #ffffff !important;
        text-decoration: underline !important;
    }
    .score-badge {
        background: rgba(0, 229, 255, 0.1) !important;
        color: #00e5ff !important;
        padding: 0.5rem 1rem !important;
        border-radius: 20px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        white-space: nowrap !important;
    }
    .meta-info {
        font-size: 0.8rem !important;
        color: #7000ff !important;
        margin-bottom: 0.3rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    try:
        return SHLRecommender('assessments_full.json')
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    # Header Section
    st.markdown("""
    <div class="title-container">
        <div class="title-text">SHL Assessment Recommender</div>
        <div class="subtitle-text">AI-Powered Talent Matching Engine • Optimized for SHL Product Catalog</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout optimization
    _, col, _ = st.columns([1, 6, 1])
    
    with col:
        recommender = load_recommender()
        if not recommender: return

        query = st.text_area("Hiring Query", 
                            placeholder="Paste Job Description here...",
                            height=200, label_visibility="collapsed")
        
        # Center the button
        _, b_col, _ = st.columns([2, 2, 2])
        with b_col:
            find_btn = st.button("FIND ASSESSMENTS", use_container_width=True)

        if find_btn:
            if query.strip():
                with st.spinner("Processing..."):
                    recommendations = recommender.recommend(query, top_n=10)
                    
                    if not recommendations:
                        st.info("No relevant matches found.")
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        for res in recommendations:
                            st.markdown(f"""
                            <div class="result-card">
                                <div class="result-info">
                                    <div class="meta-info">Assessment Solution</div>
                                    <h3>{res['Assessment name']}</h3>
                                    <a href="{res['URL']}" target="_blank">{res['URL']}</a>
                                </div>
                                <div class="score-badge">MATCH {int(res['score'] * 100)}%</div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a job description.")

if __name__ == "__main__":
    main()
