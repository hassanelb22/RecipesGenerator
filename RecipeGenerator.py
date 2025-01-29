import streamlit as st
import requests

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Language options
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez une publication détaillée de recette en français dans le format structuré suivant:"
}

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
            generated_text = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            return generated_text
        else:
            st.error(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating recipe post with Gemini: {e}")
        return None

# Streamlit app
def main():
    st.title("🍳 Recipe Post Generator 🍳")
    st.sidebar.title("Options")

    # Language selection
    language = st.sidebar.selectbox("Select Language:", list(LANGUAGES.keys()))

    # API Key Input
    st.sidebar.subheader("API Key")
    gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password", value=st.session_state.get("gemini_api_key", ""))

    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key

    # Recipe name input
    recipe_name = st.text_input("Enter the recipe name:")
    
    if st.button("Generate Recipe"):
        if recipe_name:
            if 'gemini_api_key' not in st.session_state:
                st.warning("Please enter your Gemini API key.")
            else:
                recipe_post = generate_recipe_post_gemini(recipe_name, language)
                if recipe_post:
                    st.subheader("Generated Recipe Post:")
                    st.write(recipe_post)
        else:
            st.warning("Please enter a recipe name.")

if __name__ == "__main__":
    main()
