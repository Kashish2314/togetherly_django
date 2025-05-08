document.querySelector('.search-btn').addEventListener('click', function() {
    document.querySelector('.search-input').focus();
});

// theme toggle
const themeToggle = document.getElementById('themeToggle');
// Function to toggle theme and save preference
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        // Save the current theme preference in localStorage
        const currentTheme = document.body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode';
        localStorage.setItem('theme', currentTheme);
    });
}
// Function to apply the saved theme on page load
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark-mode') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}
applySavedTheme();
document.addEventListener('DOMContentLoaded', function() {
    // This ensures the gallery works even if JavaScript is disabled
    // For more advanced functionality you could add:
    // - Dynamic loading of news items
    // - Touch support for mobile devices
    // - Event listeners for card clicks
    
    // Example of adding a click handler to each card
    const cards = document.querySelectorAll('.news-card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't follow link if clicking on the card but not the link
            if (!e.target.closest('.news-link')) {
                const link = this.querySelector('.news-link');
                if (link) {
                    window.location.href = link.href;
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Add menu icon to navbar
    const navbar = document.querySelector('.navbar');
    const menuIcon = document.createElement('div');
    menuIcon.className = 'menu-icon';
    menuIcon.innerHTML = '<i class="fas fa-bars"></i>';
    navbar.insertBefore(menuIcon, navbar.firstChild);

    // Menu toggle functionality
    const navLinks = document.querySelector('.nav-links');
    const searchContainer = document.querySelector('.search-container');
    
    menuIcon.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        searchContainer.classList.toggle('active');
        menuIcon.innerHTML = navLinks.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.navbar')) {
            navLinks.classList.remove('active');
            searchContainer.classList.remove('active');
            menuIcon.innerHTML = '<i class="fas fa-bars"></i>';
        }
    });

   // Get the URLs and current user ID
   const createPostUrl = document.getElementById('createPostUrl').value;
   const getPostsUrl = document.getElementById('getPostsUrl').value;
   const currentUserId = parseInt(document.getElementById('currentUserId').value, 10);

   console.log('Current User ID:', currentUserId); // Log the current user ID

   // Get DOM elements
   const submitPostBtn = document.getElementById('submitPost');
   const postContent = document.getElementById('postContent');
   const postsFeed = document.getElementById('postsFeed');
   const loading = document.getElementById('loading');

   // Load posts when page loads
   loadPosts();

   // Image preview functionality
   const postImage = document.getElementById('postImage');
   const imagePreview = document.getElementById('imagePreview');
   const previewImg = document.getElementById('previewImg');
   const removeImage = document.getElementById('removeImage');

   postImage.addEventListener('change', function(e) {
       const file = e.target.files[0];
       if (file) {
           const reader = new FileReader();
           reader.onload = function(e) {
               previewImg.src = e.target.result;
               imagePreview.style.display = 'block';
           }
           reader.readAsDataURL(file);
       }
   });

   removeImage.addEventListener('click', function() {
       postImage.value = '';
       imagePreview.style.display = 'none';
       previewImg.src = '';
   });

   // Handle post submission
   if (submitPostBtn && postContent) {
       submitPostBtn.addEventListener('click', function() {
           const content = postContent.value.trim();
           const imageFile = postImage.files[0];
           
           if (!content && !imageFile) {
               alert('Please enter some content or upload an image for your post.');
               return;
           }

           const formData = new FormData();
           formData.append('content', content);
           if (imageFile) {
               formData.append('image', imageFile);
           }

           const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

           fetch(createPostUrl, {
               method: 'POST',
               headers: {
                   'X-CSRFToken': csrfToken
               },
               body: formData
           })
           .then(response => response.json())
           .then(data => {
               if (data.success) {
                   postContent.value = '';
                   postImage.value = '';
                   imagePreview.style.display = 'none';
                   previewImg.src = '';
                   const newPost = createPostElement(data.post);
                   postsFeed.insertBefore(newPost, postsFeed.firstChild);
               } else {
                   alert(data.message || 'Failed to create post.');
               }
           })
           .catch(error => {
               console.error('Error:', error);
               alert('An error occurred while creating the post.');
           });
       });
   }

   // Function to create a post element
    function createPostElement(post) {
        const isCurrentUser = post.user_id === parseInt(document.getElementById('currentUserId').value);
        const postElement = document.createElement('div');
        postElement.className = 'post';
        postElement.id = `post-${post.id}`;
        
        postElement.innerHTML = `
            <div class="post-header">
                <div class="post-user">
                    <div class="post-avatar">
                        <img src="${post.profile_picture_url || 'https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg'}" 
                             alt="${post.username}"
                             loading="lazy">
                    </div>
                    <div class="post-info">
                        <span class="post-username">${post.username}</span>
                        <div class="post-timestamp">
                            <span>${new Date(post.timestamp).toLocaleString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            })}</span>
                        </div>
                    </div>
                </div>
                ${isCurrentUser ? `
                    <div class="post-actions">
                        <button class="edit-post-btn" onclick="startEditPost(${post.id})" title="Edit post">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="delete-post-btn" onclick="deletePost(${post.id})" title="Delete post">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                ` : ''}
            </div>
            <div class="post-content" id="post-content-${post.id}">
                ${post.content}
                ${post.image_url ? `<img src="${post.image_url}" alt="Post image" style="max-width: 100%; border-radius: 8px; margin-top: 10px;">` : ''}
            </div>
            <div class="post-edit-form" id="post-edit-${post.id}" style="display: none;">
                <textarea class="edit-content" placeholder="What's on your mind?">${post.content}</textarea>
                <div class="edit-actions">
                    <button class="save-edit-btn" onclick="saveEdit(${post.id})">
                        <i class="fas fa-check"></i> Save
                    </button>
                    <button class="cancel-edit-btn" onclick="cancelEdit(${post.id})">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                </div>
            </div>
            <div class="post-interactions">
                <div class="interaction-buttons">
                    <button class="like-button ${post.is_liked ? 'liked' : ''}" onclick="toggleLike(${post.id})">
                        <i class="fas fa-heart"></i> <span class="likes-count">${post.likes_count}</span>
                    </button>
                    <button class="comment-button" onclick="toggleComments(${post.id})">
                        <i class="fas fa-comment"></i> <span class="comments-count">${post.comments.length}</span>
                    </button>
                </div>
                <div class="comments-section" id="comments-${post.id}" style="display: none;">
                    <div class="comments-list" id="comments-list-${post.id}">
                        ${post.comments.map(comment => `
                            <div class="comment" id="comment-${comment.id}">
                                <div class="comment-header">
                                    <img src="${comment.profile_picture_url}" alt="${comment.username}" class="comment-avatar">
                                    <span class="comment-username">${comment.username}</span>
                                    <span class="comment-time">${new Date(comment.timestamp).toLocaleString()}</span>
                                    ${comment.user_id === parseInt(document.getElementById('currentUserId').value) ? `
                                        <button class="delete-comment" onclick="deleteComment(${comment.id})">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    ` : ''}
                                </div>
                                <div class="comment-content">${comment.content}</div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="add-comment">
                        <input type="text" placeholder="Write a comment..." id="comment-input-${post.id}">
                        <button onclick="addComment(${post.id})">Post</button>
                    </div>
                </div>
            </div>
        `;
        
        return postElement;
    }

   // Function to format timestamp
   function formatTimestamp(timestamp) {
       const date = new Date(timestamp);
       return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
   }

   // Function to update post count
   function updatePostCount(count) {
       const postCountElement = document.querySelector('.stat-card:nth-child(2) .stat-number');
       if (postCountElement) {
           postCountElement.textContent = count;
       }
   }

   // Make these functions global
   window.startEditPost = function(postId) {
        const contentDiv = document.getElementById(`post-content-${postId}`);
        const editForm = document.getElementById(`post-edit-${postId}`);
        
        contentDiv.style.display = 'none';
        editForm.style.display = 'block';
   };

   window.cancelEdit = function(postId) {
        const contentDiv = document.getElementById(`post-content-${postId}`);
        const editForm = document.getElementById(`post-edit-${postId}`);
        
        contentDiv.style.display = 'block';
        editForm.style.display = 'none';
   };

   window.saveEdit = function(postId) {
        const editForm = document.getElementById(`post-edit-${postId}`);
        const content = editForm.querySelector('.edit-content').value.trim();
        
        if (!content) {
            alert('Post content cannot be empty!');
            return;
        }
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/edit_post/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `content=${encodeURIComponent(content)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const contentDiv = document.getElementById(`post-content-${postId}`);
                contentDiv.textContent = content;
               window.cancelEdit(postId);
            } else {
               alert(data.message || 'Failed to update post.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the post.');
        });
   };

   window.deletePost = function(postId) {
       if (!confirm('Are you sure you want to delete this post?')) {
           return;
    }

       const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
       fetch(`/delete_post/${postId}/`, {
           method: 'POST',
                headers: {
               'X-CSRFToken': csrfToken
           }
       })
       .then(response => response.json())
            .then(data => {
                if (data.success) {
               const postElement = document.getElementById(`post-${postId}`);
               if (postElement) {
                   postElement.remove();
               }
               if (data.post_count !== undefined) {
                   updatePostCount(data.post_count);
               }
                } else {
               alert(data.message || 'Failed to delete post.');
                }
            })
            .catch(error => {
           console.error('Error:', error);
           alert('An error occurred while deleting the post.');
       });
   };

   window.toggleLike = function(postId) {
       const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
       
       fetch(`/like_post/${postId}/`, {
           method: 'POST',
           headers: {
               'X-CSRFToken': csrfToken
           }
       })
       .then(response => response.json())
       .then(data => {
           if (data.success) {
               const likeButton = document.querySelector(`#post-${postId} .like-button`);
               const likesCount = document.querySelector(`#post-${postId} .likes-count`);
               
               if (data.liked) {
                   likeButton.classList.add('liked');
               } else {
                   likeButton.classList.remove('liked');
               }
               
               likesCount.textContent = data.likes_count;
           }
       })
       .catch(error => {
           console.error('Error:', error);
           alert('An error occurred while liking the post.');
       });
   };

   window.toggleComments = function(postId) {
       const commentsSection = document.getElementById(`comments-${postId}`);
       commentsSection.style.display = commentsSection.style.display === 'none' ? 'block' : 'none';
   };

   window.addComment = function(postId) {
       const commentInput = document.getElementById(`comment-input-${postId}`);
       const content = commentInput.value.trim();
       
       if (!content) {
           alert('Please enter a comment.');
           return;
       }

       const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
       
       fetch(`/add_comment/${postId}/`, {
           method: 'POST',
           headers: {
               'Content-Type': 'application/x-www-form-urlencoded',
               'X-CSRFToken': csrfToken
           },
           body: `content=${encodeURIComponent(content)}`
       })
       .then(response => response.json())
       .then(data => {
           if (data.success) {
               const commentsList = document.getElementById(`comments-list-${postId}`);
               const commentElement = document.createElement('div');
               commentElement.className = 'comment';
               commentElement.id = `comment-${data.comment.id}`;
               
               commentElement.innerHTML = `
                   <div class="comment-header">
                       <img src="${data.comment.profile_picture_url}" alt="${data.comment.username}" class="comment-avatar">
                       <span class="comment-username">${data.comment.username}</span>
                       <span class="comment-time">${new Date(data.comment.timestamp).toLocaleString()}</span>
                       <button class="delete-comment" onclick="deleteComment(${data.comment.id})">
                           <i class="fas fa-trash"></i>
                       </button>
                   </div>
                   <div class="comment-content">${data.comment.content}</div>
               `;
               
               commentsList.insertBefore(commentElement, commentsList.firstChild);
               commentInput.value = '';
               
               // Update comment count
               const commentsCount = document.querySelector(`#post-${postId} .comments-count`);
               commentsCount.textContent = parseInt(commentsCount.textContent) + 1;
           } else {
               alert(data.message || 'Failed to add comment.');
           }
       })
       .catch(error => {
           console.error('Error:', error);
           alert('An error occurred while adding the comment.');
       });
   };

   window.deleteComment = function(commentId) {
       if (!confirm('Are you sure you want to delete this comment?')) {
           return;
       }

       const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
       
       fetch(`/delete_comment/${commentId}/`, {
           method: 'POST',
           headers: {
               'X-CSRFToken': csrfToken
           }
       })
       .then(response => response.json())
       .then(data => {
           if (data.success) {
               const commentElement = document.getElementById(`comment-${commentId}`);
               const postId = commentElement.closest('.post').id.split('-')[1];
               
               commentElement.remove();
               
               // Update comment count
               const commentsCount = document.querySelector(`#post-${postId} .comments-count`);
               commentsCount.textContent = parseInt(commentsCount.textContent) - 1;
           } else {
               alert(data.message || 'Failed to delete comment.');
           }
       })
       .catch(error => {
           console.error('Error:', error);
           alert('An error occurred while deleting the comment.');
       });
   };

   // Function to load posts
   function loadPosts() {
       loading.style.display = 'block';
       const currentUserId = parseInt(document.getElementById('currentUserId').value, 10);
       console.log('Current User ID:', currentUserId); // Debug line

       fetch(getPostsUrl)
           .then(response => response.json())
           .then(data => {
               if (data.success) {
                   console.log('Posts data:', data.posts); // Debug line
                   postsFeed.innerHTML = '';
                   if (data.posts.length === 0) {
                       postsFeed.innerHTML = '<div class="no-posts">No posts available. Be the first to share something!</div>';
                   } else {
                       data.posts.forEach(post => {
                           const isCurrentUser = post.user_id === currentUserId;
                           console.log(`Post ${post.id} - User ID: ${post.user_id}, Current User: ${currentUserId}, Is Match: ${isCurrentUser}`); // Debug line
                           
                           const postElement = document.createElement('div');
                           postElement.className = 'post';
                           postElement.id = `post-${post.id}`;
                           
                           postElement.innerHTML = `
                               <div class="post-header">
                                   <div class="post-user">
                                       <div class="post-avatar">
                                           <img src="${post.profile_picture_url || 'https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg'}" 
                                                alt="${post.username}"
                                                loading="lazy">
                                       </div>
                                       <div class="post-info">
                                           <span class="post-username">${post.username}</span>
                                           <div class="post-timestamp">
                                               <span>${new Date(post.timestamp).toLocaleString('en-US', {
                                                   month: 'short',
                                                   day: 'numeric',
                                                   hour: '2-digit',
                                                   minute: '2-digit'
                                               })}</span>
                                           </div>
                                       </div>
                                   </div>
                                   ${isCurrentUser ? `
                                       <div class="post-actions">
                                           <button class="edit-post-btn" onclick="startEditPost(${post.id})" title="Edit post">
                                               <i class="fas fa-edit"></i>
                                           </button>
                                           <button class="delete-post-btn" onclick="deletePost(${post.id})" title="Delete post">
                                               <i class="fas fa-trash"></i>
                                           </button>
                                       </div>
                                   ` : ''}
                               </div>
                               <div class="post-content" id="post-content-${post.id}">${post.content}</div>
                               <div class="post-edit-form" id="post-edit-${post.id}" style="display: none;">
                                   <textarea class="edit-content" placeholder="What's on your mind?">${post.content}</textarea>
                                   <div class="edit-actions">
                                       <button class="save-edit-btn" onclick="saveEdit(${post.id})">
                                           <i class="fas fa-check"></i> Save
                                       </button>
                                       <button class="cancel-edit-btn" onclick="cancelEdit(${post.id})">
                                           <i class="fas fa-times"></i> Cancel
                                       </button>
                                   </div>
                               </div>
                           `;
                           
                           postsFeed.appendChild(postElement);
                       });
                   }
            }
        })
        .catch(error => {
               console.error('Error:', error);
               postsFeed.innerHTML = '<div class="error">Failed to load posts. Please try again later.</div>';
           })
           .finally(() => {
               loading.style.display = 'none';
           });
   }
});

// Automatically hide flash messages after 2 seconds
const flashMessages = document.querySelectorAll('.flash');
flashMessages.forEach(message => {
    setTimeout(() => {
        message.style.display = 'none';
    }, 2000);  // 2 seconds
});

// Mood Indicator Update
const moodIndicator = document.querySelector('.mood-indicator');
const moods = [
    {emoji: '😊', text: 'Feeling productive today!'},
    {emoji: '🚀', text: 'Ready to innovate!'},
    {emoji: '💡', text: 'Having creative ideas!'},
    {emoji: '👩‍💻', text: 'Deep in code!'},
    {emoji: '🤝', text: 'Looking to collaborate!'}
];

function updateMood() {
    const randomMood = moods[Math.floor(Math.random() * moods.length)];
    moodIndicator.innerHTML = `${randomMood.emoji} ${randomMood.text}`;
}

// Update mood indicator every 5 seconds
setInterval(updateMood, 5000);

// Initial mood update on page load
updateMood();

