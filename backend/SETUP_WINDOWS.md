# Windows Setup Guide for A-Live-Grid Backend

## Quick Setup (Recommended)

### 1. Install Dependencies
```powershell
# Navigate to the backend directory
cd a-live-grid/backend

# Option A: Use the simple installer (recommended)
python install_deps.py

# Option B: Install manually
pip install -r minimal_requirements.txt

# Option C: Install one by one
pip install fastapi uvicorn pydantic pydantic-settings python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv requests geopy
```

### 2. Test Installation
```powershell
# Test if everything is working
python test_installation.py
```

### 3. Set up Environment
```powershell
# Copy the example environment file
copy env.example .env
```

### 4. Run the Application
```powershell
# Start the server
python run.py
```

## Alternative Setup (If above fails)

### Manual Installation
If the automatic setup fails, try installing dependencies manually:

```powershell
# Install each dependency individually
pip install fastapi
pip install uvicorn
pip install pydantic
pip install pydantic-settings
pip install python-multipart
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-dotenv
pip install requests
pip install geopy
```

## Troubleshooting

### Common Issues:

1. **Database errors**: We've removed all database dependencies. The app now uses JSON data directly.

2. **Permission errors**: Run PowerShell as Administrator if you encounter permission issues.

3. **Python not found**: Make sure Python is installed and added to PATH.

4. **pip not found**: Install pip or use `python -m pip` instead.

### Verify Installation:
```powershell
# Check if everything is working
python -c "import fastapi, pydantic, geopy; print('All dependencies installed successfully!')"
```

## Access the Application

Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Sample Data

The application comes with 10 sample urban intelligence posts:
- Traffic reports from Bangalore
- Road condition updates
- Weather-related alerts
- Public transport information

No authentication required - all data is publicly accessible via the API endpoints. 