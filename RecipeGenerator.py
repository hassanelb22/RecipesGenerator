import streamlit as st
import requests
import os

# File to store the API key
API_KEY_FILE = "gemini_api_key.txt"

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Language options
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez une publication détaillée de recette en français dans le format structuré suivant:"
}

# Emoji mapping based on recipe keywords
EMOJI_MAPPING = {
    "pizza": "🍕",
    "cake": "🍰",
    "salad": "🥗",
    "pasta": "🍝",
    "burger": "🍔",
    "sushi": "🍣",
    "taco": "🌮",
    "ice cream": "🍦",
    "bread": "🍞",
    "soup": "🍲",
    "steak": "🥩",
    "chicken": "🍗",
    "fish": "🐟",
    "rice": "🍚",
    "pancake": "🥞",
    "cookie": "🍪",
    "pie": "🥧",
    "donut": "🍩",
    "coffee": "☕",
    "tea": "🍵",
    "smoothie": "🥤",
    "juice": "🧃",
    "wine": "🍷",
    "beer": "🍺",
    "cocktail": "🍹",
}

# Function to get a dynamic emoji based on the recipe name
def get_dynamic_emoji(recipe_name):
    recipe_name_lower = recipe_name.lower()
    for keyword, emoji in EMOJI_MAPPING.items():
        if keyword in recipe_name_lower:
            return emoji
    return "🍳"  # Default emoji for recipes

# Function to generate a recipe post using Gemini API
def generate_recipe_post_gemini(recipe_name_or_text, language):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        # Get dynamic emoji for the recipe title
        emoji = get_dynamic_emoji(recipe_name_or_text)
        
        prompt = f"{LANGUAGES[language]}\n\n"
        prompt += f"{emoji}✨ {recipe_name_or_text} ✨{emoji}\n\n"
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

# Function to save API key to a file
def save_api_key(api_key):
    with open(API_KEY_FILE, "w") as file:
        file.write(api_key)

# Function to load API key from a file
def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as file:
            return file.read().strip()
    return None

# Streamlit app
def main():
    # Custom HTML and CSS for the logo and stylish font
    st.markdown("""
        <style>
            .logo {
                font-family: 'Pacifico', cursive;
                font-size: 48px;
                text-align: center;
                margin-bottom: 20px;
            }
           
        
            @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        </style>
        <div class="logo">
            <span>🍳</span> Recipe Post Generator <span>🍳</span>
        </div>
    """, unsafe_allow_html=True)

    # Load API key from file
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = load_api_key() or ""

    # API Key Input
    st.markdown("""
        <label class="api-key-label">
            Enter your Gemini API Key
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="api-key-link">
                Get your API key here →
            </a>
        </label>
    """, unsafe_allow_html=True)
    gemini_api_key = st.text_input("", type="password", value=st.session_state.gemini_api_key, key="apiKey")

    # Save API key to file when it changes
    if gemini_api_key != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key
        save_api_key(gemini_api_key)

    # Recipe name input
    recipe_name = st.text_input("Enter the recipe name:")

    # Language selection
    language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

    if st.button("Generate Recipe"):
        if recipe_name:
            if not st.session_state.gemini_api_key:
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
