# Face Matching Application

A web application that compares two facial images and calculates their similarity percentage using face embeddings.

## Features

- Face detection and alignment using MTCNN
- Face embedding generation using FaceNet
- Similarity calculation between face embeddings
- Web interface for easy image upload and comparison
- REST API for programmatic access
- Docker containerization for easy deployment

## Prerequisites

- Python 3.9 or higher
- Docker (for containerized deployment)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd face-match-material
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app/app.py
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t face-match .
```

2. Run the container:
```bash
docker run -p 8000:8000 face-match
```

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Upload two facial images using the file inputs
3. Click the "Compare Faces" button
4. View the similarity percentage result

### API Usage

The application provides a REST API endpoint for face comparison:

```bash
POST /api/compare
Content-Type: application/json

{
    "image1": "base64_encoded_image1",
    "image2": "base64_encoded_image2"
}
```

Response:
```json
{
    "similarity": 85.5,
    "message": "Face comparison successful"
}
```

Health check endpoint:
```bash
GET /api/health
```

## Error Handling

The application handles various error cases:
- No face detected in image
- Multiple faces in image
- Invalid image format
- Poor image quality

## License

This project is licensed under the MIT License - see the LICENSE file for details. 