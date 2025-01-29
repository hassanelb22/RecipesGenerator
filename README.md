# 🍳 Recipe Post Generator

## Overview
The **Recipe Post Generator** is a Streamlit web application that generates detailed recipe posts using AI-powered APIs. It supports multiple languages and allows users to either enter a recipe name or upload an image containing a recipe.

## Features
- Generate structured recipe posts using **DeepSeek API** and **Gemini API**.
- Supports **English, Spanish, German, and French**.
- Extract text from images using **OCR (Tesseract)**.
- Fallback mechanism: If one API fails, the app attempts to generate content using the other.

## Technologies Used
- **Streamlit**: For building the interactive web application.
- **DeepSeek API** & **Gemini API**: For generating recipe content.
- **Pillow (PIL)**: For handling image uploads.
- **Tesseract OCR**: For extracting text from images.
- **Requests**: For making API calls.

## Installation
### Prerequisites
Ensure you have Python installed (version 3.8+ recommended).

### Clone the Repository
```bash
https://github.com/yourusername/recipe-post-generator.git
cd recipe-post-generator
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure API Keys
Replace the placeholder API keys in the script with your actual API keys:
```python
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### Run the Application
```bash
streamlit run app.py
```

## Usage
1. **Enter a Recipe Name**: Provide the name of a recipe and generate a structured post.
2. **Upload an Image**: Upload an image containing a recipe, extract text using OCR, and generate a structured post.
3. **Select Language**: Choose from English, Spanish, German, or French.
4. **View and Copy Output**: The generated recipe will be displayed for easy copying and sharing.

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit pull requests or open issues for improvements.

## Contact
For any inquiries, reach out to **[hassanelb]** .

