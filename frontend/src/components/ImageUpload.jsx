import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = ({ onUploadSuccess }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [uploading, setUploading] = useState(false);

    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onload = (e) => setPreview(e.target.result);
            reader.readAsDataURL(file);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post('http://localhost:5000/api/match-image', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            
            if (onUploadSuccess) {
                onUploadSuccess(response.data);
            }
        } catch (error) {
            console.error('Upload failed:', error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="image-upload">
            <h3>Upload Image for Matching</h3>
            <input 
                type="file" 
                accept="image/*" 
                onChange={handleFileSelect}
                disabled={uploading}
            />
            
            {preview && (
                <div className="preview">
                    <img src={preview} alt="Preview" style={{maxWidth: '200px', maxHeight: '200px'}} />
                </div>
            )}
            
            <button 
                onClick={handleUpload} 
                disabled={!selectedFile || uploading}
                className="upload-btn"
            >
                {uploading ? 'Processing...' : 'Find Matches'}
            </button>
        </div>
    );
};

export default ImageUpload;
