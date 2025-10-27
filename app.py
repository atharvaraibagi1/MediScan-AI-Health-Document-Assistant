import streamlit as st
from PyPDF2 import PdfReader
from datetime import datetime
import torch
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

# Page Configuration
st.set_page_config(
    page_title="MediScan AI - Your Health Document Assistant",
    page_icon="🏥",
    layout="wide"
)

# Helper function to call GPT-4
@st.cache_data(ttl=3600)
def get_gpt4_response(prompt, max_tokens=5000, temperature=0.7):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Using GPT-4o mini model
            messages=[
                {"role": "system", "content": "You are a medical expert assistant helping analyze medical documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Helper Functions

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting PDF: {str(e)}")
        return None

def process_document(text, question_type, specific_query=None):
    """Process document using GPT-4"""
    try:
        if question_type == "qa":
            prompt = (
                "You are a medical expert. Answer the following question based on the provided medical document. "
                "Be precise and accurate. If the information is not in the document, say so clearly.\n\n"
                f"Document: {text[:5000]}\n\n"
                f"Question: {specific_query}"
            )
            return get_gpt4_response(prompt, max_tokens=300, temperature=0.3)

        elif question_type == "summary":
            chunks = [text[i:i+3000] for i in range(0, len(text), 3000)]
            summaries = []
            for chunk in chunks:
                prompt = (
                    "Create a detailed medical summary of the following document section. Include:\n"
                    "1. Key medical findings\n"
                    "2. Important diagnoses\n"
                    "3. Critical values\n"
                    "4. Treatment recommendations\n\n"
                    f"Document section: {chunk}"
                )
                summary = get_gpt4_response(prompt, max_tokens=400, temperature=0.3)
                summaries.append(summary)
            return "\n\n".join(summaries)

        elif question_type == "eli5":
            prompt = (
                "You are explaining medical terms to a 5-year-old child. "
                "Use simple words, friendly tone, and helpful analogies.\n\n"
                f"Medical term to explain: {specific_query}\n\n"
                f"Context from medical document: {text[:4000]}\n\n"
                "Provide a child-friendly explanation:"
            )
            return get_gpt4_response(prompt, max_tokens=250, temperature=0.7)

        elif question_type == "medications":
            prompt = (
                "As a pharmacist, create a detailed list of all medications mentioned in this medical document. "
                "For each medication, include:\n"
                "- Medicine name\n"
                "- Dosage information\n"
                "- Frequency of use\n"
                "- Administration route\n"
                "- Any special instructions\n\n"
                f"Medical document: {text[:5000]}"
            )
            medications = get_gpt4_response(prompt, max_tokens=400, temperature=0.3)
            if "no medication" in medications.lower() or not medications.strip():
                return "No medications found in the document."
            return "💊 Medication List:\n\n" + medications

        elif question_type == "recommendations":
            prompt = (
                "As a healthcare provider, provide detailed, evidence-based health recommendations "
                "based on this medical document. Cover these categories:\n"
                "1. Diet and Nutrition\n"
                "2. Physical Activity\n"
                "3. Lifestyle Modifications\n"
                "4. Preventive Care\n"
                "5. Follow-up Care\n\n"
                f"Medical document: {text[:5000]}"
            )
            recommendations = get_gpt4_response(prompt, max_tokens=500, temperature=0.4)
            return "🌟 Health Recommendations:\n\n" + recommendations

    except Exception as e:
        return f"Error processing document: {str(e)}"

    except Exception as e:
        return f"Error processing document: {str(e)}"

# Custom CSS
st.markdown("""
    <style>
    .main-header {color: #1E88E5; font-size: 2.5rem; font-weight: bold; text-align: center;}
    .feature-box {background-color: #f0f7ff; padding: 1.5rem; border-radius: 10px; 
                 margin: 1rem 0; border-left: 5px solid #1E88E5;}
    .warning-box {background-color: #fff3e0; padding: 1rem; border-radius: 5px; 
                 border-left: 4px solid #ff9800; margin: 1rem 0;}
    </style>
""", unsafe_allow_html=True)

# Main Interface
st.markdown('<p class="main-header">🏥 MediScan AI - Health Document Assistant</p>', 
            unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

# Sidebar
with st.sidebar:
    st.title("📋 Features")
    st.markdown("""
    - 🔍 Health Document Q&A
    - 📝 Smart Summaries
    - 👶 ELI5 Explanations
    - 💊 Medication Tracker
    - 🌟 Health Recommendations
    """)
    st.divider()
    st.markdown("### ℹ️ About")
    st.info("Uses specialized biomedical AI models to help understand health documents. Always consult healthcare professionals.")

# File Upload
uploaded_file = st.file_uploader("📁 Upload your health document (PDF)", type=['pdf'])

if uploaded_file:
    with st.spinner("📖 Reading document..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.session_state.extracted_text = extracted_text
            st.success("✅ Document processed successfully!")

    # Create feature tabs
    tabs = st.tabs(["💬 Q&A", "📋 Summary", "👶 ELI5", "💊 Medications", "🌟 Recommendations"])
    
    # Q&A Tab
    with tabs[0]:
        st.subheader("🔍 Ask Questions")
        question = st.text_input("Your question about the document:")
        if st.button("Get Answer") and question:
            with st.spinner("Processing..."):
                answer = process_document(st.session_state.extracted_text, "qa", question)
                st.write("Answer:", answer)
    
    # Summary Tab
    with tabs[1]:
        st.subheader("📋 Document Summary")
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = process_document(st.session_state.extracted_text, "summary")
                st.write(summary)
    
    # ELI5 Tab
    with tabs[2]:
        st.subheader("👶 Explain Like I'm 5")
        term = st.text_input("Enter medical term to explain:")
        if st.button("Explain") and term:
            with st.spinner("Simplifying..."):
                explanation = process_document(st.session_state.extracted_text, "eli5", term)
                st.info(explanation)
    
    # Medications Tab
    with tabs[3]:
        st.subheader("💊 Medication Information")
        if st.button("Extract Medications"):
            with st.spinner("Finding medications..."):
                meds = process_document(st.session_state.extracted_text, "medications")
                st.write(meds)
    
    # Recommendations Tab
    with tabs[4]:
        st.subheader("🌟 Health Recommendations")
        if st.button("Get Recommendations"):
            with st.spinner("Generating recommendations..."):
                recs = process_document(st.session_state.extracted_text, "recommendations")
                st.write(recs)

else:
    st.info("👆 Upload a PDF document to get started!")

# Footer
st.markdown("---")
st.caption("⚠️ This is an AI assistant. Always consult healthcare professionals for medical advice.")
