import streamlit as st
import requests
import pandas as pd

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
SEGMIND_API_URL = "https://api.segmind.com/v1/recraft-v3"  # Updated API URL

# Language options for recipes
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detallierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
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
            
            # Remove *** from the generated text
            generated_text = generated_text.replace("***", "")
            
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

# Function to generate images using Segmind API
def generate_segmind_image(prompt):
    try:
        headers = {
            "x-api-key": st.session_state.segmind_api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "size": "1024x1024",  # Image size
            "style": "any"  # Style of the image
        }
        
        # Debug: Print the payload being sent
        st.write("Sending payload to Segmind API:")
        st.write(payload)
        
        response = requests.post(SEGMIND_API_URL, headers=headers, json=payload)
        
        # Debug: Print the response status code and content
        st.write("API Response Status Code:", response.status_code)
        st.write("API Response Content Type:", response.headers.get("Content-Type"))
        st.write("API Response Content (first 100 characters):", response.text[:100])
        
        if response.status_code == 200:
            # Check if the response is an image (binary data)
            if response.headers.get("Content-Type", "").startswith("image/"):
                # The response is an image, so we can display it directly
                st.write("API returned an image.")
                return response.content  # Return the binary image data
            else:
                # The response is JSON or another format
                response_json = response.json()
                st.write("API Response JSON:", response_json)
                
                # Extract the image URL or data from the response
                image_url = response_json.get("data", {}).get("url", "")
                if image_url:
                    return image_url
                else:
                    st.error("No image URL or binary data found in the API response.")
                    return None
        else:
            st.error(f"Segmind API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating image with Segmind: {e}")
        return None

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

    # Custom HTML for Segmind API Key Input Label
    st.markdown("""
        <label class="api-key-label">
            Segmind API Key
            <a href="https://segmind.com/api" target="_blank" rel="noopener noreferrer" class="api-key-link">
                Get your API key here →
            </a>
        </label>
    """, unsafe_allow_html=True)

    # Segmind API Key Input with placeholder
    segmind_api_key = st.text_input(
        "",  # Empty label since we're using custom HTML above
        type="password",
        value="",
        key="segmindApiKey",
        on_change=None,
        placeholder="Enter your Segmind API key"  # Placeholder for API key input
    )

    # Save Segmind API key to localStorage when the user inputs it
    if segmind_api_key:
        st.session_state.segmind_api_key = segmind_api_key
        st.markdown(f"""
            <script>
            localStorage.setItem("segmind_api_key", "{segmind_api_key}");
            </script>
        """, unsafe_allow_html=True)

    # Navigation bar in the sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode", ["Generate Recipe", "SEO-Optimized Article Generator", "Recipe Generator from CSV", "Generate Images with Segmind"])

    if app_mode == "Generate Images with Segmind":
        st.title("Generate Images with Segmind")

        # Prompt input for image generation
        image_prompt = st.text_input(
            "Enter a prompt for the image:",
            placeholder="e.g., A delicious chocolate cake on a table, A bowl of fresh salad, etc."
        )

        if st.button("Generate Image"):
            if image_prompt:
                if 'segmind_api_key' not in st.session_state:
                    st.warning("Please enter your Segmind API key.")
                else:
                    image_data = generate_segmind_image(image_prompt)
                    if image_data:
                        # Check if the image_data is binary or a URL
                        if isinstance(image_data, bytes):
                            # Binary image data
                            st.image(image_data, caption="Generated Image", use_column_width=True)
                        else:
                            # Image URL
                            st.image(image_data, caption="Generated Image", use_column_width=True)
                    else:
                        st.error("Failed to generate image.")
            else:
                st.warning("Please enter a prompt for the image.")

if __name__ == "__main__":
    main()
