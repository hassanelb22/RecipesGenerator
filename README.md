# 🍳 RecipesGenerator

RecipesGenerator is a Streamlit-based web application that generates detailed, SEO-optimized recipe posts using AI-powered APIs like Gemini and Segmind. Whether you want a single recipe or bulk generate recipes from a CSV file, this app helps create structured, visually appealing recipe content in multiple languages.

## ✨ Features

- **Recipe Generation**: Generate detailed recipes by entering a name or processing a CSV file.
- **Multi-Language Support**: Supports English, Spanish, German, French, and Arabic.
- **AI-Powered APIs**: Uses Gemini for high-quality text generation and Segmind for stunning images.
- **CSV Processing**: Easily generate multiple recipes at once from a CSV file.
- **SEO Optimization**: Automatically generate meta titles, descriptions, and outlines for search engine ranking.
- **Image Generation**: Create visually appealing images with Segmind.
- **Fallback Mechanism**: If one API fails, the app switches to an alternative method for smooth operation.

## 🛠️ How It Works

1. **Choose a Tool:**
   - Generate a single recipe by entering its name.
   - Process a CSV file to generate multiple recipes.
   - Generate SEO-optimized articles with meta descriptions and outlines.
   - Create recipe images with Segmind.
   - View and export your recipe history as a CSV file.

2. **Select Language:**
   - Choose from English, Spanish, German, French, or Arabic.

3. **Enter API Keys:**
   - Provide your Gemini and Segmind API keys via the sidebar.

4. **Generate Content:**
   - Click the relevant button to create recipes, articles, or images.

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hassanelb22/RecipesGenerator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd RecipesGenerator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🍽️ Usage

### Generate a Single Recipe
- Input the recipe name.
- Select the desired language.
- Click **"Generate Recipe"** to create a detailed recipe post.

### Process a CSV File
- Upload a CSV file containing recipe names.
- Select the desired language.
- Click **"Generate Recipes"** to bulk-generate recipes.

### Generate SEO-Optimized Articles
- Enter a focus keyword.
- Click **"Generate Article"** to create meta titles, descriptions, and outlines.

### Create Images with Segmind
- Enter a prompt (e.g., *"A delicious chocolate cake"*).
- Click **"Generate Image"** to create a recipe image.

### View Recipe History
- Use the **"Recipes History"** tool to view past recipes.
- Export the history as a CSV file for future reference.

## 🌍 Supported Languages
- 🇬🇧 English
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇫🇷 French
- 🇸🇦 Arabic

## 🔑 API Configuration

To use the app, you need API keys for both Gemini and Segmind. Enter your API keys in the sidebar:

- **Gemini API Key**: Obtain it from [Google Gemini](https://gemini.google.com/)
- **Segmind API Key**: Obtain it from [Segmind](https://www.segmind.com/)

---

🚀 **Enjoy creating and sharing amazing recipes!** 🍲
