from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global variable to track conversation state
conversation_state = {}

# Global variable to store user-selected domain
selected_domain = None

# Global variable to store user-selected skills
selected_skills = []

# Global variable to store skills for each domain
skills = {
    "Marketing": ["Digital Marketing", "SEO", "Social Media Marketing", "Analytics", "Content Creation"],
    "Software Developer": ["iOS Development", "Android Development", "Mobile UI/UX Design", "API Integration", "Performance Optimization"],
    "Architect": ["System Design", "Enterprise Architecture", "Decision Making"],
    "Management": ["Project Management", "Budget Management", "Leadership", "Time Management", "Problem Solving"],
    "Data Analyst/Scientist": ["Data Analysis", "Statistical Analysis", "Reporting", "Problem Solving", "Attention to Detail"]
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

@app.route('/')
def home():
    return render_template('index.html')

 

@app.route('/chat', methods=['POST'])
def chat():
    global selected_domain, selected_skills

    user_message = request.form.get('user_message')

    # Default bot response
    bot_response = "I'm sorry, I didn't understand that."

    # Handling specific queries
    if user_message.lower() in ['hello', 'hi']:
        bot_response = "Hello! Select which domain you are interested to work in:"
        # Update conversation state
        conversation_state['prompt_domain_selection'] = True
    elif conversation_state.get('prompt_domain_selection'):
        if user_message.isdigit():
            # Convert number to corresponding domain
            domains = ["Marketing", "Software Developer", "Architect", "Management", "Data Analyst/Scientist"]
            selected_domain = domains[int(user_message) - 1]
        else:
            selected_domain = user_message.title()

        # Get skills for the selected domain
        domain_skills = skills.get(selected_domain, [])
        if domain_skills:
            bot_response = f"Here are the skills required in '{selected_domain}':\n\n"
            for skill in domain_skills:
                # Generate HTML checkboxes for each skill
                bot_response += f'<input type="checkbox" class="skill-option" value="{skill}"> {skill}<br>'
            # Add a submit button after listing skills
            bot_response += '<button id="submit-skills">Submit</button>'
        else:
            # Don't display the message if no skills are found
            bot_response = ""

        # Update conversation state
        conversation_state['selected_domain'] = selected_domain

    elif 'selected_domain' in conversation_state:
        selected_domain = conversation_state['selected_domain']
        if 'selected_skills' in conversation_state:
            selected_skills = conversation_state['selected_skills']
            # Get jobs for the selected domain
            domain_jobs = jobs_data.get(selected_domain, [])
            if domain_jobs:
                bot_response = f"Here are the available jobs in '{selected_domain}':\n\n"
                for job in domain_jobs:
                    bot_response += f"Job Title: {job['Job Title']}\n"
                    bot_response += f"Responsibilities: {job['Responsibilities']}\n"
                    bot_response += f"Qualifications: {job['Qualifications']}\n"
                    bot_response += f"Openings: {job['Openings']}\n\n"
            else:
                bot_response = f"No jobs found for '{selected_domain}'."
        else:
            bot_response = "Please select your skills first."

    return jsonify({'bot_response': bot_response})



@app.route('/submit_skills', methods=['POST'])
def submit_skills():
    global selected_skills
    selected_skills = request.json.get('selected_skill', [])
    conversation_state['selected_skills'] = selected_skills
    
    # Retrieve the selected domain from conversation state
    selected_domain = conversation_state.get('selected_domain')

    if selected_domain:
        # Get jobs for the selected domain
        domain_jobs = jobs_data.get(selected_domain, [])
        if domain_jobs:
            bot_response = f"Here are the available jobs in '{selected_domain}':\n\n"
            for job in domain_jobs:
                bot_response += f"Job Title: {job['Job Title']}\n"
                bot_response += f"Responsibilities: {job['Responsibilities']}\n"
                bot_response += f"Qualifications: {job['Qualifications']}\n"
                bot_response += f"Openings: {job['Openings']}\n\n"
        else:
            bot_response = f"No jobs found for '{selected_domain}'."
    else:
        bot_response = "Please select your skills first."

    return jsonify({'bot_response': bot_response})





if __name__ == '__main__':
    app.run(debug=True)
