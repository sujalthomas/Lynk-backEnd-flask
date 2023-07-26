 # Cover Letter Generator - Backend 🚀

 <p align="center">
   <img src="https://img.icons8.com/clouds/200/000000/document.png"/>
 </p>

 Elevate your job applications with the Cover Letter Generator backend. Leveraging the might of GPT-3.5 Turbo from OpenAI, this tool crafts persuasive cover letters tailored to job listings, offering you a competitive edge in the job market.

 ## 📚 Table of Contents

 - [Features](#-features)
 - [Getting Started](#-getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
 - [Usage](#-usage)
 - [API Endpoints](#-api-endpoints)
 - [Contributing](#-contributing)
 - [License](#-license)
 - [Acknowledgments](#-acknowledgments)

 ## 🌟 Features

 - **Tailored Cover Letter Generation:** Tapping into the capabilities of GPT-3.5 Turbo to deliver unique, tailored cover letters based on a user's resume and specific job listings.
 - **Seamless File Output:** Outputs a `.docx` file directly, ready for download, making the job application process more streamlined.

 ## 🚀 Getting Started

 ### Prerequisites

 - Flask
 - OpenAI API access
 - python-docx
 - PyPDF2

 ### Installation

 1. Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/CoverLetterGenerator-backend.git
    ```
 2. Change into the project directory:
    ```bash
    cd CoverLetterGenerator-backend
    ```
 3. Install the necessary packages:
    ```bash
    pip install flask openai python-docx flask_cors PyPDF2
    ```
4.  OpenAI API Key is retrieved from the front-end

 ## 🖥 Usage

 To initiate the Flask server:
 ```bash
 python server.py
 ```
 This will launch the server at `http://0.0.0.0:3000/`. The primary endpoint for interaction is `/generate-cover-letter`. When paired with the frontend, users can draw details from job listings and prompt the backend to generate a unique cover letter for that specific listing.

 ## 🤝 Contributing
 Contributions, issues, and feature requests are more than welcome! Feel free to review the [issues page](https://github.com/sujalthomas/Lynk-backEnd-flask/issues).

 ## 🎉 Acknowledgments

 - Immense gratitude to [OpenAI](https://openai.com/) for their groundbreaking GPT-3 model.
 - Kudos to Flask for being a lightweight and powerful server framework.

<p align="center">
  Made with ❤️ by Sujal Thomas Tatipelli
</p>
