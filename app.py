import streamlit as st
import joblib
import docx
import os
from PyPDF2 import PdfReader
import time  # For loading spinner

# -------------------------------
# Custom CSS for Theme and Styling
# -------------------------------
st.markdown("""
    <style>
    /* Overall Theme: Dark Cybersecurity */
    .stApp {
        background: linear-gradient(135deg, #0f4c75 0%, #1e3c72 100%);
        color: #ffffff;
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #a8b2d1;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Buttons */
    .stButton > button {
        background-color: #00d4ff;
        color: #0f4c75;
        border: 2px solid #00d4ff;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0f4c75;
        color: #00d4ff;
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.7);
        transform: scale(1.05);
    }
    .stButton > button:disabled {
        background-color: #555;
        border-color: #555;
        color: #aaa;
    }
    /* Text Areas and Inputs */
    .stTextArea > div > div > textarea {
        background-color: #1e3c72;
        color: #ffffff;
        border: 1px solid #00d4ff;
        border-radius: 10px;
        font-family: 'Monaco', monospace;
    }
    .stFileUploader > div > div > div {
        background-color: #1e3c72;
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    /* Results Badges */
    .safe-badge {
        background-color: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .suspicious-badge {
        background-color: #dc3545;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    /* Progress Bar for Confidence */
    .stProgress > div > div > div {
        background-color: #00d4ff;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f4c75;
    }
    .stInfo {
        background-color: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #a8b2d1;
        padding: 1rem;
        font-size: 0.9rem;
        border-top: 1px solid #00d4ff;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Load model and vectorizer
# -------------------------------
@st.cache_resource
def load_models():
    try:
        if not os.path.exists("NLP_Model2.pkl") or not os.path.exists("vectorizer2.pkl"):
            st.error("❌ Model or vectorizer file not found.")
            st.stop()
            return None, None
        model = joblib.load("NLP_Model2.pkl")
        vectorizer = joblib.load("vectorizer2.pkl")
        return model, vectorizer
    except Exception as e:
        st.error(f"❌ Error loading model or vectorizer: {e}")
        st.stop()
        return None, None
    
model, vectorizer = load_models()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Cybersecurity NLP Classifier Demo", layout="wide", initial_sidebar_state="expanded")

# Header
st.markdown('<h1 class="main-header">🔐 Cybersecurity NLP Classifier</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyze text or files for potential threats – Safe or Suspicious?</p>', unsafe_allow_html=True)

# Sidebar for Demo Info
with st.sidebar:
    st.markdown("### 📋 Demo Info")
    st.info("This is a demo app for classifying cybersecurity-related text. Upload files or type manually for quick analysis.")
    st.markdown("**Features:**")
    st.write("- Supports TXT, CSV, PDF, DOCX")
    st.write("- Real-time classification")
    st.write("- Confidence scoring")
    
    # Theme Toggle (simple light/dark switch)
    theme = st.selectbox("🌙 Theme", ["Dark (Default)", "Light"], index=0)
    if theme == "Light":
        st.markdown("""
            <style>
            .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); color: #333; }
            .main-header { color: #0f4c75; text-shadow: none; }
            .sub-header { color: #6c757d; }
            .stTextArea > div > div > textarea { background-color: #fff; color: #333; border: 1px solid #0f4c75; }
            .stFileUploader > div > div > div { background-color: #fff; border: 1px solid #0f4c75; }
            section[data-testid="stSidebar"] { background-color: #f8f9fa; }
            .stInfo { background-color: rgba(15, 76, 117, 0.1); border: 1px solid #0f4c75; }
            </style>
        """, unsafe_allow_html=True)

# Main Content Layout: Two Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📂 File Upload")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "csv", "pdf", "docx"],
        help="Supported formats: TXT, CSV, PDF, DOCX"
    )

    file_text = ""
    if uploaded_file is not None:
        try:
            # Handle .txt and .csv files
            if uploaded_file.name.endswith((".txt", ".csv")):
                file_text = uploaded_file.read().decode("utf-8")

            # Handle .pdf files
            elif uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                file_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

            # Handle .docx files
            elif uploaded_file.name.endswith(".docx"):
                doc = docx.Document(uploaded_file)
                file_text = " ".join([p.text for p in doc.paragraphs])

            if file_text:
                preview = file_text[:1000] + "..." if len(file_text) > 1000 else file_text
                st.text_area("📄 Preview:", value=preview, height=150, label_visibility="collapsed")
            else:
                st.warning("⚠️ Could not extract any readable text from this file.")
        except Exception as e:
            st.error(f"❌ Could not read the file: {e}")

with col2:
    st.subheader("✍️ Manual Input")
    user_input = st.text_area("Enter text here", height=200, placeholder="Type or paste your text for analysis...")

# Combine inputs
text_to_analyze = file_text if file_text.strip() else user_input

# Classification Section
st.subheader("🚀 Classify Now")
if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
    if text_to_analyze.strip():
        with st.spinner("Analyzing... 🔄"):
            time.sleep(1)  # Simulate processing for demo feel
        
        try:
            # Vectorize input text
            X = vectorizer.transform([text_to_analyze])

            # Predict
            prediction = model.predict(X)[0]
            proba = model.predict_proba(X)[0]

            # Display results
            st.subheader("📊 Results")
            label = "Suspicious 🚨" if prediction == 1 else "Safe ✅"
            confidence = proba[prediction] * 100
            
            # Badges
            if prediction == 1:
                st.markdown(f'<span class="suspicious-badge">{label}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="safe-badge">{label}</span>', unsafe_allow_html=True)
            
            st.write(f"**Confidence:** {confidence:.2f}%")
            
            # Progress Bar
            st.progress(confidence / 100)
            
            # Additional Info
            if prediction == 1:
                st.warning("⚠️ This text may contain suspicious elements. Review carefully!")
            else:
                st.success("✅ Looks good – no immediate threats detected.")
                
        except Exception as e:
            st.error(f"❌ Error during classification: {e}")
    else:
        st.warning("⚠️ Please upload a file or enter text before classifying.")

# Footer
st.markdown("""
    <div class="footer">
    🔒 Demo App by [Thuthukani Nhlengethwa] | For educational purposes only. Not for production use.
    </div>
""", unsafe_allow_html=True)
