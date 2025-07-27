import uvicorn
import os

from app.backend.backend import app

# For GCP App Engine, the app needs to be accessible as 'app'
# This is already done by importing from app.backend.backend

if __name__ == "__main__":
	# Get port from environment variable (GCP sets PORT)
	port = int(os.environ.get("PORT", 8000))
	
	uvicorn.run(
		"app.backend.backend:app",
		host="0.0.0.0",
		port=port,
		reload=False,  # Disable reload for production
		log_level="info",
	)
