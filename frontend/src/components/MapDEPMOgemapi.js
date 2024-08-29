import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import FiltretypeMO from './FiltretypeMO';
import 'leaflet/dist/leaflet.css';
import './MapDEPMOgemapi.css';

const MapViewUpdater = ({ bounds }) => {
    const map = useMap();

    useEffect(() => {
        if (bounds && bounds.length === 2) {
            map.fitBounds(bounds);
        }
    }, [bounds, map]);

    return null;
};

const MapDEPMOgemapi = ({ geoJsonData, setSelectedFolderId, bounds, highlightedFolderId, setHighlightedFolderId }) => {
    const [filter, setFilter] = useState('Syndicat');
    const [filteredGeoJsonData, setFilteredGeoJsonData] = useState(null);
    const mapRef = useRef();
    const geoJsonLayerRef = useRef();


    // Effect to filter GeoJSON data when geoJsonData or filter changes
    useEffect(() => {
        if (geoJsonData) {
            const updatedFilteredData = {
            ...geoJsonData,
                    features: geoJsonData.features.filter(feature => {
                        // Utiliser la valeur du filtre sélectionné
                        const typeMO = feature.properties['TYPE_MO'];
                        return filter ? typeMO === filter : true;
                    })
            };
            setFilteredGeoJsonData(updatedFilteredData);
        }
    }, [filter,geoJsonData]);

    useEffect(() => {
        if (geoJsonLayerRef.current && filteredGeoJsonData) {
            geoJsonLayerRef.current.eachLayer(layer => {
                const featureId = layer.feature.id;
                if (highlightedFolderId === featureId) {
                    layer.setStyle({
                        weight: 8,
                        color: '#ff0000',
                        opacity: 0.8
                    });
                } else {
                    layer.setStyle({
                        weight: 5,
                        color: '#0000ff',
                        opacity: 0.65
                    });
                }
            });
        }
    }, [highlightedFolderId, filteredGeoJsonData]);

    const onEachFeature = (feature, layer) => {
        layer.on({
            click: () => {
                setSelectedFolderId(feature.id);
            },
            mouseover: () => {
                setHighlightedFolderId(feature.id);
                layer.setStyle({
                    weight: 8,
                    color: '#ff0000',
                    opacity: 0.8
                });
            },
            mouseout: () => {
                if (feature.id !== highlightedFolderId) {
                    layer.setStyle({
                        weight: 5,
                        color: '#0000ff',
                        opacity: 0.65
                    });
                }
                setHighlightedFolderId(null);
            }
        });
    };

    return (
        <div className="map-container">
            <FiltretypeMO selectedOption={filter} setSelectedOption={setFilter} />
            <MapContainer
                center={[44, -0.98196]}
                zoom={14}
                className="map"
                whenCreated={map => { mapRef.current = map; }}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {filteredGeoJsonData && (
                    <GeoJSON
                        key={JSON.stringify(filteredGeoJsonData)}
                        data={filteredGeoJsonData}
                        onEachFeature={onEachFeature}
                        style={{
                            color: '#0000ff',
                            weight: 5,
                            opacity: 0.65
                        }}
                        ref={geoJsonLayerRef}
                    />
                )}
                <MapViewUpdater bounds={bounds} />
            </MapContainer>
        </div>
    );
};

export default MapDEPMOgemapi;
