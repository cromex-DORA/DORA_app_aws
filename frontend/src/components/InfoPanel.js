import React from 'react';

const InfoPanel = ({ info }) => {
    if (!info) return null;

    return (
        <div style={{ position: 'fixed', bottom: 0, left: 0, width: '300px', padding: '10px', backgroundColor: 'white', border: '1px solid black' }}>
            <h3>{info.name}</h3>
            <p>{info.description}</p>
            <p>{info.details}</p>
        </div>
    );
};

export default InfoPanel;
