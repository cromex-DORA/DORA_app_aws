// ParentComponent.js
import React, { useState } from 'react';
import MapComponent from './MapDEPMOgemapi';
import FilterComponent from './FilterComponent';
import UploadModal from './UploadModal';
import { Button } from 'react-bootstrap'; // Assurez-vous d'importer Button de react-bootstrap

const ParentComponent = ({ highlightedFeatureId, onFeatureHover, onFeatureClick, onFeatureMouseOver }) => {
    const [selectedOption, setSelectedOption] = useState("Syndicat");
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <div style={{ display: 'flex', height: '100%', border: '1px solid red' }}>
            <div style={{ width: '20%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div style={{ flexGrow: 1 }}>
                    <FilterComponent selectedOption={selectedOption} setSelectedOption={setSelectedOption} />
                </div>
                <Button 
                    onClick={() => setIsModalOpen(true)} 
                    variant="primary" 
                    style={{ marginTop: '10px' }}
                >
                    Upload SHP
                </Button>
                {isModalOpen && <UploadModal setIsModalOpen={setIsModalOpen} />}
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <MapComponent
                    selectedOption={selectedOption}
                    highlightedFeatureId={highlightedFeatureId}
                    onFeatureHover={onFeatureHover}
                    onFeatureClick={onFeatureClick}
                    onFeatureMouseOver={onFeatureMouseOver}
                />
            </div>
        </div>
    );
};

export default ParentComponent;
