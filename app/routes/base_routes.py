from flask import Blueprint, Response

base_bp = Blueprint("base_bp", __name__)

@base_bp.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Task List API</title>
        <style>
            body {
                font-family: sans-serif;
                background-color: #f0f4f8;
                color: #333;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #2a9d8f;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to my Task List API!</h1>
        <p>My API is up and running on Render.</p>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")
