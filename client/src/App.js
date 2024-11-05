// src/App.js
import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [output, setOutput] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
    }
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please upload an image");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setOutput(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Failed to upload image");
      setIsLoading(false);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: "image/*",
  });

  return (
    <div className="App">
      <h1>Upload Image for OCR and Analysis</h1>
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        {selectedFile ? (
          <p>{selectedFile.name}</p>
        ) : (
          <p>Drag and drop an image here, or click to select an image</p>
        )}
      </div>
      <button onClick={handleUpload}>Upload</button>

      {isLoading && <div className="loader"></div>}

      {output && !isLoading && (
        <div className="output-section">
          <h2>Extracted Information:</h2>
          <pre>{output.answers}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
