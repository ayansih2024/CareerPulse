# train_model.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Define feature names and their order (CRUCIAL FOR CONSISTENCY)
FEATURE_NAMES = [
    "Age",
    "Maths - Algebra", "Maths - Calculus", "Science - Biology", "Science - Chemistry",
    "Science - Physics", "Computer Science - Programming", "Computer Science - Data Structures",
    "History - Ancient", "History - Modern", "Economics - Microeconomics",
    "Economics - Macroeconomics", "Literature - Fiction", "Literature - Poetry",
    "Art - Painting", "Art - Sculpture",
    "Problem Solving - Logical", "Problem Solving - Creative", "Creativity - Visual",
    "Creativity - Innovation", "Communication - Written", "Communication - Verbal",
    "Leadership - Team Management", "Leadership - Initiative",
    "Technology - Artificial Intelligence", "Technology - Cybersecurity",
    "Technology - Web Development", "Business - Marketing", "Business - Finance",
    "Business - Management", "Art And Design - Visual Arts",
    "Art And Design - Industrial Design", "Healthcare - Clinical Research",
    "Healthcare - Patient Care", "Education - Primary/Secondary",
    "Education - Higher Education", "Engineering - Mechanical",
    "Engineering - Electrical", "Writing - Creative Writing", "Writing - Technical Writing",
    "Enjoy solving complex problems?", "Prefer working with machines?",
    "Interested in research?", "Enjoy working with people?", "Prefer working indoors?"
]
NUM_FEATURES = len(FEATURE_NAMES)

X = []
y = []

# Career labels (indices for the y array)
CAREER_OPTIONS = [
    "Software Engineer", "Data Scientist", "Web Developer", "Graphic Designer",
    "UX/UI Designer", "Marketing Manager", "Financial Analyst", "Product Manager",
    "Business Analyst", "Human Resources Manager", "Teacher (Primary)", "Teacher (Secondary)",
    "Professor", "Doctor (General)", "Doctor (Specialist)", "Nurse",
    "Pharmacist", "Lawyer", "Journalist", "Technical Writer",
    "Architect", "Civil Engineer", "Mechanical Engineer", "Electrical Engineer",
    "Environmental Scientist", "Data Analyst", "Management Consultant"
]

NUM_CAREERS = len(CAREER_OPTIONS)
SAMPLES_PER_CAREER = 150

def generate_random_input():
    # Generate random input based on the number of features
    return list(np.random.randint(1, 6, 15)) + list(np.random.randint(1, 6, 14)) + list(np.random.randint(0, 2, 5))



