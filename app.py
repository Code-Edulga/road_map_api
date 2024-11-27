from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from typing import Dict
from api.services import generate_roadmap
# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

@app.post("/generate-roadmaps")
async def generate_roadmaps(request: Request):
    return await generate_roadmap(request)
   
# Run the app with uvicorn if executed as a script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
