import json
import os
from openai import OpenAI
from config import COMPLETION_MODEL, MATCHING_SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def call_matching_api(portfolio2_property, portfolio1_candidates):

    messages = [
        {
            "role": "system", 
            "content": MATCHING_SYSTEM_PROMPT
        },
        {
            "role": "user", 
            "content": json.dumps({
                "portfolio2": {
                    "id": portfolio2_property["id"], 
                    "description": portfolio2_property["description"],
                    "limit": portfolio2_property.get("limit"),
                    "mortgageAmount": portfolio2_property.get("mortgageAmount")
                },
                "portfolio1_candidates": [
                    {
                        "id": candidate["id"], 
                        "description": candidate["description"],
                        "limit": candidate.get("limit"),
                        "mortgageAmount": candidate.get("mortgageAmount")
                    } for candidate in portfolio1_candidates
                ]
            })
        }
    ]

    try:
        response = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        matched_data = json.loads(content)
        return matched_data
    except Exception as e:
        print(f"API call failed: {e}")
    return None