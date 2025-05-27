import streamlit as st
import numpy as np
import pickle
import pandas as pd
import altair as alt
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
import time # Import time for the progress indicator

# Disable SSL verification (remove after fixing certificate issue)
ssl._create_default_https_context = ssl._create_unverified_context

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
    "Software Engineer",
    "Data Scientist",
    "Web Developer",
    "Graphic Designer",
    "UX/UI Designer",
    "Marketing Manager",
    "Financial Analyst",
    "Product Manager",
    "Business Analyst",
    "Human Resources Manager",
    "Teacher (Primary)",
    "Teacher (Secondary)",
    "Professor",
    "Doctor (General)",
    "Doctor (Specialist)",
    "Nurse",
    "Pharmacist",
    "Lawyer",
    "Journalist",
    "Technical Writer",
    "Architect",
    "Civil Engineer",
    "Mechanical Engineer",
    "Electrical Engineer",
    "Environmental Scientist",
    "Data Analyst",
    "Management Consultant",
]

# Detailed career information (Can be stored in a dictionary or loaded from a file)
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
        "skills": [
            "Specialized Medical Knowledge",
            "Advanced Clinical Skills",
            "Communication",
            "Problem Solving",
        ],
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
# salary comparision chart
# Salary comparison chart


# Function to classify age group
def classify_age(age):
    if age <= 18:
        return "Teenager/Young Adult"
    elif 19 <= age <= 25:
        return "Young Professional"
    elif 26 <= age <= 40:
        return "Mid-Career"
    else:
        return "Experienced Professional"


# -------------------------------
# 🎨 HEADER
# -------------------------------
st.set_page_config(
    page_title="Career Pulse",
    page_icon="logo.jpeg", # This sets your logo as the favicon
    layout="centered"
)

