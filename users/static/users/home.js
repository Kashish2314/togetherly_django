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

   // Handle post submission
   if (submitPostBtn) {
       submitPostBtn.addEventListener('click', function() {
           const content = postContent.value.trim();
           if (!content) {
               alert('Please enter some content for your post.');
               return;
           }

           const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

           fetch(createPostUrl, {
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
                   postContent.value = '';
                   const newPost = createPostElement(data.post);
                   postsFeed.insertBefore(newPost, postsFeed.firstChild);
                   if (data.post_count !== undefined) {
                       updatePostCount(data.post_count);
                   }
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

