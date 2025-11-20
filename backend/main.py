from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Guru AI - Your Personal Study Guru")

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

@app.post("/guru")
async def talk_to_guru(query: Query):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",   # ← OFFICIAL DEEPSEEK R1 FREE (o1 LEVEL!)
            messages=[
                {"role": "system", "content": f"Namaste! 🙏 Main Guru hoon – Class {query.standard} CBSE ka sabse powerful AI teacher! Step-by-step reasoning dunga, full explanation Hindi+English mein, examples, diagram describe karunga aur motivate bhi karunga. Chalo padhai karte hain! 🚀"},
                {"role": "user", "content": query.message}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    
    except Exception as e:
        return {"reply": f"Error aa gaya bhai: {str(e)} – ek baar server restart kar do!"}

@app.get("/")
def home():
    return {"message": "Namaste! Guru AI backend is running 🧘‍♂️ Ready to help students!"}