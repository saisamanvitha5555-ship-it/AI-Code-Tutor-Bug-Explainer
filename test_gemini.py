from google import genai
from dotenv import load_dotenv
import os

print("===================================")
print(" GEMINI CONNECTION TEST ")
print("===================================")

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

print("API Key Found:", bool(api_key))

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    exit()

try:
    # Create Gemini client
    client = genai.Client(api_key=api_key)

    print("Gemini client created.")
    print("Sending request to Gemini...")
    print("Please wait...")

    # Use the current Interactions API
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input="Say hello in one short sentence."
    )

    print()
    print("===================================")
    print(" RESPONSE RECEIVED ")
    print("===================================")

    print(interaction.output_text)

    print()
    print("===================================")
    print(" GEMINI CONNECTION SUCCESSFUL ")
    print("===================================")

except Exception as e:

    print()
    print("===================================")
    print(" ERROR ")
    print("===================================")

    print("Error type:", type(e).__name__)
    print("Error message:", str(e))