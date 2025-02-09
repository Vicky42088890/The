from flask import Flask, request, render_template_string
import requests
import time
import re

app = Flask(__name__)

# HTML Template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment - Raghu ACC Rullx Boy</title>
    <style>
        body { background-color: #f4f4f4; font-family: Arial; text-align: center; padding: 20px; }
        input, button { padding: 10px; margin: 5px; width: 300px; border-radius: 5px; }
        button { background-color: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <h2>Facebook Auto Comment Tool</h2>
    <form method="POST">
        <input type="text" name="cookie" placeholder="Enter Your Facebook Cookie" required><br>
        <input type="text" name="post_url" placeholder="Enter Post URL" required><br>
        <input type="text" name="message" placeholder="Enter Your Comment" required><br>
        <input type="number" name="delay" placeholder="Delay (in seconds)" value="10" required><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Extract Post ID from URL
def extract_post_id(post_url):
    post_id_pattern = re.compile(r"posts/(\d+)")
    match = post_id_pattern.search(post_url)
    return match.group(1) if match else None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookie = request.form["cookie"]
        post_url = request.form["post_url"]
        message = request.form["message"]
        delay = int(request.form["delay"])

        post_id = extract_post_id(post_url)
        if not post_id:
            return "Invalid Post URL!"

        # Facebook Graph API URL
        comment_url = f"https://graph.facebook.com/{post_id}/comments"

        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        while True:
            data = {
                "message": message,
                "access_token": "EAAAAUa..."  # यहां Access Token डालना होगा
            }

            response = requests.post(comment_url, headers=headers, data=data)

            if response.status_code == 200:
                print("✅ Comment Sent Successfully!")
            else:
                print(f"❌ Error: {response.text}")

            time.sleep(delay)

    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
