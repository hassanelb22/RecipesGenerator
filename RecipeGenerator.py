import streamlit as st
import requests

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Language options
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez una publicación detallada de recette en français dans le format structuré suivant:"
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

# Function to generate MidJourney prompt (Version 1)
def generate_midjourney_prompt_v1(recipe):
    prompt = f"{recipe} STYLE: amateur Close-up Shot | EMOTION: Tempting | SCENE: kitchen | TAGS: amateur food photography, clean composition, dramatic lighting, mouth-watering | CAMERA: iphone 15 pro max | SHOT TYPE: Close-up | COMPOSITION: top side view Centered | LIGHTING: Soft directional light | TIME: Daytime | LOCATION TYPE: Kitchen near windows --ar 1:1"
    return prompt

# Function to generate MidJourney prompt (Version 2)
def generate_midjourney_prompt_v2(recipe):
    prompt = f"Capture the essence of This Light and refreshing, {recipe}. Make our readers crave a bite just by looking at your photo. We want to see it in all its mouthwatering glory, ready to inspire cooks and bakers alike. Get creative with your composition, lighting, and styling. Make it look Realistic, camera: iphone, V6"
    return prompt

# Streamlit app
def main():
    # Custom CSS to center the logo
    st.markdown("""
        <style>
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .logo-container img {
            max-width: 300px; /* Adjust the size of the logo */
        }
        .spacer {
            margin-top: 30px; /* Space between recipe and MidJourney prompts */
        }
        </style>
    """, unsafe_allow_html=True)

    # JavaScript to load API key and password from localStorage
    st.markdown("""
        <script>
        // Load API key and password from localStorage when the page loads
        function loadFromLocalStorage() {
            const apiKey = localStorage.getItem("gemini_api_key");
            const password = localStorage.getItem("password");
            if (apiKey) {
                document.getElementById("apiKey").value = apiKey;
            }
            if (password) {
                document.getElementById("password").value = password;
            }
        }
        window.onload = loadFromLocalStorage;

        // Save API key and password to localStorage when the input changes
        function saveToLocalStorage(key, value) {
            localStorage.setItem(key, value);
        }
        </script>
    """, unsafe_allow_html=True)

    # Initialize session state for authentication and API key
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ""

    # Password check
    if not st.session_state.authenticated:
        password = st.text_input(
            "Enter Password:",
            type="password",
            key="password",
            placeholder="Enter your password",
            on_change=lambda: st.session_state.update({"password": st.session_state.password})
        )

        if password:
            if "password" not in st.secrets:
                st.error("Password key is missing in secrets. Please check your secrets configuration.")
            else:
                if password == st.secrets["password"]:
                    st.session_state.authenticated = True
                    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
                else:
                    st.error("Incorrect password. Please try again.")
            # Save password to localStorage
            st.markdown(f"""
                <script>
                localStorage.setItem("password", "{password}");
                </script>
            """, unsafe_allow_html=True)
        return

    # Logo container with your logo
    st.markdown(
        '<div class="logo-container">'
        '<img src="https://i.ibb.co/ZpdDQDr2/recipe-generator.png" alt="Recipe Generator Logo">'
        '</div>',
        unsafe_allow_html=True
    )

    # Custom HTML for API Key Input Label
    st.markdown("""
        <label class="api-key-label">
            Google GEMINI API Key
            <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" class="api-key-link">
                Get your API key here →
            </a>
        </label>
    """, unsafe_allow_html=True)

    # API Key Input with placeholder
    gemini_api_key = st.text_input(
        "",  # Empty label since we're using custom HTML above
        type="password",
        value=st.session_state.gemini_api_key,
        key="apiKey",
        on_change=lambda: st.session_state.update({"gemini_api_key": st.session_state.apiKey}),
        placeholder="Enter your Google API key"  # Placeholder for API key input
    )

    # Save API key to localStorage when the user inputs it
    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key
        st.markdown(f"""
            <script>
            localStorage.setItem("gemini_api_key", "{gemini_api_key}");
            </script>
        """, unsafe_allow_html=True)

    # Recipe name input with placeholder
    recipe_name = st.text_input(
        "Enter the recipe name:",
        placeholder="e.g., Chocolate Cake, Spaghetti Carbonara, etc."  # Placeholder for recipe name input
    )

    # Language selection
    language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

    # Custom CSS to make the button full width
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Generate Recipe"):
        if recipe_name:
            if not st.session_state.gemini_api_key:
                st.warning("Please enter your Gemini API key.")
            else:
                recipe_post = generate_recipe_post_gemini(recipe_name, language)
                if recipe_post:
                    st.subheader("Generated Recipe Post:")
                    st.write(recipe_post)

                    # Add space between recipe and MidJourney prompts
                    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

                    # Generate MidJourney Prompt (Version 1)
                    midjourney_prompt_v1 = generate_midjourney_prompt_v1(recipe_name)
                    st.subheader("MidJourney Prompt (Version 1):")
                    st.code(midjourney_prompt_v1, language="text")

                    # Copy to Clipboard Button for Version 1
                    st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText(`{midjourney_prompt_v1}`)" style="margin-top: 10px;">
                            Copy MidJourney Prompt (Version 1) to Clipboard
                        </button>
                    """, unsafe_allow_html=True)

                    # Generate MidJourney Prompt (Version 2)
                    midjourney_prompt_v2 = generate_midjourney_prompt_v2(recipe_name)
                    st.subheader("MidJourney Prompt (Version 2):")
                    st.code(midjourney_prompt_v2, language="text")

                    # Copy to Clipboard Button for Version 2
                    st.markdown(f"""
                        <button onclick="navigator.clipboard.writeText(`{midjourney_prompt_v2}`)" style="margin-top: 10px;">
                            Copy MidJourney Prompt (Version 2) to Clipboard
                        </button>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a recipe name.")

if __name__ == "__main__":
    main()
