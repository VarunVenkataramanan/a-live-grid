import React, { useState } from 'react';
import './NewsFeed.css';

const NewsFeed = () => {
  const [posts, setPosts] = useState([
    {
      id: 1,
      title: "OpenAI launches new GPT-5 model with enhanced capabilities",
      excerpt: "The latest iteration brings significant improvements in reasoning and multimodal understanding...",
      description: "OpenAI has officially announced the release of GPT-5, their most advanced language model to date. This new iteration brings significant improvements in reasoning capabilities, multimodal understanding, and creative problem-solving. The model demonstrates enhanced performance across various benchmarks and introduces new features that make it more useful for complex tasks.",
      author: "Tech Reporter",
      date: "2 hours ago",
      category: "AI",
      upvotes: 42,
      downvotes: 3,
      userVote: null,
      images: [
        "https://picsum.photos/400/300?random=1",
        "https://picsum.photos/400/300?random=2"
      ],
      url: "https://openai.com/blog/gpt-5"
    },
    {
      id: 2,
      title: "React 19 announced with concurrent features",
      excerpt: "The new version introduces groundbreaking concurrent rendering capabilities...",
      description: "React 19 introduces groundbreaking concurrent rendering capabilities that will revolutionize how developers build user interfaces. The new version includes automatic batching, improved suspense, and better performance optimizations that make React applications faster and more responsive than ever before.",
      author: "Dev News",
      date: "4 hours ago",
      category: "Development",
      upvotes: 28,
      downvotes: 1,
      userVote: null,
      images: [
        "https://picsum.photos/400/300?random=3"
      ],
      url: "https://react.dev/blog/2024/react-19"
    },
    {
      id: 3,
      title: "AI trends shaping the future of technology in 2024",
      excerpt: "From autonomous systems to generative AI, here are the key trends...",
      description: "The landscape of artificial intelligence is rapidly evolving, with several key trends shaping the future of technology. From autonomous systems and generative AI to edge computing and quantum machine learning, these developments are transforming industries and creating new opportunities for innovation.",
      author: "Future Tech",
      date: "6 hours ago",
      category: "Technology",
      upvotes: 35,
      downvotes: 2,
      userVote: null,
      images: [
        "https://picsum.photos/400/300?random=4",
        "https://picsum.photos/400/300?random=5",
        "https://picsum.photos/400/300?random=6",
        "https://picsum.photos/400/300?random=7"
      ],
      url: "https://techcrunch.com/2024/ai-trends"
    },
    {
      id: 4,
      title: "Machine learning breakthroughs in healthcare",
      excerpt: "New algorithms show promising results in early disease detection...",
      description: "Recent breakthroughs in machine learning are revolutionizing healthcare with new algorithms that show promising results in early disease detection, drug discovery, and personalized medicine. These advances are helping doctors make better diagnoses and develop more effective treatment plans.",
      author: "Health Tech",
      date: "8 hours ago",
      category: "Healthcare",
      upvotes: 51,
      downvotes: 0,
      userVote: null,
      images: [
        "https://picsum.photos/400/300?random=8",
        "https://picsum.photos/400/300?random=9",
        "https://picsum.photos/400/300?random=10"
      ],
      url: "https://healthcare.ai/breakthroughs-2024"
    },
    {
      id: 5,
      title: "The rise of edge computing in IoT applications",
      excerpt: "How edge computing is revolutionizing the Internet of Things...",
      description: "Edge computing is revolutionizing the Internet of Things by bringing computation and data storage closer to the source of data. This approach reduces latency, improves security, and enables real-time processing for IoT applications, making them more efficient and responsive.",
      author: "IoT Weekly",
      date: "12 hours ago",
      category: "IoT",
      upvotes: 19,
      downvotes: 4,
      userVote: null,
      images: [
        "https://picsum.photos/400/300?random=11"
      ],
      url: "https://iotweekly.com/edge-computing-2024"
    }
  ]);

  const [selectedPost, setSelectedPost] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);

  const handleVote = (postId, voteType) => {
    setPosts(prevPosts => 
      prevPosts.map(post => {
        if (post.id === postId) {
          let newUpvotes = post.upvotes;
          let newDownvotes = post.downvotes;
          let newUserVote = voteType;

          // Handle vote logic - user can only have one vote (up OR down)
          if (post.userVote === voteType) {
            // User is clicking the same vote again - remove it
            if (voteType === 'up') {
              newUpvotes -= 1;
            } else {
              newDownvotes -= 1;
            }
            newUserVote = null;
          } else if (post.userVote === null) {
            // User hasn't voted before - add the vote
            if (voteType === 'up') {
              newUpvotes += 1;
            } else {
              newDownvotes += 1;
            }
          } else {
            // User is changing their vote from one type to another
            // First remove the previous vote
            if (post.userVote === 'up') {
              newUpvotes -= 1;
            } else {
              newDownvotes -= 1;
            }
            // Then add the new vote
            if (voteType === 'up') {
              newUpvotes += 1;
            } else {
              newDownvotes += 1;
            }
          }

          return {
            ...post,
            upvotes: newUpvotes,
            downvotes: newDownvotes,
            userVote: newUserVote
          };
        }
        return post;
      })
    );
  };

  const handlePostClick = (post) => {
    setSelectedPost(post);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedPost(null);
    setPreviewImage(null);
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
                Click on any image to preview
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