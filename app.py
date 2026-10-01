from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_notes():

    transcript = request.form.get("transcript")

    if not transcript:
        return render_template(
            "index.html",
            notes="Please enter a lecture transcript."
        )

    prompt = f"""
You are a Smart Notes Generator.

Convert the following lecture transcript into clear and structured study notes.

Give the output in this format:

1. Topic
2. Short Summary
3. Key Points
4. Important Concepts
5. Examples
6. Exam Questions

Keep the language simple and easy for a college student.

Lecture Transcript:
{transcript}
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        notes = result["response"]

    except Exception as e:

        notes = f"Error connecting to AI model: {e}"

    return render_template("index.html", notes=notes)


if __name__ == "__main__":
    app.run(debug=True)