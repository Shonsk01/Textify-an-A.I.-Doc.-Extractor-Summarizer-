import streamlit as st
import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.tokenizers import Tokenizer
import nltk

# Ensure NLTK resources are present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Streamlit UI
st.title("📄 Textify")

# File uploader (only PDF allowed)
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# Extractive summarization using LexRank
def extractive_summary(text, num_sentences=10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return "\n".join([f"• {sentence}" for sentence in summary])

# PDF text extraction using PyMuPDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf_reader:
        text += page.get_text()
    return text

# Processing logic
if uploaded_file:
    file_name = uploaded_file.name.lower()

    # Check if the uploaded file is a PDF
    if not file_name.endswith(".pdf"):
        st.error("⚠ Please upload a valid PDF file.")
        st.experimental_rerun()  # Restart the app
    else:
        st.write(f"File uploaded: {file_name}")  # Debugging output
        st.write("Processing PDF...")  # Debugging output
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)
        st.success("✅ Text extracted from PDF.")

    # Display extracted text in scrollable area
    if text.strip():
        st.subheader("📜 Extracted Text")
        st.text_area("", text, height=300)

        if st.button("📋 Fast Summarize"):
            with st.spinner("Generating summary using extractive method..."):
                summary_text = extractive_summary(text, num_sentences=10)
            st.success("✅ Summary Ready!")
            st.subheader("Summary")
            st.text_area("", summary_text, height=300)
    else:
        st.warning("⚠ No text found to process.")