# Centered Title with Image
st.markdown(
    """
    <div style='text-align:center;'>
        <img src='logo.jpeg' width='200'/>
        <h1 style='margin-top: 10px;'>Career Pulse</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>An AI-powered career guidance tool to help you explore exciting possibilities!</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Prepare DataFrame for salary chart
df_salary = pd.DataFrame(
    {
        "Career": [k for k in CAREER_INFO],
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
    }
)

st.subheader("📊 Career Salary Comparison")

# Filters for the chart
col1, col2 = st.columns(2)
with col1:
    selected_outlook = st.selectbox(
        "Filter by Career Outlook",
        ["All"] + sorted(list(df_salary["Outlook"].unique())),
    )
with col2:
    sort_by = st.selectbox(
        "Sort By", ["None", "Min Salary (Asc)", "Min Salary (Desc)", "Max Salary (Asc)", "Max Salary (Desc)"]
    )

filtered_df = df_salary.copy()

# Apply outlook filter
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


# Add a column to highlight the predicted career
if 'predicted_career' in st.session_state:
    filtered_df['Highlight'] = filtered_df['Career'].apply(lambda x: 'Predicted Career' if x == st.session_state.predicted_career else 'Other Careers')
    color_scale = alt.Scale(domain=['Predicted Career', 'Other Careers'], range=['#FF4B4B', '#636EF6']) # Streamlit's primary color and a default blue
else:
    filtered_df['Highlight'] = 'Other Careers'
    color_scale = alt.Scale(domain=['Other Careers'], range=['#636EF6'])


chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X("Career:N", sort=None), # Disable default sorting to respect pandas sort
        y="Max Salary:Q",
        color=alt.Color('Highlight', scale=color_scale, legend=None),
        tooltip=["Career", "Min Salary", "Max Salary", "Outlook"],
    )
    .properties(width=700)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


# -------------------------------
# 🧑 User Info
# -------------------------------
st.sidebar.header("🧑‍🎓 Your Profile")
name = st.sidebar.text_input("Enter Your Name")
age = st.sidebar.slider("Select Your Age", 10, 55, 25)
age_group = classify_age(age)
st.sidebar.write(f"Age Group: {age_group}")
email = st.sidebar.text_input("Enter Your Email")


# Visualization Toggle
show_profile = st.sidebar.checkbox("Show Interest Profile")

# -------------------------------
# 📚 Input Section with Tabs
# -------------------------------
tabs = st.tabs(
    [
        "ℹ️ Career Details",
        "📘 Subjects",
        "🛠 Skills",
        "🎯 Interests",
        "🧠 Preferences",
        "💡 Information",
    ]
)

with tabs[0]:
    st.subheader("ℹ️ Explore Career Details")
    selected_career = st.selectbox("Select a Career", CAREER_OPTIONS)
    if selected_career:
        career_info = CAREER_INFO[selected_career]
        st.write(f"**{selected_career}**")
        st.write(f"**Description:** {career_info['description']}")
        st.write(f"**Required Skills:** {', '.join(career_info['skills'])}")
        st.write(f"**Education:** {career_info['education']}")
        st.write(f"**Salary:** {career_info['salary']}")
        st.write(f"**Career Outlook:** {career_info['outlook']}")

with tabs[1]:
    st.subheader(
        "📘 Rate your interest in specific subjects (0 - Not interested, 5 - Very interested)"
    )
    subjects = {
        "Maths - Algebra": st.slider("Algebra", 0, 5),
        "Maths - Calculus": st.slider("Calculus", 0, 5),
        "Science - Biology": st.slider("Biology", 0, 5),
        "Science - Chemistry": st.slider("Chemistry", 0, 5),
        "Science - Physics": st.slider("Physics", 0, 5),
        "Computer Science - Programming": st.slider("Programming", 0, 5),
        "Computer Science - Data Structures": st.slider("Data Structures", 0, 5),
        "History - Ancient": st.slider("Ancient History", 0, 5),
        "History - Modern": st.slider("Modern History", 0, 5),
        "Economics - Microeconomics": st.slider("Microeconomics", 0, 5),
        "Economics - Macroeconomics": st.slider("Macroeconomics", 0, 5),
        "Literature - Fiction": st.slider("Fiction", 0, 5),
        "Literature - Poetry": st.slider("Poetry", 0, 5),
        "Art - Painting": st.slider("Painting", 0, 5),
        "Art - Sculpture": st.slider("Sculpture", 0, 5),
    }

with tabs[2]:
    st.subheader("🛠 Rate your specific skills (0 - Not skilled, 5 - Very skilled)")
    skills = {
        "Problem Solving - Logical": st.slider("Logical Problem Solving", 0, 5),
        "Problem Solving - Creative": st.slider("Creative Problem Solving", 0, 5),
        "Creativity - Visual": st.slider("Visual Creativity", 0, 5),
        "Creativity - Innovation": st.slider("Innovation", 0, 5),
        "Communication - Written": st.slider("Written Communication", 0, 5),
        "Communication - Verbal": st.slider("Verbal Communication", 0, 5),
        "Leadership - Team Management": st.slider("Team Management", 0, 5),
        "Leadership - Initiative": st.slider("Taking Initiative", 0, 5),
        "Programming - Python": st.slider("Python Programming", 0, 5),
        "Programming - Java": st.slider("Java Programming", 0, 5),
        "Designing - UI/UX": st.slider("UI/UX Design", 0, 5),
        "Designing - Graphic": st.slider("Graphic Design", 0, 5),
        "Research - Data Analysis": st.slider("Data Analysis Research", 0, 5),
        "Research - Literature Review": st.slider("Literature Review Research", 0, 5),
    }

with tabs[3]:
    st.subheader(
        "🎯 Rate your interest in specific fields (0 - Not interested, 5 - Very interested)"
    )
    interests = {
        "Technology - Artificial Intelligence": st.slider(
            "Artificial Intelligence", 0, 5
        ),
        "Technology - Cybersecurity": st.slider("Cybersecurity", 0, 5),
        "Technology - Web Development": st.slider("Web Development", 0, 5),
        "Business - Marketing": st.slider("Marketing", 0, 5),
        "Business - Finance": st.slider("Finance", 0, 5),
        "Business - Management": st.slider("Management", 0, 5),
        "Art And Design - Visual Arts": st.slider("Visual Arts", 0, 5),
        "Art And Design - Industrial Design": st.slider("Industrial Design", 0, 5),
        "Healthcare - Clinical Research": st.slider("Clinical Research", 0, 5),
        "Healthcare - Patient Care": st.slider("Patient Care", 0, 5),
        "Education - Primary/Secondary": st.slider(
            "Primary/Secondary Education", 0, 5
        ),
        "Education - Higher Education": st.slider("Higher Education", 0, 5),
        "Engineering - Mechanical": st.slider("Mechanical Engineering", 0, 5),
        "Engineering - Electrical": st.slider("Electrical Engineering", 0, 5),
        "Writing - Creative Writing": st.slider("Creative Writing", 0, 5),
        "Writing - Technical Writing": st.slider("Technical Writing", 0, 5),
    }

with tabs[4]:
    st.subheader("🧠 Rate your preferences")
    preferences = {
        "Enjoy solving complex problems?": st.selectbox(
            "Complex Problems", ["Yes", "No"]
        ),
        "Prefer working with machines?": st.selectbox("Working with Machines", ["Yes", "No"]),
        "Interested in research?": st.selectbox("Interest in Research", ["Yes", "No"]),
        "Enjoy working with people?": st.selectbox("Working with People", ["Yes", "No"]),
        "Prefer working indoors?": st.selectbox("Working Indoors", ["Yes", "No"]),
    }

with tabs[5]: # New tab content
    st.subheader("💡 Information")
    st.info("This is just a beta version and more updates will be coming soon!, This app was developed by Ayan Gantayat and Logo Design by Shreemoyee Shaw")


# -------------------------------
# Email Sending Function
# -------------------------------
def send_career_email(user_email, recipient_name, job_title):
    """Sends an email with career details to the user."""
    print(f"send_career_email called with: {user_email}, {recipient_name}, {job_title}")  # DEBUG

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    if not SENDGRID_API_KEY:
        st.error(
            "Error: SendGrid API key is missing. Please configure it in your environment variables."
        )
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
    </head>
    <body>
        <h2>Congratulations, {recipient_name}!</h2>
        <p>We're excited to share your personalized career prediction from CareerPulse.</p>
        <p>Based on your interests, skills, and preferences, our AI suggests that you might find a fulfilling career as a <b>{job_title}</b>.</p>
        <h3>{job_title}</h3>
        <p>{career_info['description']}</p>
        <p>Here are some key aspects of this career path:</p>
        <ul>
            <li><b>Skills:</b> {', '.join(career_info['skills'])}</li>
            <li><b>Education:</b> {career_info['education']}</li>
            <li><b>Salary:</b> {career_info['salary']}</li>
            <li><b>Outlook:</b> {career_info['outlook']}</li>
        </ul>
        <p>We encourage you to explore this career further!</p>
        <p>Please check your spam folder in your inbox to check the email</p>
        <p>Sincerely,</p>
        <p>The CareerPulse Team(Ayan Gantayat, Shreemoyee Shaw)</p>
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
        print("Sending email...")  # DEBUG
        response = sg.send(message)
        print("Email sent. Response:", response.status_code, response.body)
        if 200 <= response.status_code < 300:
            return True
        else:
            st.error(
                f"Error sending email. Status code: {response.status_code}, Response: {response.body}"
            )
            return False
    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")
        return False


# -------------------------------
# 📊 Sidebar Visualization
# -------------------------------
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
# 🧮 Make Prediction
# -------------------------------
if st.button("🔍 Suggest Careers"):
    if not name:
        st.warning("Please enter your name.")
    elif not email:  # check for email
        st.warning("Please enter your email address")
    elif not all(value is not None for value in subjects.values()) or not all(
        value is not None for value in skills.values()
    ) or not all(value is not None for value in interests.values()) or not all(
        value is not None for value in preferences.values()
    ):
        st.warning(
            "Please rate your interest/skills/preferences in all the sections to get a prediction."
        )
    else:
        # Progress Indicator
        with st.spinner("Analyzing your profile and suggesting careers..."):
            time.sleep(2) # Simulate work being done

            st.subheader(f"Hi {name}, based on your profile:")


            input_data = [
                age,
                subjects["Maths - Algebra"],
                subjects["Maths - Calculus"],
                subjects["Science - Biology"],
                subjects["Science - Chemistry"],
                subjects["Science - Physics"],
                subjects["Computer Science - Programming"],
                subjects["Computer Science - Data Structures"],
                subjects["History - Ancient"],
                subjects["History - Modern"],
                subjects["Economics - Microeconomics"],
                subjects["Economics - Macroeconomics"],
                subjects["Literature - Fiction"],
                subjects["Literature - Poetry"],
                subjects["Art - Painting"],
                subjects["Art - Sculpture"],
                skills["Problem Solving - Logical"],
                skills["Problem Solving - Creative"],
                skills["Creativity - Visual"],
                skills["Creativity - Innovation"],
                skills["Communication - Written"],
                skills["Communication - Verbal"],
                skills["Leadership - Team Management"],
                skills["Leadership - Initiative"],
                interests["Technology - Artificial Intelligence"],
                interests["Technology - Cybersecurity"],
                interests["Technology - Web Development"],
                interests["Business - Marketing"],
                interests["Business - Finance"],
                interests["Business - Management"],
                interests["Art And Design - Visual Arts"],
                interests["Art And Design - Industrial Design"],
                interests["Healthcare - Clinical Research"],
                interests["Healthcare - Patient Care"],
                interests["Education - Primary/Secondary"],
                interests["Education - Higher Education"],
                interests["Engineering - Mechanical"],
                interests["Engineering - Electrical"],
                interests["Writing - Creative Writing"],
                interests["Writing - Technical Writing"],
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
                st.session_state.predicted_career = predicted_career  # Store in session state
                st.session_state.input_data = input_data

                st.success(
                    f"🎯 We suggest you might find a fulfilling career as a **{predicted_career}**!"
                )
                st.info(
                    f"This suggestion is based on your interests, skills, and preferences."
                )

            except Exception as e:
                st.error(f"❗ An error occurred during prediction: {e}")
                st.info(
                    "Please ensure the model is trained and loaded correctly....")

if 'predicted_career' in st.session_state:
    predicted_career = st.session_state.predicted_career
    send_email = st.checkbox("Send me more information via email")

    if predicted_career:
        career_info = CAREER_INFO[predicted_career]
        st.write(f"**{predicted_career}**")
        st.write(f"**Description:** {career_info['description']}")
        st.write(f"**Required Skills:** {', '.join(career_info['skills'])}")
        st.write(f"**Education:** {career_info['education']}")
        st.write(f"**Salary:** {career_info['salary']}")
        st.write(f"**Career Outlook:** {career_info['outlook']}\n")

        if send_email:
            email_sent = send_career_email(email, name, predicted_career)
            if email_sent:
                st.success("Email sent successfully!")
            else:
                st.error(
                    "Failed to send email. Please check your email address and try again. Please also check your SendGrid API key and ensure it is correctly configured."
                )

# Made By Ayan Gantayat(Anonymous)
