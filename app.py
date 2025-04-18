import streamlit as st
import requests
import PyPDF2
import json
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize Model
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_pdf(file) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def download_pdf_and_extract(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to download PDF (status {response.status_code})")
    
    with open("temp_download.pdf", "wb") as f:
        f.write(response.content)

    with open("temp_download.pdf", "rb") as f:
        return extract_text_from_pdf(f)

def structured_tnc(tnc_text: str) -> dict:
    prompt = (
        "You are a helpful assistant. "
        "Summarize the following Terms & Conditions into JSON format with the following structure:\n\n"
        "{\n"
        "  'terms_summary': [list of 10 bullet points as strings],\n"
        "  'critical_watchpoints': {'Heading 1': string, 'Heading 2': string},\n"
        "  'recommended_action': {'Heading': string}\n"
        "}\n\n"
        "Please make sure to always provide 'critical_watchpoints' and 'recommended_action'. If these sections are not present, say so clearly.\n\n"
        f"Terms & Conditions:\n{tnc_text}"
    )

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(response_mime_type="application/json")
    )

    try:
        return json.loads(response.text)
    except Exception as e:
        raise ValueError(f"Model output is not valid JSON: {e}\nRaw output:\n{response.text}")

# Streamlit App
st.set_page_config(page_title="T&C Analyzer", layout="centered")
st.title("📜 Terms & Conditions Analyzer")

input_method = st.radio("Choose Input Method:", ["Paste Text", "Upload PDF", "PDF URL"])

input_text = ""

if input_method == "Paste Text":
    input_text = st.text_area("Paste your T&C here:", height=300)

elif input_method == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_pdf is not None:
        input_text = extract_text_from_pdf(uploaded_pdf)

elif input_method == "PDF URL":
    pdf_url = st.text_input("Enter direct PDF URL")
    if st.button("Download and Extract PDF Text"):
        if pdf_url.strip():
            try:
                input_text = download_pdf_and_extract(pdf_url)
                st.success("PDF downloaded and text extracted!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if input_text.strip():
    if st.button("Analyze T&C"):
        with st.spinner("Analyzing with Gemini..."):
            try:
                response = structured_tnc(input_text)

                # Displaying Summary
                st.header("🔹 Summary")
                for idx, bullet in enumerate(response.get("terms_summary", [])):
                    st.markdown(f"✅ {bullet}")

                # Displaying Critical Watchpoints
                st.header("⚠️ Critical Watchpoints")
                critical_watchpoints = response.get("critical_watchpoints", {})
                
                # Check for critical watchpoints and display each one dynamically
                if critical_watchpoints:
                    for key, value in critical_watchpoints.items():
                        st.error(f"**{key}:** {value}")
                else:
                    st.error("No critical watchpoints provided.")

                # Displaying Recommended Action
                st.header("💡 Recommended Action")
                recommended_action = response.get("recommended_action", {})
                
                if recommended_action:
                    for key, value in recommended_action.items():
                        st.warning(f"**{key}:** {value}")
                else:
                    st.warning("No recommended action provided.")

                # Download JSON
                st.download_button(
                    "💾 Download JSON",
                    json.dumps(response, indent=2),
                    file_name="structured_tnc.json",
                    mime="application/json"
                )

                # View Raw JSON
                with st.expander("💾 View Raw JSON"):
                    st.json(response)  # View raw JSON from the model response

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Enter T&C text, upload a PDF, or use a PDF URL to start.")
