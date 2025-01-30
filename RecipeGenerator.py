import streamlit as st
import requests
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
def connect_to_google_sheet(sheet_name, json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Use the first sheet
    return sheet

# Function to generate recipe post using Gemini API
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

    # Password check
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password_input = st.text_input("Enter Password:", type="password")
        if password_input:
            if "password" not in st.secrets:
                st.error("Password key is missing in secrets. Please check your secrets configuration.")
            else:
                if password_input == st.secrets["password"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        return

    # Logo container with your logo
    st.markdown(
        '<div class="logo-container">'
        '<img src="https://i.ibb.co/ZpdDQDr2/recipe-generator.png" alt="Recipe Generator Logo">'
        '</div>',
        unsafe_allow_html=True
    )

    # Google Sheets integration
    st.subheader("Google Sheets Integration")
    sheet_name = st.text_input("Enter Google Sheet Name:", placeholder="e.g., My Recipe Sheet")
    json_keyfile = st.text_input("Enter Path to Google Sheets JSON Keyfile:", placeholder="e.g., credentials.json")

    if st.button("Connect to Google Sheet"):
        if sheet_name and json_keyfile:
            try:
                sheet = connect_to_google_sheet(sheet_name, json_keyfile)
                st.session_state.sheet = sheet
                st.success("Connected to Google Sheet successfully!")
            except Exception as e:
                st.error(f"Error connecting to Google Sheet: {e}")
        else:
            st.warning("Please enter both the sheet name and JSON keyfile path.")

    if 'sheet' in st.session_state:
        sheet = st.session_state.sheet
        recipe_names = sheet.col_values(1)  # Read recipe names from the first column

        if st.button("Generate Recipes and Update Sheet"):
            for i, recipe_name in enumerate(recipe_names[1:], start=2):  # Skip header row
                recipe_post = generate_recipe_post_gemini(recipe_name, "🇬🇧 English")  # Default to English
                if recipe_post:
                    sheet.update_cell(i, 2, recipe_post)  # Write output to the second column
                    st.success(f"Generated recipe for '{recipe_name}' and updated the sheet.")
                else:
                    st.error(f"Failed to generate recipe for '{recipe_name}'.")

if __name__ == "__main__":
    main()
