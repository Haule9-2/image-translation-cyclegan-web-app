# AI Image Generator

This project is an AI Image Generator that takes a sketch as input and generates a realistic image using a CycleGAN model. The frontend is built with React, and the backend is powered by Flask.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload a sketch image and generate a corresponding realistic image.
- Drag and drop functionality for image uploads.
- Error handling for invalid file formats.
- Responsive UI with loading indicators and error messages.

## Technologies Used

- **Frontend**: React.js, CSS, React Icons
- **Backend**: Flask, Flask-CORS, Flasgger for API documentation
- **Machine Learning**: PyTorch, torchvision
- **Image Processing**: PIL (Python Imaging Library)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Haule9-2/image-translation-cyclegan-web-app.git
   cd image-translation-cyclegan-web-app
   ```

2. **Install dependencies**:

   - For the **backend**:
     ```bash
     cd backend
     pip install -r requirements.txt
     ```

   - For the **frontend**:
     ```bash
     cd frontend
     npm install
     ```

3. **Set up the model**: Make sure to place your CycleGAN model checkpoint file in the correct directory (adjust the path in the code if necessary).

## Usage

1. **Start the Flask server**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the React frontend**:
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**: Open your browser and go to `http://localhost:3000` to use the AI Image Generator.

## API Documentation

### Endpoint: `/generate`

- **Method**: `POST`
- **Description**: Generates an image from the uploaded sketch.
- **Parameters**:
  - `image`: The image file to be processed (in `formData`).
  
- **Responses**:
  - **200 OK**: Returns the URL of the generated image.
    ```json
    {
      "generated_image_url": "http://127.0.0.1:5000/uploads/output_image.jpg"
    }
    ```
  - **400 Bad Request**: Returns an error message for invalid file formats.
    ```json
    {
      "error": "Invalid file format"
    }
    ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
