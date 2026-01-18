import { useState, useEffect, useCallback } from 'react';
import MapboxMap from './features/map/MapboxMap';
import SearchBox from './features/search/SearchBox';
import { getDirections } from './services/api'; 
import './styles/App.css';

function App() {
  const [userLocation, setUserLocation] = useState(null); //stores lat and lng
  const [parkingSpots, setParkingSpots] = useState([]); //stores list of markers to draw on the map
  const [route, setRoute] = useState(null); // for navigation
  const [searchLocation, setSearchLocation] = useState(null); //coordinates used when user searches a place in the search bar
  const [flyToLocation, setFlyToLocation] = useState(null);

  useEffect(() => {
    setUserLocation([ -122.4677, 37.7705]); //set this to Pitt
  }, []);

  // AGGREGATION LOGIC
  //combine all spots into one pin

  useEffect(() => {
    const fetchLiveStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/mapbox-data'); //calls the python backend to get current list of spots
        const data = await response.json();

        // Safety check: to make sure we have spots to aggregate
        if (!data.spots || data.spots.length === 0) return;

        // 1. Calculate Totals
        // The backend already gives us 'total_available', but let's recalculate to be safe
        // Logic: 1 = Free, 0 = Occupied. Sum them up.
        const availableCount = data.spots.reduce((sum, spot) => sum + (spot.status === 1 ? 1 : 0), 0);
        const capacity = data.spots.length;

        // 2. Determine Location of the "Main Lot"
        // We simply use the coordinates of the FIRST spot as the "Entrance" to the lot.
        const mainLotLocation = {
            lat: data.spots[0].lat,
            lng: data.spots[0].lng
        };

        // 3. Create SINGLE Virtual Marker
        const mainParkingLot = {
            id: "main_garage_1",
            name: "Main Campus Garage", // You can rename this
            address: "Live Capacity Feed",
            lat: mainLotLocation.lat,
            lng: mainLotLocation.lng,
            
            // This is what puts the number on the pin
            spotsAvailable: availableCount,
            totalSpots: capacity
        };

        // 4. Update State with an array containing ONLY this one marker
        setParkingSpots([mainParkingLot]);

      } catch (error) {
        console.error("Backend Error", error);
      }
    };

    fetchLiveStatus();
    const intervalId = setInterval(fetchLiveStatus, 2000); // Update every 2 seconds
    return () => clearInterval(intervalId);
  }, []);

  // Standard Map Handlers
  const handleLocationSelect = (coords) => { setSearchLocation(coords); setFlyToLocation(coords); };
  const calculateRoute = useCallback(async (start, end) => { const r = await getDirections(start, end); setRoute(r); }, []);

  return (
    <div className="App">
      <header className="app-header">
        <h1>Parking Spot Finder</h1>
        <SearchBox onLocationSelect={handleLocationSelect} />
      </header>
      <main>
        <MapboxMap 
          userLocation={userLocation}
          setUserLocation={setUserLocation}
          parkingSpots={parkingSpots} 
          route={route}
          calculateRoute={calculateRoute}
          searchLocation={searchLocation}
          onSearchLocationSelect={flyToLocation}
        />
      </main>
    </div>
  )
}

export default App;