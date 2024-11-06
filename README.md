# Document_capture_Application

## Full Documentation for the Application

This documentation covers the high-level architecture, front-end and back-end code, libraries used, and a breakdown of each function in a Flask and React-based OCR application. This application extracts text from uploaded images, processes it for specific field extraction, and returns formatted data for display on the front-end.

### 1. High-Level Architecture

The application consists of two main components:

1. **Flask Backend**: Handles image uploads, OCR processing, and text extraction.
2. **React Frontend**: Allows users to upload images and displays the processed data.

#### Workflow

1. **Image Upload**: The React front-end enables users to upload an image. The image is sent to the Flask back-end.
2. **Image Preprocessing**: The Flask server preprocesses the image for optimal OCR results.
3. **OCR Processing**: Using EasyOCR, the server extracts text from the image.
4. **Text Extraction**: Extracts specific information (like ID number, name, etc.) using regex and NLP techniques with spaCy.
5. **Response Generation**: Formats the extracted data into a JSON response.
6. **Display Data**: The front-end displays the processed data to the user.

### 2. Frontend Code Analysis (React)

#### File: `App.js`

The front-end is built with React. It provides an interface for uploading images and displaying extracted information. Here’s a breakdown of its components:

- **Libraries Used**:
  - `react`: Core library for building the user interface.
  - `axios`: For making HTTP requests to the Flask server.
  - `react-dropzone`: For handling drag-and-drop file uploads.

#### Code Breakdown

1. **State Management**:
   - `selectedFile`: Stores the uploaded file.
   - `output`: Stores the JSON response from the server.
   - `isLoading`: Manages loading state during file upload.

2. **File Upload Handling**:
   - `onDrop`: Function triggered when a file is dropped or selected. Sets `selectedFile`.
   - `handleUpload`: Sends the image to the Flask server using Axios, handles loading, and updates `output` with the server response.

3. **Rendering**:
   - `getRootProps` and `getInputProps`: Provided by `react-dropzone` for setting up the drag-and-drop area.
   - Displays the file name, upload button, and extracted information if available.

### 3. Backend Code Analysis (Flask)

#### File: `server.py`

The backend is implemented using Flask and includes image preprocessing, OCR, text extraction, and response formatting.

#### Libraries Used

- **Flask**: Web framework to handle HTTP requests.
- **Flask-CORS**: Allows cross-origin requests from the React frontend.
- **cv2 (OpenCV)**: Image processing library for preprocessing images.
- **easyocr**: OCR library to extract text from images.
- **re**: Regular expressions for extracting specific patterns from text.
- **spacy**: NLP library for named entity recognition.
- **requests**: For making API calls to Google Gemini for further text processing.

#### Code Breakdown

1. **Image Preprocessing**: `preprocess_image(image_path)`
   - Loads the image in grayscale, resizes it for better OCR accuracy, applies Gaussian blur to reduce noise, and uses thresholding to enhance text visibility.

2. **OCR Processing**: `extract_text_with_easyocr(image_path)`
   - Calls `preprocess_image` to prepare the image.
   - Uses EasyOCR to extract text and returns it as a string.

3. **Field Extraction**: `extract_fields_with_spacy(text)`
   - Uses regex patterns to find specific fields (e.g., ID Number, Date of Birth, Gender).
   - Applies spaCy for named entity recognition to extract the user’s name and father’s name.

4. **Question Answering (Optional)**: `answer_question_gemini(context)`
   - Sends the extracted text to Google Gemini's API to generate formatted answers. 
   - Parses the response to return the relevant fields in a formatted string.

5. **Main Route for Upload**: `/upload`
   - Handles image upload, saves it locally, performs OCR, extracts fields, and deletes the image after processing.
   - Returns a JSON response with raw text and formatted answers.

### Summary of Experience

#### How I Felt about the Challenge

This exercise was both enjoyable and challenging. The project required integrating OCR, image processing, NLP, and frontend-backend communication, which involved a broad range of technologies. Working with EasyOCR and spaCy for text extraction and entity recognition was particularly interesting, and handling the entire data flow from upload to display on the front-end was a rewarding experience.

#### Challenges Encountered

1. **OCR Accuracy**: Image preprocessing was essential to improve OCR accuracy. Without it, text extraction could be inconsistent.
2. **Regex Patterns**: Identifying relevant fields accurately with regex required careful tuning, especially given variations in text formatting.
3. **Frontend-Backend Sync**: Ensuring smooth data flow between React and Flask required managing asynchronous states and handling errors effectively.

#### Improvements for Scalability, Security, and User Experience

1. **Scalability**:
   - **Image Storage**: Use cloud storage (e.g., AWS S3) instead of saving images locally.
   - **Asynchronous Processing**: For heavy OCR workloads, consider using background workers (e.g., Celery with Redis) to handle requests asynchronously.

2. **Security**:
   - **API Key Management**: Store sensitive keys (like Google Gemini API key) securely, possibly using environment variables or a secrets management service.
   - **Input Validation**: Validate and sanitize uploaded files to prevent malicious content.
   - **Rate Limiting**: Implement rate limiting to prevent abuse of the OCR endpoint.

3. **User Experience**:
   - **Error Messages**: Provide detailed error messages for issues during upload or processing.
   - **Progress Indicators**: Use a progress bar for the upload process instead of a simple loader.
   - **Field Customization**: Allow users to specify the fields they want to extract, making the interface more flexible. 

This application could benefit from these adjustments to make it more robust and user-friendly for larger-scale deployments.
