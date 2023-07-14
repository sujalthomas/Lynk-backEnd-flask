from flask import Flask, request
import openai
from docx import Document
import os
from flask_cors import CORS
import datetime



app = Flask(__name__)
CORS(app)

linkedin = None
openai.api_key = "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"

@app.route('/generate-cover-letter', methods=['POST'])
def listen():
    global linkedin
    linkedin = request.get_json()

    resume = open("Sujal_Thomas_resume2023.txt", "r").read()

    #gets todays date
    today = datetime.date.today()
    
    company_name = linkedin.get("company", "Company") # replace with actual company name key if it exists in your linkedin JSON data

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that utilizes information from a resume and a job listing to generate a custom cover letter."},
            {"role": "user", "content": f"Generate a cover letter based on specific details from the following resume and job listing, but without including my address or the company's address. Be sure to include my name, email, phone number and linkedin profile. Resume: {resume} Job listing: {linkedin} Date: {today}"},
        ],
        temperature=0,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
    )
    
    cover_letter_content = completion.choices[0].message.content
    
    #return jsonify({'message': 'Cover letter generated.'}), 200

    print(cover_letter_content)

    # Format the filename
    base_filename = f"{company_name}_cv.docx"
    filename = base_filename
    count = 1

    # Check if the file exists and if so, create a new filename with a count
    while os.path.isfile(filename):
        filename = f"{company_name}_cv({count}).docx"
        count += 1

    # Create a new Document
    doc = Document()
    # Add the content to the document
    doc.add_paragraph(cover_letter_content)
    # Save the document
    doc.save(filename)

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)


#But, there's another important thing to note: your browser extension is expecting the server to return a file URL (based on this line: a.href = data.fileUrl;). However, your server is currently not configured to serve files, and it's also not returning any file URL. So, even after you resolve the JSON error, your code might not behave as expected because data.fileUrl will be undefined.

#Serving files and handling file downloads would involve a different setup. You could use a Python library like Flask-SendFile to serve files, and you would need to generate a URL for the created .docx file and return that URL in the server's JSON response. However, this involves significant changes to your server code. If you're interested in this, I recommend checking out Flask's documentation or other resources on how to serve files with Flask.