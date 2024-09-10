import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import { Form, Button, Alert, Row, Col } from 'react-bootstrap';
import 'leaflet/dist/leaflet.css';

const FitBounds = ({ bounds }) => {
    const map = useMap();
    map.fitBounds(bounds);
    return null;
};

const MO_gemapiTab = () => {
    const [files, setFiles] = useState([]);
    const [nomMo, setNomMo] = useState('');
    const [uploadStatus, setUploadStatus] = useState(null);
    const [geoJsonData, setGeoJsonData] = useState(null);
    const [bounds, setBounds] = useState(null);

    const token = localStorage.getItem('token');

    const onDrop = useCallback((acceptedFiles) => {
        setFiles(acceptedFiles);
    }, []);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        multiple: true,
        accept: {
            'application/octet-stream': ['.shp', '.dbf', '.shx', '.prj']
        }
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!nomMo || files.length === 0) {
            setUploadStatus('error');
            return;
        }

        const formData = new FormData();
        formData.append('NOM-MO', nomMo);
        files.forEach((file) => {
            formData.append('files', file);
        });

        try {
            const response = await fetch(`${process.env.REACT_APP_IP_SERV}/upload_MO_gemapi`, {
                method: 'POST',
                headers: {
                    'Authorization': token
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to upload');
            }

            const geoJsonResponse = await response.json();
            setGeoJsonData(geoJsonResponse);
            setUploadStatus('success');

            // Extract bounding box coordinates
            const bbox = geoJsonResponse.features.find(feature => feature.properties.name === 'Bounding Box');
            if (bbox) {
                const bboxCoords = bbox.geometry.coordinates[0];
                const bounds = [
                    [bboxCoords[1][1], bboxCoords[1][0]], // South-West
                    [bboxCoords[2][1], bboxCoords[2][0]]  // North-East
                ];
                setBounds(bounds);
            }
        } catch (error) {
            console.error('Error during upload:', error);
            setUploadStatus('error');
        }
    };

    return (
        <Row>
            {/* Colonne de gauche pour le formulaire */}
            <Col md={4}>
                <div className="form-container">
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="formNomMo">
                            <Form.Label>NOM-MO</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Entrez le NOM-MO"
                                value={nomMo}
                                onChange={(e) => setNomMo(e.target.value)}
                            />
                        </Form.Group>

                        <Form.Group>
                            <div {...getRootProps({ className: 'dropzone' })} style={{ border: '2px dashed #ccc', padding: '20px' }}>
                                <input {...getInputProps()} />
                                <p>Glissez-déposez des fichiers ici, ou cliquez pour sélectionner des fichiers (formats .shp, .dbf, .shx, .prj)</p>
                            </div>
                        </Form.Group>

                        {files.length > 0 && (
                            <ul>
                                {files.map((file) => (
                                    <li key={file.path}>{file.name}</li>
                                ))}
                            </ul>
                        )}

                        <Button variant="primary" type="submit">
                            Envoyer
                        </Button>
                    </Form>

                    {uploadStatus === 'error' && (
                        <Alert variant="danger" className="mt-3">
                            Une erreur est survenue lors de l'envoi des fichiers. Veuillez réessayer.
                        </Alert>
                    )}
                </div>
            </Col>

            {/* Colonne de droite pour la carte */}
            <Col md={8}>
                {uploadStatus === 'success' && geoJsonData && (
                    <div className="map-container">
                        <Alert variant="success">
                            Fichiers envoyés avec succès ! Aperçu du GeoJSON ci-dessous :
                        </Alert>
                        <MapContainer 
                            style={{ height: '400px', width: '100%' }} 
                            center={[44.837789, -0.57918]} 
                            zoom={12}
                        >
                            <TileLayer
                                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                            />
                            <GeoJSON data={geoJsonData} />
                            {bounds && <FitBounds bounds={bounds} />}
                        </MapContainer>
                    </div>
                )}
            </Col>
        </Row>
    );
};

export default MO_gemapiTab;
