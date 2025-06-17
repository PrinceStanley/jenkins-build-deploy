# app.py
# A simple Flask application that serves a "Hello, World!" page with a background image.
## Requirements:
# Flask
# To run this application, you need to have Flask installed. You can install it using pip:
# pip install Flask
from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                
                /* Ensure you have a directory named 'static' with an image named 'ocean-beach.jpg' */
                background-image: url('/static/ocean-beach.jpg');
                
                background-size: cover;
                background-position: center;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .hello-text {
                color: #fff;
                font-size: 3em;
                font-family: Arial, sans-serif;
                text-align: center;
                text-shadow: 2px 2px 8px #000;
                background: rgba(0,0,0,0.0);
                padding: 20px 40px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="hello-text">Hello, World!</div>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)