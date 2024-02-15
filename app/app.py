from flask import Flask, render_template, request, redirect, url_for, send_file
import os

import numpy as np
import pandas as pd
# from models.classes import *

## Require for sure.
from PyPDF2 import PdfReader
from library.utils import get_parser, preprocessing, unique, get_skills, get_work_experience, extract_, get_email, get_phone_number
from spacy import displacy

# load parser
nlp = get_parser()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        reader = PdfReader(file_path)
        page = reader.pages[0]
        text = page.extract_text()
        # text = preprocessing(raw_text, nlp)
        doc = nlp(text)

        skills = get_skills(doc, nlp)
        work_experiences = get_work_experience(doc, nlp)
        emails = get_email(text, nlp)
        phone_numbers = get_phone_number(text, nlp)

        result = dict()
        result["skills"] = unique(skills)
        result["Work Experience"] = unique(work_experiences)
        result["Email"] = emails
        result["Phone Number"] = phone_numbers

        # data = {
        #     "skills": ", ".join(skills),
        #     "work_experience": ", ".join(work_experiences),
        #     "email": ", ".join(emails),
        #     "phone_number": ", ".join(phone_numbers),
        # }

        
        df = pd.DataFrame.from_dict(result, orient='index').transpose()
        # Define the file name
        excel_file = "export/data.xlsx"

        # Save DataFrame to Excel file
        df.to_excel(excel_file, index=True)

        return render_template('index.html', result = result)
    else:
        return 'Invalid file format'
    
@app.route('/export', methods=['GET'])
def export():
    excel_file = "export/data.xlsx"
    return send_file(excel_file, as_attachment=True)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", result={})

# @app.route('/translate', methods=['POST'])
# def translate():

#     # get prompt from HTML form.
#     # prompt = request.form['query'].strip()

#     reader = PdfReader("data/chaklam_resume.pdf")
#     page = reader.pages[0]
#     raw_text = page.extract_text()
#     clearn_text = preprocessing(raw_text, nlp)
#     doc = nlp(clearn_text)
    

#     return render_template('index.html', result = translated_text, old_query = prompt)


port_number = 8000

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_number)