# Rule-based data generation
for i in range(NUM_CAREERS):
    for _ in range(SAMPLES_PER_CAREER):
        input_data = generate_random_input()
        age = np.random.randint(18, 45)
        career = CAREER_OPTIONS[i]

        # Initialize a dictionary to hold feature values, including age
        feature_values = {
            "Age": age,
            "Maths - Algebra": np.random.randint(1, 6), "Maths - Calculus": np.random.randint(1, 6),
            "Science - Biology": np.random.randint(1, 6), "Science - Chemistry": np.random.randint(1, 6),
            "Science - Physics": np.random.randint(1, 6), "Computer Science - Programming": np.random.randint(1, 6),
            "Computer Science - Data Structures": np.random.randint(1, 6), "History - Ancient": np.random.randint(1, 6),
            "History - Modern": np.random.randint(1, 6), "Economics - Microeconomics": np.random.randint(1, 6),
            "Economics - Macroeconomics": np.random.randint(1, 6), "Literature - Fiction": np.random.randint(1, 6),
            "Literature - Poetry": np.random.randint(1, 6), "Art - Painting": np.random.randint(1, 6),
            "Art - Sculpture": np.random.randint(1, 6),
            "Problem Solving - Logical": np.random.randint(1, 6), "Problem Solving - Creative":  np.random.randint(1, 6),
            "Creativity - Visual": np.random.randint(1, 6), "Creativity - Innovation":  np.random.randint(1, 6),
            "Communication - Written": np.random.randint(1, 6), "Communication - Verbal":  np.random.randint(1, 6),
            "Leadership - Team Management":  np.random.randint(1, 6), "Leadership - Initiative":  np.random.randint(1, 6),
            "Technology - Artificial Intelligence":  np.random.randint(0, 2), "Technology - Cybersecurity":  np.random.randint(0, 2),
            "Technology - Web Development":  np.random.randint(0, 2), "Business - Marketing":  np.random.randint(0, 2),
            "Business - Finance":  np.random.randint(0, 2), "Business - Management":  np.random.randint(0, 2),
            "Art And Design - Visual Arts":  np.random.randint(0, 2), "Art And Design - Industrial Design":  np.random.randint(0, 2),
            "Healthcare - Clinical Research":  np.random.randint(0, 2), "Healthcare - Patient Care":  np.random.randint(0, 2),
            "Education - Primary/Secondary":  np.random.randint(0, 2), "Education - Higher Education":  np.random.randint(0, 2),
            "Engineering - Mechanical":  np.random.randint(0, 2), "Engineering - Electrical":  np.random.randint(0, 2),
            "Writing - Creative Writing":  np.random.randint(0, 2), "Writing - Technical Writing":  np.random.randint(0, 2),
            "Enjoy solving complex problems?": np.random.choice([0, 1]),
            "Prefer working with machines?": np.random.choice([0, 1]),
            "Interested in research?": np.random.choice([0, 1]),
            "Enjoy working with people?": np.random.choice([0, 1]),
            "Prefer working indoors?": np.random.choice([0, 1]),
        }

        if career == "Software Engineer":
            feature_values["Computer Science - Programming"] = np.random.randint(4, 6)
            feature_values["Computer Science - Data Structures"] = np.random.randint(3, 6)
            feature_values["Technology - Artificial Intelligence"] = np.random.randint(4, 6)
            feature_values["Technology - Cybersecurity"] = np.random.randint(3, 6)
            feature_values["Enjoy solving complex problems?"] = 1
            feature_values["Prefer working with machines?"] = 1
            feature_values["Maths - Algebra"] = np.random.randint(3,5)
        elif career == "Data Scientist":
            feature_values["Maths - Algebra"] = np.random.randint(4, 6)
            feature_values["Research - Data Analysis"] = np.random.randint(4, 6)
            feature_values["Computer Science - Programming"] = np.random.randint(4, 6)
            feature_values["Technology - Artificial Intelligence"] = np.random.randint(4, 6)
            feature_values["Enjoy solving complex problems?"] = 1
            feature_values["Interested in research?"] = 1
        elif career == "Web Developer":
            feature_values["Computer Science - Programming"] = np.random.randint(4, 6)
            feature_values["Technology - Artificial Intelligence"] = np.random.randint(4, 6)
            feature_values["Designing - UI/UX"] = np.random.randint(3, 6)
            feature_values["Designing - Graphic"] = np.random.randint(3, 6)
            feature_values["Technology - Web Development"] = np.random.randint(3, 5)
            feature_values["Prefer working with machines?"] = 1
        elif career == "Graphic Designer":
            feature_values["Designing - Graphic"] = np.random.randint(4, 6)
            feature_values["Art - Painting"] = np.random.randint(4, 6)
            feature_values["Art - Sculpture"] = np.random.randint(3, 6)
            feature_values["Creativity - Visual"] = np.random.randint(4, 6)
        elif career == "UX/UI Designer":
            feature_values["Computer Science - Programming"] = np.random.randint(3, 5)
            feature_values["Designing - UI/UX"] = np.random.randint(4, 6)
            feature_values["Creativity - Visual"] = np.random.randint(4, 6)
            feature_values["Creativity - Innovation"] = np.random.randint(3, 5)
            feature_values["Technology - Web Development"] = np.random.randint(3, 5)
        elif career == "Marketing Manager":
            feature_values["Communication - Written"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Creativity - Innovation"] = np.random.randint(3, 6)
            feature_values["Business - Marketing"] = np.random.randint(3, 5)
            feature_values["Business - Management"] = np.random.randint(2, 4)
        elif career == "Financial Analyst":
            feature_values["Maths - Algebra"] = np.random.randint(4, 6)
            feature_values["Research - Data Analysis"] = np.random.randint(3, 5)
            feature_values["Business - Finance"] = np.random.randint(4, 6)
            feature_values["Interested in research?"] = 1
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Product Manager":
            feature_values["Computer Science - Programming"] = np.random.randint(3, 5)
            feature_values["Communication - Verbal"] = np.random.randint(3, 5)
            feature_values["Leadership - Team Management"] = np.random.randint(3, 5)
            feature_values["Business - Management"] = np.random.randint(3, 5)
            feature_values["Technology - Artificial Intelligence"] = np.random.randint(3, 5)
        elif career == "Business Analyst":
            feature_values["Maths - Algebra"] = np.random.randint(3, 5)
            feature_values["Research - Data Analysis"] = np.random.randint(3, 5)
            feature_values["Communication - Verbal"] = np.random.randint(3, 5)
            feature_values["Business - Management"] = np.random.randint(3, 5)
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Human Resources Manager":
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Leadership - Team Management"] = np.random.randint(4, 6)
            feature_values["Leadership - Initiative"] = np.random.randint(3, 5)
            feature_values["Enjoy working with people?"] = 1
            feature_values["Business - Management"] = np.random.randint(3, 5)
        elif career == "Teacher (Primary)":
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Education - Primary/Secondary"] = np.random.randint(4, 6)
            feature_values["Enjoy working with people?"] = 1
            feature_values["Creativity - Visual"] = np.random.randint(3, 5)
            feature_values["History - Ancient"] = np.random.randint(3, 5)
        elif career == "Teacher (Secondary)":
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Education - Primary/Secondary"] = np.random.randint(4, 6)
            feature_values["Enjoy working with people?"] = 1
            feature_values["History - Ancient"] = np.random.randint(3, 5)
            feature_values["Computer Science - Programming"] = np.random.randint(3, 5)
        elif career == "Professor":
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Research - Literature Review"] = np.random.randint(4, 6)
            feature_values["Education - Higher Education"] = np.random.randint(4, 6)
            feature_values["Interested in research?"] = 1
            #randomly select a subject
            subject_features = ["Maths - Algebra", "Maths - Calculus", "Science - Biology", "Science - Chemistry",
                                "Science - Physics", "Computer Science - Programming","Computer Science - Data Structures"]
            chosen_subject = np.random.choice(subject_features)
            feature_values[chosen_subject] = np.random.randint(4, 6)
        elif career == "Doctor (General)":
            feature_values["Science - Biology"] = np.random.randint(4, 6)
            feature_values["Healthcare - Clinical Research"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(3, 5)
            feature_values["Enjoy working with people?"] = 1
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Doctor (Specialist)":
            feature_values["Science - Biology"] = np.random.randint(4, 6)
            feature_values["Healthcare - Clinical Research"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(3, 5)
            feature_values["Enjoy working with people?"] = 1
            feature_values["Interested in research?"] = 1
        elif career == "Nurse":
            feature_values["Science - Biology"] = np.random.randint(3, 5)
            feature_values["Healthcare - Patient Care"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Enjoy working with people?"] = 1
            feature_values["Leadership - Team Management"] = np.random.randint(2, 4)
        elif career == "Pharmacist":
            feature_values["Science - Chemistry"] = np.random.randint(3, 5)
            feature_values["Healthcare - Patient Care"] = np.random.randint(4, 6)
            feature_values["Maths - Algebra"] = np.random.randint(3, 5)
            feature_values["Research - Data Analysis"] = np.random.randint(2, 4)
        elif career == "Lawyer":
            feature_values["History - Ancient"] = np.random.randint(4, 6)
            feature_values["Communication - Written"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Problem Solving - Logical"] = 1
            feature_values["Research - Literature Review"] = np.random.randint(3, 5)
        elif career == "Journalist":
            feature_values["History - Ancient"] = np.random.randint(3, 5)
            feature_values["Communication - Written"] = np.random.randint(4, 6)
            feature_values["Communication - Verbal"] = np.random.randint(4, 6)
            feature_values["Writing - Creative Writing"] = np.random.randint(4, 6)
            feature_values["Research - Literature Review"] = np.random.randint(3, 5)
        elif career == "Technical Writer":
            feature_values["Computer Science - Programming"] = np.random.randint(3, 5)
            feature_values["Communication - Written"] = np.random.randint(4, 6)
            feature_values["Writing - Technical Writing"] = np.random.randint(4, 6)
            feature_values["Research - Data Analysis"] = np.random.randint(3, 5)
        elif career == "Architect":
            feature_values["Maths - Algebra"] = np.random.randint(3, 5)
            feature_values["Art - Painting"] = np.random.randint(3, 5)
            feature_values["Designing - UI/UX"] = np.random.randint(4, 6)
            feature_values["Engineering - Mechanical"] = np.random.randint(3, 5)
            feature_values["Creativity - Visual"] = np.random.randint(3, 5)
        elif career == "Civil Engineer":
            feature_values["Maths - Calculus"] = np.random.randint(4, 6)
            feature_values["Science - Physics"] = np.random.randint(3, 5)
            feature_values["Engineering - Mechanical"] = np.random.randint(4, 6)
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Mechanical Engineer":
            feature_values["Maths - Calculus"] = np.random.randint(4, 6)
            feature_values["Science - Physics"] = np.random.randint(4, 6)
            feature_values["Engineering - Mechanical"] = np.random.randint(4, 6)
            feature_values["Prefer working with machines?"] = 1
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Electrical Engineer":
            feature_values["Maths - Calculus"] = np.random.randint(4, 6)
            feature_values["Science - Physics"] = np.random.randint(4, 6)
            feature_values["Computer Science - Programming"] = np.random.randint(2, 4)
            feature_values["Engineering - Electrical"] = np.random.randint(4, 6)
            feature_values["Prefer working with machines?"] = 1
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Environmental Scientist":
            feature_values["Science - Biology"] = np.random.randint(4, 6)
            feature_values["Research - Literature Review"] = np.random.randint(3, 5)
            feature_values["Engineering - Mechanical"] = np.random.randint(4, 6)
            feature_values["Interested in research?"] = 1
        elif career == "Data Analyst":
            feature_values["Maths - Algebra"] = np.random.randint(4, 6)
            feature_values["Computer Science - Programming"] = np.random.randint(3, 5)
            feature_values["Research - Data Analysis"] = np.random.randint(4, 6)
            feature_values["Problem Solving - Logical"] = 1
        elif career == "Management Consultant":
            feature_values["Economics - Microeconomics"] = np.random.randint(3, 5)
            feature_values["Communication - Verbal"] = np.random.randint(3, 5)
            feature_values["Business - Management"] = np.random.randint(3, 5)

        # Create the input vector in the correct order
        ordered_input_data = [feature_values[name] for name in FEATURE_NAMES]
        X.append(ordered_input_data)
        y.append(i)

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Create and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the trained model
with open("career_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(f"Trained and saved a new career model with {NUM_FEATURES} features!")
