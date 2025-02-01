import streamlit as st
import requests
import pandas as pd

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
SEGMIND_API_URL = "https://api.segmind.com/v1/recraft-v3"  # Segmind API URL

# Language options for recipes
LANGUAGES = {
    "🇬🇧 English": "Generate a detailed recipe post in English in the following structured format:",
    "🇪🇸 Spanish": "Genera una publicación detallada de una receta en español en el siguiente formato estructurado:",
    "🇩🇪 German": "Erstellen Sie einen detaillierten Rezeptbeitrag auf Deutsch im folgenden strukturierten Format:",
    "🇫🇷 French": "Générez une publication détaillée de recette en français dans le format structuré suivant:",
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
    "cocktail": "🍹"
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
        prompt += ("Ingredients:\n\n"
                   "- [Ingredient 1]\n"
                   "- [Ingredient 2]\n\n"
                   "- [Ingredient 1]\n"
                   "- [Ingredient 2]\n\n"
                   + ("Directions:\n\n"
                      + "\n".join([f"{i+1}. [Step {i+1}]" for i in range(2)]) + "\n\n"
                      + ("Nutritional Information:\n\n"
                         + f"⏰ Prep Time: [Time] | Cooking Time: [Time] | Total Time: [Time]\n"
                         + f"🔥 Kcal: [Calories] | 🍽️ Servings: [Servings]")))

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{prompt}\n\n{recipe_name_or_text}"
                }]
            }]
        }

        params = {
            'key': st.session_state.gemini_api_key
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

# Function to process a CSV file and generate recipes
def process_csv(file_path, language):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Check if the required column exists
    if 'recipe_name' not in df.columns:
        st.error("The CSV file must contain a 'recipe_name' column.")
        return None

    # Initialize an empty list to store results
    results = []

    # Process each recipe name
    for recipe_name in df['recipe_name']:
        recipe_post = generate_recipe_post_gemini(recipe_name, language)
        if recipe_post:
            midjourney_prompt_v1 = generate_midjourney_prompt_v1(recipe_name)
            midjourney_prompt_v2 = generate_midjourney_prompt_v2(recipe_name)
            results.append({
                'recipe_name': recipe_name,
                'generated_recipe': recipe_post,
                'midjourney_prompt_v1': midjourney_prompt_v1,
                'midjourney_prompt_v2': midjourney_prompt_v2
            })

    # Convert results to a DataFrame
    output_df = pd.DataFrame(results)
    return output_df

# Streamlit app main function
def main():
    
   # Sidebar for logo and API key input
   st.sidebar.title("Navigation")
   st.sidebar.markdown(
       '<div class="logo-container">'
       '<img src="https://raw.githubusercontent.com/hassanelb22/RecipesGenerator/refs/heads/main/assets/recipe-generator.png" alt="Recipe Generator Logo" style="max-width: 300px;">'
       '</div>',
       unsafe_allow_html=True
   )

   # API Key Input in Sidebar
   st.sidebar.subheader("API Key")
   api_key = st.sidebar.text_input("Google GEMINI API Key", type="password")
   
   # Store API key in session state for later use
   if api_key:
       st.session_state.gemini_api_key = api_key

   # Custom CSS for styling (optional)
   st.markdown("""
       <style>
       .logo-container {
           display: flex;
           justify-content: center;
           align-items: center;
           margin-bottom: 20px;
       }
       </style>
   """, unsafe_allow_html=True)

   # Password check (if needed)
   if 'authenticated' not in st.session_state:
       st.session_state.authenticated = False

   if not st.session_state.authenticated:
       if 'password' not in st.secrets:
           st.error("Password key is missing in secrets. Please check your secrets configuration.")
       else:
           if st.secrets["password"]:
               st.session_state.authenticated = True
               st.rerun()
           else:
               st.error("Incorrect password. Please try again.")
       return

   # Main content goes here...
   st.title("Recipe Generator")
   # Add further functionality as needed...

if __name__ == "__main__":
   main()
