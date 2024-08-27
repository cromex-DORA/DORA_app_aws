import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import GeoJSONRewind from './GeoJSONRewind'; // Assurez-vous que ce chemin est correct

const MapDEPMOgemapi = ({ geoJsonData, setSelectedFolderId, bounds }) => {
    const [rewoundGeoJson, setRewoundGeoJson] = useState(null);
    const mapRef = useRef();

    // Fonction pour gérer les clics sur les polygones
    const onEachFeature = (feature, layer) => {
        layer.on({
            click: () => {
                const folderId = feature.id; // ID du polygone
                setSelectedFolderId(folderId); // Met à jour l'ID du dossier sélectionné
            }
        });
    };

    useEffect(() => {
        if (geoJsonData) {
            const rewind = new GeoJSONRewind();
            const rewoundData = rewind.rewind(JSON.parse(JSON.stringify(geoJsonData))); // Clone et rewind
            setRewoundGeoJson(rewoundData);
        }
    }, [geoJsonData]);

    // Hook to update map view
    const MapViewUpdater = ({ bounds }) => {
        const map = useMap();
        useEffect(() => {
            if (bounds && bounds.length === 2) {
                map.fitBounds(bounds);
            }
        }, [bounds, map]);
        return null;
    };

    return (
        <MapContainer
            center={[60.7681, -73.98196]} // Valeur par défaut, sera mise à jour par fitBounds
            zoom={14}
            style={{ height: '400px', width: '100%' }} // Ajustez les dimensions si nécessaire
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {rewoundGeoJson && (
                <GeoJSON
                    data={rewoundGeoJson}
                    onEachFeature={onEachFeature}
                    style={{
                        color: '#ff7800',
                        weight: 5,
                        opacity: 0.65
                    }}
                />
            )}
            <MapViewUpdater bounds={bounds} />
        </MapContainer>
    );
};

export default MapDEPMOgemapi;
