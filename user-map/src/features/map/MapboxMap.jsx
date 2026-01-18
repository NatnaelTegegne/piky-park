import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

//map element and related variables
const MapboxMap = ({ userLocation, setUserLocation, parkingSpots, route, calculateRoute, searchLocation, onSearchLocationSelect }) => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const userMarkerRef = useRef(null);
  const markersRef = useRef([]);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const [hasFlownToUser, setHasFlownToUser] = useState(false);
  const [lng, setLng] = useState(parseFloat(import.meta.env.VITE_MAP_CENTER_LNG) || -122.4194);
  const [lat, setLat] = useState(parseFloat(import.meta.env.VITE_MAP_CENTER_LAT) || 37.7749);
  const [zoom, setZoom] = useState(parseFloat(import.meta.env.VITE_MAP_ZOOM) || 12);


  useEffect(() => {
    if (map.current) return; //initialize map only once

    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'raster-tiles': {
            type: 'raster',
            tiles: [
              'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
              'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
              'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors'
          }
        },
        layers: [
          {
            id: 'simple-tiles',
            type: 'raster',
            source: 'raster-tiles',
            minzoom: 0,
            maxzoom: 22
          }
        ]
      },
      center: [lng, lat],
      zoom: zoom
    });

    map.current.on('load', () => {
      setIsMapLoaded(true);
    });

    map.current.on('move', () => {
      setLng(map.current.getCenter().lng.toFixed(4));
      setLat(map.current.getCenter().lat.toFixed(4));
      setZoom(map.current.getZoom().toFixed(2));
    });

    //navigation controls
    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
    
    //geolocate controls
    const geolocate = new mapboxgl.GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true
      },
      trackUserLocation: true,
      showUserHeading: true
    });

    map.current.addControl(geolocate, 'top-right');

    geolocate.on('geolocate', (e) => {
      try {
        setUserLocation([e.coords.longitude, e.coords.latitude]);
      } catch (error) {
        console.error('Error setting user location from geolocation:', error);
      }
    });


  }, []);



  useEffect(() => {
    if (!isMapLoaded || parkingSpots.length === 0) return;

    //clear existing parking markers
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    //add new destination markers
    parkingSpots.forEach(spot => {
      const availabilityPercentage = (spot.spotsAvailable / spot.totalSpots) * 100;
      let markerColor;

      if (availabilityPercentage >= 50) {
        markerColor = '#0c8d00ff';
      } else if (availabilityPercentage > 0) {
        // Gradient from yellow to green-yellow
        const percentageOfGradient = availabilityPercentage / 50;
        const red = Math.round(255 - (255 - 173) * percentageOfGradient);
        const green = 255;
        const blue = Math.round(47 * percentageOfGradient);
        markerColor = `rgb(${red}, ${green}, ${blue})`;
      } else {
        markerColor = '#F44336';
      }

      const availabilityStatus = spot.spotsAvailable > 0 ? `Available Spots: ${spot.spotsAvailable}/${spot.totalSpots}` : 'Full';
      const popup = new mapboxgl.Popup({ offset: 25 })
        .setHTML(`<h3>${spot.name}</h3><p>${spot.address}</p><p style="color: #000000; font-weight: bold;">${availabilityStatus}</p>`);

      const markerElement = document.createElement('div');
      markerElement.className = 'custom-marker';
      markerElement.style.backgroundColor = markerColor;
      markerElement.innerText = spot.spotsAvailable;

      markerElement.addEventListener('click', () => {
        if (userLocation) {
          calculateRoute(userLocation, [spot.lng, spot.lat]);
        } else {
          alert('User location not available. Please enable location services.');
        }
      });

      const marker = new mapboxgl.Marker(markerElement)
        .setLngLat([spot.lng, spot.lat])
        .setPopup(popup)
        .addTo(map.current);
      
      markersRef.current.push(marker);
    });
  }, [parkingSpots, isMapLoaded, userLocation]);

  useEffect(() => {
    if (!isMapLoaded || !userLocation) return;

    //clear existing user location marker
    if (userMarkerRef.current) {
      userMarkerRef.current.remove();
    }

    //add user location marker
    const userMarkerElement = document.createElement('div');
    userMarkerElement.className = 'user-location-marker';

    userMarkerRef.current = new mapboxgl.Marker(userMarkerElement)
      .setLngLat(userLocation)
      .setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML('<h3>Your Location</h3>'))
      .addTo(map.current);

    if (!hasFlownToUser) {
      map.current.flyTo({
        center: userLocation,
        zoom: 14,
        essential: true
      });
      setHasFlownToUser(true);
    }
  }, [userLocation, isMapLoaded, hasFlownToUser]);

  useEffect(() => {
    if (!isMapLoaded || !route || route.length === 0) return;

    try {
      if (map.current.getSource('route')) {
        map.current.removeLayer('route');
        map.current.removeSource('route');
      }

      map.current.addSource('route', {
        'type': 'geojson',
        'data': {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'LineString',
            'coordinates': route
          }
        }
      });

      map.current.addLayer({
        'id': 'route',
        'type': 'line',
        'source': 'route',
        'layout': {
          'line-join': 'round',
          'line-cap': 'round'
        },
        'paint': {
          'line-color': '#3887be',
          'line-width': 5,
          'line-opacity': 0.75
        }
      });

      if (route.length > 0) {
        const bounds = new mapboxgl.LngLatBounds(route[0], route[0]);
        for (const coord of route) {
          bounds.extend(coord);
        }
        map.current.fitBounds(bounds, {
          padding: 50
        });
      }
    } catch (error) {
      console.error('Error updating route:', error);
    }

  }, [route, isMapLoaded]);

  useEffect(() => {
    if (!map.current || !onSearchLocationSelect) return;

    map.current.flyTo({
      center: onSearchLocationSelect,
      essential: true
    });
  }, [onSearchLocationSelect]);

  //sidebar with location information
  return (
    <div className="map-container">
      <div className="sidebar">
        Map Location: {lng}, {lat}
      </div>
      <div ref={mapContainer} className="map" />
    </div>
  );
};

export default MapboxMap;
