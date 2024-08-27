import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
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
    const mapRef = useRef();
    const geoJsonLayerRef = useRef();

    useEffect(() => {
        if (geoJsonLayerRef.current && geoJsonData) {
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
    }, [highlightedFolderId, geoJsonData]);

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
        <MapContainer
            center={[44, -0.98196]}
            zoom={14}
            className="map-container" // Appliquez la classe CSS ici
            whenCreated={map => { mapRef.current = map; }}
        >
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {geoJsonData && (
                <GeoJSON
                    data={geoJsonData}
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
    );
};

export default MapDEPMOgemapi;
