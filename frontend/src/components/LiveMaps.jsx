import React, { useState, useEffect, useRef } from 'react';
import './LiveMaps.css';

const LiveMaps = () => {
  const [currentLocation, setCurrentLocation] = useState(null);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const mapRef = useRef(null);

  // Traffic obstructions in Bangalore
  const predefinedLocations = [
    { 
      position: { lat: 12.9716, lng: 77.5946 }, 
      title: "Traffic Congestion", 
      snippet: "Heavy traffic on MG Road. Expect 20-30 min delays.", 
      icon: 'congestion' 
    }, // MG Road, Bangalore
    { 
      position: { lat: 12.9789, lng: 77.5917 }, 
      title: "Road Accident", 
      snippet: "Multi-vehicle collision on Brigade Road. Road partially blocked.", 
      icon: 'accident' 
    }, // Brigade Road
    { 
      position: { lat: 12.9758, lng: 77.5995 }, 
      title: "Pothole Alert", 
      snippet: "Large pothole on Residency Road. Drive carefully.", 
      icon: 'pothole' 
    }, // Residency Road
    { 
      position: { lat: 12.9721, lng: 77.5933 }, 
      title: "Construction Work", 
      snippet: "Metro construction on Church Street. Lane closure.", 
      icon: 'construction' 
    }, // Church Street
    { 
      position: { lat: 12.9769, lng: 77.5968 }, 
      title: "Traffic Signal Down", 
      snippet: "Traffic light malfunction at Richmond Circle.", 
      icon: 'signal' 
    }, // Richmond Circle
    { 
      position: { lat: 12.9738, lng: 77.5982 }, 
      title: "Waterlogging", 
      snippet: "Heavy rain causing waterlogging on St. Marks Road.", 
      icon: 'waterlogging' 
    }, // St. Marks Road
    { 
      position: { lat: 12.9745, lng: 77.5921 }, 
      title: "Vehicle Breakdown", 
      snippet: "Truck breakdown on Commercial Street. Traffic diverted.", 
      icon: 'breakdown' 
    }, // Commercial Street
    { 
      position: { lat: 12.9772, lng: 77.5949 }, 
      title: "Protest March", 
      snippet: "Protest march on Infantry Road. Expect delays.", 
      icon: 'protest' 
    }, // Infantry Road
    { 
      position: { lat: 12.9751, lng: 77.5975 }, 
      title: "Tree Fall", 
      snippet: "Tree fallen on Cunningham Road. Road blocked.", 
      icon: 'tree' 
    }, // Cunningham Road
    { 
      position: { lat: 12.9732, lng: 77.5958 }, 
      title: "Traffic Jam", 
      snippet: "Severe traffic jam on Lavelle Road. Avoid this route.", 
      icon: 'jam' 
    }  // Lavelle Road
  ];

  // Custom marker icons as SVG for traffic obstructions
  const getCustomMarkerIcon = (iconType) => {
    const icons = {
      congestion: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#FF9800" stroke="white" stroke-width="2"/>
            <path d="M8 12h16M8 16h16M8 20h16" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      accident: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#F44336" stroke="white" stroke-width="2"/>
            <path d="M12 8l8 16H4l8-16z" fill="white"/>
            <path d="M16 8v16" stroke="white" stroke-width="2"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      pothole: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#795548" stroke="white" stroke-width="2"/>
            <ellipse cx="16" cy="16" rx="6" ry="4" fill="white"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      construction: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#FFC107" stroke="white" stroke-width="2"/>
            <path d="M8 8l16 16M24 8L8 24" stroke="white" stroke-width="3" stroke-linecap="round"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      signal: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#9C27B0" stroke="white" stroke-width="2"/>
            <rect x="12" y="8" width="8" height="16" rx="2" fill="white"/>
            <circle cx="16" cy="12" r="2" fill="#F44336"/>
            <circle cx="16" cy="16" r="2" fill="#FFC107"/>
            <circle cx="16" cy="20" r="2" fill="#4CAF50"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      waterlogging: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#2196F3" stroke="white" stroke-width="2"/>
            <path d="M8 20c0-4 8-12 8-12s8 8 8 12" stroke="white" stroke-width="2" fill="none"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      breakdown: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#607D8B" stroke="white" stroke-width="2"/>
            <rect x="10" y="12" width="12" height="8" rx="1" fill="white"/>
            <circle cx="13" cy="20" r="2" fill="white"/>
            <circle cx="19" cy="20" r="2" fill="white"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      protest: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#E91E63" stroke="white" stroke-width="2"/>
            <path d="M8 16h16M12 12l4 4-4 4" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      tree: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#4CAF50" stroke="white" stroke-width="2"/>
            <path d="M16 8c-4 0-8 3-8 8s4 8 8 8 8-3 8-8-4-8-8-8z" fill="white"/>
            <rect x="14" y="20" width="4" height="6" fill="white"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      jam: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="#D32F2F" stroke="white" stroke-width="2"/>
            <path d="M8 12h16M8 16h16M8 20h16" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M12 10l8 12M20 10l-8 12" stroke="white" stroke-width="1"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(32, 32),
        anchor: new window.google.maps.Point(16, 32),
      },
      current: {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="8" fill="#4285F4" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" fill="white"/>
          </svg>
        `),
        scaledSize: new window.google.maps.Size(24, 24),
        anchor: new window.google.maps.Point(12, 24),
      }
    };
    return icons[iconType] || icons.congestion;
  };

  useEffect(() => {
    // Use environment variable for API key
    const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
    console.log('API Key loaded:', apiKey ? 'Present' : 'Missing');
    
    if (!apiKey) {
      setError('Google Maps API key is not configured. Please add REACT_APP_GOOGLE_MAPS_API_KEY to your .env file.');
      setLoading(false);
      return;
    }

    // Load Google Maps API
    const loadGoogleMapsAPI = () => {
      if (window.google && window.google.maps) {
        initializeMap();
        return;
      }

      console.log('Loading Google Maps script...');
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => {
        console.log('Google Maps script loaded successfully');
        initializeMap();
      };
      script.onerror = (error) => {
        console.error('Failed to load Google Maps script:', error);
        setError('Failed to load Google Maps API. Please check your API key and internet connection.');
        setLoading(false);
      };
      document.head.appendChild(script);
    };

    const initializeMap = () => {
      console.log('Initializing map...');
      if (!window.google || !window.google.maps) {
        console.error('Google Maps API not loaded properly');
        setError('Google Maps API not loaded');
        setLoading(false);
        return;
      }

      // Ensure the map container exists
      if (!mapRef.current) {
        console.error('Map container element not found');
        setError('Map container not found');
        setLoading(false);
        return;
      }
      
      console.log('Map container found, dimensions:', {
        width: mapRef.current.clientWidth,
        height: mapRef.current.clientHeight
      });

      // Initialize map with default center (Bangalore)
      const defaultCenter = { lat: 12.9716, lng: 77.5946 }; // Bangalore
      const mapInstance = new window.google.maps.Map(mapRef.current, {
        center: defaultCenter,
        zoom: 13, // Closer zoom for city view
        mapTypeId: window.google.maps.MapTypeId.ROADMAP,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
        zoomControl: true,
      });

      setMap(mapInstance);

      // Add custom markers for predefined locations
      addCustomMarkers(mapInstance);

      // Get current location and add marker
      getCurrentLocation(mapInstance);
    };

    const addCustomMarkers = (mapInstance) => {
      const newMarkers = [];
      
      predefinedLocations.forEach((location) => {
        const marker = new window.google.maps.Marker({
          position: location.position,
          map: mapInstance,
          title: location.title,
          snippet: location.snippet,
          icon: getCustomMarkerIcon(location.icon),
        });

        // Add info window for snippet text
        if (location.snippet) {
          const infoWindow = new window.google.maps.InfoWindow({
            content: `<div><strong>${location.title}</strong><br>${location.snippet}</div>`
          });

          marker.addListener('click', () => {
            infoWindow.open(mapInstance, marker);
          });
        }

        newMarkers.push(marker);
      });

      setMarkers(newMarkers);
    };

    const getCurrentLocation = (mapInstance) => {
      if (navigator.geolocation) {
        console.log('Geolocation supported, getting current position...');
        
        const geolocationOptions = {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000
        };
        
        navigator.geolocation.getCurrentPosition(
          (position) => {
            console.log('Geolocation success:', position.coords);
            
            const { latitude, longitude } = position.coords;
            const location = { lat: latitude, lng: longitude };
            setCurrentLocation(location);
            
            // Add current location marker
            const currentMarker = new window.google.maps.Marker({
              position: location,
              map: mapInstance,
              title: 'You are here',
              icon: getCustomMarkerIcon('current'),
            });

            setMarkers(prev => [...prev, currentMarker]);
            setLoading(false);
          },
          (error) => {
            console.error('Geolocation error:', error);
            
            let errorMessage = 'Unable to get your current location. ';
            switch (error.code) {
              case error.PERMISSION_DENIED:
                errorMessage += 'Please allow location access in your browser settings.';
                break;
              case error.POSITION_UNAVAILABLE:
                errorMessage += 'Location information is unavailable.';
                break;
              case error.TIMEOUT:
                errorMessage += 'Location request timed out. Please try again.';
                break;
              default:
                errorMessage += 'Please enable location services.';
            }
            
            console.warn(errorMessage);
            setLoading(false);
          },
          geolocationOptions
        );
      } else {
        console.log('Geolocation not supported');
        setLoading(false);
      }
    };

    let retryCount = 0;
    const maxRetries = 50;
    
    const initMapWithDelay = () => {
      console.log('initMapWithDelay called, mapRef.current:', mapRef.current, 'retryCount:', retryCount);
      if (!mapRef.current) {
        retryCount++;
        if (retryCount >= maxRetries) {
          console.error('Map container not ready after maximum retries');
          setError('Failed to initialize map container. Please refresh the page.');
          setLoading(false);
          return;
        }
        console.log('Map container not ready, retrying in 100ms... (attempt', retryCount, 'of', maxRetries, ')');
        setTimeout(initMapWithDelay, 100);
        return;
      }
      console.log('Map container ready, calling loadGoogleMapsAPI...');
      loadGoogleMapsAPI();
    };

    console.log('Starting map initialization...');
    initMapWithDelay();

    return () => {
      // Cleanup markers
      markers.forEach(marker => {
        if (marker && marker.setMap) {
          marker.setMap(null);
        }
      });
    };
  }, []);

  const centerOnCurrentLocation = () => {
    if (map && currentLocation) {
      map.setCenter(currentLocation);
      map.setZoom(15);
    }
  };

  const showCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log('Manual location request success:', position.coords);
          const { latitude, longitude } = position.coords;
          const location = { lat: latitude, lng: longitude };
          setCurrentLocation(location);
          
          if (map) {
            map.setCenter(location);
            map.setZoom(15);
            
            // Add or update current location marker
            const currentMarker = new window.google.maps.Marker({
              position: location,
              map: map,
              title: 'You are here',
              icon: getCustomMarkerIcon('current'),
            });

            setMarkers(prev => {
              // Remove existing current location marker
              const filtered = prev.filter(marker => marker.title !== 'You are here');
              return [...filtered, currentMarker];
            });
          }
        },
        (error) => {
          console.error('Manual location request failed:', error);
          alert('Location access denied. Please enable location services in your browser settings.');
        }
      );
    }
  };

  if (loading) {
    return (
      <div className="live-maps-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading map...</p>
        </div>
        <div ref={mapRef} className="map-container" style={{ display: 'none' }}></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="live-maps-container">
        <div className="error-message">
          <h3>Network Error - Showing Offline Route</h3>
          <p>Unable to load live map data. Here's a suggested route:</p>
          <div className="dummy-route">
            <h4>🚗 Route: Krishnarajaura → HAL Museum</h4>
            <div className="route-details">
              <div className="route-step">
                <span className="step-number">1</span>
                <span className="step-text">Start from Krishnarajaura Metro Station</span>
              </div>
              <div className="route-step">
                <span className="step-number">2</span>
                <span className="step-text">Take Outer Ring Road (ORR) towards Marathahalli</span>
              </div>
              <div className="route-step">
                <span className="step-number">3</span>
                <span className="step-text">Continue on ORR past Marathahalli Bridge</span>
              </div>
              <div className="route-step">
                <span className="step-number">4</span>
                <span className="step-text">Take exit towards HAL Airport Road</span>
              </div>
              <div className="route-step">
                <span className="step-number">5</span>
                <span className="step-text">Turn right onto HAL Airport Road</span>
              </div>
              <div className="route-step">
                <span className="step-number">6</span>
                <span className="step-text">Continue straight for 2.5 km</span>
              </div>
              <div className="route-step">
                <span className="step-number">7</span>
                <span className="step-text">Arrive at HAL Heritage Centre & Aerospace Museum</span>
              </div>
            </div>
            <div className="route-info">
              <p><strong>Distance:</strong> ~8.5 km</p>
              <p><strong>Estimated Time:</strong> 20-25 minutes (normal traffic)</p>
              <p><strong>Route Type:</strong> Primary roads with moderate traffic</p>
            </div>
          </div>
          <button onClick={() => window.location.reload()}>Retry Loading Map</button>
        </div>
        <div ref={mapRef} className="map-container" style={{ display: 'none' }}></div>
      </div>
    );
  }

  return (
    <div className="live-maps-container">
      <div className="map-controls">
        <button 
          className="location-button"
          onClick={centerOnCurrentLocation}
          title="Center on current location"
          disabled={!currentLocation}
        >
          📍 My Location
        </button>
        {currentLocation && (
          <div className="coordinates">
            <span>Lat: {currentLocation.lat.toFixed(6)}</span>
            <span>Lng: {currentLocation.lng.toFixed(6)}</span>
          </div>
        )}
      </div>
      <div ref={mapRef} className="map-container" style={{ display: 'block' }}></div>
    </div>
  );
};

export default LiveMaps; 