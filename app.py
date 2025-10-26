import streamlit as st
from PyPDF2 import PdfReader
from datetime import datetime
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("Please set OPENAI_API_KEY in your .env file")
    st.stop()

# Helper Functions
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """Get completion from OpenAI API"""
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

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
    """Generic document processing function"""
    prompts = {
        "qa": f"""As a medical assistant, answer this question based on the document:
                Document Content: {text[:3000]}
                Question: {specific_query}
                Provide a clear, patient-friendly answer. If the information isn't in the document, say so.""",
        
        "summary": f"""Summarize this medical document in clear, simple language:
                    Document: {text[:3000]}
                    Create a structured summary with:
                    1. Document Type
                    2. Key Findings (bullet points)
                    3. Critical Values or Concerns (if any)
                    4. Recommendations (if mentioned)""",
        
        "eli5": f"""Explain this medical term as if explaining to a 5-year-old:
                Term: {specific_query}
                Context: {text[:1500]}
                Use simple words and friendly explanations.""",
        
        "medications": f"""Extract all medications from this document:
                        {text[:2000]}
                        List each medication with:
                        - Medicine name
                        - Dosage
                        - Frequency
                        - Special instructions""",
        
        "recommendations": f"""Based on this health document, provide lifestyle recommendations:
                            {text[:2000]}
                            Include:
                            1. Diet suggestions
                            2. Exercise recommendations
                            3. Lifestyle modifications
                            4. Preventive care tips
                            5. Follow-up suggestions"""
    }
    
    temperatures = {
        "qa": 0.3,
        "summary": 0.3,
        "eli5": 0.7,
        "medications": 0.1,
        "recommendations": 0.7
    }
    
    return get_completion(prompts[question_type], temperature=temperatures[question_type])

# Page Configuration
st.set_page_config(
    page_title="MediScan AI - Your Health Document Assistant",
    page_icon="🏥",
    layout="wide"
)

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
    st.info("Uses OpenAI GPT to help understand health documents. Always consult healthcare professionals.")

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
