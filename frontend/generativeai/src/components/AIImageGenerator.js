import React, { useState } from "react";
import { FiUploadCloud } from "react-icons/fi";
import { BiErrorCircle } from "react-icons/bi";
import { AiOutlineLoading3Quarters } from "react-icons/ai";
import './AIImageGenerator.css'; // Import the CSS file

const AIImageGenerator = () => {
    const [inputImage, setInputImage] = useState(null);
    const [outputImage, setOutputImage] = useState(null);
    const [error, setError] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file && file.type.startsWith("image/")) {
            setInputImage(URL.createObjectURL(file));
            setError(null);
            processImage(file);
        } else {
            setError("Please upload a valid image file.");
        }
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        if (file && file.type.startsWith("image/")) {
            setInputImage(URL.createObjectURL(file));
            setError(null);
            processImage(file);
        } else {
            setError("Please drop a valid image file.");
        }
    };

    const processImage = (file) => {
        setIsProcessing(true);
        const formData = new FormData();
        formData.append("image", file);

        // Send the image to the Flask API
        fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Image processing failed");
                }
                return response.json();
            })
            .then(data => {
                // Assuming the response contains the image URL
                setOutputImage(data.generated_image_url);
                setIsProcessing(false);
            })
            .catch(err => {
                setError(err.message);
                setIsProcessing(false);
            });
    };

    // Reset function to clear input and output images
    const resetImages = () => {
        setInputImage(null);
        setOutputImage(null);
        setError(null);
        setIsProcessing(false);
    };

    return (
        <div className="container">
            <h1 className="title">AI Image Generator</h1>

            <div className="grid">
                {/* Input Image Section */}
                <div
                    className="section"
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                >
                    <h2 className="section-title">Input Sketch</h2>
                    <div className="image-preview">
                        {inputImage ? (
                            <img
                                src={inputImage}
                                alt="Input sketch preview"
                                className="image"
                            />
                        ) : (
                            <label className="py-8 cursor-pointer" htmlFor="fileInput">
                                <FiUploadCloud className="upload-icon" />
                                <p className="text-gray-500">Drag and drop an image here, or</p>
                                <input
                                    type="file"
                                    id="fileInput"
                                    className="hidden"
                                    onChange={handleImageUpload}
                                    accept="image/*"
                                />
                            </label>
                        )}
                    </div>
                </div>

                {/* Output Image Section */}
                <div className="section">
                    <h2 className="section-title">Generated Image</h2>
                    <div className="image-preview h-64 flex items-center justify-center">
                        {isProcessing ? (
                            <div className="processing">
                                <AiOutlineLoading3Quarters className="processing-icon" />
                                <p className="text-gray-500">Processing image...</p>
                            </div>
                        ) : outputImage ? (
                            <img
                                src={outputImage}
                                alt="Generated realistic image preview"
                                className="image"
                            />
                        ) : (
                            <p className="text-gray-500">Generated image will appear here</p>
                        )}
                    </div>
                </div>
            </div>

            {/* Error Display */}
            {error && (
                <div className="error-message" role="alert">
                    <BiErrorCircle className="inline-block mr-2" />
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            {/* Reset Button */}
            <div className="reset-button-container">
                <button
                    onClick={resetImages}
                    className="reset-button"
                >
                    Reset
                </button>
            </div>

            {/* Accessibility Features */}
            <div className="sr-only">
                <p id="inputDescription">Upload your sketch image for AI processing</p>
                <p id="outputDescription">View the AI-generated realistic image based on your sketch</p>
            </div>
        </div>
    );
};

export default AIImageGenerator;
