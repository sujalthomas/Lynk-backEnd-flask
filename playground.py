from flask import Flask, request, send_file, jsonify, send_file

import openai
from docx import Document
import os
from flask_cors import CORS
import PyPDF2
from itsdangerous import URLSafeTimedSerializer as Serializer

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["https://www.linkedin.com"]}},
    supports_credentials=True,
)

SECRET_KEY = "YOUR_SECRET_KEY"
serializer = Serializer(SECRET_KEY)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))


def is_api_key_valid(api_key):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="davinci", prompt="This is a test.", max_tokens=5
        )
    except:
        return False
    else:
        return True


def convert_to_txt(file, file_type):
    if file_type == "docx":
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_type == "pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join(
            [reader.pages[i].extract_text() for i in range(len(reader.pages))]
        )
    else:
        raise ValueError("Unsupported file type")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.get_json()
    api_key = data.get("apiKey")

    if is_api_key_valid(api_key):
        token = serializer.dumps({"user": "YOUR_USER_IDENTIFIER"})
        return jsonify(success=True, token=token)
    return jsonify(success=False, message="Invalid API key"), 401


@app.route("/generate-cover-letter", methods=["POST"])
def listen():
    token = request.headers.get("Authorization")
    try:
        data = serializer.loads(token, max_age=3600)
    except:
        return jsonify(success=False, message="Invalid or expired token"), 401

    data = request.get_json()
    api_key = data.get("apiKey")
    openai.api_key = api_key

    company_name = data.get("Company-name", "")
    job_listing = data.get("Job-Listing", "")
    recruiter = data.get("Recruiter", "")
    date = data.get("Date", "")

    try:
        resume = open("current_resume.txt", "r").read()
    except FileNotFoundError:
        return "Resume file not found.", 404

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that crafts tailored cover letters using a resume and a job listing. Your goal is to create a compelling cover letter that showcases the candidate's skills and experiences, aligning them with the job's requirements.",
                },
                {
                    "role": "user",
                    "content": f"Using this resume, {resume}, and this job listing, {job_listing}, craft a cover letter that doesn't include addresses but highlights the candidate's fit for the role. Ensure it includes the candidate's name, email, phone number, and LinkedIn profile. Also, only include the company name {company_name}, followed by recruiter's name {recruiter} and today's date {date}. No place holder text is allowed, if recruiters name is not found use 'Dear Hiring Manager.' ",
                },
            ],
            temperature=1.3,
            top_p=0.9,
            max_tokens=700,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )
    except openai.error.OpenAIError as e:
        print("OpenAI API Error:", e)
        return jsonify(success=False, message="OpenAI API Error"), 500

    cover_letter_content = completion.choices[0].message.content
    base_filename = f"{company_name}_cv.docx"
    filename = base_filename
    count = 1

    # Check if "Generated_CVs" folder exists, if not, create it
    folder_name = "Generated_CVs"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Ensure unique filename within the "Generated_CVs" folder
    while os.path.isfile(os.path.join(folder_name, filename)):
        filename = f"{company_name}_cv({count}).docx"
        count += 1

    # Create the document and save it inside "Generated_CVs" folder
    doc = Document()
    doc.add_paragraph(cover_letter_content)
    full_path = os.path.join(folder_name, filename)
    doc.save(full_path)

    return send_file(full_path, as_attachment=True, download_name=filename)


@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify(success=False, message="No file part"), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify(success=False, message="No selected file"), 400

    if file and (len(file.read()) <= 5 * 1024 * 1024):
        file.seek(0)
        file_type = os.path.splitext(file.filename)[1][1:]

        try:
            txt_content = convert_to_txt(file, file_type)
        except ValueError:
            return jsonify(success=False, message="Unsupported file type"), 400

        filename = os.path.join(UPLOAD_FOLDER, "current_resume.txt")
        with open(filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(txt_content)

        return (
            jsonify(success=True, message="File uploaded and converted successfully"),
            200,
        )

    return jsonify(success=False, message="File is too large"), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
