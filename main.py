import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Error: GROQ_API_KEY not found. Please set it in a .env file.")
    st.stop()

st.title("💰 AI Financial Planner (Powered by Groq)")
st.markdown("**Disclaimer**: This app provides general financial guidance. Consult a certified financial advisor for personalized advice.")

# Input fields
income = st.number_input("Monthly Income (₹)", min_value=0.0, step=100.0)
expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, step=100.0)
savings = st.number_input("Current Savings (₹)", min_value=0.0, step=100.0)
goal_name = st.text_input("Financial Goal (e.g., Buy a car)", max_chars=50)
goal_amount = st.number_input("Goal Amount (₹)", min_value=0.0, step=100.0)
months = st.slider("Time to achieve goal (months)", 1, 36, 12)

# Expense breakdown
st.subheader("Expense Breakdown (Optional)")
rent = st.number_input("Rent/Mortgage (₹)", min_value=0.0, step=50.0)
groceries = st.number_input("Groceries (₹)", min_value=0.0, step=50.0)
entertainment = st.number_input("Entertainment (₹)", min_value=0.0, step=50.0)
other = st.number_input("Other (₹)", min_value=0.0, step=50.0)

if st.button("Generate Plan"):
    # Input validation
    if goal_name.strip() == "":
        st.error("Error: Please enter a valid financial goal.")
        st.stop()
    
    total_expenses = rent + groceries + entertainment + other
    if total_expenses > 0:
        expenses = total_expenses
    
    # Feasibility check
    disposable_income = income - expenses
    required_monthly_savings = (goal_amount - savings) / months
    if disposable_income < required_monthly_savings + 500:
        st.warning(f"Warning: Your disposable income (₹{disposable_income}) is insufficient. Consider adjustments.")
    
    # Prompt
    prompt = f"""
    You are an expert financial advisor. Create a detailed monthly savings plan for a user with:
    - Monthly income: ₹{income}
    - Monthly expenses: ₹{expenses}
    - Current savings: ₹{savings}
    - Goal: Save ₹{goal_amount} for '{goal_name}' in {months} months
    {(f'Expense breakdown: Rent/Mortgage: ₹{rent}, Groceries: ₹{groceries}, Entertainment: ₹{entertainment}, Other: ₹{other}' if total_expenses > 0 else '')}

    Requirements:
    1. Maintain a ₹500 emergency buffer.
    2. Calculate monthly savings needed.
    3. If unfeasible, suggest adjustments.
    4. Provide two actionable strategies to optimize savings.
    5. Include a monthly breakdown.
    6. Suggest low-risk investment options if applicable.
    """
    
    @st.cache_data
    def get_financial_plan(prompt):
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application W/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful AI financial advisor."},
                {"role": "user", "content": prompt}
            ]
        }
        return requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    
    with st.spinner("Thinking..."):
        response = get_financial_plan(prompt)
        if response.status_code == 200:
            result = response.json()
            plan = result["choices"][0]["message"]["content"]
            st.success("Here’s your plan:")
            st.markdown(plan)
            
            # Savings progress chart
            months_range = list(range(1, months + 1))
            savings_progress = [savings + (goal_amount - savings) / months * i for i in months_range]
            df = pd.DataFrame({"Month": months_range, "Savings": savings_progress})
            fig = px.line(df, x="Month", y="Savings", title=f"Savings Progress for {goal_name}")
            st.plotly_chart(fig)
            
            # Download plan
            st.download_button(
                label="Download Plan as Text",
                data=plan,
                file_name="financial_plan.txt",
                mime="text/plain"
            )
        elif response.status_code == 429:
            st.error("Rate limit exceeded. Please try again later or check your Groq API quota.")
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)