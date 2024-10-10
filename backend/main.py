from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from model import Generator, load_model  # Import Generator here
import os
import torch
from torchvision import transforms
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
swagger = Swagger(app)  # Initialize Swagger

# Ensure you have a folder to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load your model
checkpoint_path = r"E:\Documents\Workspace\DoAn\backend\model\latest_net_G_B.pth"  # Adjust the path as needed
model = load_model(checkpoint_path, generator_type='B')
 
@app.route('/')
def home():
    return "Welcome to the AI Image Generator API! Use /generate to upload an image."

@app.route('/generate', methods=['POST'])
def generate_image():
    """
    Generate an image from the uploaded sketch.
    ---
    tags:
      - Image Generation
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: The image file to be processed.
    responses:
      200:
        description: The generated image URL
        schema:
          type: object
          properties:
            generated_image_url:
              type: string
              example: "http://127.0.0.1:5000/uploads/output_image.jpg"
      400:
        description: Error in image processing
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid file format"
    """
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.content_type.startswith('image/'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Load the image and prepare it for the model
        image = Image.open(filepath).convert("RGB")
        image = image.resize((256, 256))  # Resize to the size your model expects
        image_tensor = transforms.ToTensor()(image).unsqueeze(0)  # Convert to tensor and add batch dimension

        # Process the image using the model
        with torch.no_grad():
            output_tensor = model(image_tensor)

        # Convert the output tensor back to a PIL image
        output_image = output_tensor.squeeze(0).permute(1, 2, 0).numpy()  # Remove batch dimension and reorder dimensions
        output_image = (output_image * 255).astype(np.uint8)  # Convert to [0, 255]
        output_pil_image = Image.fromarray(output_image)

        # Save the output image
        output_image_path = os.path.join(UPLOAD_FOLDER, f'output_{file.filename}')
        output_pil_image.save(output_image_path)

        # Return the path to the generated image
        generated_image_url = f"http://127.0.0.1:5000/uploads/output_{file.filename}"
        return jsonify({"generated_image_url": generated_image_url}), 200

    return jsonify({"error": "Invalid file format"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
