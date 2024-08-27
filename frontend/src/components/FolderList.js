import React, { useState } from 'react';

const FolderList = ({
    folders, 
    files, 
    currentPath, 
    folderName, 
    highlightedFolderId, 
    setHighlightedFolderId, 
    handleFolderClick, 
    downloadFile
}) => {
    const [searchQuery, setSearchQuery] = useState('');

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
                {filteredFolders.map((folder) => (
                    <li
                        key={folder.id}
                        onClick={() => handleFolderClick(folder)}
                        onMouseOver={() => setHighlightedFolderId(folder.id)}
                        onMouseOut={() => setHighlightedFolderId(null)}
                        style={{
                            cursor: 'pointer',
                            color: highlightedFolderId === folder.id ? 'red' : 'blue',
                            fontWeight: highlightedFolderId === folder.id ? 'bold' : 'normal'
                        }}
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
