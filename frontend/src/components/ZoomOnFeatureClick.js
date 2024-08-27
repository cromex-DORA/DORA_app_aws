import React, { useEffect, useCallback } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet'; // Assurez-vous d'importer L pour les fonctions de Leaflet

const ZoomOnFeatureClick = ({ geoJsonLayerRef }) => {
    const map = useMap();

    const handleFeatureClick = useCallback((e) => {
        const layer = e.target;
        const bounds = layer.getBounds();
        console.log('Feature clicked:', layer);
        console.log('Bounds of clicked feature:', bounds);

        if (bounds) {
            map.fitBounds(bounds, { padding: [45, 45] }); // Ajuste le zoom pour inclure le polygone avec du padding
            console.log('Map zoomed to feature bounds');
        }
    }, [map]);

    useEffect(() => {
        if (geoJsonLayerRef.current) {
            console.log('geoJsonLayerRef.current is available');

            // Associer les événements de clic aux couches GeoJSON
            geoJsonLayerRef.current.eachLayer(layer => { 
                console.log('Layer found:', layer);
                if (layer instanceof L.Layer) {
                    layer.on('click', handleFeatureClick);
                }
            }); 

            return () => {
                if (geoJsonLayerRef.current) {
                    console.log('Cleaning up geoJsonLayerRef.current');
                    geoJsonLayerRef.current.eachLayer(layer => {
                        if (layer instanceof L.Layer) {
                            layer.off('click', handleFeatureClick);
                        }
                    });
                }
            };
        } else {
            console.log('geoJsonLayerRef.current is not available');
        }
    }, [geoJsonLayerRef, handleFeatureClick]);

    return null;
};

export default ZoomOnFeatureClick;
