import React, { useEffect, useState, useRef, useCallback } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapDEPMOgemapi.css'; // Assurez-vous que ce chemin est correct

// Composant pour configurer le zoomSnap
const MapConfig = () => {
    const map = useMap();

    useEffect(() => {
        if (map) {
            map.options.zoomSnap = 0.5; // Configure le zoomSnap
            map.setZoom(map.getZoom()); // Applique le changement de zoomSnap
        }
    }, [map]);

    return null;
};

// Composant pour ajuster les bornes de la carte
const FitBounds = ({ bounds }) => {
    const map = useMap();

    useEffect(() => {
        if (bounds) {
            map.fitBounds(bounds);
        }
    }, [bounds, map]);

    return null;
};

// Composant pour gérer les événements de la carte
const MapEvents = ({ setZoomLevel }) => {
    useMapEvents({
        zoomend: (e) => {
            const zoom = e.target.getZoom();
            setZoomLevel(zoom);
            console.log("niveau zoom:", zoom);
        }
    });

    return null;
};

// Composant pour gérer le zoom sur le polygone cliqué
const ZoomOnFeatureClick = ({ geoJsonData }) => {
    const map = useMap();

    useEffect(() => {
        if (geoJsonData) {
            // Fonction pour ajuster le zoom sur le polygone
            const zoomToFeature = (e) => {
                const layer = e.target;
                const bounds = layer.getBounds();
                if (bounds) {
                    map.fitBounds(bounds, { padding: [20, 20] }); // Ajuste le zoom pour inclure le polygone avec du padding
                }
            };

            // Associer les événements de clic aux couches GeoJSON

        }
    }, [map, geoJsonData]);

    return null;
};

const MapComponent = ({ selectedOption, highlightedFeatureId, onFeatureHover, onFeatureClick }) => {
    const [geoJsonData, setGeoJsonData] = useState(null);
    const [bounds, setBounds] = useState(null);
    const [zoomLevel, setZoomLevel] = useState(null);
    const geoJsonLayerRef = useRef();

    useEffect(() => {
        const token = localStorage.getItem('token');

        fetch('http://localhost:5000/carte_MIA_MO_syndicat', {
            headers: { 'Authorization': token }
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.features) {
                const rewind = new window.GeoJSONRewind();
                data.features = data.features.map(feature => {
                    if (feature.geometry.type === 'Polygon' || feature.geometry.type === 'MultiPolygon') {
                        feature.geometry = rewind.rewind(feature.geometry);
                    }
                    return feature;
                });
            }
            setGeoJsonData(data);
        })
        .catch(error => console.error('Error fetching GeoJSON data:', error));

        fetch('http://localhost:5000/bb_box', {
            headers: { 'Authorization': token }
        })
        .then(response => response.json())
        .then(settings => {
            const bounds = [
                [settings.miny, settings.minx],
                [settings.maxy, settings.maxx]
            ];
            setBounds(bounds);
        })
        .catch(error => console.error('Error fetching map settings:', error));
    }, []);

    useEffect(() => {
        if (geoJsonLayerRef.current) {
            geoJsonLayerRef.current.eachLayer(layer => {
                const featureId = layer.feature?.properties?.id;
                const isHighlighted = featureId === highlightedFeatureId;

                layer.setStyle({
                    weight: isHighlighted ? 5 : 2,
                    color: isHighlighted ? '#666' : '#3388ff',
                    fillOpacity: isHighlighted ? 0.7 : 0.5
                });
            });
        }
    }, [highlightedFeatureId, geoJsonData]);

    const updateLabels = useCallback(() => {
        if (geoJsonLayerRef.current) {
            geoJsonLayerRef.current.eachLayer(layer => {
                const featureId = layer.feature?.properties?.id;
                const featureName = layer.feature?.properties?.ALIAS;

                if (zoomLevel >= 9) {
                    layer.bindTooltip(featureName, { permanent: true, direction: "center", className: "polygon-label" });
                } else {
                    layer.unbindTooltip();
                }

                layer.on({
                    mouseover: () => onFeatureHover(featureId),
                    mouseout: () => onFeatureHover(null),
                    click: () => onFeatureClick(featureId)
                });
            });
        }
    }, [zoomLevel, onFeatureHover, onFeatureClick]);

    useEffect(() => {
        updateLabels();
    }, [zoomLevel, updateLabels]);

    const filteredGeoJsonData = geoJsonData ? {
        ...geoJsonData,
        features: geoJsonData.features.filter(feature => {
            const typeMO = feature.properties['TYPE_MO'];
            return selectedOption ? typeMO === selectedOption : true;
        })
    } : null;

    return (
        <MapContainer
            className="map-container"
            style={{ height: '100%', width: '100%' }}
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {filteredGeoJsonData && (
                <GeoJSON 
                    data={filteredGeoJsonData}
                    ref={geoJsonLayerRef}
                    key={`${selectedOption}-${filteredGeoJsonData.features.length}`} 
                />
            )}
            {bounds && <FitBounds bounds={bounds} />}
            <MapEvents setZoomLevel={setZoomLevel} />
            <MapConfig />
            <ZoomOnFeatureClick geoJsonData={filteredGeoJsonData} />
        </MapContainer>
    );
};

export default MapComponent;
