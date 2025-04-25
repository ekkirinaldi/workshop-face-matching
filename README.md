# Face Matching Application

A web application that compares two facial images and calculates their similarity percentage using face embeddings.

## Features

- Face detection and alignment using MTCNN
- Face embedding generation using FaceNet
- Similarity calculation between face embeddings
- Web interface for easy image upload and comparison
- REST API for programmatic access
- Docker containerization for easy deployment
- Optimized performance with image resizing and model caching
- Multi-worker support for concurrent requests

## System Requirements

- Python 3.9 or higher
- Docker (for containerized deployment)
- Minimum 2GB RAM (4GB recommended)
- CPU with AVX2 support (for optimal performance)
- CUDA-capable GPU (optional, for faster processing)

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

Note: The Docker container is configured with:
- 120-second timeout for face processing
- 2 worker processes for concurrent requests
- Optimized memory usage

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

### Performance Tips

1. Image Size:
   - Recommended maximum image size: 1024x1024 pixels
   - Larger images will be automatically resized
   - Supported formats: JPEG, PNG

2. Face Detection:
   - Images should contain exactly one face
   - Face should be clearly visible and well-lit
   - Minimum face size: 20x20 pixels

## Error Handling

The application handles various error cases:
- No face detected in image
- Multiple faces in image
- Invalid image format
- Poor image quality
- Processing timeout (after 120 seconds)

## Troubleshooting

Common issues and solutions:

1. Worker Timeout:
   - Ensure images are not too large
   - Check system resources
   - Verify image quality

2. No Face Detected:
   - Ensure face is clearly visible
   - Check image lighting
   - Verify image format

3. Memory Issues:
   - Reduce image size
   - Restart the container
   - Check system resources

## License

This project is licensed under the MIT License - see the LICENSE file for details. 