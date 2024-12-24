import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face API token and model URL
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"

# Authorization headers
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"
}

def generate_response(user_message, company_name="GMS Solar"):
    """
    Generate a response from the Hugging Face model acting as a solar appointment setter.
    """
    prompt = f"""
    You are an appointment setter for {company_name}.
    Your job is to handle objections like "not interested" or "too expensive" and guide the user to schedule a free consultation.
    Be polite, professional, and persuasive.
    
    User: {user_message}
    AI:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_length": 200,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)

        # Debug the full response
        print("DEBUG: Full API Response:", response.json())

        # Handle possible errors
        if response.status_code == 503:
            return "The model is loading. Please try again in a moment."
        elif response.status_code != 200:
            return f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}"

        # Parse the response
        result = response.json()
        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        elif isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No valid response generated.")
        return "No valid response generated."
    except Exception as e:
        return f"Exception occurred: {str(e)}"

if __name__ == "__main__":
    print("Solar Appointment Setter Chat! Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        ai_response = generate_response(user_input)
        print(f"AI: {ai_response}")
