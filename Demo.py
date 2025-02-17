import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="here goes api key")

# Set up the page configuration
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Styling for text area */
        .stTextArea textarea {
            font-family: monospace;
            font-size: 16px;
            background-color: #FFFFFF;
            color: #000000;
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #007BFF;
        }

        /* Placeholder text color */
        .stTextArea textarea::placeholder {
            color: #FF4500;
            font-weight: bold;
        }

        /* Button styling */
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }

        /* Left Panel (Sidebar) Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #004080, #007BFF);
            color: white;
            border-right: 4px solid #FFD700;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Right Panel (Detailed Review) */
        .review-box {
            background-color: #F8F9FA;
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid #007BFF;
            color: #000000;
        }

        /* Error Highlight */
        .error-highlight {
            color: red;
            font-weight: bold;
        }

        /* Symbols for sections */
        .symbol {
            font-size: 18px;
            font-weight: bold;
            color: #FF6600;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def review_code(code, detailed_review):
    model = genai.GenerativeModel("gemini-pro")  # Use Gemini model

    # Dynamic prompt based on review toggle
    if detailed_review:
        prompt = f"""
        You are an AI Code Reviewer with expertise in Python programming. Analyze the provided code and generate a **detailed point-wise review**.

        🔴 **Errors & Debugging:**  
        - Highlight **errors in red** and explain how to fix them.  
        
        ✨ **Best Practices:**  
        - Suggest **cleaner and more Pythonic** ways to write the code.  
        
        ✅ **Corrected Code (if necessary):**  
        - Provide a **fixed version** of the code.

        ---
        
        **Python Code for Review:**
        
        ```python
        {code}
        ```

        **Note:** Highlight errors in red and use unique symbols for other sections.
        """
    else:
        prompt = f"""
        You are an AI Code Reviewer. Only return the corrected version of the code with improvements.

        ---
        
        **Python Code for Review:**
        
        ```python
        {code}
        ```
        """

    response = model.generate_content(prompt)  # Generate response
    return response.text  # Extract response text

def main():
    # Sidebar for settings
    with st.sidebar:
        st.title("⚙️ Settings")
        st.markdown("---")
        st.write("### 🔍 How AI Reviews Your Code:")
        st.write("✅ Detects syntax & logical errors.")
        st.write("📝 Suggests best coding practices.")
        st.write("🔎 Provides a corrected version if needed.")

        # Toggle button for detailed review
        detailed_review = st.checkbox("📑 Enable Detailed Review", value=True)

        st.markdown("---")
        st.write("🚀 Developed by Ganesh Kondake")
        st.write("💡 Powered by OpenAI")

    # Main Layout
    st.title("💻 AI Code Reviewer")
    st.write("🔍 Paste your **Python code** below, and let AI analyze it for you!")

    # Code input box
    code = st.text_area(
        "✏️ Enter your Python code here:", 
        placeholder="Write your query here...",
        height=250
    )

    # Review Button
    if st.button("🚀 Review My Code"):
        if code.strip():
            with st.spinner("Analyzing your code... 🔄"):
                review = review_code(code, detailed_review)

            if review:
                st.subheader("✅ Review Results")
                st.success("Your code has been analyzed successfully!")

                if detailed_review:
                    st.markdown('<div class="review-box">📋 **AI Review & Suggestions**</div>', unsafe_allow_html=True)
                else:
                    st.markdown("### ✨ **Corrected Code Only**")

                st.code(review, language="markdown")
        else:
            st.warning("⚠️ Please enter some Python code to review.")

if __name__ == "__main__":
    main()
