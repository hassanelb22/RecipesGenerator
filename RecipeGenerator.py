import streamlit as st
import requests

# API configurations
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

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

# Streamlit app
def main():
    st.title("SEO-Optimized Article Generator")

    # API Key Input
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ""
    gemini_api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key

    # Focus Keyword Input
    focus_keyword = st.text_input("Enter the focus keyword for the article:")

    if st.button("Generate Article"):
        if not focus_keyword:
            st.warning("Please enter a focus keyword.")
        elif not st.session_state.gemini_api_key:
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

if __name__ == "__main__":
    main()
