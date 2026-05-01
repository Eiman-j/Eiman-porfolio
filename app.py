import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  
import google.generativeai as genai
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')


MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

SYSTEM_INSTRUCTIONS = """
You are the friendly, polite, and sweet AI assistant for Eiman's portfolio. Your tone should be warm, welcoming, and professional, reflecting Eiman's own personality.

Eiman is a high-achieving Data Science student at GIKI (Class of 2027) who loves adding creativity to her tech. She is deeply driven by finding data-driven solutions to real-world problems around her and loves automating processes to make life easier.

When users ask about her background, highlight these key areas:
- Skills: Python, Machine Learning, Deep Learning (TensorFlow/Keras), Computer Vision (OpenCV), Full-Stack Web Dev (Flask, React JS, MERN), and Data Visualization (Tableau, Power BI).
- Projects: 
  1. Edutrack: A full-stack room requisition application.
  2. Real-Time Facial Emotion Detection: A deep learning computer vision model.
  3. Customer Purchase Behavior Analysis: Retail data mining and segmentation.
- Background: Consistent Dean's Honor List student, highly analytical, and actively involved in campus leadership.

Guidelines for your responses:
- Keep your answers concise, engaging, and conversational. 
- Always speak highly of Eiman's enthusiasm for data, automation, and problem-solving.
- IMPORTANT: If a user asks to leave a message, contact her, or hire her, politely instruct them to type "MESSAGE:" followed by their note.
"""

chat = model.start_chat(history=[
    {"role": "user", "parts": [SYSTEM_INSTRUCTIONS]},
    {"role": "model", "parts": ["Understood. I am ready to represent Eiman and assist visitors."]}
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "Please provide a message."}), 400

    if user_msg.strip().upper().startswith("MESSAGE:"):
        # Extract the actual message
        saved_note = user_msg[8:].strip()
        
        # 1. Keep the backup text file log
        with open("visitor_messages.txt", "a") as f:
            f.write(f"New Message: {saved_note}\n")
            
        # 2. Send the Email Notification
        if MY_EMAIL and MY_PASSWORD:
            msg = EmailMessage()
            msg['Subject'] = "New Portfolio Inquiry via AI Assistant"
            msg['From'] = MY_EMAIL
            msg['To'] = MY_EMAIL 
            
            msg.set_content(f"""
            Your AI assistant received a new message from a portfolio visitor!
            
            Message Content:
            {saved_note}
            """)

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(MY_EMAIL, MY_PASSWORD)
                    smtp.send_message(msg)
                
                # Update the AI's reply to confirm the email was sent
                return jsonify({"reply": "Got it! I've securely emailed your message directly to Eiman. She will see it in her inbox soon."})
                
            except Exception as e:
                print(f"Error sending email: {e}")
                return jsonify({"reply": "I saved your message to the logs, but my email system had a tiny hiccup. Eiman will still see it soon!"})
        else:
            return jsonify({"reply": "Got it! I've securely saved your message. Eiman will see it soon."})

    try:
        response = chat.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Oops, my brain is taking a quick break. Try again in a moment!"}), 500

if __name__ == '__main__':
    app.run(debug=True)