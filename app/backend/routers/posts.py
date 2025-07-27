from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status

# Temporarily disable agent import to fix deployment
# from app.agent import Agent
from app.backend.schemas.post import PostResponse, PostShortResponse, VoteRequest
from app.backend.services.data_service import data_service
from app.backend.services.storage_service import storage_service

router = APIRouter()

# Temporarily disable agent initialization
# agent = Agent()


@router.get("/short-post", response_model=list[PostShortResponse])
def get_posts_short():
	"""
	Get posts with short format (username, title, image) for feed display
	"""
	posts = data_service.get_posts_short()
	return posts


@router.get("/long-post", response_model=list[PostResponse])
def get_posts_long():
	"""
	Get posts with full data for detailed view
	"""
	posts = data_service.get_posts_long()
	return posts


@router.post("/create-post", response_model=PostResponse)
async def create_post_with_image(
	title: str = Form(...),
	description: str = Form(...),
	username: str = Form(...),
	user_id: str = Form(...),
	latitude: float = Form(...),
	longitude: float = Form(...),
	category: str | None = Form(None),  # Comma-separated string
	image: UploadFile = File(...),
):
	"""
	Create a new post with image upload to Google Cloud Storage
	Supports both file uploads and base64 data
	"""
	try:
		# Parse category string to list
		category_list = []
		if category:
			category_list = [cat.strip() for cat in category.split(",") if cat.strip()]

		# Check if it's a base64 string or file
		if image.content_type == "text/plain" or image.filename is None:
			# Handle as base64 data
			image_data = await image.read()
			image_bitmap = image_data.decode("utf-8")

			# Validate bitmap format
			if not image_bitmap.startswith("data:image/"):
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Invalid bitmap format. Must start with 'data:image/'",
				)

			# Upload base64 image to Google Cloud Storage
			image_url = await storage_service.upload_base64_image(image_bitmap, folder="posts")
		else:
			# Handle as file upload
			image_url = await storage_service.upload_image(image, folder="posts")

		# Temporarily disable agent categorization
		# location, condition = agent.categorize(description)
		location, condition = "general", "information"

		# Create post data
		post_data = {
			"title": title,
			"description": description,
			"username": username,
			"user_id": user_id,
			"image_bitmap": image_url,  # Store the public URL
			"Geolocation": [latitude, longitude],
			"category": [location, condition],
		}

		return data_service.create_post(post_data)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Error processing image: {e!s}",
		) from e


@router.post("/{post_id}/vote")
async def vote_post(post_id: int, vote: VoteRequest):
	"""
	Vote on a post (upvote or downvote)
	"""
	success = data_service.vote_post(post_id, vote.user_id, vote.vote_type)
	if not success:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Post not found",
		)

	return {"message": f"Successfully {vote.vote_type}d post"}


# Temporarily disable chat endpoint
# @router.post("/chat")
# async def chat(user_input: str, session_id: str = Query(...)):
# 	"""
# 	Chat with the agent
# 	"""
# 	try:
# 		response = agent.process_message(user_input, session_id)
# 		return {"response": response}
# 	except Exception as e:
# 		raise HTTPException(
# 			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# 			detail=f"Error processing chat message: {e!s}",
# 		) from e
