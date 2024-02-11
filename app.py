from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Global variable to track conversation state
conversation_state = {}

# Global variable to store user-selected domain
selected_domain = None

# Global variable to store skills for each domain
skills = {
    "Marketing": [],
    "Software Developer": [],
    "Architect": [],
    "Management": [],
    "Data Analyst/Scientist": []
}

# Jobs data
jobs_data = {
    "Marketing": [
        {
            "Job Title": "Marketing Manager",
            "Responsibilities": "Developing marketing strategies, managing campaigns, analyzing market trends, conducting market research.",
            "Qualifications": "Bachelor's degree in marketing or related field, experience in marketing roles, strong communication skills.",
            "Openings": 20,
            "Skills Required": ["Market Research", "Campaign Management", "Strategic Planning", "Communication Skills", "Data Analysis"]
        },
        {
            "Job Title": "Digital Marketing Specialist",
            "Responsibilities": "Creating and managing digital marketing campaigns, optimizing online presence, analyzing digital metrics.",
            "Qualifications": "Bachelor's degree in marketing or related field, experience in digital marketing, proficiency in digital marketing tools.",
            "Openings": 20,
            "Skills Required": ["Digital Marketing", "SEO", "Social Media Marketing", "Analytics", "Content Creation"]
        }
    ],
    "Software Developer": [
        {
            "Job Title": "Full Stack Developer",
            "Responsibilities": "Developing web applications, collaborating with cross-functional teams, troubleshooting and debugging code.",
            "Qualifications": "Bachelor's degree in computer science or related field, proficiency in programming languages (e.g., Java, Python), experience with web development frameworks.",
            "Openings": 50,
            "Skills Required": ["Java", "Python", "Web Development", "Problem Solving", "Team Collaboration"]
        },
        {
            "Job Title": "Mobile App Developer",
            "Responsibilities": "Designing and developing mobile applications for iOS and Android platforms, optimizing performance.",
            "Qualifications": "Bachelor's degree in computer science or related field, experience in mobile app development, familiarity with mobile development frameworks.",
            "Openings": 50,
            "Skills Required": ["iOS Development", "Android Development", "Mobile UI/UX Design", "API Integration", "Performance Optimization"]
        }
    ],
    "Architect": [
        {
            "Job Title": "Enterprise Architect",
            "Responsibilities": "Designing and implementing enterprise-level systems, ensuring architectural integrity, advising on technology decisions.",
            "Qualifications": "Bachelor's or master's degree in architecture, relevant certifications (e.g., TOGAF), experience in enterprise architecture roles.",
            "Openings": 10,
            "Skills Required": ["System Design", "Enterprise Architecture", "Decision Making", "Certifications", "Communication Skills"]
        },
        {
            "Job Title": "Solution Architect",
            "Responsibilities": "Developing architecture solutions for specific business problems, collaborating with stakeholders, ensuring alignment with business goals.",
            "Qualifications": "Bachelor's or master's degree in architecture, experience in solution architecture roles, strong analytical skills.",
            "Openings": 10,
            "Skills Required": ["Solution Design", "Stakeholder Management", "Problem Solving", "Analytical Skills", "Business Alignment"]
        }
    ],
    "Management": [
        {
            "Job Title": "Project Manager",
            "Responsibilities": "Leading project teams, managing budgets and resources, ensuring project milestones are met.",
            "Qualifications": "Bachelor's degree in business administration or related field, project management certification (e.g., PMP), strong leadership skills.",
            "Openings": 30,
            "Skills Required": ["Project Management", "Budget Management", "Leadership", "Time Management", "Problem Solving"]
        },
        {
            "Job Title": "Operations Manager",
            "Responsibilities": "Overseeing daily operations, optimizing processes, managing resources, ensuring compliance.",
            "Qualifications": "Bachelor's degree in business administration or related field, experience in operations management, strong organizational skills.",
            "Openings": 30,
            "Skills Required": ["Operations Management", "Process Optimization", "Resource Management", "Compliance", "Organizational Skills"]
        }
    ],
    "Data Analyst/Scientist": [
        {
            "Job Title": "Data Analyst",
            "Responsibilities": "Analyzing data, generating reports, identifying trends and patterns, providing insights to support decision-making.",
            "Qualifications": "Bachelor's degree in mathematics, statistics, computer science, or related field, experience in data analysis, proficiency in data analysis tools (e.g., Excel, SQL).",
            "Openings": 20,
            "Skills Required": ["Data Analysis", "Statistical Analysis", "Reporting", "Problem Solving", "Attention to Detail"]
        },
        {
            "Job Title": "Business Analyst",
            "Responsibilities": "Gathering and analyzing business requirements, identifying opportunities for process improvement, developing business cases.",
            "Qualifications": "Bachelor's degree in business administration, economics, or related field, experience in business analysis, strong analytical and communication skills.",
            "Openings": 20,
            "Skills Required": ["Business Analysis", "Requirement Gathering", "Process Improvement", "Analytical Skills", "Communication Skills"]
        },
        {
            "Job Title": "Data Scientist",
            "Responsibilities": "Analyzing complex datasets, building predictive models, developing algorithms, interpreting results.",
            "Qualifications": "Master's or Ph.D. in statistics, mathematics, computer science, or related field, experience in data science, proficiency in programming languages (e.g., Python, R).",
            "Openings": 20,
            "Skills Required": ["Data Science", "Predictive Modeling", "Algorithm Development", "Python", "R"]
        }
    ]
}

@app.route('/chat', methods=['POST'])
def chat():
    global selected_domain

    user_message = request.form.get('user_message')

    # Default bot response
    bot_response = "I'm sorry, I didn't understand that."

    # Handling specific queries
    if user_message.lower() == 'hello':
        bot_response = "Hello! Select which domain you are interested to work in:\n1. Marketing\n2. Software Developer\n3. Architect\n4. Management\n5. Data Analyst/Scientist"
        # Update conversation state
        conversation_state['prompt_domain_selection'] = True
    elif user_message.lower() in ['marketing', 'software developer', 'architect', 'management', 'data analyst/scientist']:
        selected_domain = user_message.title()
        bot_response = f"You have selected '{selected_domain}' domain. Please provide the skills you know in this domain, separated by commas."
    elif selected_domain:
        skills[selected_domain] = [skill.strip() for skill in user_message.split(',')]
        bot_response = f"Thank you for providing your skills in '{selected_domain}' domain.\n\nHere are some jobs available in '{selected_domain}':\n\n"
        jobs = jobs_data.get(selected_domain, [])
        if jobs:
            for job in jobs:
                bot_response += f"Job Title: {job['Job Title']}\n"
                bot_response += f"Responsibilities: {job['Responsibilities']}\n"
                bot_response += f"Qualifications: {job['Qualifications']}\n"
                bot_response += f"Openings: {job['Openings']}\n"
                bot_response += f"Skills Required: {', '.join(job['Skills Required'])}\n\n"
        else:
            bot_response += "No jobs found for this domain."
        selected_domain = None

    return jsonify({'bot_response': bot_response, 'selected_domain': selected_domain, 'skills': skills})

if __name__ == '__main__':
    app.run(debug=True)
