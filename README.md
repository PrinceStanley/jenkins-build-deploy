# Jenkins Build & Deploy Flask App

![Flask App Screenshot](static/ocean-beach.jpg)

---

This repository demonstrates a simple Python Flask web application, containerized with Docker, and designed for automated build and deployment using Jenkins. It serves as a practical example for learning and implementing CI/CD pipelines with modern DevOps tools.

---

## Features

- **Flask Web Application:** Serves a "Hello, World!" page styled with a custom background image.
- **Static File Support:** Includes a static directory for serving images and other assets.
- **Docker Support:** Easily containerize the application using the provided Dockerfile.
- **Jenkins Ready:** Suitable for integration into Jenkins pipelines for automated build, test, and deployment.

---

## Prerequisites

- Python 3.11+
- Flask
- Docker
- Jenkins (optional, for CI/CD)

---

## Getting Started

1. **Clone the Repository**
2. **Run Locally (Without Docker)**
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Ensure the `static/ocean-beach.jpg` image exists.
    - Start the Flask app:
      ```bash
      python app.py
      ```
    - Open [http://localhost:8080](http://localhost:8080) in your browser.
3. **Run with Docker**
    - Build the Docker image:
      ```bash
      docker build -t flask-app .
      ```
    - Run the container:
      ```bash
      docker run -p 8080:8080 flask-app
      ```
    - Access the app at [http://localhost:8080](http://localhost:8080).
4. **Jenkins Integration**
    - This project is ideal for Jenkins-based CI/CD pipelines. A typical pipeline might:
      - Clone the repository
      - Build the Docker image
      - Run tests (if any)
      - Push the image to a Docker registry
      - Deploy the container to a server or cloud platform
    - You can use a Jenkinsfile or freestyle project to automate these steps.

---

## Project Structure

```
.
├── app.py
├── Dockerfile
├── requirements.txt
├── static/
│   └── ocean-beach.jpg
└── README.md
```

---

## Customization

- Replace `ocean-beach.jpg` in the `static` folder with your own image for a different background.
- Modify `app.py` to add more routes or features as needed.
- Add a `requirements.txt` if you introduce more dependencies.

---

## License

This project is for educational and demonstration purposes. Feel free to use and modify it for your own CI/CD experiments and learning.

---

Happy Building & Deploying!