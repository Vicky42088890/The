from flask import Flask, request, render_template_string
import requests
import re
import time

app = Flask(__name__)

class FacebookCommenter:
    def __init__(self):
        self.comment_count = 0

    def comment_on_post(self, cookie, post_id, comment):
        with requests.Session() as r:
            r.headers.update({
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Mobile Safari/537.36)',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
            })

            response = r.get(f'https://mbasic.facebook.com/{post_id}', cookies={"cookie": cookie})
            next_action = re.search('method="post" action="([^"]+)"', response.text)
            fb_dtsg = re.search('name="fb_dtsg" value="([^"]+)"', response.text)
            jazoest = re.search('name="jazoest" value="([^"]+)"', response.text)

            if not (next_action and fb_dtsg and jazoest):
                return "Invalid post or session expired."

            post_url = f"https://mbasic.facebook.com{next_action.group(1).replace('amp;', '')}"
            data = {
                'fb_dtsg': fb_dtsg.group(1),
                'jazoest': jazoest.group(1),
                'comment_text': comment,
                'submit': 'Submit'
            }

            result = r.post(post_url, data=data, cookies={"cookie": cookie})
            if 'comment_success' in result.url:
                self.comment_count += 1
                return f"✅ Comment {self.comment_count} sent successfully!"
            else:
                return "❌ Failed to post comment."

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        cookie = request.form['cookie']
        post_id = request.form['post_id']
        comment = request.form['comment']
        delay = int(request.form['delay'])

        commenter = FacebookCommenter()
        for _ in range(5):  # Loop to send comment 5 times, modify as needed
            time.sleep(delay)
            message = commenter.comment_on_post(cookie, post_id, comment)

    html_form = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Auto Commenter - Raghu ACC Rullx Boy</title>
        <style>
            body { background-color: #222; color: #fff; text-align: center; font-family: Arial, sans-serif; }
            .container { background: #333; padding: 20px; border-radius: 10px; display: inline-block; margin-top: 50px; }
            input, button { padding: 10px; margin: 5px; width: 90%; border-radius: 5px; }
            button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Auto Commenter</h2>
            <form method="POST">
                Cookie: <input type="text" name="cookie" required><br>
                Post ID: <input type="text" name="post_id" required><br>
                Comment: <input type="text" name="comment" required><br>
                Delay (in seconds): <input type="number" name="delay" value="5" required><br>
                <button type="submit">Submit</button>
            </form>
            <p>{{ message }}</p>
        </div>
        <footer>Created by Raghu ACC Rullx Boy</footer>
    </body>
    </html>
    '''
    return render_template_string(html_form, message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
