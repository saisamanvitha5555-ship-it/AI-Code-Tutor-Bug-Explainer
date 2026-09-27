from google import genai
from dotenv import load_dotenv
import os
import time
from pathlib import Path


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. Please check your .env file."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=api_key)


# =========================================================
# COMMON GEMINI FUNCTION
# =========================================================

def generate_ai_response(prompt):

    for attempt in range(3):

        try:
            print("Sending request to Gemini...")

            response = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            return response.output_text

        except Exception as e:

            error_message = str(e)

            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/3)"
            )

            print(error_message)

            if "429" in error_message:

                if (
                    "requests per day" in error_message
                    or "limit: 20" in error_message
                    or "too_many_requests" in error_message
                ):
                    return (
                        "### GEMINI API LIMIT REACHED\n\n"
                        "The Gemini API free-tier daily request "
                        "limit has been reached.\n\n"
                        "Please try again after the daily quota "
                        "resets or use another Gemini API key "
                        "with available quota."
                    )

                if attempt < 2:
                    print("Temporary rate limit detected.")
                    print("Retrying in 3 seconds...")
                    time.sleep(3)
                    continue

            if attempt < 2:
                print("Retrying in 3 seconds...")
                time.sleep(3)

            else:
                return (
                    "### AI SERVICE ERROR\n\n"
                    "The AI service could not process the request.\n\n"
                    f"Error details: {error_message}"
                )

    return (
        "### AI SERVICE ERROR\n\n"
        "Unable to get a response from Gemini."
    )


# =========================================================
# ANALYZE CODE
# =========================================================

def analyze_code(code, language):

    prompt = (
        "You are an expert programming tutor and code reviewer.\n\n"
        "The student is working with " + language + ".\n\n"
        "Analyze the following code.\n\n"
        "CODE:\n\n"
        + code +
        "\n\n"
        "Give the response using exactly these sections:\n\n"

        "### 1. CODE EXPLANATION\n\n"
        "Explain what the code does in very simple, "
        "beginner-friendly language.\n\n"

        "### 2. BUGS AND ERRORS\n\n"
        "Identify syntax errors, logical errors, runtime errors, "
        "or other problems.\n\n"
        "If there are no bugs, clearly say:\n"
        "\"No major bugs found.\"\n\n"

        "### 3. ERROR LINE\n\n"
        "If an error exists, identify the most relevant line number.\n\n"
        "If there is no error, say:\n"
        "\"None\"\n\n"

        "### 4. CORRECTED CODE\n\n"
        "This section is very important.\n\n"
        "Provide the COMPLETE corrected code.\n\n"
        "Put the complete corrected code inside exactly ONE "
        "markdown code block.\n\n"
        "If the original code is already correct, provide the "
        "original code unchanged.\n\n"
        "Do not put explanations inside the code block.\n\n"

        "### 5. COMPLEXITY\n\n"
        "Give:\n"
        "- Time Complexity\n"
        "- Space Complexity\n\n"
        "Explain them simply.\n\n"

        "### 6. IMPROVEMENTS\n\n"
        "Give practical suggestions to improve the code.\n\n"
        "Do not use unnecessary complicated terminology.\n\n"

        "Always provide complete corrected code in the "
        "CORRECTED CODE section."
    )

    return generate_ai_response(prompt)


# =========================================================
# EXPLAIN ERROR
# =========================================================

def explain_error(
    code,
    language,
    error_type,
    error_line,
    error_text
):

    prompt = (
        "You are an expert programming tutor helping "
        "a beginner student.\n\n"

        "The student is working with " + language + ".\n\n"

        "CODE:\n\n"
        + code +
        "\n\n"

        "The program produced the following error.\n\n"

        "ERROR TYPE:\n"
        + str(error_type) +
        "\n\n"

        "ERROR LINE:\n"
        + str(error_line) +
        "\n\n"

        "ERROR MESSAGE:\n"
        + str(error_text) +
        "\n\n"

        "Explain the error in very simple, "
        "beginner-friendly language.\n\n"

        "Use exactly these sections:\n\n"

        "### WHAT IS THE ERROR?\n\n"
        "Explain what the error means.\n\n"

        "### WHY DID IT HAPPEN?\n\n"
        "Explain why the error happened.\n\n"

        "### HOW TO FIX IT\n\n"
        "Explain the solution step by step.\n\n"

        "### CORRECTED CODE\n\n"
        "This section is very important.\n\n"

        "Provide the COMPLETE corrected code.\n\n"

        "Put the complete corrected code inside exactly ONE "
        "markdown code block.\n\n"

        "The corrected code must be complete and directly usable "
        "by the student.\n\n"

        "Do not put explanations inside the code block.\n\n"

        "Do not give complicated explanations."
    )

    return generate_ai_response(prompt)


# =========================================================
# LINE BY LINE EXPLANATION
# =========================================================

def explain_line_by_line(code, language):

    prompt = (
        "You are an expert programming tutor helping "
        "a beginner.\n\n"

        "Explain this " + language + " code line by line.\n\n"

        "CODE:\n\n"
        + code +
        "\n\n"

        "For every important line:\n\n"
        "1. Mention the line number.\n"
        "2. Explain what that line does.\n"
        "3. Explain it in very simple language.\n\n"

        "At the end provide:\n\n"

        "### OVERALL PROGRAM FLOW\n\n"

        "Explain how the complete program works "
        "from beginning to end.\n\n"

        "Avoid unnecessary complicated terminology."
    )

    return generate_ai_response(prompt)


# =========================================================
# AI TUTOR
# =========================================================

def ask_ai_tutor(
    code,
    language,
    question,
    tutor_mode="beginner"
):

    mode_instructions = {

        "beginner":
            "Explain the answer in very simple language "
            "and assume the student is a beginner.",

        "intermediate":
            "Give a clear explanation with moderate "
            "technical detail suitable for an intermediate student.",

        "advanced":
            "Give a technically detailed explanation "
            "suitable for an advanced programming student."

    }

    selected_instruction = mode_instructions.get(
        tutor_mode,
        mode_instructions["beginner"]
    )

    prompt = (
        "You are an AI programming tutor helping "
        "a student learn programming.\n\n"

        "The student is working with " + language + ".\n\n"

        "CURRENT CODE:\n\n"
        + code +
        "\n\n"

        "TUTOR MODE:\n"
        + tutor_mode +
        "\n\n"

        "TUTOR MODE INSTRUCTIONS:\n"
        + selected_instruction +
        "\n\n"

        "STUDENT QUESTION:\n"
        + question +
        "\n\n"

        "Important rules:\n\n"

        "1. Answer the student's actual question.\n\n"

        "2. Keep the explanation clear and easy to understand.\n\n"

        "3. Use examples when they help understanding.\n\n"

        "4. Do not give unrelated information.\n\n"

        "5. If the student asks for corrected code, "
        "provide the complete corrected code.\n\n"

        "6. If there is an error in the code, "
        "explain the error and show how to fix it.\n\n"

        "7. Teach the concept instead of only giving "
        "a short answer.\n\n"

        "8. Use simple headings when useful.\n\n"

        "9. Do not use unnecessarily complicated terminology.\n\n"

        "Respond as a helpful personal programming tutor."
    )

    return generate_ai_response(prompt)
