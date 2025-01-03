import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")

# Configure the generative AI model
genai.configure(api_key=BARD_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def main():
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for inputs
    st.sidebar.header("Enter your details")

    # Input fields
    fasting_sugar = st.sidebar.number_input("Fasting Sugar Level (mg/dL)", min_value=0, step=1)
    pre_food_sugar = st.sidebar.number_input("Pre-Food Sugar Level (mg/dL)", min_value=0, step=1)
    post_food_sugar = st.sidebar.number_input("Post-Food Sugar Level (mg/dL)", min_value=0, step=1)
    food_type = st.sidebar.selectbox(
        "Type of Food Consumed",
        ["Select", "Vegetarian", "Fast Food", "Mixed", "Other"]
    )

    # Checkbox to confirm input accuracy
    confirm_info = st.sidebar.checkbox("I confirm that the information provided is accurate.")

    # Submit button
    submit = st.sidebar.button("Submit")

    # Main area title
    st.title("Diabetes Diet Recommendation System")

    if submit:
        if not confirm_info:
            st.error("Please confirm the information by checking the box.")
        elif food_type == "Select":
            st.error("Please select a valid food type.")
        else:
            # Processing placeholder
            st.info("Processing your details...")

            # Call the Bard API with the inputs
            bard_response = process_with_bard_api(fasting_sugar, pre_food_sugar, post_food_sugar, food_type)

            # Save interaction to chat history with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chat_history.append({
                "timestamp": timestamp,
                "user": f"Fasting Sugar Level: {fasting_sugar} mg/dL\n"
                        f"Pre-Food Sugar Level: {pre_food_sugar} mg/dL\n"
                        f"Post-Food Sugar Level: {post_food_sugar} mg/dL\n"
                        f"Food Type: {food_type}",
                "bard": bard_response
            })

            # Display the chat history
            display_chat_history()

def process_with_bard_api(fasting_sugar, pre_food_sugar, post_food_sugar, food_type):
    if not BARD_API_KEY:
        return "API key is missing. Please check your configuration."

    # Generate content using the configured model
    try:
        prompt = (f"Based on the following details, provide a diet recommendation:\n"
                  f"Fasting Sugar Level: {fasting_sugar} mg/dL\n"
                  f"Pre-Food Sugar Level: {pre_food_sugar} mg/dL\n"
                  f"Post-Food Sugar Level: {post_food_sugar} mg/dL\n"
                  f"Food Type: {food_type}")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def display_chat_history():
    """Display the saved chat history in reverse order with timestamps and separation."""
    
    # Loop through chat history in reverse order (newest first)
    for interaction in reversed(st.session_state.chat_history):
        timestamp = interaction["timestamp"]
        
        # User message style
        user_style = f"""
            <div style="background-color:#555; color: white; padding: 10px; border-radius: 10px; margin-bottom: 6px;">
                <h4 style=" color: #000;"><strong>You:</strong> <span style="font-size: 15px; color: #000;">({timestamp})</span></h4>
                {interaction["user"].replace('\n', '<br>')}
            </div>
        """
        
        # Bard response style
        bard_style = f"""
            <div style="background-color: #555; color: white; padding: 10px; border-radius: 10px; margin-bottom: 6px;">
                <h4 style=" color: #000;"><strong>Bard Suggestions:</strong></h4>
                {interaction["bard"]}
            
        """
        
        # Separation line
        separator = "<hr style='border: 1px solid #333; margin: 10px 0;'>"

        # Display user message, Bard response, and separator
        st.markdown(user_style, unsafe_allow_html=True)
        st.markdown(bard_style, unsafe_allow_html=True)
        st.markdown(separator, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
