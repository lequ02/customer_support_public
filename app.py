from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, render_template_string, session
import os
from werkzeug.utils import secure_filename
from main import *
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session
executor = ThreadPoolExecutor(max_workers=2)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global variable to store the future
save_future = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/thank-you', methods=['GET'])
def thank_you():
    response_content = session.get('response_content', 'GET: No additional information available.')
    with open('thankyou.html', 'r') as file:
        template = file.read()
    
    formatted_content = f"{response_content}"
    return render_template_string(template, response_content=formatted_content)

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    global save_future
    
    product_name = request.form.get('productName', '')
    complaint_text = request.form.get('complaintText', '')
    
    # Handle file uploads
    uploaded_files = request.files.getlist('fileUpload')
    file_paths = []
    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            file_paths.append(file_path)
    
    # Handle audio complaint
    audio_complaint = request.files.get('audioComplaint')
    audio_path = None
    if audio_complaint and audio_complaint.filename:
        audio_filename = secure_filename(audio_complaint.filename)
        audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
        audio_complaint.save(audio_path)
    
    # Check if at least one required field is provided
    if not complaint_text and not file_paths and not audio_path:
        return jsonify({"error": "Please provide at least one of: complaint details, file upload, or audio recording."}), 400

    start_time = time.time()
    
    # Process the complaint
    response_json, response_content, future_save = process_complaint(product_name, complaint_text, file_paths, audio_path)
    
    # Store response_content in session
    session['response_content'] = response_content
    
    # Store the future in the global variable
    save_future = future_save
    
    # Add a callback to print message when save_to_db is done
    if save_future is not None:
        save_future.add_done_callback(save_to_db_completed)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")
    
    # Redirect to thank you page immediately
    return redirect(url_for('thank_you'), code=307)

@app.route('/check-save-status', methods=['GET'])
def check_save_status():
    global save_future
    
    if save_future is None:
        return jsonify({"status": "No save operation initiated."}), 400

    # Check if the save_to_db function has completed
    if save_future.done():
        return jsonify({"status": "Save operation completed successfully."}), 200
    else:
        return jsonify({"status": "Save operation still in progress."}), 200

def process_complaint(product_name, complaint_text, file_paths, audio_path):
    response_json, response_content, future_save = main(product_name, complaint_text, file_paths, audio_path)
    return response_json, response_content, future_save

def save_to_db_completed(future):
    # print("\n\nSave to db completed \n\n")
    print(future.result())

if __name__ == '__main__':
    app.run(debug=True)
