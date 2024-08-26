import React, { useState } from 'react';
import MapComponent from './MapDEPMOgemapi';
import FilterComponent from './FilterComponent';

const ParentComponent = ({ highlightedFeatureId, onFeatureHover, onFeatureClick, onFeatureMouseOver }) => {
    const [selectedOption, setSelectedOption] = useState("Syndicat");
    console.log("Selected Option in ParentComponent:", selectedOption);
    const handleClick = (featureId) => {
        if (onFeatureClick) {
            onFeatureClick(featureId);
        }
    };

    return (
        <div style={{ display: 'flex', height: '100%', border: '1px solid red' }}>
            <div style={{ width: '20%', display: 'flex', flexDirection: 'column' }}>
                <FilterComponent selectedOption={selectedOption} setSelectedOption={setSelectedOption} />
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <MapComponent
                    selectedOption={selectedOption}
                    highlightedFeatureId={highlightedFeatureId}
                    onFeatureHover={onFeatureHover}
                    onFeatureClick={onFeatureClick}
                    onFeatureMouseOver={onFeatureMouseOver} // Passer la fonction de survol
                />
            </div>
        </div>
    );
};

export default ParentComponent;
