from flask import Flask, render_template, request, jsonify

from utils.ai_helper import (
    analyze_code,
    explain_error,
    explain_line_by_line,
    ask_ai_tutor
)

from database import (
    save_history,
    create_database,
    get_history,
    delete_history
)

import subprocess
import sys
import tempfile
import os
import re


app = Flask(__name__)

create_database()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# ANALYZE CODE
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json() or {}

        code = data.get("code", "")
        language = data.get("language", "python")

        if not code.strip():
            return jsonify({
                "success": False,
                "error": "Please provide some code."
            }), 400

        result = analyze_code(code, language)

        save_history(
            language,
            code,
            result
        )

        fixed_code = extract_corrected_code(result)

        return jsonify({
            "success": True,
            "analysis": result,
            "fixed_code": fixed_code
        })

    except Exception as e:
        print("Analyze Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# HISTORY
# =========================================================

@app.route("/history", methods=["GET"])
def history():
    try:
        rows = get_history()

        history_data = []

        for row in rows:
            history_data.append({
                "id": row[0],
                "language": row[1],
                "code": row[2],
                "analysis": row[3],
                "created_at": row[4]
            })

        return jsonify({
            "success": True,
            "history": history_data
        })

    except Exception as e:
        print("History Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# DELETE HISTORY
# =========================================================

@app.route("/history/<int:record_id>", methods=["DELETE"])
def delete_history_record(record_id):
    try:
        delete_history(record_id)

        return jsonify({
            "success": True,
            "message": "History deleted successfully."
        })

    except Exception as e:
        print("Delete History Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# EXPLAIN LINE BY LINE
# =========================================================

@app.route("/explain-line-by-line", methods=["POST"])
def explain_line_by_line_route():
    try:
        data = request.get_json() or {}

        code = data.get("code", "")
        language = data.get("language", "python")

        if not code.strip():
            return jsonify({
                "success": False,
                "error": "Please provide some code."
            }), 400

        result = explain_line_by_line(
            code,
            language
        )

        return jsonify({
            "success": True,
            "explanation": result
        })

    except Exception as e:
        print("Explain Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# AI TUTOR
# =========================================================

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json() or {}

        code = data.get("code", "")
        language = data.get("language", "python")
        question = data.get("question", "")

        tutor_mode = data.get(
            "tutor_mode",
            "beginner"
        )

        if not question.strip():
            return jsonify({
                "success": False,
                "error": "Please enter a question."
            }), 400

        result = ask_ai_tutor(
            code,
            language,
            question,
            tutor_mode
        )

        return jsonify({
            "success": True,
            "answer": result
        })

    except Exception as e:
        print("AI Tutor Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# EXPLAIN ERROR
# =========================================================

@app.route("/explain-error", methods=["POST"])
def explain_error_route():
    try:
        data = request.get_json() or {}

        code = data.get("code", "")
        language = data.get("language", "python")

        error_type = data.get(
            "error_type",
            "UnknownError"
        )

        error_line = data.get(
            "error_line",
            "Unknown"
        )

        error_text = data.get(
            "error_text",
            ""
        )

        result = explain_error(
            code,
            language,
            error_type,
            error_line,
            error_text
        )

        fixed_code = extract_corrected_code(result)

        return jsonify({
            "success": True,
            "explanation": result,
            "fixed_code": fixed_code
        })

    except Exception as e:
        print("Explain Error Route Error:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# EXTRACT PYTHON ERROR
# =========================================================

def extract_python_error(error_text):

    line_match = re.search(
        r"line\s+(\d+)",
        error_text,
        re.IGNORECASE
    )

    error_match = re.search(
        r"([A-Za-z]+(?:Error|Exception)):",
        error_text
    )

    line_number = None
    error_type = "RuntimeError"

    if line_match:
        line_number = int(line_match.group(1))

    if error_match:
        error_type = error_match.group(1)

    return {
        "line": line_number,
        "type": error_type
    }


# =========================================================
# EXTRACT CORRECTED CODE FROM AI RESPONSE
# =========================================================

def extract_corrected_code(ai_text):

    if not ai_text:
        return None

    patterns = [
        r"###\s*CORRECTED CODE\s*\n(.*?)(?=\n###|\Z)",
        r"CORRECTED CODE\s*:?\s*\n(.*?)(?=\n###|\Z)",
        r"```(?:python|c|cpp|java|javascript|js)?\s*\n(.*?)```"
    ]

    corrected_code = None

    for pattern in patterns:

        match = re.search(
            pattern,
            ai_text,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            corrected_code = match.group(1).strip()
            break

    if not corrected_code:
        return None

    corrected_code = re.sub(
        r"^```[a-zA-Z0-9_+#-]*\s*",
        "",
        corrected_code
    )

    corrected_code = re.sub(
        r"\s*```$",
        "",
        corrected_code
    )

    corrected_code = corrected_code.strip()

    if not corrected_code:
        return None

    return corrected_code


# =========================================================
# RUN CODE
# =========================================================

@app.route("/run", methods=["POST"])
def run_code():

    temp_file = None

    try:

        data = request.get_json() or {}

        code = data.get("code", "")
        language = data.get("language", "python")

        if not code.strip():
            return jsonify({
                "success": False,
                "error": "Please provide some code."
            }), 400


        # =================================================
        # PYTHON
        # =================================================

        if language == "python":

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8"
            ) as temp:

                temp.write(code)
                temp_file = temp.name

            result = subprocess.run(
                [
                    sys.executable,
                    temp_file
                ],
                capture_output=True,
                text=True,
                timeout=5
            )


        # =================================================
        # C
        # =================================================

        elif language == "c":

            with tempfile.TemporaryDirectory() as temp_dir:

                source_file = os.path.join(
                    temp_dir,
                    "program.c"
                )

                executable_file = os.path.join(
                    temp_dir,
                    "program.exe"
                )

                with open(
                    source_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(code)

                compile_result = subprocess.run(
                    [
                        "gcc",
                        source_file,
                        "-o",
                        executable_file
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if compile_result.returncode != 0:

                    error_text = (
                        compile_result.stderr
                        or compile_result.stdout
                        or "C compilation error."
                    )

                    ai_explanation = explain_error(
                        code,
                        language,
                        "CompilationError",
                        None,
                        error_text
                    )

                    fixed_code = extract_corrected_code(
                        ai_explanation
                    )

                    return jsonify({
                        "success": False,
                        "error": error_text,
                        "output": error_text,
                        "error_line": None,
                        "error_type": "CompilationError",
                        "ai_explanation": ai_explanation,
                        "fixed_code": fixed_code
                    })

                result = subprocess.run(
                    [executable_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )


        # =================================================
        # C++
        # =================================================

        elif language == "cpp":

            with tempfile.TemporaryDirectory() as temp_dir:

                source_file = os.path.join(
                    temp_dir,
                    "program.cpp"
                )

                executable_file = os.path.join(
                    temp_dir,
                    "program.exe"
                )

                with open(
                    source_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(code)

                compile_result = subprocess.run(
                    [
                        "g++",
                        source_file,
                        "-o",
                        executable_file
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if compile_result.returncode != 0:

                    error_text = (
                        compile_result.stderr
                        or compile_result.stdout
                        or "C++ compilation error."
                    )

                    ai_explanation = explain_error(
                        code,
                        language,
                        "CompilationError",
                        None,
                        error_text
                    )

                    fixed_code = extract_corrected_code(
                        ai_explanation
                    )

                    return jsonify({
                        "success": False,
                        "error": error_text,
                        "output": error_text,
                        "error_line": None,
                        "error_type": "CompilationError",
                        "ai_explanation": ai_explanation,
                        "fixed_code": fixed_code
                    })

                result = subprocess.run(
                    [executable_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )


        # =================================================
        # JAVA
        # =================================================

        elif language == "java":

            with tempfile.TemporaryDirectory() as temp_dir:

                source_file = os.path.join(
                    temp_dir,
                    "Main.java"
                )

                with open(
                    source_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(code)

                compile_result = subprocess.run(
                    [
                        "javac",
                        source_file
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if compile_result.returncode != 0:

                    error_text = (
                        compile_result.stderr
                        or compile_result.stdout
                        or "Java compilation error."
                    )

                    ai_explanation = explain_error(
                        code,
                        language,
                        "CompilationError",
                        None,
                        error_text
                    )

                    fixed_code = extract_corrected_code(
                        ai_explanation
                    )

                    return jsonify({
                        "success": False,
                        "error": error_text,
                        "output": error_text,
                        "error_line": None,
                        "error_type": "CompilationError",
                        "ai_explanation": ai_explanation,
                        "fixed_code": fixed_code
                    })

                result = subprocess.run(
                    [
                        "java",
                        "-cp",
                        temp_dir,
                        "Main"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5
                )


        # =================================================
        # JAVASCRIPT
        # =================================================

        elif language == "javascript":

            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".js",
                delete=False,
                encoding="utf-8"
            ) as temp:

                temp.write(code)
                temp_file = temp.name

            result = subprocess.run(
                [
                    "node",
                    temp_file
                ],
                capture_output=True,
                text=True,
                timeout=5
            )


        # =================================================
        # UNSUPPORTED LANGUAGE
        # =================================================

        else:

            return jsonify({
                "success": False,
                "error": "Unsupported programming language.",
                "output": "Unsupported programming language.",
                "fixed_code": None
            })


        # =================================================
        # SUCCESS
        # =================================================

        if result.returncode == 0:

            return jsonify({
                "success": True,
                "output": result.stdout,
                "error": "",
                "error_line": None,
                "error_type": None,
                "ai_explanation": None,
                "fixed_code": None
            })


        # =================================================
        # ERROR
        # =================================================

        error_text = (
            result.stderr
            or result.stdout
            or "Unknown programming error."
        )


        # =================================================
        # PYTHON ERROR INFORMATION
        # =================================================

        if language == "python":

            error_info = extract_python_error(
                error_text
            )

            error_type = error_info["type"]
            error_line = error_info["line"]

        else:

            error_type = "RuntimeError"
            error_line = None


        # =================================================
        # AI EXPLANATION
        # =================================================

        ai_explanation = explain_error(
            code,
            language,
            error_type,
            error_line,
            error_text
        )


        # =================================================
        # EXTRACT FIXED CODE
        # =================================================

        fixed_code = extract_corrected_code(
            ai_explanation
        )


        return jsonify({
            "success": False,
            "error": error_text,
            "output": error_text,
            "error_line": error_line,
            "error_type": error_type,
            "ai_explanation": ai_explanation,
            "fixed_code": fixed_code
        })


    except subprocess.TimeoutExpired:

        return jsonify({
            "success": False,
            "error": "Program execution exceeded the 5-second limit.",
            "output": "Program execution exceeded the 5-second limit.",
            "fixed_code": None
        })


    except FileNotFoundError as e:

        return jsonify({
            "success": False,
            "error": (
                "The required compiler/interpreter "
                "is not installed or is not available "
                "in your system PATH.\n\n"
                f"Details: {e}"
            ),
            "output": (
                "Required compiler/interpreter is missing."
            ),
            "fixed_code": None
        })


    except Exception as e:

        print("Run Error:", e)

        return jsonify({
            "success": False,
            "error": str(e),
            "output": str(e),
            "fixed_code": None
        }), 500


    finally:

        if temp_file and os.path.exists(temp_file):

            try:
                os.remove(temp_file)

            except Exception:
                pass


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )