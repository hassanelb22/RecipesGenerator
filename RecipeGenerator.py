import streamlit as st
import requests
from PIL import Image


# API configurations
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/recipe/generate"  # Replace with actual DeepSeek API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Language options
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez une publicación détaillée de recette en français dans le format structuré suivant:"
}

# Function to generate a recipe post using DeepSeek API
def generate_recipe_post_deepseek(recipe_name_or_text, language):
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        prompt = f"{LANGUAGES[language]}\n\n"
        prompt += "🧁✨ [Recipe Name] ✨🧁\n\n"
        prompt += "Ingredients:\n\n"
        prompt += "For [Component 1]:\n"
        prompt += "- [Ingredient 1]\n"
        prompt += "- [Ingredient 2]\n\n"
        prompt += "For [Component 2]:\n"
        prompt += "- [Ingredient 1]\n"
        prompt += "- [Ingredient 2]\n\n"
        prompt += "Directions:\n\n"
        prompt += "1. [Step 1]\n"
        prompt += "2. [Step 2]\n\n"
        prompt += "Nutritional Information:\n\n"
        prompt += "⏰ Prep Time: [Time] | Cooking Time: [Time] | Total Time: [Time]\n"
        prompt += "🔥 Kcal: [Calories] | 🍽️ Servings: [Servings]"
        payload = {
            "prompt": f"{prompt}\n\n{recipe_name_or_text}",
            "max_tokens": 500,
            "temperature": 0.7
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "").strip()
        else:
            st.error(f"DeepSeek API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating recipe post with DeepSeek: {e}")
        return None

# Function to generate a recipe post using Gemini API
def generate_recipe_post_gemini(recipe_name_or_text, language):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        prompt = f"{LANGUAGES[language]}\n\n"
        prompt += "🧁✨ [Recipe Name] ✨🧁\n\n"
        prompt += "Ingredients:\n\n"
        prompt += "For [Component 1]:\n"
        prompt += "- [Ingredient 1]\n"
        prompt += "- [Ingredient 2]\n\n"
        prompt += "For [Component 2]:\n"
        prompt += "- [Ingredient 1]\n"
        prompt += "- [Ingredient 2]\n\n"
        prompt += "Directions:\n\n"
        prompt += "1. [Step 1]\n"
        prompt += "2. [Step 2]\n\n"
        prompt += "Nutritional Information:\n\n"
        prompt += "⏰ Prep Time: [Time] | Cooking Time: [Time] | Total Time: [Time]\n"
        prompt += "🔥 Kcal: [Calories] | 🍽️ Servings: [Servings]"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{prompt}\n\n{recipe_name_or_text}"
                }]
            }]
        }
        params = {
            "key": st.session_state.gemini_api_key
        }
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, params=params)
        if response.status_code == 200:
            # Extract the generated text from the response
            generated_text = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            return generated_text
        else:
            st.error(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating recipe post with Gemini: {e}")
        return None

# Function to extract text from an image using OCR
def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return None

# Main function to generate recipe post using both APIs
def generate_recipe_post(recipe_name_or_text, language):
    # Try DeepSeek API first
    recipe_post = generate_recipe_post_deepseek(recipe_name_or_text, language)
    if not recipe_post:
        st.warning("DeepSeek API failed. Trying Gemini API...")
        # Fallback to Gemini API
        recipe_post = generate_recipe_post_gemini(recipe_name_or_text, language)
    return recipe_post

# Streamlit app
def main():
    st.title("🍳 Recipe Post Generator 🍳")
    st.sidebar.title("Options")

    # User choice: Upload image or enter recipe name
    option = st.sidebar.radio("Choose an option:", ("Enter Recipe Name", "Upload Image"))

    # Language selection
    language = st.sidebar.selectbox("Select Language:", list(LANGUAGES.keys()))

    # API Key Input
    st.sidebar.subheader("API Keys")
    deepseek_api_key = st.sidebar.text_input("Enter your DeepSeek API Key:", type="password")
    gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

    if deepseek_api_key:
        st.session_state.deepseek_api_key = deepseek_api_key
    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key

    if option == "Enter Recipe Name":
        recipe_name = st.text_input("Enter the recipe name:")
        if st.button("Generate Recipe"):
            if recipe_name:
                if 'deepseek_api_key' not in st.session_state or 'gemini_api_key' not in st.session_state:
                    st.warning("Please enter both API keys.")
                else:
                    recipe_post = generate_recipe_post(recipe_name, language)
                    if recipe_post:
                        st.subheader("Generated Recipe Post:")
                        st.write(recipe_post)
            else:
                st.warning("Please enter a recipe name.")

    elif option == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image of the recipe:", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            if st.button("Extract Text and Generate Recipe"):
                if 'deepseek_api_key' not in st.session_state or 'gemini_api_key' not in st.session_state:
                    st.warning("Please enter both API keys.")
                else:
                    extracted_text = extract_text_from_image(image)
                    if extracted_text:
                        st.subheader("Extracted Text:")
                        st.write(extracted_text)
                        recipe_post = generate_recipe_post(extracted_text, language)
                        if recipe_post:
                            st.subheader("Generated Recipe Post:")
                            st.write(recipe_post)
                    else:
                        st.error("Failed to extract text from the image.")

if __name__ == "__main__":
    main()
