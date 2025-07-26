from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from geopy.distance import geodesic
from app.schemas.post import PostCreate, PostResponse, PostShortResponse, VoteRequest
from app.services.data_service import data_service
from app.services.ranking import RerankingService

router = APIRouter()

@router.get("/short", response_model=List[PostShortResponse])
def get_posts_short(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None)
):
    """
    Get posts with short format (username, title, image) for feed display
    """
    posts = data_service.get_posts_short()
    
    # Apply pagination
    posts = posts[skip:skip + limit]
    
    # Apply reranking if user location is provided
    if user_lat and user_lng:
        reranking_service = RerankingService()
        posts = reranking_service.rerank_posts_json(posts, user_lat, user_lng)
    
    return posts

@router.get("/long", response_model=List[PostResponse])
def get_posts_long(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_lat: Optional[float] = Query(None),
    user_lng: Optional[float] = Query(None)
):
    """
    Get posts with full data for detailed view
    """
    posts = data_service.get_posts_long()
    
    # Apply pagination
    posts = posts[skip:skip + limit]
    
    # Apply reranking if user location is provided
    if user_lat and user_lng:
        reranking_service = RerankingService()
        posts = reranking_service.rerank_posts_json(posts, user_lat, user_lng)
    
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    """
    Get a specific post by ID
    """
    post = data_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate):
    """
    Create a new post
    """
    post_data = post.dict()
    new_post = data_service.create_post(post_data)
    return new_post

@router.post("/{post_id}/vote")
def vote_post(post_id: int, vote: VoteRequest):
    """
    Vote on a post (upvote or downvote)
    """
    success = data_service.vote_post(post_id, vote.user_id, vote.vote_type)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return {"message": f"Successfully {vote.vote_type}d post"} 