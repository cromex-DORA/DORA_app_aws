import React, { useState } from 'react';

const FolderList = ({
    folders, 
    files, 
    currentPath, 
    folderName, 
    highlightedFolderId, 
    handleFolderClick, 
    setHighlightedFeatureId, 
    downloadFile,
    setIsModalOpen
}) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedOption, setSelectedOption] = useState('');

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value.toLowerCase());
    };

    const filteredFolders = folders.filter(folder =>
        folder.name.toLowerCase().includes(searchQuery)
    );

    return (
        <div>
            {/* Champ de recherche */}
            <input
                type="text"
                placeholder="Rechercher un dossier..."
                value={searchQuery}
                onChange={handleSearchChange}
                style={{ marginBottom: '10px', display: 'block' }}
            />

            {/* Liste des dossiers filtrés */}
            <ul>
                {filteredFolders.map((folder, index) => (
                    <li
                        key={index}
                        onClick={() => handleFolderClick(folder)}
                        onMouseEnter={() => setHighlightedFeatureId(folder.id)}
                        onMouseLeave={() => setHighlightedFeatureId(null)}
                        style={{ cursor: 'pointer', color: highlightedFolderId === folder.id ? 'red' : 'blue' }}
                    >
                        📁 {folder.name}
                    </li>
                ))}
                {files.map((file, index) => (
                    <li key={index}>
                        <span
                            onClick={() => downloadFile(currentPath ? `${currentPath}/${file}` : file)}
                            style={{ cursor: 'pointer', color: 'blue' }}
                        >
                            {file}
                        </span>
                    </li>
                ))}
            </ul>

            {/* Bouton pour ouvrir la modale d'upload */}
            <button onClick={() => setIsModalOpen(true)}>Upload SHP</button>
        </div>
    );
};

export default FolderList;
