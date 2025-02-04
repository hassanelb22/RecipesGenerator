🍳 RecipesGenerator 🍳
RecipesGenerator is a Streamlit-based web application that generates detailed recipe posts using AI-powered APIs like Gemini and Segmind. Whether you have a recipe name or need bulk recipe generation from a CSV file, this app can create structured, SEO-optimized, and visually appealing recipe content in multiple languages.

Features ✨
Recipe Generation : Generate detailed recipe posts by entering a recipe name or processing a CSV file containing recipe names.
Multi-Language Support : Supports recipe generation in English, Spanish, German, French, and Arabic.
AI-Powered APIs : Utilizes Gemini for generating high-quality text content and Segmind for creating stunning images.
CSV Processing : Bulk-generate recipes from a CSV file with just a few clicks.
SEO Optimization : Generate meta titles, descriptions, outlines, and full-length articles optimized for search engines.
Image Generation : Create visually appealing images using Segmind based on your prompts.
Fallback Mechanism : If one API fails, the app automatically switches to an alternative method for seamless operation.
How It Works 🛠️
Choose a Tool :
Generate a single recipe by entering its name.
Process a CSV file to generate multiple recipes at once.
Generate SEO-optimized articles with meta titles, descriptions, and full content.
Create images using Segmind based on your prompts.
View and export your recipe history as a CSV file.
Select Language :
Choose from English, Spanish, German, French, or Arabic for your recipe posts.
Enter API Keys :
Provide your Gemini and Segmind API keys for authentication via the sidebar.
Generate Content :
Click the appropriate button to generate recipes, articles, or images.
Installation 🚀
Clone the repository:
bash
Copy
1
git clone https://github.com/hassanelb22/RecipesGenerator.git  
Navigate to the project directory:
bash
Copy
1
cd RecipesGenerator  
Install the required dependencies:
bash
Copy
1
pip install -r requirements.txt  
Run the Streamlit app:
bash
Copy
1
streamlit run app.py  
Usage 🍽️
Generate a Single Recipe :
Input the name of the recipe you want to generate.
Select the desired language.
Click "Generate Recipe" to get a detailed recipe post.
Process a CSV File :
Upload a CSV file containing recipe names.
Select the desired language.
Click "Generate Recipes" to create multiple recipe posts in bulk.
Generate SEO-Optimized Articles :
Enter a focus keyword for the article.
Click "Generate Article" to create meta titles, descriptions, outlines, and full-length content.
Create Images with Segmind :
Enter a prompt for the image (e.g., "A delicious chocolate cake").
Click "Generate Image" to create a visually appealing image.
View Recipe History :
Access the "Recipes History" tool to view all previously generated recipes.
Export the history as a CSV file for future reference.
Supported Languages 🌍
🇬🇧 English
🇪🇸 Spanish
🇩🇪 German
🇫🇷 French
🇸🇦 Arabic
API Configuration 🔑
To use the app, you need API keys for both Gemini and Segmind. Enter your API keys in the sidebar of the app:

Gemini API Key : Obtain it from Google Gemini .
Segmind API Key : Obtain it from Segmind .
