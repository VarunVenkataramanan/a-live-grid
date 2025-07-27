# Google Maps API Setup

To use the Live Maps feature, you need to set up a Google Maps API key.

## Steps to get your API key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API** (optional, for additional features)
4. Go to "Credentials" and create an API key
5. Restrict the API key to your domain for security

## Environment Configuration:

Create a `.env` file in the `frontend` directory with the following content:

```
REACT_APP_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

## Security Notes:

- Never commit your actual API key to version control
- Add `.env` to your `.gitignore` file
- Restrict your API key to specific domains/IPs in Google Cloud Console
- Monitor your API usage to avoid unexpected charges

## Features:

The Live Maps component includes all the functionality from the Android app:

### Core Features:
- **Current location detection** with high accuracy GPS support
- **Interactive Google Map** with full controls (zoom, street view, fullscreen)
- **Custom marker icons** for different location types:
  - 📍 Location pin (blue) - for general locations
  - ➕ Add pin (green) - for adding new locations
  - 💬 Chat pin (red) - for chat/communication points
  - 🔵 Current location pin (blue circle) - for user's current position

### Predefined Locations:
- **San Francisco** (37.7749, -122.4194) - Default center with "Aditiya was here" snippet
- **Los Angeles** (34.0522, -118.2437) - Add pin marker
- **Las Vegas** (36.1699, -115.1398) - Chat pin marker

### User Interface:
- **"Get My Location" button** - Requests location permission and centers map
- **"My Location" button** - Centers map on current location (enabled when location available)
- **Coordinates display** - Shows current latitude and longitude
- **Info windows** - Click markers to see title and snippet text
- **Responsive design** - Works on desktop and mobile devices
- **Error handling** - Graceful handling of location permission denied
- **Loading states** - Visual feedback during map initialization

### Technical Features:
- **Default zoom level 5** - Matches Android app behavior
- **San Francisco default center** - Same as Android app
- **Marker management** - Proper cleanup and state management
- **Geolocation options** - High accuracy, timeout, and cache settings
- **SVG custom markers** - Scalable vector graphics for crisp display

## Troubleshooting:

- If the map doesn't load, check your API key and ensure the Maps JavaScript API is enabled
- If location doesn't work, make sure the user has granted location permissions
- For HTTPS requirements, ensure your development server uses HTTPS or localhost
- If markers don't appear, check browser console for JavaScript errors
- For mobile devices, ensure location services are enabled in device settings 