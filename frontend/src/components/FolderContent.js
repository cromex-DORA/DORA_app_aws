import React, { useState, useEffect } from 'react';
import MapDEPMOgemapi from './MapDEPMOgemapi';
import FolderList from './FolderList';
import './FolderContent.css';

const FolderContent = () => {
    const [folders, setFolders] = useState([]);
    const [files, setFiles] = useState([]);
    const [currentPath, setCurrentPath] = useState('');
    const [folderName, setFolderName] = useState('');
    const [selectedFolderId, setSelectedFolderId] = useState(null);
    const [geoJsonData, setGeoJsonData] = useState(null);
    const [view, setView] = useState('folders'); // 'folders' or 'files'
    const [bounds, setBounds] = useState([]);

    const fetchContent = async () => {
        const token = localStorage.getItem('token');
        try {
            // Fetch GeoJSON Data
            const geoResponse = await fetch(`${process.env.REACT_APP_IP_SERV}/geojson_complet_folders`, {
                headers: { 'Authorization': token }
            });
            if (!geoResponse.ok) throw new Error(`HTTP error! Status: ${geoResponse.status}`);
            const geoJsonData = await geoResponse.json();
            setGeoJsonData(geoJsonData);

            // Extract folders from geoJsonData
            const folderData = geoJsonData.features.map(feature => ({
                id: feature.id,
                name: feature.properties.NOM_MO,
                files: feature.properties.files || []  // Assume files are in properties
            }));
            
            setFolders(folderData);

            // Fetch Bounds Data
            const bboxResponse = await fetch(`${process.env.REACT_APP_IP_SERV}/bb_box`, {
                headers: { 'Authorization': token }
            });
            if (!bboxResponse.ok) throw new Error(`HTTP error! Status: ${bboxResponse.status}`);
            const bboxData = await bboxResponse.json();
            setBounds([
                [bboxData.miny, bboxData.minx],
                [bboxData.maxy, bboxData.maxx]
            ]);

        } catch (error) {
            console.error('Fetching content failed:', error);
        }
    };

    useEffect(() => {
        fetchContent();
    }, []);

    useEffect(() => {
        if (selectedFolderId) {
            const selectedFolder = folders.find(folder => folder.id === selectedFolderId);
            if (selectedFolder) {
                setFiles(selectedFolder.files || []);
                setCurrentPath(selectedFolder.path || '');
                setFolderName(selectedFolder.name || '');
                setView('files');
            }
        }
    }, [selectedFolderId, folders]);

    const handleFolderClick = (folder) => {
        setSelectedFolderId(folder.id);
        setFiles(folder.files || []);
        setCurrentPath(folder.path || '');
        setFolderName(folder.name || '');
        setView('files');
    };

    const handleBackClick = () => {
        setSelectedFolderId(null);
        setFiles([]);
        setCurrentPath('');
        setFolderName('');
        setView('folders');
    };

    return (
        <div className="container">
            <div className="folder-list-container">
                {/* Afficher le bouton "Back" seulement si nous ne sommes pas dans la vue des dossiers */}
                {view === 'files' && (
                    <button onClick={handleBackClick} style={{ marginBottom: '10px' }}>
                        Back
                    </button>
                )}
                <FolderList
                    folders={view === 'folders' ? folders : []}
                    files={view === 'files' ? files : []}
                    currentPath={currentPath}
                    folderName={folderName}
                    handleFolderClick={handleFolderClick}
                    downloadFile={(file) => { /* Télécharger le fichier */ }}
                    highlightedFolderId={selectedFolderId}
                />
            </div>
            <div className="map-container">
                <MapDEPMOgemapi
                    geoJsonData={geoJsonData}
                    setSelectedFolderId={setSelectedFolderId}
                    bounds={bounds}
                />
            </div>
            <div className="info-panel-section">
                {/* Autres sections ou informations */}
            </div>
            <div className="other-section">
                {/* Autres sections ou informations */}
            </div>
        </div>
    );
};

export default FolderContent;
