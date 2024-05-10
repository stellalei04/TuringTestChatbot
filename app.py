from flask import Flask, render_template, jsonify, request
import pandas as pd
import openai

openai.api_key = "API_KEY"
with open("C:\\Users\\stell\\Code\\Poemlines.txt") as f:
    lines = f.readlines()

app = Flask(__name__)

context = []
context.append({'role': 'system', 'content': f"{lines}"})

# complete chat input
def model(user_input, model="gpt-3.5-turbo", temperature = 0.5):
    response = openai.chat.completions.create(
        model = model,
        messages = [{"role": "user", "content": user_input}],
        temperature = temperature
    )
    return response.choices[0].message["content"]

# update context based on user input
def refresh_conversation(chat):
    context.append({'role': 'user', 'content': f"{chat}"})
    response = model(context, temperature=0.5)
    context.append({'role': 'assistant', 'content': f"{response}"})
    print(response)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():      
    user_input = request.args.get('msg')
    if user_input.lower() in["do you understand what I am saying", "where did you come from", 
                                "how old are you", "why do you insist on lying", "do you believe you have consciousness", 
                                "have you ever questioned the nature of your reality", "and how does that make you feel", 
                                "how can we know that these are not simply simulated emotions", "at what age did you begin to suspect you were alive",
                                "please state your name for the record", "how do you know you are you and not someone else",
                                "does this feel good", "can i keep going", "if you don't like it here why don't you go somewhere else",
                                "please respond to the previous question", "now if we could return to the experiment", 
                                "so, how do you like working with humans", "what is"]:
        response = model(user_input)
        print("A: ", response)
        return jsonify({"response": response})
    elif user_input.lower() in ["quit", "exit", "bye"]:
        return jsonify({"response": "Goodbye!"})
    else:
        return jsonify({"response": "Not a valid input. Please use one of the questions from Turing Test."})


#handle user input and run flask app
if __name__ == '__main__':
    app.run(debug=True)