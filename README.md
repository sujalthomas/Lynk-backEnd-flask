# Cover Letter Generator - Backend 🚀

<p align="center">
  <img src="https://img.icons8.com/clouds/200/000000/document.png"/>
</p>

The Cover Letter Generator backend uses the power of GPT-3.5 Turbo from OpenAI to craft compelling cover letters tailored to job listings.

## 📚 Table of Contents

- [Features](#-features)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 🌟 Features

- **Automatic Cover Letter Generation:** Using GPT-3.5 Turbo's capabilities to create unique cover letters based on user's resume and job listings.
- **File Output:** Automatically generates a `.docx` file ready for download.

## 🚀 Getting Started

### Prerequisites

- Flask
- OpenAI API access
- python-docx

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/YourUsername/CoverLetterGenerator-backend.git
    ```
2. Navigate to the project directory:
    ```bash
    cd CoverLetterGenerator-backend
    ```
3. Install the required packages:
    ```bash
    pip install flask openai python-docx flask_cors
    ```
4. Set up your OpenAI API key in `keysconfig.py`:
    ```python
    openai_api_key = "YOUR_OPENAI_API_KEY"
    ```

## 🖥 Usage

Run the Flask server:
```bash
python server.py

The server will start on `http://0.0.0.0:3000/`. The main endpoint to interact with is `/generate-cover-letter`.

When paired with the frontend, users can extract details from job listings and request the backend to create a unique cover letter tailored to that listing.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/sujalthomas/Lynk-backEnd-flask/issues).

## 🎉 Acknowledgments

- Thanks to [OpenAI](https://openai.com/) for their amazing GPT-3 model.
- Flask for being a lightweight and efficient server framework.
```
---

<p align="center">
  Made with ❤️ by Sujal Thomas Tatipelli
</p>
