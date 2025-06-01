import streamlit as st
import numpy as np
import pickle
import pandas as pd
import altair as alt
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
import time

# Disable SSL verification (remove after fixing certificate issue)
ssl._create_default_https_context = ssl._create_unverified_context

# --- CAREER_INFO (GLOBAL) ---
# Define CAREER_INFO globally so send_career_email can access it
CAREER_INFO = {
    "Software Engineer": {
        "description": "Designs, develops, tests, and maintains software systems.",
        "skills": ["Programming", "Problem-solving", "Teamwork"],
        "education": "Bachelor's degree in Computer Science or related field",
        "salary": "$80,000 - $150,000",
        "outlook": "High growth potential",
    },
    "Data Scientist": {
        "description": "Analyzes complex data to extract insights and inform business decisions.",
        "skills": ["Data analysis", "Machine learning", "Statistics"],
        "education": "Bachelor's or Master's degree in a quantitative field",
        "salary": "$90,000 - $170,000",
        "outlook": "Very high growth potential",
    },
    "Web Developer": {
        "description": "Creates and maintains websites and web applications.",
        "skills": ["HTML", "CSS", "JavaScript", "Frameworks"],
        "education": "Bachelor's degree in Computer Science or related field, or relevant certifications",
        "salary": "$60,000 - $120,000",
        "outlook": "Good growth potential",
    },
    "Graphic Designer": {
        "description": "Creates visual concepts to communicate ideas.",
        "skills": ["Adobe Creative Suite", "Typography", "Visual Communication"],
        "education": "Bachelor's degree in Graphic Design or related field",
        "salary": "$40,000 - $80,000",
        "outlook": "Moderate growth potential",
    },
    "UX/UI Designer": {
        "description": "Enhances user satisfaction by improving the usability, accessibility, and pleasure provided in the interaction between the user and the product.",
        "skills": ["User Research", "Wireframing", "Prototyping", "Visual Design"],
        "education": "Bachelor's degree in Design, HCI, or related field",
        "salary": "$70,000 - $130,000",
        "outlook": "High growth potential",
    },
    "Marketing Manager": {
        "description": "Plans and executes marketing campaigns to increase brand awareness and sales.",
        "skills": ["Marketing Strategy", "Communication", "Data Analysis", "Leadership"],
        "education": "Bachelor's degree in Marketing or related field",
        "salary": "$70,000 - $140,000",
        "outlook": "Stable growth potential",
    },
    "Financial Analyst": {
        "description": "Provides guidance to businesses and individuals in making decisions regarding their investments.",
        "skills": ["Financial Modeling", "Data Analysis", "Accounting", "Communication"],
        "education": "Bachelor's degree in Finance, Economics, or related field",
        "salary": "$65,000 - $120,000",
        "outlook": "Moderate growth potential",
    },
    "Product Manager": {
        "description": "Responsible for the strategy, roadmap, and feature definition of a product.",
        "skills": ["Product Strategy", "Market Research", "Communication", "Project Management"],
        "education": "Bachelor's degree in Business, Engineering, or related field",
        "salary": "$80,000 - $150,000",
        "outlook": "High growth potential",
    },
    "Business Analyst": {
        "description": "Identifies business needs and determines solutions to business problems.",
        "skills": ["Data Analysis", "Business Process Modeling", "Communication", "Problem Solving"],
        "education": "Bachelor's degree in Business, Economics, or related field",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
    },
    "Human Resources Manager": {
        "description": "Recruits, hires, and manages employees; handles employee relations and benefits.",
        "skills": ["Communication", "Interpersonal Skills", "HR Knowledge", "Leadership"],
        "education": "Bachelor's degree in Human Resources or related field",
        "salary": "$60,000 - $110,000",
        "outlook": "Stable growth potential",
    },
    "Teacher (Primary)": {
        "description": "Educates young children in various subjects to foster their intellectual and social development.",
        "skills": ["Communication", "Patience", "Classroom Management", "Creativity"],
        "education": "Bachelor's degree in Education",
        "salary": "$45,000 - $75,000",
        "outlook": "Stable growth potential",
    },
    "Teacher (Secondary)": {
        "description": "Instructs students in specific subjects within a secondary education setting, preparing them for higher education or careers.",
        "skills": ["Subject Matter Expertise", "Communication", "Classroom Management", "Mentoring"],
        "education": "Bachelor's degree in Education with subject specialization",
        "salary": "$48,000 - $80,000",
        "outlook": "Stable growth potential",
    },
    "Professor": {
        "description": "Conducts research and teaches undergraduate or graduate level courses in a specialized field of study.",
        "skills": ["Research", "Teaching", "Communication", "Subject Matter Expertise"],
        "education": "Doctoral degree in a specialized field",
        "salary": "$80,000 - $150,000",
        "outlook": "Moderate growth potential",
    },
    "Doctor (General)": {
        "description": "Diagnoses and treats a variety of medical conditions and injuries in patients.",
        "skills": ["Medical Knowledge", "Diagnostic Skills", "Communication", "Empathy"],
        "education": "Doctor of Medicine (MD) degree",
        "salary": "$180,000 - $250,000",
        "outlook": "High growth potential",
    },
    "Doctor (Specialist)": {
        "description": "Provides specialized medical care in a specific area of medicine, such as cardiology or oncology.",
        "skills": ["Specialized Medical Knowledge", "Advanced Clinical Skills", "Communication", "Problem Solving"],
        "education": "Doctor of Medicine (MD) degree with specialty training",
        "salary": "$250,000 - $400,000+",
        "outlook": "High growth potential",
    },
    "Nurse": {
        "description": "Provides and coordinates patient care, educates patients and the public about various health conditions, and provide advice and emotional support to patients and their family members.",
        "skills": ["Patient Care", "Communication", "Critical Thinking", "Empathy"],
        "education": "Bachelor of Science in Nursing (BSN) or Associate's Degree in Nursing (ADN)",
        "salary": "$60,000 - $90,000",
        "outlook": "High growth potential",
    },
    "Pharmacist": {
        "description": "Dispenses medications, ensures drug safety and efficacy, and provides pharmaceutical care to patients.",
        "skills": ["Pharmaceutical Knowledge", "Communication", "Attention to Detail", "Customer Service"],
        "education": "Doctor of Pharmacy (PharmD) degree",
        "salary": "$120,000 - $150,000",
        "outlook": "Stable growth potential",
    },
    "Lawyer": {
        "description": "Represents clients in legal proceedings, advises them on their legal rights and obligations, and draws up legal documents.",
        "skills": ["Legal Knowledge", "Communication", "Critical Thinking", "Negotiation"],
        "education": "Juris Doctor (JD) degree",
        "salary": "$80,000 - $200,000+",
        "outlook": "Moderate growth potential",
    },
    "Journalist": {
        "description": "Investigates and reports on news and current events for publication or broadcast.",
        "skills": ["Writing", "Research", "Interviewing", "Communication"],
        "education": "Bachelor's degree in Journalism or related field",
        "salary": "$40,000 - $70,000",
        "outlook": "Declining growth potential",
    },
    "Technical Writer": {
        "description": "Creates technical documentation, such as user manuals, help guides, and API documentation.",
        "skills": ["Writing", "Technical Knowledge", "Communication", "Attention to Detail"],
        "education": "Bachelor's degree in English, Technical Writing, or related field",
        "salary": "$60,000 - $100,000",
        "outlook": "Stable growth potential",
    },
    "Architect": {
        "description": "Designs buildings and other structures, considering both their form and function.",
        "skills": ["Design", "Technical Knowledge", "Communication", "Creativity"],
        "education": "Bachelor's or Master's degree in Architecture",
        "salary": "$70,000 - $140,000",
        "outlook": "Moderate growth potential",
    },
    "Civil Engineer": {
        "description": "Designs and oversees the construction of infrastructure projects, such as roads, bridges, and dams.",
        "skills": ["Engineering Knowledge", "Project Management", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Civil Engineering",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
    },
    "Mechanical Engineer": {
        "description": "Designs, develops, tests, and manufactures mechanical devices and systems.",
        "skills": ["Engineering Knowledge", "Design", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Mechanical Engineering",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
    },
    "Electrical Engineer": {
        "description": "Designs, develops, tests, and supervises the manufacturing of electrical equipment.",
        "skills": ["Engineering Knowledge", "Electrical Systems Design", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Electrical Engineering",
        "salary": "$75,000 - $140,000",
        "outlook": "Stable growth potential",
    },
    "Environmental Scientist": {
        "description": "Studies environmental problems and develops solutions to protect the environment and human health.",
        "skills": ["Environmental Science Knowledge", "Research", "Data Analysis", "Problem Solving"],
        "education": "Bachelor's or Master's degree in Environmental Science or related field",
        "salary": "$60,000 - $110,000",
        "outlook": "Good growth potential",
    },
    "Data Analyst": {
        "description": "Collects, processes, and performs statistical analysis of data.",
        "skills": ["Data Analysis", "Statistics", "Data Visualization", "Database Knowledge"],
        "education": "Bachelor's degree in Mathematics, Statistics, Computer Science, or related field",
        "salary": "$60,000 - $100,000",
        "outlook": "High growth potential",
    },
    "Management Consultant": {
        "description": "Advises top management on how to improve the organization's efficiency and effectiveness.",
        "skills": ["Analytical thinking", "Communication", "Problem-solving"],
        "education": "Bachelor's degree in business or a related field",
        "salary": "$85,000 - $160,000",
        "outlook": "Growing",
    },
}

# --- EMAIL SENDING FUNCTION (Moved to top-level) ---
def send_career_email(user_email, recipient_name, job_title):
    """Sends an email with career details to the user."""
    # It's highly recommended NOT to hardcode API keys directly in your code.
    # Use Streamlit secrets or environment variables for production.
SENDGRID_API_KEY = st.secrets["SENDGRID_API_KEY"]
    if not SENDGRID_API_KEY:
        st.error("Error: SendGrid API key is missing. Please configure it in your environment variables.")
        return False

    career_info = CAREER_INFO.get(job_title)
    if not career_info:
        st.error(f"Error: Could not find career information for '{job_title}'.")
        return False

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your CareerPulse Prediction: {job_title}!</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .career-details {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 CareerPulse Prediction Results</h1>
        </div>
        <div class="content">
            <h2>Congratulations, {recipient_name}!</h2>
            <p>We're excited to share your personalized career prediction from CareerPulse.</p>
            <p>Based on your interests, skills, and preferences, our AI suggests that you might find a fulfilling career as a <strong>{job_title}</strong>.</p>
            
            <div class="career-details">
                <h3>🎯 {job_title}</h3>
                <p><strong>Description:</strong> {career_info['description']}</p>
                <p><strong>Required Skills:</strong> {', '.join(career_info['skills'])}</p>
                <p><strong>Education:</strong> {career_info['education']}</p>
                <p><strong>Salary Range:</strong> {career_info['salary']}</p>
                <p><strong>Career Outlook:</strong> {career_info['outlook']}</p>
            </div>
            
            <p>We encourage you to explore this career further and consider the next steps in your journey!</p>
                <p><em>Please check your spam folder if you don't see this email in your inbox.</em></p>
                
                <p>Best regards,<br>
                The CareerPulse Team<br>
                <small>Ayan Gantayat & Shreemoyee Shaw</small></p>
            </div>
        </body>
        </html>
        """

    message = Mail(
        from_email="ayangantayat095@gmail.com",
        to_emails=user_email,
        subject=f"Your CareerPulse Prediction: {job_title}!",
        html_content=html_content,
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            return True
        else:
            st.error(f"Error sending email. Status code: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")
        return False

# --- Login Page Functionality ---
def login_page():
    st.set_page_config(
        page_title="Career Pulse - Login",
        page_icon="🔒",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: linear-gradient(to right, #3A277A, #2D2D4D, #1A5A9A, #009688);
            color: white; /* Ensure text is white on dark background */
            padding: 20px;
            text-align: center;
        }
        .login-box {
            background: white; /* Keep login box white for contrast */
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            width: 80%;
            max-width: 400px;
        }
        .login-box h2 {
            color: #333; /* Dark text for headings in white box */
            margin-bottom: 30px;
        }
        .stTextInput > div > div > input {
            border-radius: 25px;
            padding: 10px 15px;
            border: 1px solid #ddd;
            color: #333; /* Ensure input text is dark in white box */
        }
        .stTextInput label { /* Label for text input in login box */
            color: #555;
        }
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Kept original for button */
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-container">
        <div class="login-box">
            <h2>Welcome to CareerPulse</h2>
            <p style="color: #555;">Please log in to continue</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username (e.g., your name)", key="login_username")
        email = st.text_input("Gmail Address", key="login_email")
        
        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not email:
                st.warning("Please enter both username and Gmail address.")
            elif "@gmail.com" not in email:
                st.warning("Please enter a valid Gmail address.")
            else:
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = username
                st.session_state['user_email'] = email
                st.success("Login successful!")
                st.rerun() # Rerun to switch to the main app

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- Main App Functionality ---
def main_app():
    # Load or define model
    try:
        with open("career_model.pkl", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        st.warning(
            "Warning: 'career_model.pkl' not found. A default model will be used, but accuracy may be low. Consider training and saving a model for better predictions."
        )
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()

    # Career options (must match the training script)
    CAREER_OPTIONS = [
        "Software Engineer", "Data Scientist", "Web Developer", "Graphic Designer", "UX/UI Designer",
        "Marketing Manager", "Financial Analyst", "Product Manager", "Business Analyst", "Human Resources Manager",
        "Teacher (Primary)", "Teacher (Secondary)", "Professor", "Doctor (General)", "Doctor (Specialist)",
        "Nurse", "Pharmacist", "Lawyer", "Journalist", "Technical Writer", "Architect", "Civil Engineer",
        "Mechanical Engineer", "Electrical Engineer", "Environmental Scientist", "Data Analyst", "Management Consultant",
    ]

    def classify_age(age):
        if age <= 18:
            return "Teenager/Young Adult"
        elif 19 <= age <= 25:
            return "Young Professional"
        elif 26 <= age <= 40:
            return "Mid-Career"
        else:
            return "Experienced Professional"

    # Initialize subject, skill, and interest dictionaries with default values
    # This ensures they are defined even before the user interacts with the tabs.
    subjects = {
        "Maths - Algebra": 0, "Maths - Calculus": 0,
        "Science - Biology": 0, "Science - Chemistry": 0, "Science - Physics": 0,
        "Computer Science - Programming": 0, "Computer Science - Data Structures": 0,
        "History - Ancient": 0, "History - Modern": 0,
        "Economics - Microeconomics": 0, "Economics - Macroeconomics": 0,
        "Literature - Fiction": 0, "Literature - Poetry": 0,
        "Art - Painting": 0, "Art - Sculpture": 0,
    }

    skills = {
        "Problem Solving - Logical": 0, "Problem Solving - Creative": 0,
        "Creativity - Visual": 0, "Creativity - Innovation": 0,
        "Communication - Written": 0, "Communication - Verbal": 0,
        "Leadership - Team Management": 0, "Leadership - Initiative": 0,
        "Programming - Python": 0, "Programming - Java": 0,
        "Designing - UI/UX": 0, "Designing - Graphic": 0,
        "Research - Data Analysis": 0, "Research - Literature Review": 0,
    }

    interests = {
        "Technology - Artificial Intelligence": 0, "Technology - Cybersecurity": 0,
        "Technology - Web Development": 0, "Business - Marketing": 0,
        "Business - Finance": 0, "Business - Management": 0,
        "Art And Design - Visual Arts": 0, "Art And Design - Industrial Design": 0,
        "Healthcare - Clinical Research": 0, "Healthcare - Patient Care": 0,
        "Education - Primary/Secondary": 0, "Education - Higher Education": 0,
        "Engineering - Mechanical": 0, "Engineering - Electrical": 0,
        "Writing - Creative Writing": 0, "Writing - Technical Writing": 0,
    }

    preferences = {
        "Enjoy solving complex problems?": "No",
        "Prefer working with machines?": "No",
        "Interested in research?": "No",
        "Enjoy working with people?": "No",
        "Prefer working indoors?": "No",
    }

    # -------------------------------
    # 🎨 PAGE CONFIGURATION & STYLING
    # -------------------------------
    st.set_page_config(
        page_title="Career Pulse",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Get user's name from session state
    user_name = st.session_state.get('user_name', 'Guest')

    # Custom CSS for better styling
    st.markdown(f"""
    <style>
        /* Apply the gradient to the entire Streamlit app background */
        .stApp {{
            background: linear-gradient(to right, #3A277A, #2D2D4D, #1A5A9A, #009688);
            min-height: 100vh; /* Ensure it covers the whole viewport height */
            background-attachment: fixed; /* Keep background fixed during scroll */
            color: white; /* Default text color for the app */
        }}
        
        .main-header {{
            text-align: center;
            padding: 2rem 0;
            background: rgba(0,0,0,0.4); /* Semi-transparent dark background for header */
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .main-header h1 {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}
        
        .main-header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin: 0;
        }}
        
        /* Modified .career-info-card to match main-header style */
        .career-info-card {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)); /* Gradient background with transparency */
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3); /* Slightly stronger shadow */
            margin: 1rem 0;
            color: white; /* Default white text for these cards */
        }}

        .career-info-card h3, 
        .career-info-card p, 
        .career-info-card strong {{
            color: white !important; /* Ensure all text inside is white */
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent white for unselected tabs */
            border-radius: 10px 10px 0 0;
            border: none;
            color: white; /* White text for tabs */
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: #667eea; /* Accent color for selected tab */
            color: white;
        }}
        
        .prediction-result {{
            background: rgba(118, 75, 162, 0.8); /* Darker, slightly transparent purple from original gradient range */
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        /* NEW: About section font color fix - Revert to light background for black text */
        .about-card.career-info-card {{ /* Target specifically the about card that also has career-info-card class */
            background: #f8f9fa; /* Revert background to light for about-card */
            color: black; /* Force black text for about-card */
            border: 1px solid #e9ecef;
        }}
        .about-card h4, .about-card p, .about-card strong, .about-card em {{
            color: black !important; /* Ensure all text within is black */
        }}

        .sidebar .element-container {{
            margin-bottom: 1rem;
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Kept original for buttons */
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        /* Adjust input field backgrounds and labels for better readability against dark gradient */
        .stTextInput > div > div > input,
        .stSelectbox > div > div, /* This targets the displayed value area of the selectbox */
        .stSlider > div > div > div,
        .stNumberInput > div > label + div > div > input,
        .stNumberInput > div > label + div {{
            background-color: white;
            border-radius: 5px;
            padding: 8px 10px;
            border: 1px solid #ddd;
            color: #333; /* Ensure input text is dark */
        }}
        
        /* Labels for all input types */
        .stTextInput label,
        .stSelectbox label,
        .stSlider label,
        .stNumberInput label,
        .stCheckbox span {{
            color: white; /* Ensure labels are white on dark background */
        }}
        
        /* Specific styling for info, warning, success message boxes */
        .stInfo {{
            background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent white for info boxes */
            border-left: 5px solid #fff;
            color: white;
        }}
        .stWarning {{
            background-color: rgba(255, 165, 0, 0.1); /* Slightly transparent orange for warnings */
            border-left: 5px solid orange;
            color: #ffe0b2; /* Lighter orange text */
        }}
        .stSuccess {{
            background-color: rgba(144, 238, 144, 0.1); /* Slightly transparent green for success */
            border-left: 5px solid lightgreen;
            color: #d0e0d0; /* Lighter green text */
        }}

        /* Sidebar background - can also be a gradient or solid dark */
        .stSidebar {{
            background: rgba(0,0,0,0.3); /* Slightly transparent dark background for sidebar */
        }}

        /* Ensure all headings are white by default (if not in a white card) */
        h1, h2, h3, h4, h5, h6 {{
            color: white; 
        }}
        /* Default paragraph text color (if not in a white card) */
        p {{
            color: white; 
        }}

        /* Styles for the selectbox dropdown list when it's open */
        .stSelectbox div[role="listbox"] {{
            background-color: white; /* Make dropdown background white */
            color: #333; /* Dark text for readability */
        }}
        .stSelectbox div[role="option"] {{
            color: #333; /* Ensure individual options are dark */
        }}
        .stSelectbox div[data-baseweb="popover"] {{
            background-color: white; /* White background for the popover */
            color: #333; /* Default text color for popover */
        }}
        .stSelectbox ul {{
            background-color: white; /* For the actual unordered list */
        }}
        .stSelectbox li {{
            color: #333; /* Individual list items */
        }}
        /* Fix for scroll issue in selectbox options */
        .stSelectbox div[data-baseweb="select"] > div:first-child {{
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }}
        .stSelectbox div[data-baseweb="select"] {{
            height: auto !important; /* Allow content to dictate height */
        }}
        .stSelectbox div[role="listbox"] {{
            overflow-y: auto !important; /* Ensure scrollbar if needed */
        }}

    </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    # 🎨 HEADER (Updated with user's name)
    # -------------------------------
    st.markdown(f"""
    <div class="main-header">
        <h1>🎯 Career Pulse</h1>
        <p>Hello {user_name}, welcome to CareerPulse!</p>
        <p>Discover your perfect career path with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # 📊 SALARY COMPARISON SECTION (Now with a checkbox)
    # -------------------------------
    show_salary_chart = st.checkbox("📊 Show Career Salary & Outlook Analysis")

    if show_salary_chart:
        st.markdown("### 📊 Career Salary & Outlook Analysis")

        # Prepare DataFrame for salary chart
        df_salary = pd.DataFrame({
            "Career": [k for k in CAREER_INFO], # Use CAREER_INFO directly
            "Min Salary": [
                int(v["salary"].split(" - ")[0].replace("$", "").replace(",", ""))
                for v in CAREER_INFO.values()
            ],
            "Max Salary": [
                int(v["salary"].split(" - ")[1].replace("$", "").replace(",", "").replace("+", ""))
                if len(v["salary"].split(" - ")) > 1 else
                int(v["salary"].split(" - ")[0].replace("$", "").replace(",", "").replace("+", ""))
                for v in CAREER_INFO.values()
            ],
            "Outlook": [v["outlook"] for v in CAREER_INFO.values()],
        })

        # Filters in columns for better layout
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selected_outlook = st.selectbox(
                "🔍 Filter by Career Outlook",
                ["All"] + sorted(list(df_salary["Outlook"].unique())),
            )
        with col2:
            sort_by = st.selectbox(
                "📈 Sort By",
                ["None", "Min Salary (Asc)", "Min Salary (Desc)", "Max Salary (Asc)", "Max Salary (Desc)"]
            )

        filtered_df = df_salary.copy()

        # Apply filters
        if selected_outlook != "All":
            filtered_df = filtered_df[filtered_df["Outlook"] == selected_outlook]

        # Apply sorting
        if sort_by == "Min Salary (Asc)":
            filtered_df = filtered_df.sort_values(by="Min Salary", ascending=True)
        elif sort_by == "Min Salary (Desc)":
            filtered_df = filtered_df.sort_values(by="Min Salary", ascending=False)
        elif sort_by == "Max Salary (Asc)":
            filtered_df = filtered_df.sort_values(by="Max Salary", ascending=True)
        elif sort_by == "Max Salary (Desc)":
            filtered_df = filtered_df.sort_values(by="Max Salary", ascending=False)

        # Enhanced chart - Using mark_bar and adjusted encoding
        chart = (
            alt.Chart(filtered_df)
            .mark_bar() 
            .encode(
                x=alt.X("Career:N", sort=None, axis=alt.Axis(labelAngle=-45)), 
                y=alt.Y("Max Salary:Q", title="Maximum Salary ($)"),
                color=alt.Color('Career:N', legend=alt.Legend(title="Career")), 
                tooltip=["Career", "Min Salary", "Max Salary", "Outlook"],
            )
            .properties(height=400) 
            .interactive()
        )

        st.altair_chart(chart, use_container_width=True)

    # -------------------------------
    # 🧑 SIDEBAR - USER PROFILE
    # -------------------------------
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        
        # Display logged-in user info
        st.info(f"Logged in as: **{st.session_state.get('user_name', 'Guest')}**")
        st.info(f"Email: **{st.session_state.get('user_email', 'N/A')}**")

        if st.button("Logout"):
            st.session_state['logged_in'] = False
            del st.session_state['user_name']
            del st.session_state['user_email']
            if 'predicted_career' in st.session_state:
                del st.session_state['predicted_career']
            st.rerun()


        with st.container():
            # name variable is already fetched at the beginning of main_app
            age = st.slider("🎂 Age", 10, 55, 25)
            age_group = classify_age(age)
            st.info(f"Age Group: **{age_group}**")
        
        st.markdown("---")
        
        # Profile visualization toggle
        show_profile = st.checkbox("📊 Show Interest Profile", value=False)
        
        if show_profile:
            subject_scores_df = pd.DataFrame(subjects.items(), columns=["Subject", "Score"])
            skill_scores_df = pd.DataFrame(skills.items(), columns=["Skill", "Score"])
            interest_scores_df = pd.DataFrame(interests.items(), columns=["Interest", "Score"])

            avg_subject_interest = subject_scores_df["Score"].mean()
            avg_skill_level = skill_scores_df["Score"].mean()
            avg_field_interest = interest_scores_df["Score"].mean()

            profile_data = pd.DataFrame(
                {
                    "Category": ["Subjects", "Skills", "Interests"],
                    "Average Score": [
                        avg_subject_interest,
                        avg_skill_level,
                        avg_field_interest,
                    ],
                }
            )

            chart = (
                alt.Chart(profile_data)
                .mark_bar()
                .encode(
                    x="Category",
                    y="Average Score",
                    tooltip=["Category", "Average Score"],
                )
                .properties(title="Your Interest Profile")
            )
            st.sidebar.altair_chart(chart, use_container_width=True)



    # -------------------------------
    # 📚 MAIN CONTENT - INPUT SECTIONS
    # -------------------------------
    col_main, col_side = st.columns([3, 1])

    with col_main:
        tabs = st.tabs([
            "ℹ️ Career Explorer",
            "📘 Academic Interests", 
            "🛠️ Skills Assessment",
            "🎯 Field Interests",
            "🧠 Work Preferences",
            "💡 About"
        ])

        with tabs[1]:
            st.markdown("### 📚 Rate Your Academic Interests")
            st.markdown("*Rate from 0 (Not interested) to 5 (Very interested)*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔢 Mathematics**")
                subjects["Maths - Algebra"] = st.slider("Algebra", 0, 5, value=subjects["Maths - Algebra"], key="algebra")
                subjects["Maths - Calculus"] = st.slider("Calculus", 0, 5, value=subjects["Maths - Calculus"], key="calculus")
                
                st.markdown("**🔬 Sciences**")
                subjects["Science - Biology"] = st.slider("Biology", 0, 5, value=subjects["Science - Biology"], key="biology")
                subjects["Science - Chemistry"] = st.slider("Chemistry", 0, 5, value=subjects["Science - Chemistry"], key="chemistry")
                subjects["Science - Physics"] = st.slider("Physics", 0, 5, value=subjects["Science - Physics"], key="physics")
                
                st.markdown("**💻 Computer Science**")
                subjects["Computer Science - Programming"] = st.slider("Programming", 0, 5, value=subjects["Computer Science - Programming"], key="programming")
                subjects["Computer Science - Data Structures"] = st.slider("Data Structures", 0, 5, value=subjects["Computer Science - Data Structures"], key="data_structures")
            
            with col2:
                st.markdown("**📜 History**")
                subjects["History - Ancient"] = st.slider("Ancient History", 0, 5, value=subjects["History - Ancient"], key="ancient_history")
                subjects["History - Modern"] = st.slider("Modern History", 0, 5, value=subjects["History - Modern"], key="modern_history")
                
                st.markdown("**💼 Economics**")
                subjects["Economics - Microeconomics"] = st.slider("Microeconomics", 0, 5, value=subjects["Economics - Microeconomics"], key="microeconomics")
                subjects["Economics - Macroeconomics"] = st.slider("Macroeconomics", 0, 5, value=subjects["Economics - Macroeconomics"], key="macroeconomics")
                
                st.markdown("**📖 Literature & Arts**")
                subjects["Literature - Fiction"] = st.slider("Fiction", 0, 5, value=subjects["Literature - Fiction"], key="fiction")
                subjects["Literature - Poetry"] = st.slider("Poetry", 0, 5, value=subjects["Literature - Poetry"], key="poetry")
                subjects["Art - Painting"] = st.slider("Painting", 0, 5, value=subjects["Art - Painting"], key="painting")
                subjects["Art - Sculpture"] = st.slider("Sculpture", 0, 5, value=subjects["Art - Sculpture"], key="sculpture")
            

        with tabs[2]:
            st.markdown("### 🛠️ Skills Assessment")
            st.markdown("*Rate your proficiency from 0 (Beginner) to 5 (Expert)*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🧩 Problem Solving**")
                skills["Problem Solving - Logical"] = st.slider("Logical Problem Solving", 0, 5, value=skills["Problem Solving - Logical"], key="ps_logical")
                skills["Problem Solving - Creative"] = st.slider("Creative Problem Solving", 0, 5, value=skills["Problem Solving - Creative"], key="ps_creative")
                
                st.markdown("**🎨 Creativity**")
                skills["Creativity - Visual"] = st.slider("Visual Creativity", 0, 5, value=skills["Creativity - Visual"], key="creativity_visual")
                skills["Creativity - Innovation"] = st.slider("Innovation", 0, 5, value=skills["Creativity - Innovation"], key="creativity_innovation")
                
                st.markdown("**💬 Communication**")
                skills["Communication - Written"] = st.slider("Written Communication", 0, 5, value=skills["Communication - Written"], key="comm_written")
                skills["Communication - Verbal"] = st.slider("Verbal Communication", 0, 5, value=skills["Communication - Verbal"], key="comm_verbal")
            
            with col2:
                st.markdown("**👥 Leadership**")
                skills["Leadership - Team Management"] = st.slider("Team Management", 0, 5, value=skills["Leadership - Team Management"], key="leadership_team")
                skills["Leadership - Initiative"] = st.slider("Taking Initiative", 0, 5, value=skills["Leadership - Initiative"], key="leadership_initiative")
                
                st.markdown("**💻 Programming**")
                skills["Programming - Python"] = st.slider("Python Programming", 0, 5, value=skills["Programming - Python"], key="prog_python")
                skills["Programming - Java"] = st.slider("Java Programming", 0, 5, value=skills["Programming - Java"], key="prog_java")
                
                st.markdown("**🎨 Design**")
                skills["Designing - UI/UX"] = st.slider("UI/UX Design", 0, 5, value=skills["Designing - UI/UX"], key="design_ui")
                skills["Designing - Graphic"] = st.slider("Graphic Design", 0, 5, value=skills["Designing - Graphic"], key="design_graphic")
                
                st.markdown("**🔍 Research**")
                skills["Research - Data Analysis"] = st.slider("Data Analysis Research", 0, 5, value=skills["Research - Data Analysis"], key="research_data")
                skills["Research - Literature Review"] = st.slider("Literature Review Research", 0, 5, value=skills["Research - Literature Review"], key="research_lit")
            

        with tabs[3]:
            st.markdown("### 🎯 Field Interests")
            st.markdown("*Rate your interest in these professional fields*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💻 Technology**")
                interests["Technology - Artificial Intelligence"] = st.slider("Artificial Intelligence", 0, 5, value=interests["Technology - Artificial Intelligence"], key="tech_ai")
                interests["Technology - Cybersecurity"] = st.slider("Cybersecurity", 0, 5, value=interests["Technology - Cybersecurity"], key="tech_cyber")
                interests["Technology - Web Development"] = st.slider("Web Development", 0, 5, value=interests["Technology - Web Development"], key="tech_web")
                
                st.markdown("**💼 Business**")
                interests["Business - Marketing"] = st.slider("Marketing", 0, 5, value=interests["Business - Marketing"], key="biz_marketing")
                interests["Business - Finance"] = st.slider("Finance", 0, 5, value=interests["Business - Finance"], key="biz_finance")
                interests["Business - Management"] = st.slider("Management", 0, 5, value=interests["Business - Management"], key="biz_management")
                
                st.markdown("**🎨 Art & Design**")
                interests["Art And Design - Visual Arts"] = st.slider("Visual Arts", 0, 5, value=interests["Art And Design - Visual Arts"], key="art_visual")
                interests["Art And Design - Industrial Design"] = st.slider("Industrial Design", 0, 5, value=interests["Art And Design - Industrial Design"], key="art_industrial")
            
            with col2:
                st.markdown("**🏥 Healthcare**")
                interests["Healthcare - Clinical Research"] = st.slider("Clinical Research", 0, 5, value=interests["Healthcare - Clinical Research"], key="health_research")
                interests["Healthcare - Patient Care"] = st.slider("Patient Care", 0, 5, value=interests["Healthcare - Patient Care"], key="health_care")
                
                st.markdown("**🎓 Education**")
                interests["Education - Primary/Secondary"] = st.slider("Primary/Secondary Education", 0, 5, value=interests["Education - Primary/Secondary"], key="edu_primary")
                interests["Education - Higher Education"] = st.slider("Higher Education", 0, 5, value=interests["Education - Higher Education"], key="edu_higher")
                
                st.markdown("**⚙️ Engineering**")
                interests["Engineering - Mechanical"] = st.slider("Mechanical Engineering", 0, 5, value=interests["Engineering - Mechanical"], key="eng_mechanical")
                interests["Engineering - Electrical"] = st.slider("Electrical Engineering", 0, 5, value=interests["Engineering - Electrical"], key="eng_electrical")
                
                st.markdown("**✍️ Writing**")
                interests["Writing - Creative Writing"] = st.slider("Creative Writing", 0, 5, value=interests["Writing - Creative Writing"], key="writing_creative")
                interests["Writing - Technical Writing"] = st.slider("Technical Writing", 0, 5, value=interests["Writing - Technical Writing"], key="writing_technical")
            

        with tabs[4]:
            st.markdown("### 🧠 Work Preferences")
            st.markdown("*Tell us about your work style preferences*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                preferences["Enjoy solving complex problems?"] = st.selectbox("🧩 Enjoy solving complex problems?", ["Yes", "No"], index=["Yes", "No"].index(preferences["Enjoy solving complex problems?"]), key="pref_complex")
                preferences["Prefer working with machines?"] = st.selectbox("⚙️ Prefer working with machines?", ["Yes", "No"], index=["Yes", "No"].index(preferences["Prefer working with machines?"]), key="pref_machines")
                preferences["Interested in research?"] = st.selectbox("🔬 Interested in research?", ["Yes", "No"], index=["Yes", "No"].index(preferences["Interested in research?"]), key="pref_research")
            
            with col2:
                preferences["Enjoy working with people?"] = st.selectbox("👥 Enjoy working with people?", ["Yes", "No"], index=["Yes", "No"].index(preferences["Enjoy working with people?"]), key="pref_people")
                preferences["Prefer working indoors?"] = st.selectbox("🏢 Prefer working indoors?", ["Yes", "No"], index=["Yes", "No"].index(preferences["Prefer working indoors?"]), key="pref_indoors")
            

        with tabs[0]: # Moved this tab back to its original position
            st.markdown("### 🔍 Explore Career Details")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                # This is the selectbox whose font needs to be black (already handled by .stSelectbox CSS)
                selected_career = st.selectbox("Select a Career to Explore", CAREER_OPTIONS)
            
            if selected_career:
                career_info = CAREER_INFO[selected_career]
                
                # The 'career-info-card' class will now apply the desired gradient style
                st.markdown(f"""
                <div class="career-info-card"> 
                    <h3>🎯 {selected_career}</h3>
                    <p><strong>📝 Description:</strong> {career_info['description']}</p>
                    <p><strong>🛠️ Key Skills:</strong> {', '.join(career_info['skills'])}</p>
                    <p><strong>🎓 Education:</strong> {career_info['education']}</p>
                    <p><strong>💰 Salary Range:</strong> {career_info['salary']}</p>
                    <p><strong>📈 Career Outlook:</strong> {career_info['outlook']}</p>
                </div>
                """, unsafe_allow_html=True)

        with tabs[5]:
            st.markdown("### 💡 About Career Pulse")
            
            # The 'about-card' class will override the background if black text is needed
            st.markdown("""
            <div class="career-info-card about-card"> 
                <h4>🚀 Welcome to Career Pulse Beta!</h4>
                <p>This is an AI-powered career guidance tool designed to help you discover your ideal career path based on your interests, skills, and preferences. This app was developed by Ayan Gantayat and design by Shreemoyee Shaw</p>
                <p><em>We're constantly improving to provide you with the best career guidance experience!</em></p>
            </div>
            """, unsafe_allow_html=True)
# -------------------------------
    # 🔍 PREDICTION SECTION
    # -------------------------------
    st.markdown("---")
    st.markdown("### 🎯 Get Your Career Recommendation")

    if st.button("🔍 Analyze My Profile & Suggest Careers", type="primary"):
        # Use user_name from session_state
        current_user_name = st.session_state.get('user_name', 'Guest')
        current_user_email = st.session_state.get('user_email', 'N/A')

        if current_user_name == 'Guest': # Check if a proper name was set during login
            st.warning("⚠️ Please log in with your name to continue.")
        elif current_user_email == 'N/A' or "@gmail.com" not in current_user_email: # Check for a valid email from session state
            st.warning("⚠️ Please log in with a valid Gmail address.")
        elif not all(value is not None for value in subjects.values()) or not all(
            value is not None for value in skills.values()
        ) or not all(value is not None for value in interests.values()) or not all(
            value is not None for value in preferences.values()
        ):
            st.warning("⚠️ Please complete all sections to get an accurate prediction.")
        else:
            with st.spinner("🤖 Analyzing your profile and finding the perfect career match..."):
                time.sleep(3)  # Simulate processing time
                
                # Prepare input data
                input_data = [
                    age,
                    subjects["Maths - Algebra"], subjects["Maths - Calculus"],
                    subjects["Science - Biology"], subjects["Science - Chemistry"], subjects["Science - Physics"],
                    subjects["Computer Science - Programming"], subjects["Computer Science - Data Structures"],
                    subjects["History - Ancient"], subjects["History - Modern"],
                    subjects["Economics - Microeconomics"], subjects["Economics - Macroeconomics"],
                    subjects["Literature - Fiction"], subjects["Literature - Poetry"],
                    subjects["Art - Painting"], subjects["Art - Sculpture"],
                    skills["Problem Solving - Logical"], skills["Problem Solving - Creative"],
                    skills["Creativity - Visual"], skills["Creativity - Innovation"],
                    skills["Communication - Written"], skills["Communication - Verbal"],
                    skills["Leadership - Team Management"], skills["Leadership - Initiative"],
                    interests["Technology - Artificial Intelligence"], interests["Technology - Cybersecurity"],
                    interests["Technology - Web Development"], interests["Business - Marketing"],
                    interests["Business - Finance"], interests["Business - Management"],
                    interests["Art And Design - Visual Arts"], interests["Art And Design - Industrial Design"],
                    interests["Healthcare - Clinical Research"], interests["Healthcare - Patient Care"],
                    interests["Education - Primary/Secondary"], interests["Education - Higher Education"],
                    interests["Engineering - Mechanical"], interests["Engineering - Electrical"],
                    interests["Writing - Creative Writing"], interests["Writing - Technical Writing"],
                    1 if preferences["Enjoy solving complex problems?"] == "Yes" else 0,
                    1 if preferences["Prefer working with machines?"] == "Yes" else 0,
                    1 if preferences["Interested in research?"] == "Yes" else 0,
                    1 if preferences["Enjoy working with people?"] == "Yes" else 0,
                    1 if preferences["Prefer working indoors?"] == "Yes" else 0,
                ]
                
                input_vector = np.array(input_data).reshape(1, -1)
                
                try:
                    prediction = model.predict(input_vector)[0]
                    predicted_career = CAREER_OPTIONS[prediction]
                    st.session_state.predicted_career = predicted_career
                    st.session_state.input_data = input_data 
                    
                    # Display prediction result
                    st.markdown(f"""
                    <div class="prediction-result">
                        <h2>🎉 Congratulations, {current_user_name}!</h2>
                        <h3>Your recommended career path is:</h3>
                        <h1>🎯 {predicted_career}</h1>
                        <p>This recommendation is based on your unique profile of interests, skills, and preferences.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()  # Celebration effect
                    
                except Exception as e:
                    st.error(f"❗ An error occurred during prediction: {e}")
                    st.info("Please ensure the model is trained and loaded correctly.")


    # -------------------------------
    # 📧 EMAIL & CAREER DETAILS
    # -------------------------------
    if 'predicted_career' in st.session_state:
        predicted_career = st.session_state.predicted_career
        career_info = CAREER_INFO[predicted_career]
        
        st.markdown("### 📋 Your Career Details")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="career-info-card">
                <h3>🎯 {predicted_career}</h3>
                <p><strong>📝 Description:</strong> {career_info['description']}</p>
                <p><strong>🛠️ Required Skills:</strong> {', '.join(career_info['skills'])}</p>
                <p><strong>🎓 Education Requirements:</strong> {career_info['education']}</p>
                <p><strong>💰 Salary Range:</strong> {career_info['salary']}</p>
                <p><strong>📈 Career Outlook:</strong> {career_info['outlook']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📧 Get Detailed Report")
            send_email_report = st.checkbox("📨 Send detailed career report to my email") 
            
            if send_email_report and st.button("Send Report", type="secondary"):
                email_sent = send_career_email(st.session_state.get('user_email'), st.session_state.get('user_name'), predicted_career)
                if email_sent:
                    st.success("📧 Career report sent successfully!")
                    st.info("Please check your email (including spam folder) for the detailed report.")
                else:
                    st.error(
                        "Failed to send email. Please check your email address and try again. Please also check your SendGrid API key and ensure it is correctly configured."
                    )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #AAA; padding: 20px;'>
        <p>Made  by <strong>Ayan Gantayat</strong> & <strong>Shreemoyee Shaw</strong></p>
        <p><em>Career Pulse - Discover Your Future</em></p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Application Logic ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_page()
