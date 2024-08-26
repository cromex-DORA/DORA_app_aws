import React, { useState, useEffect } from 'react';
import ParentComponent from './ParentComponentMAPDEPMOgemapi';
import InfoPanel from './InfoPanel';
import UploadModal from './UploadModal';
import FolderList from './FolderList';
import FilterComponent from './FilterComponent';
import './FolderContent.css';

const FolderContent = () => {
    const [files, setFiles] = useState([]);
    const [folders, setFolders] = useState([]);
    const [currentPath, setCurrentPath] = useState('');
    const [folderName, setFolderName] = useState('');
    const [showFileList, setShowFileList] = useState(false);
    const [infoPanel, setInfoPanel] = useState(null);
    const [info, setInfo] = useState(null); // Pour stocker les informations à afficher
    const [highlightedFeatureId, setHighlightedFeatureId] = useState(null);
    const [highlightedFolderId, setHighlightedFolderId] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedOption, setSelectedOption] = useState('');
    


const fetchContent = async (path = '') => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${process.env.REACT_APP_IP_SERV}/folder`, {
            headers: {
                'Authorization': token,
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched Data:', data);  // Ajouter cette ligne pour vérifier les données reçues

        setFiles(data.files || []);
        setFolders(data.folders || []);
        setCurrentPath(data.current_path || '');

        const pathParts = data.current_path.split('/');
        if (pathParts.length === 1 && pathParts[0] !== '') {
            setFolderName(pathParts[0]);
        } else {
            setFolderName('');
        }
    } catch (error) {
        console.error('Fetching content failed:', error);
    }
};


    useEffect(() => {
        fetchContent();
    }, []);

    const handleBackClick = () => {
        const pathParts = currentPath.split('/').filter(part => part);
        const parentPath = pathParts.slice(0, -1).join('/') + '/';
        fetchContent(parentPath || ''); // Passer un chemin vide pour la racine
    };

    const handleFeatureHover = (featureId) => {
        setHighlightedFeatureId(featureId);
    };

    const fetchInfo = async (id) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(`${process.env.REACT_APP_IP_SERV}/info/${id}`, {
                headers: {
                    'Authorization': token,
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Fetched Info:', data);
            setInfoPanel(data);
        } catch (error) {
            console.error('Error fetching info:', error);
            setInfoPanel(null);
        }
    };

const handleEntityClick = async (id) => {
    console.log('Entity Clicked ID:', id);

    // Cherche le dossier correspondant dans la liste des folders
    const folder = folders.find(folder => folder.id === id);

    // Si le dossier est trouvé, on met à jour les états avec ses informations
    if (folder) {
        console.log('Folder found:', folder);
        setCurrentPath(folder.path || '');  // Vérification que le chemin existe
        setFolderName(folder.name || '');  // Vérification que le nom existe
        setFiles(folder.files || []);  // Vérification que la liste de fichiers existe
        setFolders(folder.folders || []);  // Vérification que la liste de sous-dossiers existe
        setShowFileList(true);
        setHighlightedFeatureId(null); 
        await fetchInfo(folder.id); // Récupère et met à jour le panneau d'information
        return;
    }

    // Si aucun dossier n'est trouvé, on vérifie si c'est une entité sélectionnée dans les features
    const feature = highlightedFeatureId === id ? { id: id } : null; // Utilisation de l'ID de la feature
    if (feature) {
        console.log('Feature found:', feature);
        // Comme le dossier est undefined, on évite de l'utiliser ici
        setCurrentPath(currentPath || '');  // Utilise le chemin actuel
        setFolderName('');  // Réinitialise le nom du dossier (aucun nom de dossier dans ce cas)
        setFiles([]);  // Réinitialise la liste des fichiers
        setFolders([]);  // Réinitialise la liste des dossiers
        setShowFileList(false);
        await fetchInfo(feature.id); // Récupère et met à jour le panneau d'information
    } else {
        console.error('No folder or feature found for the clicked ID:', id);
    }
};



    const handleFolderClick = (folder) => {
        if (folder) {
            handleEntityClick(folder.id);
        } else {
            handleBackClick();
        }
    };

    const handleFeatureClick = (featureId) => {
        handleEntityClick(featureId);
    };

    const handleFeatureMouseOver = (featureId) => {
        setHighlightedFolderId(featureId);
    };

    useEffect(() => {
        setHighlightedFolderId(highlightedFeatureId);
    }, [highlightedFeatureId]);

    const downloadFile = (filePath) => {
        const token = localStorage.getItem('token');
        fetch(`${process.env.REACT_APP_IP_SERV}/download?file=${filePath}`, {
            headers: {
                'Authorization': token,
            }
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Download failed');
            }
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filePath.split('/').pop();
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => console.error('Error downloading file:', error));
    };

    useEffect(() => {
        console.log('Info Panel:', infoPanel);
    }, [infoPanel]);

    const showBackButton = currentPath && currentPath !== '/';

   return (
        <div className="folder-content-container">

            <div className="folder-list-section">
                <h2>DORA v0.1</h2>
                
                <p>{folderName || 'Liste des MO'}</p>
                <FolderList 
                    folders={folders} 
                    files={files} 
                    currentPath={currentPath}
                    folderName={folderName}
                    highlightedFolderId={highlightedFolderId}
                    handleFolderClick={handleFolderClick}
                    setHighlightedFeatureId={setHighlightedFeatureId}
                    downloadFile={downloadFile}
                    setIsModalOpen={setIsModalOpen} // Pass the state setter to FolderList
                />
                {showBackButton && <button onClick={handleBackClick}>Back</button>}
            </div>
            
            <div className="map-section">
                {/* Ajoutez le composant de carte ici */}
                <ParentComponent 
                    highlightedFeatureId={highlightedFeatureId} 
                    onFeatureHover={handleFeatureHover} 
                    onFeatureClick={handleFeatureClick}
                    onFeatureMouseOver={handleFeatureMouseOver}
                    selectedOption={selectedOption} // Passez le filtre à la carte
                />
                {showFileList && infoPanel && <InfoPanel info={infoPanel} />}
            </div>
            {/* Affichage de la modale si elle est ouverte */}
            {isModalOpen && <UploadModal setIsModalOpen={setIsModalOpen} />}
        </div>
    );
};

export default FolderContent;
