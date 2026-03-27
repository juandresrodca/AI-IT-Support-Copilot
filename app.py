import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/IT-Engineer/IT-Support-Copilot",
        "X-Title": "AI IT Support Copilot"
    }
)

st.set_page_config(page_title="AI IT Support Copilot")

st.title("🛠️ AI IT Support Copilot")
st.write("Describe your issue and get troubleshooting help instantly.")

issue = st.text_area("Enter the IT issue:")
st.markdown("### 💡 Designed for IT engineers to speed up troubleshooting using AI")
category = st.selectbox(
    "Select category",
    ["General", "Windows", "Network", "M365", "Security"]
)

if st.button("Analyze Issue"):
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error("OpenRouter API Key not found. Please check your .env file.")
    elif issue:
        with st.spinner("Analyzing with OpenRouter..."):
            try:
                prompt = f"""
You are a senior IT Support Engineer.

Analyze the following issue and provide:

1. Likely root cause
2. Step-by-step troubleshooting
3. Commands (if applicable)
4. Suggested resolution

Category: {category}
Issue: {issue}
"""

                response = client.chat.completions.create(
                    model="google/gemini-2.0-flash-lite-preview-02-05:free",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )


                result = response.choices[0].message.content

                st.subheader("🧠 Analysis")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter an issue.")