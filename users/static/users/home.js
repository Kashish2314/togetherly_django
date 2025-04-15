
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

   // Get the URLs for the create_post and get_posts routes
   const createPostUrl = document.getElementById('createPostUrl').value;
   const getPostsUrl = document.getElementById('getPostsUrl').value;
   const currentUserId = parseInt(document.getElementById('currentUserId').value, 10);

   console.log('Current User ID:', currentUserId); // Log the current user ID

   // Get references to DOM elements
   const submitPostBtn = document.getElementById('submitPost'); // Submit button
   const postContent = document.getElementById('postContent'); // Post input field
   const postsFeed = document.getElementById('postsFeed'); // Posts feed container
   const loading = document.getElementById('loading'); // Loading indicator

   // Function to load posts
   function loadPosts() {
    console.log('Loading posts...'); // Log when the function starts
    loading.style.display = 'block'; // Show loading indicator

    fetch(getPostsUrl)
        .then(response => {
            console.log('Fetch response:', response); // Log the fetch response
            if (!response.ok) {
                throw new Error('Failed to fetch posts');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response Data:', data); // Log the response data
            if (data.success) {
                console.log('Posts fetched successfully:', data.posts); // Log the posts
                postsFeed.innerHTML = ''; // Clear existing posts
                if (data.posts.length === 0) {
                    console.log('No posts available.'); // Log if there are no posts
                    postsFeed.innerHTML = '<div class="no-posts">No posts available. Be the first to share something!</div>';
                } else {
                    console.log('Displaying posts...'); // Log before displaying posts
                    data.posts.forEach(post => {
                        const postElement = document.createElement('div');
                        postElement.className = 'post';
                        postElement.innerHTML = `
                            <div class="post-header">
                                <div class="post-user">
                                    <span class="post-username">${post.username}</span>
                                    <div class="post-timestamp">
                                        <span class="post-date">${new Date(post.timestamp).toLocaleDateString()}</span>
                                        <span class="post-time">${new Date(post.timestamp).toLocaleTimeString()}</span>
                                    </div>
                                </div>
                                ${post.user_id === currentUserId ? 
                                    `<button class="delete-post" data-post-id="${post.id}">
                                        <i class="fas fa-trash"></i>
                                    </button>` : ''
                                }
                            </div>
                            <div class="post-content">${post.content}</div>
                        `;
                        postsFeed.appendChild(postElement);
                    });

                    console.log('Posts displayed.'); // Log after displaying posts

                    // Add event listeners to delete buttons
                    document.querySelectorAll('.delete-post').forEach(button => {
                        button.addEventListener('click', () => {
                            const postId = button.getAttribute('data-post-id');
                            deletePost(postId);
                        });
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
            postsFeed.innerHTML = '<div class="error">Failed to load posts. Please try again later.</div>';
        })
        .finally(() => {
            console.log('Loading complete.'); // Log when loading is complete
            loading.style.display = 'none'; // Hide loading indicator
        });
    }

   // Function to delete a post
   function deletePost(postId) {
       if (confirm('Are you sure you want to delete this post?')) {
           fetch(`/delete_post/${postId}`, {
               method: 'DELETE',
           })
               .then(response => response.json())
               .then(data => {
                   if (data.success) {
                       loadPosts(); // Reload posts after deletion
                   } else {
                       alert(data.message);
                   }
               })
               .catch(error => {
                   console.error('Error deleting post:', error);
                   alert('An error occurred while deleting the post.');
               });
       }
   }

   // Handle post submission
   submitPostBtn.addEventListener('click', () => {
       const content = postContent.value.trim();
       if (!content) {
           alert('Post content cannot be empty.');
           return;
       }

       console.log('Submitting post:', content); // Log the post content

       const formData = new FormData();
       formData.append('content', content);

       fetch(createPostUrl, {
           method: 'POST',
           body: formData
       })
           .then(response => {
               console.log('Create post response:', response); // Log the response
               return response.json();
           })
           .then(data => {
               console.log('Create post data:', data); // Log the response data
               if (data.success) {
                   postContent.value = ''; // Clear the input
                   loadPosts(); // Reload posts
               } else {
                   alert(data.message);
               }
           })
           .catch(error => {
               console.error('Error creating post:', error);
               alert('An error occurred while creating the post.');
           });
   });

   // Handle post submission on Enter key press
   postContent.addEventListener('keypress', function(event) {
       if (event.key === 'Enter') {
           event.preventDefault(); // Prevent default behavior (e.g., new line)
           submitPostBtn.click(); // Trigger the post submission
       }
   });

   // Load posts when the page loads
   loadPosts();
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

