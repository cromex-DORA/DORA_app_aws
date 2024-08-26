import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapDEPMOgemapi.css'; // Assurez-vous que ce chemin est correct

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
        }
    });

    return null;
};

const MapComponent = ({ selectedOption, highlightedFeatureId, onFeatureHover, onFeatureClick }) => {
    const [geoJsonData, setGeoJsonData] = useState(null);
    const [bounds, setBounds] = useState(null);
    const [zoomLevel, setZoomLevel] = useState(null);
    const geoJsonLayerRef = useRef();


    useEffect(() => {
        const token = localStorage.getItem('token');
        console.log("Selected Option:", selectedOption);
        
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

    useEffect(() => {
        console.log("Selected Option:", selectedOption);
    }, [selectedOption]);    

    const onEachFeature = (feature, layer) => {
        const featureId = feature.properties.id;
        const featureName = feature.properties.NOM_MO;

        if (zoomLevel >= 10) { // Afficher le label si le niveau de zoom est 10 ou plus
            layer.bindTooltip(featureName, { permanent: true, direction: "center", className: "polygon-label" });
        } else {
            layer.unbindTooltip(); // Supprimer le label si le niveau de zoom est inférieur à 10
        }

        layer.on({
            mouseover: () => onFeatureHover(featureId),
            mouseout: () => onFeatureHover(null),
            click: () => onFeatureClick(featureId)
        });
    };

    const filteredGeoJsonData = geoJsonData ? {
        ...geoJsonData,
        features: geoJsonData.features.filter(feature => {
            // Utiliser la valeur du filtre sélectionné
            const typeMO = feature.properties['TYPE_MO'];
            return selectedOption ? typeMO === selectedOption : true;
        })
    } : null;

    return (
        <MapContainer
            className="map-container" // Appliquer le style CSS ici
        >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {filteredGeoJsonData && (
                <GeoJSON data={filteredGeoJsonData}
                 ref={geoJsonLayerRef}
                  onEachFeature={onEachFeature}
                  key={`${selectedOption}-${filteredGeoJsonData.features.length}`} />
            )}
            {bounds && <FitBounds bounds={bounds} />}
            <MapEvents setZoomLevel={setZoomLevel} />
        </MapContainer>
    );
};

export default MapComponent;
