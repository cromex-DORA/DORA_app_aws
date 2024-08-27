import React, { useState } from 'react';

const FolderList = ({
    folders, 
    files, 
    currentPath, 
    folderName, 
    highlightedFolderId, 
    handleFolderClick, 
    downloadFile
}) => {
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value.toLowerCase());
    };

    // Assurez-vous que `folder.name` est bien une chaîne avant d'appeler `toLowerCase()`
    const filteredFolders = folders.filter(folder =>
        typeof folder.name === 'string' && folder.name.toLowerCase().includes(searchQuery)
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
                        key={folder.id || index}  // Assurez-vous que `folder.id` est unique
                        onClick={() => handleFolderClick(folder)}
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
        </div>
    );
};

export default FolderList;
