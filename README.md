# AI-Financial-Supporter

A Streamlit app powered by [Groq](https://x.ai/) to help users create personalized financial plans. Input your monthly income, expenses, savings, and financial goals, and the app generates a detailed savings plan with actionable advice, ensuring a $500 emergency buffer.

## Features
- **Personalized Financial Plans**: Generate monthly savings plans based on your income, expenses, and goals.
- **Emergency Buffer**: Ensures a $500 buffer for unexpected expenses.
- **Actionable Advice**: Provides strategies to optimize savings (e.g., reduce discretionary spending).
- **Visualizations**: Includes charts to track savings progress over time.
- **Secure**: API keys are managed securely using `.env` (not tracked in Git).

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Groq API (`llama-3.3-70b-versatile` model)
- **Language**: Python
- **Dependencies**: `streamlit`, `requests`, `python-dotenv`, `plotly`

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aryannegi14/AI-Financial-Supporter.git
   cd AI-Financial-Supporter
