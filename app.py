from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')

    # Default bot response
    bot_response = "I'm sorry, I didn't understand that."

    # Handling specific queries
    if user_message.lower() == 'hello':
        bot_response = "Hello! How can I help you today?"
    elif 'artificial intelligence' in user_message.lower():
        bot_response = "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn."
    elif 'machine learning' in user_message.lower():
        bot_response = "Machine Learning is a subset of AI that provides systems the ability to learn and improve from experience without being explicitly programmed."
    elif 'today\'s date' in user_message.lower():
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        bot_response = f"Today's date is {current_date}."
    elif 'how are you' in user_message.lower() or 'how are you feeling' in user_message.lower():
        bot_response = "I'm just a computer program, so I don't have feelings, but I'm here to assist you!"

    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    # Use 0.0.0.0 to listen on all network interfaces
    # Use a port other than 5000 if needed (e.g., 8000)
    app.run(host='0.0.0.0', port=5000, debug=True)
