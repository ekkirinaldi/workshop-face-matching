import os
import base64
import numpy as np
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from werkzeug.utils import secure_filename
import torchvision.transforms as transforms
import time

app = Flask(__name__)

# Initialize device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize MTCNN with optimized settings
mtcnn = MTCNN(
    image_size=160,
    margin=0,
    keep_all=False,
    min_face_size=20,
    device=device,
    post_process=False  # Disable post-processing for faster detection
)

# Initialize FaceNet model with caching
facenet = None
def get_facenet():
    global facenet
    if facenet is None:
        facenet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    return facenet

def preprocess_image(image_data):
    """Convert base64 image to PIL Image and detect face"""
    try:
        # Remove the data:image/jpeg;base64, prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to speed up face detection
        max_size = 1024
        ratio = max_size / max(image.size)
        if ratio < 1:
            new_size = tuple([int(x * ratio) for x in image.size])
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Detect and align face
        face = mtcnn(image)
        if face is None:
            return None, "No face detected"
        
        return face.to(device), None
    except Exception as e:
        return None, str(e)

def get_face_embedding(face):
    """Get face embedding using FaceNet"""
    with torch.no_grad():
        embedding = get_facenet()(face.unsqueeze(0))
    return embedding.cpu().numpy()

def calculate_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two face embeddings"""
    similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return float(similarity[0][0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compare', methods=['POST'])
def compare_faces():
    try:
        data = request.get_json()
        
        if not data or 'image1' not in data or 'image2' not in data:
            return jsonify({'error': 'Missing image data'}), 400
        
        # Process first image
        face1, error1 = preprocess_image(data['image1'])
        if error1:
            return jsonify({'error': f'Error processing first image: {error1}'}), 400
        
        # Process second image
        face2, error2 = preprocess_image(data['image2'])
        if error2:
            return jsonify({'error': f'Error processing second image: {error2}'}), 400
        
        # Get embeddings
        embedding1 = get_face_embedding(face1)
        embedding2 = get_face_embedding(face2)
        
        # Calculate similarity
        similarity = calculate_similarity(embedding1, embedding2)
        similarity_percentage = round(similarity * 100, 2)
        
        return jsonify({
            'similarity': similarity_percentage,
            'message': 'Face comparison successful'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Face matching service is running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 