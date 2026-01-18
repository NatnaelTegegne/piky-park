const MAPBOX_ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

export const fetchParkingData = async () => {
  try {
    const response = await fetch('/parking-data.json');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data.parkingSpots || [];
  } catch (error) {
    console.error('Error fetching parking data:', error);
    return [];
  }
};

export const searchLocation = async (query) => {
  if (!query) return [];
  
  const geocodingUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${MAPBOX_ACCESS_TOKEN}&autocomplete=true`;
  
  try {
    const response = await fetch(geocodingUrl);
    const data = await response.json();
    return data.features || [];
  } catch (error) {
    console.error('Error searching location:', error);
    return [];
  }
};

export const getDirections = async (start, end) => {
  const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${MAPBOX_ACCESS_TOKEN}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    if (data.routes && data.routes.length > 0) {
      return data.routes[0].geometry.coordinates;
    }
    return null;
  } catch (error) {
    console.error('Error fetching directions:', error);
    return null;
  }
};
