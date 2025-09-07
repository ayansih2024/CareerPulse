import streamlit as st
import google.generativeai as genai
import os

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    st.error("GEMINI_API_KEY environment variable not set. Please set it to your Gemini API key.")
    st.stop()


def list_available_gemini_models():
    st.subheader("💡 Available Gemini Models (for debugging):")
    models_info = []
    try:
        for m in genai.list_models():
            # Filter for models that support generateContent
            if 'generateContent' in m.supported_generation_methods:
                models_info.append(f"- **Name:** `{m.name}` | **Description:** {m.description}")
        if models_info:
            st.markdown("Please choose one of these models for your `model_name` parameter:")
            st.markdown("\n".join(models_info))
        else:
            st.warning("No models supporting 'generateContent' found with your API key. "
                       "This could indicate an issue with your API key or region availability.")
    except Exception as e:
        st.error(f"Error listing models: {e}. Ensure your API key is valid and has access to model listing.")
    st.markdown("---") # Separator for clarity




def get_gemini_response(prompt, model_name="models/gemini-2.5-flash-preview-05-20"):
    """
    Sends a prompt to the Gemini model and returns the text response.
    """
    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Streamlit App Design ---
st.set_page_config(
    page_title="The Justice Hub",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5em;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    .subheader {
        font-size: 1.8em;
        color: #F0F2F6;
        text-align: center;
        margin-bottom: 30px;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #FFFFFF;
        border: 1px solid #666666;
        border-radius: 8px;
        padding: 10px;
    }
    .stTextArea>div>div>textarea {
        background-color: #333333;
        color: #FFFFFF;
        border: 1px solid #666666;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1.2em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .response-container {
        background-color: #2a2a2a;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        border: 1px solid #444444;
    }
    .response-text {
        color: #E0E0E0;
        font-size: 1.1em;
        line-height: 1.6;
    }
    /* Streamlit's default dark theme already provides good contrast,
       but these ensure background for sidebar and main area are consistent */
    .st-emotion-cache-vk336y { /* Specific class for sidebar container */
        background-color: #1a1a1a;
    }
    .st-emotion-cache-1r6dm1s { /* Specific class for sidebar text/elements */
        color: #FFFFFF;
    }
    .st-emotion-cache-1cyp85j { /* Adjust main content background if needed, often not necessary with 'dark' theme */
        background-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>⚖️ The Justice Hub ⚖️</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Your AI Assistant for Legal Information & Guidance (Experimental)</h3>", unsafe_allow_html=True)

st.write("---") # Separator

# --- Display Available Models at the top for debugging ---
list_available_gemini_models() # This will show the list of models
# --- You can comment out or remove the line above after you've fixed the model_name ---


# Sidebar for additional features or info
with st.sidebar:
    st.header("About The Justice Hub")
    st.write(
        "This experimental application leverages the power of Google's Gemini AI to "
        "provide general information and insights related to legal topics. "
        "**Please note: This is not a substitute for professional legal advice.** "
        "Always consult with a qualified legal professional for specific legal concerns."
    )
    st.markdown("---")
    st.header("How to Use")
    st.write(
        "1. Enter your legal question or scenario in the text area.\n"
        "2. Click 'Get Legal Insights' to receive an AI-generated response.\n"
        "3. Remember to verify information with a legal expert."
    )
    st.markdown("---")
    st.write("Developed with ❤️ using Streamlit and Gemini API")

# Main content area
st.subheader("Ask a Legal Question or Describe a Scenario:")

user_query = st.text_area(
    "Enter your query here (e.g., 'What are the basic rights of a consumer in India?', 'Explain intellectual property law.', 'What is the process for filing a patent?')",
    height=150
)

if st.button("Get Legal Insights"):
    if user_query:
        with st.spinner("Fetching insights from Gemini AI..."):
            response = get_gemini_response(user_query)
            st.markdown("<div class='response-container'>", unsafe_allow_html=True)
            st.markdown(f"<p class='response-text'>{response}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter your question or scenario to get insights.")

st.write("---")

st.info(
    "**Disclaimer:** The information provided by The Justice Hub is for general informational "
    "purposes only and does not constitute legal advice. While efforts are made to provide "
    "accurate information, legal concepts are complex and vary by jurisdiction. "
    "Always consult with a qualified legal professional for advice tailored to your specific situation."
)
#Made By Ayan Gantayat who is a good boy  trying to survive in a world full of shit ppl other than a  few 