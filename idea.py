import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

model = ChatOpenAI(temperature=0)

class Idea(BaseModel):
    one_line_summary: str = Field(description="One-line summary of the idea.")
    pros: List[str] = Field(description="Five reasons this idea would work in 2026.")
    cons: List[str] = Field(description="Five reasons this idea might not work in 2026.")
    competition: List[str] = Field(description="Three competing companies.")
    will_work_or_not: str = Field(description="Analyze the idea realistically and do not overestimate success. Consider current tech trends, market size, and practicality, Chances this idea will work then give a percentage, add % sign after number.") 

structured_model = model.with_structured_output(Idea, method="function_calling")

st.set_page_config(page_title="Startup Idea Analyzer", page_icon="🚀")

# Sidebar with detailed description
st.sidebar.title("About This App")
st.sidebar.write("""
Welcome to the **AI-Powered Startup Idea Analyzer**!

This app allows you to paste your startup or product idea and get a detailed, AI-generated evaluation including:

- A concise one-line summary  
- Five pros explaining why your idea could succeed  
- Five cons highlighting potential challenges  
- Top 3 competitors in the market  
- An estimated success probability percentage  

Leverage the power of AI to validate your ideas, understand the competition, and get fast, structured feedback to help you innovate smarter!

Built using LangChain, OpenAI GPT models, Pydantic for schema validation, and Streamlit for an interactive web experience.
""")

st.title("🚀 Startup Idea Analyzer")
st.write("""
Paste your startup or product idea below and receive a detailed, AI-generated analysis.
""")

idea_input = st.text_area("🧠 Enter your startup idea here", height=250)

if st.button("Analyze Idea"):
    if not idea_input.strip():
        st.warning("Please enter an idea before clicking Analyze.")
    else:
        with st.spinner("Analyzing your idea..."):
            try:
                result = structured_model.invoke(idea_input)
                st.subheader("📌 One-Line Summary")
                st.success(result.one_line_summary)

                st.subheader("✅ Pros (Why it could work in 2026)")
                for i, pro in enumerate(result.pros, 1):
                    st.markdown(f"{i}. {pro}")

                st.subheader("❌ Cons (Why it might not work in 2026)")
                for i, con in enumerate(result.cons, 1):
                    st.markdown(f"{i}. {con}")

                st.subheader("🏢 Competition")
                for competitor in result.competition:
                    st.markdown(f"- {competitor}")

                st.subheader("📊 Will it work?")
                st.success(f"Chance of success: **{result.will_work_or_not}**")

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
