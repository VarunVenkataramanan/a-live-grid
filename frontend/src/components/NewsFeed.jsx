import React, { useState, useEffect } from 'react';
import './NewsFeed.css';

const API_BASE_URL = 'https://livegrid-467013.el.r.appspot.com';

const NewsFeed = ({ selectedPostId, onPostClose }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedPost, setSelectedPost] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);

  // API Functions
  const fetchShortPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/posts/short-post`);
      if (!response.ok) {
        throw new Error('Failed to fetch posts');
      }
      const data = await response.json();
      
      // Transform the data to use local images - assign specific image to each post
      const transformedPosts = data.map((post, index) => {
        // Assign specific images to each post based on index
        const imagePaths = [
          '/images/IMG-20250727-WA0014.jpg',
          '/images/IMG-20250727-WA0013.jpg',
          '/images/IMG-20250727-WA0012.jpg',
          '/images/IMG-20250727-WA0011.jpg',
          '/images/IMG-20250727-WA0010.jpg',
          '/images/IMG-20250727-WA0009.jpg',
          '/images/IMG-20250727-WA0008.jpg',
          '/images/IMG-20250727-WA0007.jpg',
          '/images/IMG-20250727-WA0006.jpg',
          '/images/IMG-20250727-WA0005.jpg'
        ];
        
        // Use the image at the current index, or cycle back if more than 10 posts
        const imagePath = imagePaths[index % imagePaths.length];

          return {
            ...post,
          images: [imagePath],
          excerpt: post.title || post.excerpt || '',
          author: post.username || post.author || 'Anonymous',
          date: post.created_at ? new Date(post.created_at).toLocaleDateString() : post.date || 'Unknown',
          category: post.category || 'Traffic',
          upvotes: post.upvote_count || post.upvotes || 0,
          downvotes: post.downvote_count || post.downvotes || 0,
          userVote: null
        };
      });
      
      setPosts(transformedPosts);
      setError(null);
    } catch (err) {
      setError('Failed to load posts. Please try again later.');
      console.error('Error fetching posts:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchLongPost = async (postId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/posts/long-post/${postId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch post details');
      }
      const data = await response.json();
      
      // Find the corresponding short post to get the same image
      const shortPost = posts.find(post => post.id === postId);
      const imagePaths = [
        '/images/IMG-20250727-WA0014.jpg',
        '/images/IMG-20250727-WA0013.jpg',
        '/images/IMG-20250727-WA0012.jpg',
        '/images/IMG-20250727-WA0011.jpg',
        '/images/IMG-20250727-WA0010.jpg',
        '/images/IMG-20250727-WA0009.jpg',
        '/images/IMG-20250727-WA0008.jpg',
        '/images/IMG-20250727-WA0007.jpg',
        '/images/IMG-20250727-WA0006.jpg',
        '/images/IMG-20250727-WA0005.jpg'
      ];
      
      // Use the same image as the short post, or default to first image
      const postIndex = posts.findIndex(post => post.id === postId);
      const imagePath = postIndex >= 0 ? imagePaths[postIndex % imagePaths.length] : imagePaths[0];
      
      // Transform the long post data to use local images
      const transformedPost = {
        ...data,
        images: [imagePath],
        excerpt: data.title || data.excerpt || '',
        author: data.username || data.author || 'Anonymous',
        date: data.created_at ? new Date(data.created_at).toLocaleDateString() : data.date || 'Unknown',
        category: data.category || 'Traffic',
        upvotes: data.upvote_count || data.upvotes || 0,
        downvotes: data.downvote_count || data.downvotes || 0,
        userVote: null
      };
      
      return transformedPost;
    } catch (err) {
      console.error('Error fetching post details:', err);
      return null;
    }
  };

  const handleVoteAPI = async (postId, voteType) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/posts/${postId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ vote_type: voteType }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit vote');
      }
      
      // Refresh posts to get updated vote counts
      await fetchShortPosts();
    } catch (err) {
      console.error('Error submitting vote:', err);
    }
  };

  // Fetch posts on component mount
  useEffect(() => {
    fetchShortPosts();
  }, []);

  // Effect to handle selectedPostId from sidebar
  useEffect(() => {
    if (selectedPostId) {
      const post = posts.find(p => p.id === selectedPostId);
      if (post) {
    setSelectedPost(post);
        setShowModal(true);
      }
    }
  }, [selectedPostId, posts]);

  const handleVote = async (postId, voteType) => {
    // Call the API to handle voting
    await handleVoteAPI(postId, voteType);
  };

  const handlePostClick = async (post) => {
    // Fetch detailed post data for modal
    const detailedPost = await fetchLongPost(post.id);
    if (detailedPost) {
      setSelectedPost(detailedPost);
    } else {
      setSelectedPost(post); // Fallback to short post data
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedPost(null);
    setPreviewImage(null);
    if (onPostClose) {
      onPostClose();
    }
  };

  const handleImageClick = (imageUrl) => {
    setPreviewImage(imageUrl);
  };

  const closeImagePreview = () => {
    setPreviewImage(null);
  };

  const renderModalImageCollage = (images) => {
    if (!images || images.length === 0) return null;

    if (images.length === 1) {
      return (
        <div className="modal-image-single">
          <img 
            src={images[0]} 
            alt="Post content" 
            className="modal-post-image"
            onClick={() => handleImageClick(images[0])}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      );
    }

    if (images.length === 2) {
      return (
        <div className="modal-image-grid modal-image-grid-2">
          {images.map((image, index) => (
            <img 
              key={index}
              src={image} 
              alt={`Post content ${index + 1}`} 
              className="modal-post-image"
              onClick={() => handleImageClick(image)}
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          ))}
        </div>
      );
    }

    if (images.length === 3) {
      return (
        <div className="modal-image-grid modal-image-grid-3">
          <img 
            src={images[0]} 
            alt="Post content 1" 
            className="modal-post-image modal-main-image"
            onClick={() => handleImageClick(images[0])}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          <div className="modal-side-images">
            {images.slice(1).map((image, index) => (
              <img 
                key={index + 1}
                src={image} 
                alt={`Post content ${index + 2}`} 
                className="modal-post-image"
                onClick={() => handleImageClick(image)}
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            ))}
          </div>
        </div>
      );
    }

    if (images.length === 4) {
      return (
        <div className="modal-image-grid modal-image-grid-4">
          {images.map((image, index) => (
            <img 
              key={index}
              src={image} 
              alt={`Post content ${index + 1}`} 
              className="modal-post-image"
              onClick={() => handleImageClick(image)}
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          ))}
        </div>
      );
    }

    return null;
  };

  return (
    <div className="news-feed">
      <div className="news-feed-header">
        <h2>Report Feed</h2>
        <p>Latest news and updates</p>
      </div>
      
      {loading && (
        <div className="loading-container">
          <p>Loading posts...</p>
        </div>
      )}
      
      {error && (
        <div className="error-container">
          <p>{error}</p>
          <button onClick={fetchShortPosts} className="retry-button">
            Try Again
          </button>
        </div>
      )}
      
      {!loading && !error && (
      <div className="news-posts">
        {posts.map(post => (
          <article key={post.id} className="news-post" onClick={() => handlePostClick(post)}>
            <div className="post-voting" onClick={(e) => e.stopPropagation()}>
              <button 
                className={`vote-btn upvote ${post.userVote === 'up' ? 'voted disabled' : post.userVote === 'down' ? 'enabled' : ''}`}
                onClick={() => handleVote(post.id, 'up')}
                disabled={post.userVote === 'up'}
                aria-label="Upvote"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 4l8 8h-6v8h-4v-8H4z"/>
                </svg>
              </button>
              <div className="vote-count">
                <span className="upvote-count">{post.upvotes}</span>
                <span className="downvote-count">{post.downvotes}</span>
              </div>
              <button 
                className={`vote-btn downvote ${post.userVote === 'down' ? 'voted disabled' : post.userVote === 'up' ? 'enabled' : ''}`}
                onClick={() => handleVote(post.id, 'down')}
                disabled={post.userVote === 'down'}
                aria-label="Downvote"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 20l8-8h-6V4h-4v8H4z"/>
                </svg>
              </button>
            </div>
            <div className="post-content">
            <div className="post-header">
              <span className="post-category">{post.category}</span>
              <span className="post-date">{post.date}</span>
            </div>
            <h3 className="post-title">{post.title}</h3>
            <p className="post-excerpt">{post.excerpt}</p>
              
              {renderModalImageCollage(post.images)}
              
            <div className="post-footer">
              <span className="post-author">By {post.author}</span>
              </div>
            </div>
          </article>
        ))}
      </div>
      )}

      {/* Post Detail Modal */}
      {showModal && selectedPost && (
        <div className="post-modal-overlay" onClick={closeModal}>
          <div className="post-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={closeModal}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
            
            <div className="modal-image-container">
              <div className="modal-images-section">
                {renderModalImageCollage(selectedPost.images)}
              </div>
              <div className="modal-image-caption">
                Click image to preview
              </div>
            </div>
            
            <div className="modal-content">
              <div className="modal-header">
                <span className="modal-category">{selectedPost.category}</span>
                <span className="modal-date">{selectedPost.date}</span>
              </div>
              <h2 className="modal-title">{selectedPost.title}</h2>
              <p className="modal-description">{selectedPost.description}</p>
              <div className="modal-footer">
                <span className="modal-author">By {selectedPost.author}</span>
                <a 
                  href={selectedPost.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="modal-link-btn"
                >
                  Read Full Article
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Image Preview Modal */}
      {previewImage && (
        <div className="image-preview-overlay" onClick={closeImagePreview}>
          <div className="image-preview-container" onClick={(e) => e.stopPropagation()}>
            <button className="preview-close-btn" onClick={closeImagePreview}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
            <img 
              src={previewImage} 
              alt="Preview" 
              className="preview-image"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default NewsFeed; 