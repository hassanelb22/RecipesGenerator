
---

# 🍳 RecipesGenerator 🍳

**RecipesGenerator** is a Streamlit-based web application that generates detailed recipe posts using AI-powered APIs like DeepSeek and Gemini. Whether you have a recipe name or an image of a recipe, this app can create a structured and visually appealing recipe post in multiple languages.

---

## Features ✨

- **Recipe Generation**: Generate detailed recipe posts by entering a recipe name or uploading an image of a recipe.
- **Multi-Language Support**: Supports recipe generation in English, Spanish, German, and French.
- **AI-Powered APIs**: Utilizes DeepSeek and Gemini APIs for generating high-quality recipe content.
- **Image-to-Text Extraction**: Extracts text from uploaded recipe images using OCR (Optical Character Recognition).
- **Fallback Mechanism**: If one API fails, the app automatically switches to the other API for seamless recipe generation.

---

## How It Works 🛠️

1. **Choose an Option**:
   - Enter a recipe name manually.
   - Upload an image of a recipe for text extraction.

2. **Select Language**:
   - Choose from English, Spanish, German, or French.

3. **Enter API Keys**:
   - Provide your DeepSeek and Gemini API keys for authentication.

4. **Generate Recipe**:
   - Click the "Generate Recipe" button to create a detailed recipe post.

---

## Installation 🚀

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

---

## Usage 🍽️

1. **Enter Recipe Name**:
   - Input the name of the recipe you want to generate.
   - Select the desired language.
   - Click "Generate Recipe" to get a detailed recipe post.

2. **Upload Recipe Image**:
   - Upload an image of the recipe.
   - The app will extract text from the image using OCR.
   - Select the desired language.
   - Click "Generate Recipe" to create a recipe post.

---

## Supported Languages 🌍

- 🇬🇧 English
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇫🇷 French

---

## API Configuration 🔑

To use the app, you need API keys for both DeepSeek and Gemini. Enter your API keys in the sidebar of the app.

- **DeepSeek API Key**: Obtain it from [DeepSeek](https://www.deepseek.com/).
- **Gemini API Key**: Obtain it from [Gemini](https://developers.generativelanguage.google/](https://aistudio.google.com/app/apikey)).

---

## Example Output 📄

Here’s an example of a generated recipe post:

```
🧁✨ Chocolate Cake ✨🧁

Ingredients:

For Cake:
- 2 cups flour
- 1 cup sugar
- 1/2 cup cocoa powder

For Frosting:
- 1 cup butter
- 2 cups powdered sugar
- 1 tsp vanilla extract

Directions:

1. Preheat the oven to 350°F (175°C).
2. Mix the dry ingredients in a bowl.
3. Add wet ingredients and mix until smooth.
4. Bake for 30 minutes.

Nutritional Information:

⏰ Prep Time: 20 mins | Cooking Time: 30 mins | Total Time: 50 mins
🔥 Kcal: 350 | 🍽️ Servings: 8
```

---

## Requirements 📦

- Python 3.8+
- Streamlit
- Requests
- Pillow (PIL)
- pytesseract (for OCR)

Install the dependencies using:
```bash
pip install -r requirements.txt
```

---

## Contributing 🤝

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏

- Thanks to [DeepSeek](https://www.deepseek.com/) and [Gemini](https://developers.generativelanguage.google/) for their powerful APIs.
- Built with ❤️ using [Streamlit](https://streamlit.io/).

---

Enjoy cooking with **RecipesGenerator**! 🍳✨

---
