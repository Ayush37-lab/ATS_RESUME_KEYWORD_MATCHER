from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def home():
    match = None

    if request.method == 'POST':
        resume = request.files['resume']
        jd = request.form['jd'].lower()

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(resume_path)

    
        pdf = PyPDF2.PdfReader(resume_path)
        resume_text = ""

        for page in pdf.pages:
            resume_text += page.extract_text().lower()

    
        resume_words = resume_text.split()
        jd_words = jd.split()

        matched = 0
        for word in set(resume_words):
            if word in jd_words:
                matched += 1

        match = round((matched / len(set(jd_words))) * 100, 2)

    return render_template('index.html', match=match)

if __name__ == '__main__':
    app.run(debug=True)