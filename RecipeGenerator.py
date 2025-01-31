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
        
        # Step 1: Generate Meta Titles
        meta_title_prompt = f"""
        You are an expert copywriter who writes catchy, SEO-friendly blog titles in a friendly tone. Follow these rules:
        1. Write 10 titles for "{topic}" using the exact phrase "{topic}".
        2. Keep titles under 65 characters.
        3. Make sure the focus keyword appears at the beginning of the title.
        4. Use hooks like "How," "Why," or "Best" to spark curiosity.
        5. Mix formats: listicles, questions, and how-tos.
        6. Avoid quotes, markdown, or self-references.
        7. Prioritize SEO keywords related to "{topic}".
        8. Title should contain a number.
        """
        
        # Step 2: Generate Meta Descriptions
        meta_description_prompt = f"""
        You are an SEO-savvy content strategist who writes compelling blog descriptions. Follow these rules:
        1. Write 10 descriptions for the blog post titled "{topic}".
        2. Use the exact phrase "{topic}" naturally in each description.
        3. Keep descriptions under 160 characters (ideal for SEO).
        4. Start with a hook: ask a question, use action verbs, or highlight a pain point.
        5. Include SEO keywords related to "{topic}" and address user intent (e.g., tips, solutions).
        6. End with a subtle CTA like *Discover, Learn, Try*.
        7. Avoid quotes, markdown, or self-references.
        8. Maintain a friendly, conversational tone.
        """
        
        # Step 3: Create Detailed Outlines
        outline_prompt = f"""
        Act as a professional Copywriter and SEO specialist. Write an outline for a WordPress blog post based on "{topic}" using "{topic}" as a focus keyword. Don’t include title and description in your results and make sure you use proper heading structure.
        """
        
        # Step 4: Write Content Based on Detailed Outlines
        content_prompt = f"""
        You are a professional Copywriter and SEO specialist. Write the content of this outline that I will provide you in this prompt and you need to follow the exact Instructions below:
        Instructions:
        1. Focus keyword: "{topic}"
        2. Content length: 1200 words.
        3. Tone: Friendly, engaging, and easy to read (4th-grade reading level).
        4. Structure: Follow the blog outline provided. Use headings and subheadings with the focus keyword naturally integrated.
        5. SEO:
           - Include the focus keyword in the first 100 words, headings, and 2-3 times per 300 words.
           - Add related keywords where relevant.
        6. Audience: Write for readers who are interested in "{topic}".
        7. Formatting:
           ○ Use detailed paragraphs.
           ○ Include bullet points, lists, or numbered steps if necessary.
           ○ End with a strong call-to-action.
        8. Additional Notes: Keep the content conversational and engaging. Avoid fluff or overly technical language.
        Blog Outline:
        [Insert your blog outline here]
        """
        
        # Step 5: Write Content Based on Custom Prompt
        custom_prompt = f"""
        Act as a professional recipe blogger and SEO specialist. Write a 1,000+ word WordPress blog post for "{topic}" using "{topic}" as a focus keyword. Follow this structure and guidelines strictly:
        Introduction
        Write a 200-word captivating introduction using friendly and simple words for a recipe blog post about "{topic}". Start with a strong hook that highlights the dish’s key qualities (e.g., creamy, flavorful, juicy). Include an interesting anecdote or fun fact about the recipe to grab attention. Describe why this dish is special and why readers should try it, emphasizing its simplicity, quick preparation time, and family-friendly appeal. Compare it briefly to another popular recipe on the blog to establish credibility and encourage readers to explore other content. End with a positive and inviting tone that makes the reader excited to try the recipe.
        What is {topic}?
        Write a conversational and engaging 120-word paragraph about the name of this recipe. Use a lighthearted and humorous tone, incorporating rhetorical questions to pique curiosity about the name’s origin. Add a playful anecdote about why it’s called this and include a classic saying like 'the way to a man’s heart is through his stomach.' End with an encouraging call to action that invites readers to try the recipe.
        Why You’ll Love This {topic}:
        Write a clear and engaging section about this recipe, focusing on three key aspects: the main highlight of the dish, the cost-saving benefits of making it at home, and the flavorful toppings or ingredients that make it special. Use descriptive language to appeal to the reader's senses and create a friendly tone throughout. Include a brief comparison to a related recipe, encouraging readers to explore more content. Ensure the section is well-structured, concise, and ends with a call to action that invites readers to try making the recipe at home.
        How to Make {topic}:
        ● Quick Overview
        Offer a brief preview of what makes this dish easy, delicious, and satisfying. Highlight key features such as its simplicity, taste, and any standout elements like a creamy sauce or rich texture. Also, mention the preparation time to give the reader an idea of how long the recipe will take to make.
        ● Key Ingredients for {topic}:
        List all the ingredients needed to make the recipe. Include a high-quality image showing the ingredients to provide the reader with a clear visual representation of what’s required. Make sure each ingredient is listed clearly, including specific quantities and any special preparations needed.
        ● Step-by-Step Instructions:
        Break down the cooking process into clear, actionable steps with detailed instructions. Ensure each step is easy to follow and includes specific details about the ingredients, techniques, and timing involved. Use simple language and provide enough detail so that someone with minimal cooking experience can successfully complete the recipe.
        What to Serve {topic} With:
        Suggest complementary dishes, sides, or drinks that pair well with the recipe. Provide a few ideas that enhance the main dish and offer variety, considering flavors, textures, and overall meal balance.
        Top Tips for Perfecting {topic}:
        Offer valuable tips to enhance the cooking process or flavor. Include detailed advice on ingredient substitutions, timing adjustments, and common mistakes to avoid. Make sure the tips are practical and helpful for both beginners and experienced cooks.
        Storing and Reheating Tips:
        Provide practical advice on how to store leftovers and how long the dish stays fresh. Include detailed instructions on proper storage methods, such as refrigeration or freezing, and specify how long the dish can be kept. Also, offer guidance on how to reheat the dish for optimal taste or how to freeze it for future meals.
        """
        
        # Step 6: Recipe Schema Markup
        schema_prompt = f"""
        Give me these info for "{topic}":
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
        
        # Combine all prompts into one payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{meta_title_prompt}\n\n{meta_description_prompt}\n\n{outline_prompt}\n\n{content_prompt}\n\n{custom_prompt}\n\n{schema_prompt}"
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
