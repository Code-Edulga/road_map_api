from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# API Key for OpenAI
api_key = os.getenv("OPENAI_API_KEY")


def generate_road_maps(query: str) -> dict:
    """
    Generates a roadmap based on the query using OpenAI.
    Returns the roadmap as a Python dictionary.
    """
    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4", api_key=api_key)

    # Updated Prompt
    prompt = f"""
    You are an expert in creating structured, step-by-step learning roadmaps to help individuals achieve mastery in specific topics.
    Generate a JSON representation of a **directed learning roadmap** based on the user's query. Ensure the relationships clearly show the order of learning.

    The output should include:
    - `entity1`: The main concept or higher-level topic.
    - `entity2`: The subtopic or concept that depends on `entity1`.
    - `relationship`: Describe the connection (e.g., "prerequisite for", "includes", "builds upon").
    - `priority`: A number indicating the order in which the concepts should be learned, where lower numbers are learned first. No two nodes should have the same priority, and the graph should reflect a clear progression.

    ### Query:
    {query}
    """

    # Generate response from OpenAI
    try:
        response = llm.predict(prompt)
    except Exception as e:
        raise Exception(f"Error interacting with OpenAI: {str(e)}")

    # Parse and clean the JSON response
    try:
        cleaned_response = response.content.strip('```json').strip('```').strip()
        roadmap = json.loads(cleaned_response)
    except Exception as e:
        raise Exception(f"Error parsing OpenAI response: {str(e)}")

    return roadmap


@app.route("/generate-roadmap", methods=["POST"])
def generate_roadmap_endpoint():
    """
    API endpoint to generate a learning roadmap.
    Expects a `query` string in the JSON body of the request.
    """
    data = request.get_json()

    # Validate the request
    if not data or "query" not in data:
        return jsonify({"error": "Query is required."}), 400

    query = data["query"]

    try:
        roadmap = generate_road_maps(query)
        return jsonify({"roadmap": roadmap}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app (for local development)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
