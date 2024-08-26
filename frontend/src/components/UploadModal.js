// UploadModal.js
import React, { useState } from 'react';
import './UploadModal.css';  // Importer le fichier CSS spécifique à la modale

const UploadModal = ({ isOpen, onClose, onSubmit }) => {
    const [shpFile, setShpFile] = useState(null);
    const [additionalInfo, setAdditionalInfo] = useState({
        name: '',
        description: ''
    });
    const [imageUrl, setImageUrl] = useState(null);

    const handleFileChange = (e) => {
        setShpFile(e.target.files[0]);
        setImageUrl(null); // Reset image URL when a new file is selected
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (shpFile) {
            const formData = new FormData();
            formData.append('file', shpFile);
            formData.append('name', additionalInfo.name);
            formData.append('description', additionalInfo.description);

            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`${process.env.REACT_APP_IP_SERV}/upload`, {
                    method: 'POST',
                    headers: {
                        'Authorization': token,
                    },
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log('File uploaded successfully', data);
                    setImageUrl(data.imageUrl); // Assure-toi que ton backend renvoie l'URL de l'image
                } else {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            } catch (error) {
                console.error('File upload failed:', error);
            }
        }
    };

    return isOpen ? (
        <>
            <div className="modal">
                <h2>Upload SHP File</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>
                            File:
                            <input type="file" accept=".shp" onChange={handleFileChange} required />
                        </label>
                    </div>
                    <div>
                        <label>
                            Name:
                            <input type="text" value={additionalInfo.name} onChange={(e) => setAdditionalInfo({ ...additionalInfo, name: e.target.value })} required />
                        </label>
                    </div>
                    <div>
                        <label>
                            Description:
                            <textarea value={additionalInfo.description} onChange={(e) => setAdditionalInfo({ ...additionalInfo, description: e.target.value })} required />
                        </label>
                    </div>
                    <button type="submit">Upload</button>
                    <button type="button" onClick={onClose}>Cancel</button>
                </form>
                {imageUrl && (
                    <div>
                        <h3>Uploaded SHP Preview:</h3>
                        <img src={imageUrl} alt="SHP Preview" style={{ width: '100%', height: 'auto' }} />
                    </div>
                )}
            </div>
            <div className="modal-overlay" onClick={onClose} />
        </>
    ) : null;
};

export default UploadModal;
