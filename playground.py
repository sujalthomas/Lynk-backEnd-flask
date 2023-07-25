from flask import Flask, request, send_file
import openai
from docx import Document
import os
from flask_cors import CORS
import keysconfig as keys

app = Flask(__name__)
CORS(app)

openai.api_key = keys.openai_api_key


@app.route("/generate-cover-letter", methods=["POST"])
def listen():
    data = request.get_json()

    # Extract relevant information from the JSON
    company_name = data.get("Company-name", "Unknown_Company")
    job_listing = data.get("Job-Listing", "")
    recruiter = data.get("Recruiter", "")
    date = data.get("Date", "")

    try:
        resume = open("Sujal_Thomas_resume2023.txt", "r").read()
    except FileNotFoundError:
        return "Resume file not found.", 404

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that crafts tailored cover letters using a resume and a job listing. Your goal is to create a compelling cover letter that showcases the candidate's skills and experiences, aligning them with the job's requirements.",
            },
            {
                "role": "user",
                "content": f"Using this resume, {resume}, and this job listing, {job_listing}, craft a cover letter that doesn't include addresses but highlights the candidate's fit for the role. Ensure it includes the candidate's name, email, phone number, and LinkedIn profile. Also, only include the company name {company_name} , followed by dear recruiters name {recruiter} and today's date {date}.",
            },
        ],
        temperature=1.3,
        top_p=0.9,
        max_tokens=700,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    cover_letter_content = completion.choices[0].message.content

    print(cover_letter_content)

    # Format the filename
    base_filename = f"{company_name}_cv.docx"
    filename = base_filename
    count = 1

    # Ensure filename is unique
    while os.path.isfile(filename):
        filename = f"{company_name}_cv({count}).docx"
        count += 1

    # Create and save the document
    doc = Document()
    doc.add_paragraph(cover_letter_content)
    doc.save(filename)

    return send_file(filename, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
