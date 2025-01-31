import streamlit as st
import requests
from datetime import datetime

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Language options for recipes
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez una publicación detallada de recette en français dans le format structuré suivant:",
    "🇸🇦 Arabic": "قم بإنشاء منشور وصفة تفصيلي باللغة العربية بالتنسيق المنظم التالي:"
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

# Function to generate an SEO-optimized article using Gemini API
def generate_seo_article_gemini(topic, language):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        prompt = f"Generate an SEO-optimized article in {language} on the topic: {topic}. Include relevant keywords, headings, and a conclusion."
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
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
        st.error(f"Error generating SEO article with Gemini: {e}")
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
    # Custom CSS to center the logo and handle RTL for Arabic
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
        .rtl-text {
            direction: rtl;
            text-align: right;
            font-weight: 400;
            font-family: 'Almarai', serif;
        }
        .facebook-post {
            margin-bottom: 30px;
        }
        .facebook-post-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        .facebook-post-header img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .facebook-post-header .post-info {
            display: flex;
            flex-direction: column;
        }
        .facebook-post-header .post-info .page-name {
            font-weight: bold;
            font-size: 16px;
            display: flex;
            align-items: center;
        }
        .facebook-post-header .post-info .post-time {
            font-size: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Password check
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        if "password" not in st.secrets:
            st.error("Password key is missing in secrets. Please check your secrets configuration.")
        else:
            if st.secrets["password"]:
                st.session_state.authenticated = True
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
            else:
                st.error("Incorrect password. Please try again.")
        return

    # Logo container with your logo
    st.markdown(
        '<div class="logo-container">'
        '<img src="https://raw.githubusercontent.com/hassanelb22/RecipesGenerator/refs/heads/main/assets/recipe-generator.png" alt="Recipe Generator Logo">'
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

    # JavaScript to load API key from localStorage
    st.markdown("""
        <script>
        // Load API key from localStorage when the page loads
        function loadApiKey() {
            const apiKey = localStorage.getItem("gemini_api_key");
            if (apiKey) {
                document.getElementById("apiKey").value = apiKey;
            }
        }
        window.onload = loadApiKey;

        // Save API key to localStorage when the input changes
        function saveApiKey() {
            const apiKey = document.getElementById("apiKey").value;
            localStorage.setItem("gemini_api_key", apiKey);
        }
        </script>
    """, unsafe_allow_html=True)

    # API Key Input with placeholder
    gemini_api_key = st.text_input(
        "",  # Empty label since we're using custom HTML above
        type="password",
        value="",
        key="apiKey",
        on_change=None,
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

    # Navigation bar in the sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode", ["Generate Recipe", "Generate SEO Article"])

    if app_mode == "Generate Recipe":
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
                if 'gemini_api_key' not in st.session_state:
                    st.warning("Please enter your Gemini API key.")
                else:
                    recipe_post = generate_recipe_post_gemini(recipe_name, language)
                    if recipe_post:
                        # Facebook-like post styling
                        st.markdown(f"""
        <div class="facebook-post">
            <div class="facebook-post-header">
                <div style="display: flex; align-items: center;">
                    <img src="https://raw.githubusercontent.com/hassanelb22/RecipesGenerator/refs/heads/main/assets/recipe-generator.png" alt="Profile Image">
                    <div class="post-info">
                        <div class="page-name">
                            Recipe Generator
                            <svg viewBox="0 0 12 13" width="12" height="12" fill="#007bff" title="Verified account" style="margin-left: 4px;">
                                <title>Verified account</title>
                                <g fill-rule="evenodd" transform="translate(-98 -917)">
                                    <path d="m106.853 922.354-3.5 3.5a.499.499 0 0 1-.706 0l-1.5-1.5a.5.5 0 1 1 .706-.708l1.147 1.147 3.147-3.147a.5.5 0 1 1 .706.708m3.078 2.295-.589-1.149.588-1.15a.633.633 0 0 0-.219-.82l-1.085-.7-.065-1.287a.627.627 0 0 0-.6-.603l-1.29-.066-.703-1.087a.636.636 0 0 0-.82-.217l-1.148.588-1.15-.588a.631.631 0 0 0-.82.22l-.701 1.085-1.289.065a.626.626 0 0 0-.6.6l-.066 1.29-1.088.702a.634.634 0 0 0-.216.82l.588 1.149-.588 1.15a.632.632 0 0 0 .219.819l1.085.701.065 1.286c.014.33.274.59.6.604l1.29.065.703 1.088c.177.27.53.362.82.216l1.148-.588 1.15.589a.629.629 0 0 0 .82-.22l.701-1.085 1.286-.064a.627.627 0 0 0 .604-.601l.065-1.29 1.088-.703a.633.633 0 0 0 .216-.819"></path>
                                </g>
                            </svg>
                        </div>
                        <div class="post-time">Just now</div>
                    </div>
                </div>
            </div>
            <div class="facebook-post-content">
                {recipe_post}
            </div>
        </div>
                        """, unsafe_allow_html=True)

                        # Add space between recipe and MidJourney prompts
                        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

                        # Generate MidJourney Prompt (Version 1)
                        midjourney_prompt_v1 = generate_midjourney_prompt_v1(recipe_name)
                        st.subheader("MidJourney Prompt (Version 1):")
                        st.code(midjourney_prompt_v1, language="text")

                        # Generate MidJourney Prompt (Version 2)
                        midjourney_prompt_v2 = generate_midjourney_prompt_v2(recipe_name)
                        st.subheader("MidJourney Prompt (Version 2):")
                        st.code(midjourney_prompt_v2, language="text")
            else:
                st.warning("Please enter a recipe name.")

    elif app_mode == "Generate SEO Article":
        # Topic input for SEO article
        topic = st.text_input(
            "Enter the topic for the SEO article:",
            placeholder="e.g., Digital Marketing Trends, Healthy Eating Habits, etc."
        )

        # Language selection for SEO article
        language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

        if st.button("Generate SEO Article"):
            if topic:
                if 'gemini_api_key' not in st.session_state:
                    st.warning("Please enter your Gemini API key.")
                else:
                    seo_article = generate_seo_article_gemini(topic, language)
                    if seo_article:
                        st.subheader("Generated SEO Article:")
                        st.write(seo_article)
            else:
                st.warning("Please enter a topic for the SEO article.")

if __name__ == "__main__":
    main()
