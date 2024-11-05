# Step 2: Import required libraries
import os
import cv2
import easyocr
import re
import numpy as np
import spacy
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load spaCy model
nlp = spacy.load('en_core_web_sm')  # Load the small English model

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Function to preprocess the image for better OCR accuracy
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return image

# Function to extract text using EasyOCR
def extract_text_with_easyocr(image_path):
    image = preprocess_image(image_path)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image, detail=0)
    extracted_text = ' '.join(result)
    return extracted_text

# Function to extract specific fields using spaCy and regex
def extract_fields_with_spacy(text):
    doc = nlp(text)
    extracted_data = {
        'ID Number': None,
        'Name': None,
        'Father\'s Name': None,
        'Date of Birth': None,
        'Gender': None
    }

    patterns = {
        'ID Number': r'\b(?:ID|ID No|ID Number)\s?:?\s?([A-Z0-9-]+)',
        'Date of Birth': r'\b(?:DOB|Date of Birth|Age)\s?:?\s?(\d{2}[/-]\d{2}[/-]\d{4})',
        'Gender': r'\b(Gender)\s?:?\s?(Male|Female|M|F|Other)'
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_data[field] = match.group(1)

    for ent in doc.ents:
        if ent.label_ == 'PERSON' and extracted_data['Name'] is None:
            extracted_data['Name'] = ent.text
        elif 'father' in ent.text.lower() and extracted_data['Father\'s Name'] is None:
            extracted_data['Father\'s Name'] = ent.text

    return extracted_data

# Function to answer questions using Google Gemini API
def answer_question_gemini(context):
    api_key = "your_api_key" # Replace with your actual API key
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'contents': [
            {
                'parts': [
                    {
                        'text': (
                            f"Context: {context}\n\n"
                            "Extract the following information from the context and format it as:\n"
                            "Name: <name>\n"
                            "Father's Name: <father's name>\n"
                            "Date of Birth: <date of birth>\n"
                            "ID Number: <ID number>\n"
                            "Gender: <gender>\n"
                            "Answer concisely in this format (Do not show the field if info is missing):"
                        )
                    }
                ]
            }
        ]
    }

    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            response_json = response.json()
            answer = response_json['candidates'][0]['content']['parts'][0]['text'].strip()
            return answer
        except (IndexError, KeyError, TypeError) as e:
            return f"Error parsing response: {e}"
    else:
        return f"Error: {response.status_code}, {response.text}"

# Route for uploading and processing the image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_path = f"./{image.filename}"
    image.save(image_path)

    # Extract text from the image and generate answers
    extracted_text = extract_text_with_easyocr(image_path)
    formatted_answer = answer_question_gemini(extracted_text)

    # Remove the image after processing
    os.remove(image_path)

    return jsonify({'raw_text': extracted_text, 'answers': formatted_answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
