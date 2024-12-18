from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import  Request
from typing import Dict

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

async def generate_roadmap(request: Request):
    """
    API endpoint to generate learning roadmaps.
    """
    data = await request.json()
    json_input = data.get("json", {})

    prompt = f"""
        Given a json with the following template

        interface NestedTopic {{
            title?: string;
            topic?: string;
            definition?: {{
                title?: string;
                topics?: NestedTopic[];
            }};
            topics?: NestedTopic[];
        }}

        Create a roadmap of learning that considers the order of learning the concepts in json, consider the pedagogical aspects and fill important gaps if there is.
        Output is ONLY a list, with nothing else.

        Response: 
        ["learning1", "learning2", "learning3"....]

        ### json:
        {json_input}
    """

    # Call OpenAI API
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )
        cleaned_response = chat_completion.choices[0].message.content.strip()
        roadmap = eval(cleaned_response)

        return {"roadmap": roadmap}

    except Exception as e:
        return {"error": str(e)}