from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://chatapi.akash.network/api/v1",
    api_key="sk-5F7Kna9Tb3gxGsXWYo0KlA",  # Replace with your actual API key
)

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = None

    if request.method == "POST":
        user_input = request.form.get("user_input")
        image_url = request.form.get("image_url").strip()

        # Prepare message content
        content = [{"type": "text", "text": user_input}]
        if image_url:
            content.append({"type": "image_url", "image_url": {"url": image_url}})

        # Call OpenAI API
        try:
            completion = client.chat.completions.create(
                model="Meta-Llama-3-1-8B-Instruct-FP8",  # Ensure this model supports vision if using images
                messages=[{"role": "user", "content": content}],
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
                    "X-Title": "<YOUR_SITE_NAME>",  # Optional
                },
                extra_body={},
            )
            response_text = completion.choices[0].message.content
        except Exception as e:
            response_text = f"Error: {str(e)}"

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(debug=True)
