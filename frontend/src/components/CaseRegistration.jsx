import React, { useState } from 'react';
import axios from 'axios';

const CaseRegistration = ({ onRegistrationSuccess }) => {
    const [formData, setFormData] = useState({
        name: '',
        age: '',
        location: '',
        description: ''
    });
    const [imageFile, setImageFile] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleImageChange = (e) => {
        setImageFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!imageFile) {
            alert('Please select an image');
            return;
        }

        setSubmitting(true);
        const submitData = new FormData();
        
        Object.keys(formData).forEach(key => {
            submitData.append(key, formData[key]);
        });
        submitData.append('image', imageFile);

        try {
            const response = await axios.post('http://localhost:5000/api/upload-case', submitData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            
            if (response.data.success) {
                alert('Case registered successfully!');
                if (onRegistrationSuccess) {
                    onRegistrationSuccess(response.data);
                }
                // Reset form
                setFormData({ name: '', age: '', location: '', description: '' });
                setImageFile(null);
            }
        } catch (error) {
            console.error('Registration failed:', error);
            alert('Registration failed. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="case-registration">
            <h2>Register Missing Person Case</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Age:</label>
                    <input
                        type="number"
                        name="age"
                        value={formData.age}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Last Known Location:</label>
                    <input
                        type="text"
                        name="location"
                        value={formData.location}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>Description:</label>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleInputChange}
                        rows="3"
                    />
                </div>

                <div className="form-group">
                    <label>Photo:</label>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageChange}
                        required
                    />
                </div>

                <button type="submit" disabled={submitting}>
                    {submitting ? 'Registering...' : 'Register Case'}
                </button>
            </form>
        </div>
    );
};

export default CaseRegistration;
