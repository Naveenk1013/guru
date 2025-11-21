from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Guru AI - India's #1 Free CBSE Teacher 🧘‍♂️")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

class Query(BaseModel):
    message: str
    standard: str = "10"
    subject: str = "General"

# Multiple free models with fallback (429-proof!)
FREE_MODELS = [
    " deepseek/deepseek-r1-0528:free "
]

@app.post("/guru")
async def talk_to_guru(query: Query):
    system_prompt = f"Namaste! 🙏 Main Guru hoon – Class {query.standard} CBSE ka sabse powerful AI teacher! Step-by-step reasoning dunga, full explanation Hindi+English mein, examples, diagrams describe karunga aur full motivation bhi! Chalo padhai karte hain! 🚀"

    for model in FREE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query.message}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            reply = response.choices[0].message.content.strip()
            return {"reply": reply}
        except Exception as e:
            continue  # Next model try karo

    return {"reply": "Bhai thodi der baad try karo, sab models busy hain! Main jaldi wapas aaunga 💪"}

@app.get("/")
def home():
    return {"message": "Namaste! Guru AI backend is running 🧘‍♂️ Ready to help students!"}
