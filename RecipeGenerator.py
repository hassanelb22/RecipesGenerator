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

# Function to process a CSV file and generate recipes
def process_csv(file_path, language, api_key):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Check if the required column exists
    if "recipe_name" not in df.columns:
        st.error("The CSV file must contain a 'recipe_name' column.")
        return None
    
    # Initialize an empty list to store results
    results = []
    
    # Process each recipe name
    for recipe_name in df["recipe_name"]:
        recipe_post = generate_recipe_post_gemini(recipe_name, language)
        if recipe_post:
            # Remove *** from the generated recipe text
            recipe_post = recipe_post.replace("***", "")
            
            midjourney_prompt_v1 = generate_midjourney_prompt_v1(recipe_name)
            midjourney_prompt_v2 = generate_midjourney_prompt_v2(recipe_name)
            results.append({
                "recipe_name": recipe_name,
                "generated_recipe": recipe_post,  # Use the cleaned text
                "midjourney_prompt_v1": midjourney_prompt_v1,
                "midjourney_prompt_v2": midjourney_prompt_v2
            })
    
    # Convert results to a DataFrame
    output_df = pd.DataFrame(results)
    return output_df

# Function to generate content using Gemini API
def generate_content(prompt):
    try:
        headers = {
            "Content-Type": "application/json"
        }
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
            return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        else:
            st.error(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Function to generate meta titles
def generate_meta_titles(focus_keyword):
    prompt = f"""
    You are an expert copywriter who writes catchy, SEO-friendly blog titles in a friendly tone. Follow these rules:
    1. Write 10 titles for "{focus_keyword}" using the exact phrase "{focus_keyword}".
    2. Keep titles under 65 characters.
    3. Make sure the focus keyword appears at the beginning of the title.
    4. Use hooks like "How," "Why," or "Best" to spark curiosity.
    5. Mix formats: listicles, questions, and how-tos.
    6. Avoid quotes, markdown, or self-references.
    7. Prioritize SEO keywords related to "{focus_keyword}".
    8. Title should contain a number.
    """
    return generate_content(prompt)

# Function to generate meta descriptions
def generate_meta_descriptions(meta_title, focus_keyword):
    prompt = f"""
    You are an SEO-savvy content strategist who writes compelling blog descriptions. Follow these rules:
    1. Write 10 descriptions for the blog post titled "{meta_title}".
    2. Use the exact phrase "{focus_keyword}" naturally in each description.
    3. Keep descriptions under 160 characters (ideal for SEO).
    4. Start with a hook: ask a question, use action verbs, or highlight a pain point.
    5. Include SEO keywords related to "{focus_keyword}" and address user intent (e.g., tips, solutions).
    6. End with a subtle CTA like *Discover, Learn, Try*.
    7. Avoid quotes, markdown, or self-references.
    8. Maintain a friendly, conversational tone.
    """
    return generate_content(prompt)

# Function to generate a detailed outline
def generate_outline(meta_title, focus_keyword):
    prompt = f"""
    Act as a professional Copywriter and SEO specialist. Write an outline for a WordPress blog post based on "{meta_title}" using "{focus_keyword}" as a focus keyword. Don’t include title and description in your results and make sure you use proper heading structure.
    """
    return generate_content(prompt)

# Function to generate content based on the outline
def generate_article_content(outline, focus_keyword):
    prompt = f"""
    You are a professional Copywriter and SEO specialist. Write the content of this outline that I will provide you in this prompt and you need to follow the exact Instructions below:
    Instructions:
    1. Focus keyword: "{focus_keyword}"
    2. Content length: 1200 words.
    3. Tone: Friendly, engaging, and easy to read (4th-grade reading level).
    4. Structure: Follow the blog outline provided. Use headings and subheadings with the focus keyword naturally integrated.
    5. SEO:
       - Include the focus keyword in the first 100 words, headings, and 2-3 times per 300 words.
       - Add related keywords where relevant.
    6. Audience: Write for readers who are interested in "{focus_keyword}".
    7. Formatting:
       ○ Use detailed paragraphs.
       ○ Include bullet points, lists, or numbered steps if necessary.
       ○ End with a strong call-to-action.
    8. Additional Notes: Keep the content conversational and engaging. Avoid fluff or overly technical language.
    Blog Outline:
    {outline}
    """
    return generate_content(prompt)

# Function to generate recipe schema markup
def generate_recipe_schema(recipe_name):
    prompt = f"""
    Give me these info for "{recipe_name}":
    Preparation Time: ISO 8601 duration format.
    Cooking Time: ISO 8601 duration format.
    Total Time: ISO 8601 duration format.
    Type of recipe: Type of dish, for example appetizer, or dessert.
    Cuisine: The cuisine of the recipe.
    Keywords: Other terms for your recipe such as the season, the holiday, or other descriptors. Separate multiple entries with commas.
    Recipe Yield: Quantity produced by the recipe.
    Calories: The number of calories in the recipes.
    Recipe Ingredients: List all ingredients.
    Pros: Use this section only for editorial reviews. Positive notes, add one item per line.
    Cons: Negative notes, add one item per line.
    Recipe Instructions: Provide detailed instructions.
    """
    return generate_content(prompt)

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
        
        response = requests.post(SEGMIND_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            if response.headers.get("Content-Type", "").startswith("image/"):
                return response.content
            else:
                response_json = response.json()
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
    # Custom CSS for the carousel
    st.markdown("""
        <style>
        .carousel {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 10px;
            padding: 10px;
        }
        .carousel-item {
            flex: 0 0 auto;
            scroll-snap-align: start;
            width: 300px;
            height: 200px;
            background-color: #f0f0f0;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: #333;
        }
        .carousel-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Carousel HTML
    carousel_html = """
    <div class="carousel">
        <div class="carousel-item">
            <img src="https://via.placeholder.com/300x200" alt="Image 1">
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/300x200" alt="Image 2">
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/300x200" alt="Image 3">
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/300x200" alt="Image 4">
        </div>
        <div class="carousel-item">
            <img src="https://via.placeholder.com/300x200" alt="Image 5">
        </div>
    </div>
    """

    # Display the carousel
    st.title("Recipe Carousel")
    st.markdown(carousel_html, unsafe_allow_html=True)

    # Rest of your existing code...
    # (Keep the rest of your script as it is, including the API configurations, functions, and main logic)

if __name__ == "__main__":
    main()
