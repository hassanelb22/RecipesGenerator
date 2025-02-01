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
            "key": st.session_state.get("gemini_api_key", "")
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
            "key": st.session_state.get("gemini_api_key", "")
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
            "x-api-key": st.session_state.get("segmind_api_key", ""),
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "size": "1024x1024",  # Image size
            "style": "any"  # Style of the image
        }
        
        response = requests.post(SEGMIND_API_URL, headers=headers, json=payload)
        
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

    # Navigation bar in the sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode", ["Generate Recipe", "SEO-Optimized Article Generator", "Recipe Generator from CSV", "Generate Images with Segmind"])

    # JavaScript to load API keys from localStorage
    st.markdown("""
        <script>
        // Load API keys from localStorage when the page loads
        function loadApiKeys() {
            const geminiApiKey = localStorage.getItem("gemini_api_key");
            const segmindApiKey = localStorage.getItem("segmind_api_key");
            if (geminiApiKey) {
                document.getElementById("gemini_api_key").value = geminiApiKey;
            }
            if (segmindApiKey) {
                document.getElementById("segmind_api_key").value = segmindApiKey;
            }
        }
        window.onload = loadApiKeys;

        // Save API keys to localStorage when the input changes
        function saveApiKey(key, value) {
            localStorage.setItem(key, value);
        }
        </script>
    """, unsafe_allow_html=True)

    # API Key Input in the Sidebar
    st.sidebar.markdown("### API Keys")
    gemini_api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        value="",
        key="gemini_api_key",
        on_change=None,
        placeholder="Enter your Google API key"
    )

    segmind_api_key = st.sidebar.text_input(
        "Segmind API Key",
        type="password",
        value="",
        key="segmind_api_key",
        on_change=None,
        placeholder="Enter your Segmind API key"
    )

    # Save API keys to localStorage and session state when the user inputs them
    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key
        st.markdown(f"""
            <script>
            saveApiKey("gemini_api_key", "{gemini_api_key}");
            </script>
        """, unsafe_allow_html=True)

    if segmind_api_key:
        st.session_state.segmind_api_key = segmind_api_key
        st.markdown(f"""
            <script>
            saveApiKey("segmind_api_key", "{segmind_api_key}");
            </script>
        """, unsafe_allow_html=True)

    # Rest of the code remains the same...
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

    elif app_mode == "SEO-Optimized Article Generator":
        # Focus Keyword Input
        focus_keyword = st.text_input(
            "Enter the focus keyword for the article:",
            placeholder="e.g., Healthy Eating Habits, Digital Marketing Trends, etc."
        )

        if st.button("Generate SEO-Optimized Article"):
            if focus_keyword:
                if 'gemini_api_key' not in st.session_state:
                    st.warning("Please enter your Gemini API key.")
                else:
                    # Step 1: Generate Meta Titles
                    st.subheader("Meta Titles")
                    meta_titles = generate_meta_titles(focus_keyword)
                    if meta_titles:
                        st.write(meta_titles)

                    # Step 2: Generate Meta Descriptions
                    st.subheader("Meta Descriptions")
                    meta_descriptions = generate_meta_descriptions(meta_titles.split("\n")[0], focus_keyword)
                    if meta_descriptions:
                        st.write(meta_descriptions)

                    # Step 3: Generate Outline
                    st.subheader("Article Outline")
                    outline = generate_outline(meta_titles.split("\n")[0], focus_keyword)
                    if outline:
                        st.write(outline)

                    # Step 4: Generate Article Content
                    st.subheader("Article Content")
                    article_content = generate_article_content(outline, focus_keyword)
                    if article_content:
                        st.write(article_content)

                    # Step 5: Generate Recipe Schema Markup
                    st.subheader("Recipe Schema Markup")
                    recipe_schema = generate_recipe_schema(focus_keyword)
                    if recipe_schema:
                        st.write(recipe_schema)
            else:
                st.warning("Please enter a focus keyword.")

    elif app_mode == "Recipe Generator from CSV":
        st.title("Recipe Generator from CSV")

        # Upload CSV file
        uploaded_file = st.file_uploader("Upload a CSV file with recipe names", type=["csv"])
        
        # Language selection
        language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

        if uploaded_file is not None and 'gemini_api_key' in st.session_state:
            # Process the CSV file
            output_df = process_csv(uploaded_file, language, st.session_state.gemini_api_key)
            
            if output_df is not None:
                # Display the results
                st.write("Generated Recipes:")
                st.dataframe(output_df)
                
                # Download the results as a CSV file
                csv = output_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Output CSV",
                    data=csv,
                    file_name="generated_recipes.csv",
                    mime="text/csv"
                )

    elif app_mode == "Generate Images with Segmind":
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
