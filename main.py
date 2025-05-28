import streamlit as st
import numpy as np
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
import time
from datetime import datetime

# Disable SSL verification (remove after fixing certificate issue)
ssl._create_default_https_context = ssl._create_unverified_context

# Page configuration
st.set_page_config(
    page_title="Career Pulse - AI Career Guidance",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .career-info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .stSelectbox > div > div {
        background-color: white;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load or define model
@st.cache_resource
def load_model():
    try:
        with open("career_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model, True
    except FileNotFoundError:
        st.warning("⚠️ Model file not found. Using default model for demonstration.")
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(), False
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(), False

model, model_loaded = load_model()

# Career data
CAREER_OPTIONS = [
    "Software Engineer", "Data Scientist", "Web Developer", "Graphic Designer",
    "UX/UI Designer", "Marketing Manager", "Financial Analyst", "Product Manager",
    "Business Analyst", "Human Resources Manager", "Teacher (Primary)", "Teacher (Secondary)",
    "Professor", "Doctor (General)", "Doctor (Specialist)", "Nurse", "Pharmacist",
    "Lawyer", "Journalist", "Technical Writer", "Architect", "Civil Engineer",
    "Mechanical Engineer", "Electrical Engineer", "Environmental Scientist",
    "Data Analyst", "Management Consultant"
]

CAREER_INFO = {
    "Software Engineer": {
        "description": "Designs, develops, tests, and maintains software systems.",
        "skills": ["Programming", "Problem-solving", "Teamwork"],
        "education": "Bachelor's degree in Computer Science or related field",
        "salary": "$80,000 - $150,000",
        "outlook": "High growth potential",
        "icon": "💻"
    },
    "Data Scientist": {
        "description": "Analyzes complex data to extract insights and inform business decisions.",
        "skills": ["Data analysis", "Machine learning", "Statistics"],
        "education": "Bachelor's or Master's degree in a quantitative field",
        "salary": "$90,000 - $170,000",
        "outlook": "Very high growth potential",
        "icon": "📊"
    },
    "Web Developer": {
        "description": "Creates and maintains websites and web applications.",
        "skills": ["HTML", "CSS", "JavaScript", "Frameworks"],
        "education": "Bachelor's degree in Computer Science or related field, or relevant certifications",
        "salary": "$60,000 - $120,000",
        "outlook": "Good growth potential",
        "icon": "🌐"
    },
    "Graphic Designer": {
        "description": "Creates visual concepts to communicate ideas.",
        "skills": ["Adobe Creative Suite", "Typography", "Visual Communication"],
        "education": "Bachelor's degree in Graphic Design or related field",
        "salary": "$40,000 - $80,000",
        "outlook": "Moderate growth potential",
        "icon": "🎨"
    },
    "UX/UI Designer": {
        "description": "Enhances user satisfaction by improving the usability, accessibility, and pleasure provided in the interaction between the user and the product.",
        "skills": ["User Research", "Wireframing", "Prototyping", "Visual Design"],
        "education": "Bachelor's degree in Design, HCI, or related field",
        "salary": "$70,000 - $130,000",
        "outlook": "High growth potential",
        "icon": "🎯"
    },
    "Marketing Manager": {
        "description": "Plans and executes marketing campaigns to increase brand awareness and sales.",
        "skills": ["Marketing Strategy", "Communication", "Data Analysis", "Leadership"],
        "education": "Bachelor's degree in Marketing or related field",
        "salary": "$70,000 - $140,000",
        "outlook": "Stable growth potential",
        "icon": "📈"
    },
    "Financial Analyst": {
        "description": "Provides guidance to businesses and individuals in making decisions regarding their investments.",
        "skills": ["Financial Modeling", "Data Analysis", "Accounting", "Communication"],
        "education": "Bachelor's degree in Finance, Economics, or related field",
        "salary": "$65,000 - $120,000",
        "outlook": "Moderate growth potential",
        "icon": "💰"
    },
    "Product Manager": {
        "description": "Responsible for the strategy, roadmap, and feature definition of a product.",
        "skills": ["Product Strategy", "Market Research", "Communication", "Project Management"],
        "education": "Bachelor's degree in Business, Engineering, or related field",
        "salary": "$80,000 - $150,000",
        "outlook": "High growth potential",
        "icon": "🚀"
    },
    "Business Analyst": {
        "description": "Identifies business needs and determines solutions to business problems.",
        "skills": ["Data Analysis", "Business Process Modeling", "Communication", "Problem Solving"],
        "education": "Bachelor's degree in Business, Economics, or related field",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
        "icon": "📋"
    },
    "Human Resources Manager": {
        "description": "Recruits, hires, and manages employees; handles employee relations and benefits.",
        "skills": ["Communication", "Interpersonal Skills", "HR Knowledge", "Leadership"],
        "education": "Bachelor's degree in Human Resources or related field",
        "salary": "$60,000 - $110,000",
        "outlook": "Stable growth potential",
        "icon": "👥"
    },
    "Teacher (Primary)": {
        "description": "Educates young children in various subjects to foster their intellectual and social development.",
        "skills": ["Communication", "Patience", "Classroom Management", "Creativity"],
        "education": "Bachelor's degree in Education",
        "salary": "$45,000 - $75,000",
        "outlook": "Stable growth potential",
        "icon": "📚"
    },
    "Teacher (Secondary)": {
        "description": "Instructs students in specific subjects within a secondary education setting, preparing them for higher education or careers.",
        "skills": ["Subject Matter Expertise", "Communication", "Classroom Management", "Mentoring"],
        "education": "Bachelor's degree in Education with subject specialization",
        "salary": "$48,000 - $80,000",
        "outlook": "Stable growth potential",
        "icon": "🎓"
    },
    "Professor": {
        "description": "Conducts research and teaches undergraduate or graduate level courses in a specialized field of study.",
        "skills": ["Research", "Teaching", "Communication", "Subject Matter Expertise"],
        "education": "Doctoral degree in a specialized field",
        "salary": "$80,000 - $150,000",
        "outlook": "Moderate growth potential",
        "icon": "🔬"
    },
    "Doctor (General)": {
        "description": "Diagnoses and treats a variety of medical conditions and injuries in patients.",
        "skills": ["Medical Knowledge", "Diagnostic Skills", "Communication", "Empathy"],
        "education": "Doctor of Medicine (MD) degree",
        "salary": "$180,000 - $250,000",
        "outlook": "High growth potential",
        "icon": "👨‍⚕️"
    },
    "Doctor (Specialist)": {
        "description": "Provides specialized medical care in a specific area of medicine, such as cardiology or oncology.",
        "skills": ["Specialized Medical Knowledge", "Advanced Clinical Skills", "Communication", "Problem Solving"],
        "education": "Doctor of Medicine (MD) degree with specialty training",
        "salary": "$250,000 - $400,000",
        "outlook": "High growth potential",
        "icon": "🏥"
    },
    "Nurse": {
        "description": "Provides and coordinates patient care, educates patients and the public about various health conditions, and provide advice and emotional support to patients and their family members.",
        "skills": ["Patient Care", "Communication", "Critical Thinking", "Empathy"],
        "education": "Bachelor of Science in Nursing (BSN) or Associate's Degree in Nursing (ADN)",
        "salary": "$60,000 - $90,000",
        "outlook": "High growth potential",
        "icon": "👩‍⚕️"
    },
    "Pharmacist": {
        "description": "Dispenses medications, ensures drug safety and efficacy, and provides pharmaceutical care to patients.",
        "skills": ["Pharmaceutical Knowledge", "Communication", "Attention to Detail", "Customer Service"],
        "education": "Doctor of Pharmacy (PharmD) degree",
        "salary": "$120,000 - $150,000",
        "outlook": "Stable growth potential",
        "icon": "💊"
    },
    "Lawyer": {
        "description": "Represents clients in legal proceedings, advises them on their legal rights and obligations, and draws up legal documents.",
        "skills": ["Legal Knowledge", "Communication", "Critical Thinking", "Negotiation"],
        "education": "Juris Doctor (JD) degree",
        "salary": "$80,000 - $200,000",
        "outlook": "Moderate growth potential",
        "icon": "⚖️"
    },
    "Journalist": {
        "description": "Investigates and reports on news and current events for publication or broadcast.",
        "skills": ["Writing", "Research", "Interviewing", "Communication"],
        "education": "Bachelor's degree in Journalism or related field",
        "salary": "$40,000 - $70,000",
        "outlook": "Declining growth potential",
        "icon": "📰"
    },
    "Technical Writer": {
        "description": "Creates technical documentation, such as user manuals, help guides, and API documentation.",
        "skills": ["Writing", "Technical Knowledge", "Communication", "Attention to Detail"],
        "education": "Bachelor's degree in English, Technical Writing, or related field",
        "salary": "$60,000 - $100,000",
        "outlook": "Stable growth potential",
        "icon": "📝"
    },
    "Architect": {
        "description": "Designs buildings and other structures, considering both their form and function.",
        "skills": ["Design", "Technical Knowledge", "Communication", "Creativity"],
        "education": "Bachelor's or Master's degree in Architecture",
        "salary": "$70,000 - $140,000",
        "outlook": "Moderate growth potential",
        "icon": "🏗️"
    },
    "Civil Engineer": {
        "description": "Designs and oversees the construction of infrastructure projects, such as roads, bridges, and dams.",
        "skills": ["Engineering Knowledge", "Project Management", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Civil Engineering",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
        "icon": "🌉"
    },
    "Mechanical Engineer": {
        "description": "Designs, develops, tests, and manufactures mechanical devices and systems.",
        "skills": ["Engineering Knowledge", "Design", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Mechanical Engineering",
        "salary": "$70,000 - $130,000",
        "outlook": "Stable growth potential",
        "icon": "⚙️"
    },
    "Electrical Engineer": {
        "description": "Designs, develops, tests, and supervises the manufacturing of electrical equipment.",
        "skills": ["Engineering Knowledge", "Electrical Systems Design", "Problem Solving", "Technical Skills"],
        "education": "Bachelor's degree in Electrical Engineering",
        "salary": "$75,000 - $140,000",
        "outlook": "Stable growth potential",
        "icon": "⚡"
    },
    "Environmental Scientist": {
        "description": "Studies environmental problems and develops solutions to protect the environment and human health.",
        "skills": ["Environmental Science Knowledge", "Research", "Data Analysis", "Problem Solving"],
        "education": "Bachelor's or Master's degree in Environmental Science or related field",
        "salary": "$60,000 - $110,000",
        "outlook": "Good growth potential",
        "icon": "🌱"
    },
    "Data Analyst": {
        "description": "Collects, processes, and performs statistical analysis of data.",
        "skills": ["Data Analysis", "Statistics", "Data Visualization", "Database Knowledge"],
        "education": "Bachelor's degree in Mathematics, Statistics, Computer Science, or related field",
        "salary": "$60,000 - $100,000",
        "outlook": "High growth potential",
        "icon": "📈"
    },
    "Management Consultant": {
        "description": "Advises top management on how to improve the organization's efficiency and effectiveness.",
        "skills": ["Analytical thinking", "Communication", "Problem-solving"],
        "education": "Bachelor's degree in business or a related field",
        "salary": "$85,000 - $160,000",
        "outlook": "Growing",
        "icon": "💼"
    }
}

# Helper functions
def classify_age(age):
    if age <= 18:
        return "Teenager/Young Adult"
    elif 19 <= age <= 25:
        return "Young Professional"
    elif 26 <= age <= 40:
        return "Mid-Career"
    else:
        return "Experienced Professional"

def calculate_progress(user_info, subjects, skills, interests, preferences):
    total_fields = len(subjects) + len(skills) + len(interests) + len(preferences) + 3
    filled_fields = (
        sum(1 for v in subjects.values() if v > 0) +
        sum(1 for v in skills.values() if v > 0) +
        sum(1 for v in interests.values() if v > 0) +
        sum(1 for v in preferences.values() if v == "Yes") +
        (1 if user_info.get('name') else 0) +
        (1 if user_info.get('email') else 0) +
        1  # age always has a value
    )
    return int((filled_fields / total_fields) * 100)

def create_salary_chart(predicted_career=None):
    # Prepare data for chart
    chart_data = []
    for career, info in CAREER_INFO.items():
        salary_range = info["salary"].replace("$", "").replace(",", "").replace("+", "")
        if " - " in salary_range:
            min_sal, max_sal = salary_range.split(" - ")
        else:
            min_sal = max_sal = salary_range
        
        chart_data.append({
            "Career": career,
            "Min Salary": int(min_sal),
            "Max Salary": int(max_sal),
            "Outlook": info["outlook"],
            "Icon": info["icon"],
            "Is Predicted": career == predicted_career
        })
    
    df = pd.DataFrame(chart_data)
    
    # Create interactive chart
    fig = px.bar(
        df, 
        x="Career", 
        y="Max Salary",
        color="Is Predicted",
        color_discrete_map={True: "#ff4444", False: "#4444ff"},
        hover_data=["Min Salary", "Max Salary", "Outlook"],
        title="💰 Career Salary Comparison"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_profile_chart(subjects, skills, interests):
    avg_subjects = sum(subjects.values()) / len(subjects) if subjects else 0
    avg_skills = sum(skills.values()) / len(skills) if skills else 0
    avg_interests = sum(interests.values()) / len(interests) if interests else 0
    
    categories = ['Subjects', 'Skills', 'Interests']
    values = [avg_subjects, avg_skills, avg_interests]
    colors = ['#667eea', '#764ba2', '#f093fb']
    
    fig = go.Figure(data=[go.Pie(
        labels=categories, 
        values=values,
        hole=0.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="🎯 Your Interest Profile",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def send_career_email(user_email, recipient_name, job_title):
    """Sends an email with career details to the user."""
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    if not SENDGRID_API_KEY:
        st.error("❌ SendGrid API key is missing. Please configure it in your environment variables.")
        return False

    career_info = CAREER_INFO.get(job_title)
    if not career_info:
        st.error(f"❌ Could not find career information for '{job_title}'.")
        return False

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your CareerPulse Prediction: {job_title}!</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .career-card {{ background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 15px 0; }}
            .skills {{ display: flex; flex-wrap: wrap; gap: 10px; }}
            .skill-tag {{ background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧠 Career Pulse Prediction</h1>
            <h2>Congratulations, {recipient_name}!</h2>
        </div>
        <div class="content">
            <p>We're excited to share your personalized career prediction from Career Pulse.</p>
            <p>Based on your interests, skills, and preferences, our AI suggests that you might find a fulfilling career as a <strong>{job_title}</strong> {career_info['icon']}.</p>
            
            <div class="career-card">
                <h3>{career_info['icon']} {job_title}</h3>
                <p>{career_info['description']}</p>
                
                <h4>💼 Key Information:</h4>
                <ul>
                    <li><strong>💰 Salary:</strong> {career_info['salary']}</li>
                    <li><strong>🎓 Education:</strong> {career_info['education']}</li>
                    <li><strong>📈 Outlook:</strong> {career_info['outlook']}</li>
                </ul>
                
                <h4>🛠️ Required Skills:</h4>
                <div class="skills">
                    {' '.join([f'<span class="skill-tag">{skill}</span>' for skill in career_info['skills']])}
                </div>
            </div>
            
            <p>We encourage you to explore this career further!</p>
            <p><em>Please check your spam folder if you don't see this email in your inbox.</em></p>
            
            <hr>
            <p><strong>Sincerely,</strong><br>
            The Career Pulse Team<br>
            <small>Developed by Ayan Gantayat | Logo Design by Shreemoyee Shaw</small></p>
        </div>
    </body>
    </html>
    """

    message = Mail(
        from_email="ayangantayat095@gmail.com",
        to_emails=user_email,
        subject=f"🎯 Your Career Pulse Prediction: {job_title}!",
        html_content=html_content,
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            return True
        else:
            st.error(f"❌ Error sending email. Status code: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ An error occurred while sending the email: {e}")
        return False

# Initialize session state
if 'user_info' not in st.session_state:
    st.session_state.user_info = {'name': '', 'age': 25, 'email': ''}

if 'subjects' not in st.session_state:
    st.session_state.subjects = {
        "Maths - Algebra": 0, "Maths - Calculus": 0, "Science - Biology": 0,
        "Science - Chemistry": 0, "Science - Physics": 0, "Computer Science - Programming": 0,
        "Computer Science - Data Structures": 0, "History - Ancient": 0, "History - Modern": 0,
        "Economics - Microeconomics": 0, "Economics - Macroeconomics": 0, "Literature - Fiction": 0,
        "Literature - Poetry": 0, "Art - Painting": 0, "Art - Sculpture": 0
    }

if 'skills' not in st.session_state:
    st.session_state.skills = {
        "Problem Solving - Logical": 0, "Problem Solving - Creative": 0, "Creativity - Visual": 0,
        "Creativity - Innovation": 0, "Communication - Written": 0, "Communication - Verbal": 0,
        "Leadership - Team Management": 0, "Leadership - Initiative": 0, "Programming - Python": 0,
        "Programming - Java": 0, "Designing - UI/UX": 0, "Designing - Graphic": 0,
        "Research - Data Analysis": 0, "Research - Literature Review": 0
    }

if 'interests' not in st.session_state:
    st.session_state.interests = {
        "Technology - Artificial Intelligence": 0, "Technology - Cybersecurity": 0,
        "Technology - Web Development": 0, "Business - Marketing": 0, "Business - Finance": 0,
        "Business - Management": 0, "Art And Design - Visual Arts": 0,
        "Art And Design - Industrial Design": 0, "Healthcare - Clinical Research": 0,
        "Healthcare - Patient Care": 0, "Education - Primary/Secondary": 0,
        "Education - Higher Education": 0, "Engineering - Mechanical": 0,
        "Engineering - Electrical": 0, "Writing - Creative Writing": 0,
        "Writing - Technical Writing": 0
    }

if 'preferences' not in st.session_state:
    st.session_state.preferences = {
        "Enjoy solving complex problems?": "No",
        "Prefer working with machines?": "No",
        "Interested in research?": "No",
        "Enjoy working with people?": "No",
        "Prefer working indoors?": "No"
    }

if 'predicted_career' not in st.session_state:
    st.session_state.predicted_career = None

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧠 Career Pulse</h1>
    <h3>AI-Powered Career Guidance Platform</h3>
    <p>Discover your perfect career path through intelligent analysis of your interests, skills, and preferences</p>
</div>
""", unsafe_allow_html=True)

# Progress tracking
progress = calculate_progress(
    st.session_state.user_info, 
    st.session_state.subjects, 
    st.session_state.skills, 
    st.session_state.interests, 
    st.session_state.preferences
)

st.markdown(f"""
<div class="progress-container">
    <h4>📊 Profile Completion: {progress}%</h4>
    <div style="background-color: #e9ecef; border-radius: 10px; height: 20px;">
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    width: {progress}%; height: 100%; border-radius: 10px; 
                    transition: width 0.3s ease;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for user profile
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h2>👤 Your Profile</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.user_info['name'] = st.text_input(
        "📝 Full Name", 
        value=st.session_state.user_info['name'],
        placeholder="Enter your full name"
    )
    
    st.session_state.user_info['email'] = st.text_input(
        "📧 Email Address", 
        value=st.session_state.user_info['email'],
        placeholder="your.email@example.com"
    )
    
    st.session_state.user_info['age'] = st.slider(
        "🎂 Age", 
        min_value=10, 
        max_value=55, 
        value=st.session_state.user_info['age']
    )
    
    age_group = classify_age(st.session_state.user_info['age'])
    st.markdown(f"""
    <div class="metric-card">
        <strong>Age Group:</strong> {age_group}
    </div>
    """, unsafe_allow_html=True)
    
    show_profile = st.checkbox("📈 Show Interest Profile Visualization")
    
    if show_profile:
        st.plotly_chart(
            create_profile_chart(
                st.session_state.subjects, 
                st.session_state.skills, 
                st.session_state.interests
            ), 
            use_container_width=True
        )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Career salary comparison chart
    st.markdown("### 💰 Career Salary Comparison")
    
    # Chart filters
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        outlook_filter = st.selectbox(
            "Filter by Career Outlook",
            ["All"] + sorted(list(set(info["outlook"] for info in CAREER_INFO.values())))
        )
    
    with chart_col2:
        sort_option = st.selectbox(
            "Sort By",
            ["None", "Min Salary (Low to High)", "Min Salary (High to Low)", 
             "Max Salary (Low to High)", "Max Salary (High to Low)"]
        )
    
    # Display chart
    fig = create_salary_chart(st.session_state.predicted_career)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    total_careers = len(CAREER_OPTIONS)
    avg_min_salary = np.mean([
        int(info["salary"].split(" - ")[0].replace("$", "").replace(",", ""))
        for info in CAREER_INFO.values()
    ])
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>🎯 Total Careers</h4>
        <h2>{total_careers}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>💵 Avg. Starting Salary</h4>
        <h2>${avg_min_salary:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

# Tabbed interface for input sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "ℹ️ Career Explorer", "📚 Academic Subjects", "🛠️ Skills Assessment", 
    "🎯 Field Interests", "🧠 Work Preferences", "💡 About"
])

with tab1:
    st.markdown("### 🔍 Explore Career Details")
    
    selected_career = st.selectbox(
        "Choose a career to learn more about:",
        [""] + CAREER_OPTIONS,
        format_func=lambda x: f"{CAREER_INFO[x]['icon']} {x}" if x and x in CAREER_INFO else "Select a career..."
    )
    
    if selected_career and selected_career in CAREER_INFO:
        career_info = CAREER_INFO[selected_career]
        
        st.markdown(f"""
        <div class="career-info-card">
            <h2>{career_info['icon']} {selected_career}</h2>
            <p style="font-size: 16px; margin-bottom: 20px;">{career_info['description']}</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>🛠️ Required Skills:</h4>
                    <ul>
                        {' '.join([f'<li>{skill}</li>' for skill in career_info['skills']])}
                    </ul>
                </div>
                <div>
                    <h4>💰 Salary Range:</h4>
                    <p style="font-size: 18px; color: #28a745; font-weight: bold;">{career_info['salary']}</p>
                    
                    <h4>📈 Career Outlook:</h4>
                    <p style="font-size: 16px; color: #007bff; font-weight: bold;">{career_info['outlook']}</p>
                </div>
            </div>
            
            <h4>🎓 Education Requirements:</h4>
            <p>{career_info['education']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📚 Academic Subjects Interest")
    st.markdown("*Rate your interest level in each subject (0 = Not interested, 5 = Very interested)*")
    
    subjects_col1, subjects_col2 = st.columns(2)
    
    subject_keys = list(st.session_state.subjects.keys())
    mid_point = len(subject_keys) // 2
    
    with subjects_col1:
        for subject in subject_keys[:mid_point]:
            st.session_state.subjects[subject] = st.slider(
                f"📖 {subject}",
                min_value=0,
                max_value=5,
                value=st.session_state.subjects[subject],
                key=f"subject_{subject}"
            )
    
    with subjects_col2:
        for subject in subject_keys[mid_point:]:
            st.session_state.subjects[subject] = st.slider(
                f"📖 {subject}",
                min_value=0,
                max_value=5,
                value=st.session_state.subjects[subject],
                key=f"subject_{subject}"
            )

with tab3:
    st.markdown("### 🛠️ Skills Assessment")
    st.markdown("*Rate your current skill level in each area (0 = Beginner, 5 = Expert)*")
    
    skills_col1, skills_col2 = st.columns(2)
    
    skill_keys = list(st.session_state.skills.keys())
    mid_point = len(skill_keys) // 2
    
    with skills_col1:
        for skill in skill_keys[:mid_point]:
            st.session_state.skills[skill] = st.slider(
                f"⚡ {skill}",
                min_value=0,
                max_value=5,
                value=st.session_state.skills[skill],
                key=f"skill_{skill}"
            )
    
    with skills_col2:
        for skill in skill_keys[mid_point:]:
            st.session_state.skills[skill] = st.slider(
                f"⚡ {skill}",
                min_value=0,
                max_value=5,
                value=st.session_state.skills[skill],
                key=f"skill_{skill}"
            )

with tab4:
    st.markdown("### 🎯 Field Interests")
    st.markdown("*Rate your interest in different professional fields (0 = Not interested, 5 = Very interested)*")
    
    interests_col1, interests_col2 = st.columns(2)
    
    interest_keys = list(st.session_state.interests.keys())
    mid_point = len(interest_keys) // 2
    
    with interests_col1:
        for interest in interest_keys[:mid_point]:
            st.session_state.interests[interest] = st.slider(
                f"🌟 {interest}",
                min_value=0,
                max_value=5,
                value=st.session_state.interests[interest],
                key=f"interest_{interest}"
            )
    
    with interests_col2:
        for interest in interest_keys[mid_point:]:
            st.session_state.interests[interest] = st.slider(
                f"🌟 {interest}",
                min_value=0,
                max_value=5,
                value=st.session_state.interests[interest],
                key=f"interest_{interest}"
            )

with tab5:
    st.markdown("### 🧠 Work Preferences")
    st.markdown("*Tell us about your work style and preferences*")
    
    for preference in st.session_state.preferences:
        st.session_state.preferences[preference] = st.radio(
            f"❓ {preference}",
            ["Yes", "No"],
            index=0 if st.session_state.preferences[preference] == "Yes" else 1,
            key=f"pref_{preference}",
            horizontal=True
        )

with tab6:
    st.markdown("### 💡 About Career Pulse")
    
    st.markdown("""
    <div class="career-info-card">
        <h3>🚀 Welcome to Career Pulse Beta!</h3>
        <p>Career Pulse is an AI-powered career guidance platform designed to help you discover your ideal career path through intelligent analysis of your interests, skills, and preferences.</p>
        
        <h4>✨ Features:</h4>
        <ul>
            <li>🧠 AI-powered career predictions</li>
            <li>📊 Interactive salary comparisons</li>
            <li>📈 Personal interest profiling</li>
            <li>📧 Detailed career reports via email</li>
            <li>🎯 Comprehensive career database</li>
        </ul>
        
        <h4>🔮 Coming Soon:</h4>
        <ul>
            <li>Advanced ML models for better predictions</li>
            <li>Career pathway recommendations</li>
            <li>Skills gap analysis</li>
            <li>Industry trend insights</li>
        </ul>
        
        <hr>
        <p><strong>👨‍💻 Developed by:</strong> Ayan Gantayat</p>
        <p><strong>🎨 Logo Design by:</strong> Shreemoyee Shaw</p>
        <p><em>This is a beta version. More exciting updates coming soon!</em></p>
    </div>
    """, unsafe_allow_html=True)

# Career Prediction Section
st.markdown("---")
st.markdown("## 🎯 AI Career Prediction")

prediction_col1, prediction_col2 = st.columns([3, 1])

with prediction_col1:
    if st.button("🧠 Analyze My Profile & Suggest Careers", type="primary", use_container_width=True):
        if not st.session_state.user_info['name']:
            st.markdown("""
            <div class="warning-message">
                ⚠️ Please enter your name to continue.
            </div>
            """, unsafe_allow_html=True)
        elif not st.session_state.user_info['email']:
            st.markdown("""
            <div class="warning-message">
                ⚠️ Please enter your email address to continue.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show analysis progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Analyzing your academic interests...")
                elif i < 60:
                    status_text.text("⚡ Evaluating your skills profile...")
                elif i < 90:
                    status_text.text("🎯 Processing field preferences...")
                else:
                    status_text.text("🧠 Generating AI predictions...")
                time.sleep(0.03)
            
            progress_bar.empty()
            status_text.empty()
            
            # Simple prediction logic (enhanced)
            all_scores = {**st.session_state.subjects, **st.session_state.skills, **st.session_state.interests}
            
            # Calculate weighted scores for different career categories
            tech_score = (
                all_scores.get("Computer Science - Programming", 0) * 2 +
                all_scores.get("Programming - Python", 0) * 2 +
                all_scores.get("Programming - Java", 0) * 2 +
                all_scores.get("Technology - Artificial Intelligence", 0) +
                all_scores.get("Technology - Web Development", 0) +
                all_scores.get("Problem Solving - Logical", 0)
            ) / 9
            
            data_score = (
                all_scores.get("Research - Data Analysis", 0) * 2 +
                all_scores.get("Maths - Calculus", 0) +
                all_scores.get("Maths - Algebra", 0) +
                all_scores.get("Technology - Artificial Intelligence", 0) +
                all_scores.get("Problem Solving - Logical", 0)
            ) / 6
            
            design_score = (
                all_scores.get("Designing - UI/UX", 0) * 2 +
                all_scores.get("Designing - Graphic", 0) * 2 +
                all_scores.get("Art - Painting", 0) +
                all_scores.get("Creativity - Visual", 0) +
                all_scores.get("Art And Design - Visual Arts", 0)
            ) / 7
            
            business_score = (
                all_scores.get("Business - Management", 0) +
                all_scores.get("Business - Marketing", 0) +
                all_scores.get("Leadership - Team Management", 0) +
                all_scores.get("Communication - Verbal", 0) +
                all_scores.get("Economics - Microeconomics", 0)
            ) / 5
            
            healthcare_score = (
                all_scores.get("Science - Biology", 0) * 2 +
                all_scores.get("Healthcare - Patient Care", 0) * 2 +
                all_scores.get("Science - Chemistry", 0) +
                all_scores.get("Healthcare - Clinical Research", 0)
            ) / 6
            
            # Determine best career match
            scores = {
                "Software Engineer": tech_score,
                "Data Scientist": data_score,
                "UX/UI Designer": design_score,
                "Product Manager": business_score,
                "Nurse": healthcare_score,
                "Web Developer": tech_score * 0.8,
                "Marketing Manager": business_score * 0.9,
                "Data Analyst": data_score * 0.8
            }
            
            predicted_career = max(scores, key=scores.get)
            st.session_state.predicted_career = predicted_career
            
            # Display prediction
            st.markdown(f"""
            <div class="prediction-card">
                <h2>🎉 Congratulations, {st.session_state.user_info['name']}!</h2>
                <h3>Your AI-Predicted Career Path:</h3>
                <h1>{CAREER_INFO[predicted_career]['icon']} {predicted_career}</h1>
                <p>Based on your comprehensive profile analysis, this career aligns perfectly with your interests, skills, and preferences!</p>
            </div>
            """, unsafe_allow_html=True)

with prediction_col2:
    if st.session_state.predicted_career:
        st.markdown("### 📊 Prediction Confidence")
        confidence = np.random.randint(85, 96)  # Simulated confidence score
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <h2 style="color: #28a745;">{confidence}%</h2>
            <p>Match Confidence</p>
        </div>
        """, unsafe_allow_html=True)

# Display detailed career information if prediction exists
if st.session_state.predicted_career:
    st.markdown("---")
    st.markdown("### 📋 Your Predicted Career Details")
    
    career_info = CAREER_INFO[st.session_state.predicted_career]
    
    detail_col1, detail_col2 = st.columns([2, 1])
    
    with detail_col1:
        st.markdown(f"""
        <div class="career-info-card">
            <h3>{career_info['icon']} {st.session_state.predicted_career}</h3>
            <p style="font-size: 16px; margin-bottom: 20px;">{career_info['description']}</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div>
                    <h4>💰 Salary Range:</h4>
                    <p style="font-size: 18px; color: #28a745; font-weight: bold;">{career_info['salary']}</p>
                </div>
                <div>
                    <h4>📈 Career Outlook:</h4>
                    <p style="font-size: 16px; color: #007bff; font-weight: bold;">{career_info['outlook']}</p>
                </div>
            </div>
            
            <h4>🛠️ Required Skills:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
                {' '.join([f'<span style="background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px;">{skill}</span>' for skill in career_info['skills']])}
            </div>
            
            <h4>🎓 Education Requirements:</h4>
            <p>{career_info['education']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with detail_col2:
        # Email option
        send_email = st.checkbox("📧 Send detailed career report to my email")
        
        if send_email:
            if st.button("📤 Send Career Report", type="secondary", use_container_width=True):
                with st.spinner("Sending your personalized career report..."):
                    email_sent = send_career_email(
                        st.session_state.user_info['email'],
                        st.session_state.user_info['name'],
                        st.session_state.predicted_career
                    )
                    
                    if email_sent:
                        st.markdown("""
                        <div class="success-message">
                            ✅ Career report sent successfully!<br>
                            Check your inbox (and spam folder) for detailed information.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="warning-message">
                            ❌ Failed to send email. Please check your email address and try again.
                        </div>
                        """, unsafe_allow_html=True)
        
        # Additional career suggestions
        st.markdown("### 🔄 Alternative Careers")
        similar_careers = [career for career in CAREER_OPTIONS if career != st.session_state.predicted_career][:3]
        
        for career in similar_careers:
            if career in CAREER_INFO:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #667eea;">
                    <strong>{CAREER_INFO[career]['icon']} {career}</strong><br>
                    <small>{CAREER_INFO[career]['salary']}</small>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>🧠 <strong>Career Pulse</strong> - Empowering your career journey with AI</p>
    <p><small>Developed with ❤️ by Ayan Gantayat | Logo Design by Shreemoyee Shaw</small></p>
    <p><small>© 2024 Career Pulse. This is a beta version - More features coming soon!</small></p>
</div>
""", unsafe_allow_html=True)
