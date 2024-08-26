// UploadModal.js
import React, { useState } from 'react';
import { Modal, Tab, Tabs, Button } from 'react-bootstrap';

const UploadModal = ({ setIsModalOpen }) => {
    const [key, setKey] = useState('upload'); // Onglet actif

    return (
        <Modal show onHide={() => setIsModalOpen(false)} size="lg">
            <Modal.Header closeButton>
            </Modal.Header>
            <Modal.Body>
                <Tabs
                    id="controlled-tab-example"
                    activeKey={key}
                    onSelect={(k) => setKey(k)}
                    className="mb-3"
                >
                    <Tab eventKey="upload" title="Upload">
                        <UploadContent />
                    </Tab>
                    <Tab eventKey="preview" title="Preview">
                        <PreviewContent />
                    </Tab>
                    {/* Ajoutez d'autres onglets si nécessaire */}
                </Tabs>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
                    Close
                </Button>
                <Button variant="primary">Save Changes</Button>
            </Modal.Footer>
        </Modal>
    );
};

const UploadContent = () => (
    <div>
        <h4>Upload Content</h4>
        <input type="file" className="form-control" />
        <Button className="mt-2" variant="primary">Upload</Button>
    </div>
);

const PreviewContent = () => (
    <div>
        <h4>Preview Content</h4>
        <p>Aperçu des fichiers...</p>
    </div>
);

export default UploadModal;
