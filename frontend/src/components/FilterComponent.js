import React from 'react';

const FilterComponent = ({ selectedOption, setSelectedOption }) => {
    return (
        <div className="filter-component" style={{ marginBottom: '10px' }}>
            <h2>Type de Maitres d'ouvrages</h2>
            {/* Liste déroulante */}
            <select
                value={selectedOption}
                onChange={(e) => {
                    console.log("New Selected Option:", e.target.value); // <-- Ajoutez ce log ici
                    setSelectedOption(e.target.value);
                }}
                style={{ marginBottom: '10px' }}
            >
                <option value="">Type de Gemapien</option>
                <option value="EPTB">EPTB</option>
                <option value="Syndicat">Syndicat</option>
                <option value="EPCI">EPCI</option>
            </select>
        </div>
    );
};

export default FilterComponent;
