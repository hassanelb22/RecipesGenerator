import streamlit as st
import requests

# Custom CSS for the API key input field and overall design
st.markdown(
    """
    <style>
    .api-key-container {
        position: relative;
        width: 100%;
        margin-bottom: 1rem;
    }
    .api-key-container input {
        width: 100%;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: 1px solid #d1d5db;
        outline: none;
        font-size: 1rem;
    }
    .api-key-container input:focus {
        border-color: #f97316;
        box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.5);
    }
    .api-key-container button {
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        font-size: 0.875rem;
    }
    .api-key-container button:hover {
        color: #374151;
    }
    .title {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.25rem;
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# Streamlit app
def main():
    # Title and Subtitle
    st.markdown('<div class="title">CookShare</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Sharing Community</div>', unsafe_allow_html=True)

    # API Key Input with custom styling
    st.markdown(
        """
        <div class="api-key-container" bis_skin_checked="1">
            <input id="apiKey" type="text" placeholder="Enter your Google API key" class="w-full px-4 py-2 rounded-md border border-gray-200 focus:ring-2 focus:ring-orange-500 focus:border-transparent" required="" value="">
            <button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700">Hide</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Use Streamlit's text_input for actual functionality
    gemini_api_key = st.text_input("", type="password", key="gemini_api_key", label_visibility="collapsed")

    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key

    # Language selection
    language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

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
