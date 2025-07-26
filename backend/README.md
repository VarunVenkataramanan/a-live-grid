# A-Live-Grid Backend

A comprehensive backend for the A-Live-Grid urban intelligence platform, built with FastAPI and following the requirements from the PRD and todo.txt.

## Features

### ✅ Completed Features (Following todo.txt steps)

1. **Step 1: Data Structure** ✅
   - Created JSON data file with 10 sample data sources
   - All required fields: username, title, short desc, image, long desc, location, time, upvote count, downvote count, karma

2. **Step 2: API Endpoints** ✅
   - `GET /api/v1/posts/short` - Returns username, title, and image for feed display
   - `GET /api/v1/posts/long` - Returns all post data for detailed view
   - `POST /api/v1/posts/` - Creates new posts with all required data

3. **Step 3: Reranking Algorithm** ✅
   - Based on number of upvotes
   - Location-based proximity scoring
   - User uploaded reports proximity
   - Recency factor

4. **Step 4: Karma Allocation Algorithm** ✅
   - Exponential decay formula for karma
   - First upvotes contribute significantly more karma
   - Logarithmic scaling to prevent domination

5. **Step 5: Voting System** ✅
   - `POST /api/v1/posts/{post_id}/vote` - Upvote/downvote posts
   - Real-time karma recalculation
   - User vote tracking

## Architecture

```
backend/
├── app/
│   ├── core/           # Core configuration and utilities
│   ├── schemas/        # Pydantic validation schemas
│   ├── routers/        # FastAPI route handlers
│   └── services/       # Business logic services
├── data/               # JSON sample data
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Installation
```bash
python test_app.py
```

### 3. Run the Application
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Posts
- `GET /api/v1/posts/short` - Get posts with short format (feed)
- `GET /api/v1/posts/long` - Get posts with full data
- `GET /api/v1/posts/{post_id}` - Get specific post
- `POST /api/v1/posts/` - Create new post
- `POST /api/v1/posts/{post_id}/vote` - Vote on post

### Users
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/{user_id}` - Get user profile

## Key Features

### 🎯 Reranking Algorithm
The posts are dynamically reranked based on:
- **Location Proximity** (40% weight) - Closer posts get higher scores
- **Upvote Popularity** (40% weight) - More upvotes = higher score
- **Recency** (20% weight) - Newer posts get priority

### 🏆 Karma System
- Exponential decay formula: `karma += 1.0 / (upvote_number ^ 0.5)`
- First upvotes contribute significantly more karma
- Prevents extremely popular posts from dominating

### 🔐 Security
- JWT-based authentication
- Password hashing with bcrypt
- Protected routes with dependency injection

### 📊 Data Models
- **User**: username, email, karma, post counts
- **Post**: title, descriptions, location, votes, karma
- **Vote**: user-post relationship with vote type

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
GOOGLE_ADDRESS_VALIDATION_API_KEY=your-address-validation-key
```

## Testing

Run tests with pytest:
```bash
pytest
```

## Data Management

The application uses JSON files for data storage. To add new posts:

1. Edit `data/sample_data.json` directly
2. Or use the API endpoints to create posts dynamically
3. All changes are automatically saved to the JSON file

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Run linting and formatting

## License

This project is part of the A-Live-Grid urban intelligence platform. 