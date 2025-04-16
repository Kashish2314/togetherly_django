document.addEventListener('DOMContentLoaded', function() {
    // Handle connect button clicks
    document.querySelectorAll('.connect-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const userId = this.dataset.userId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/connections/send_request/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update button appearance
                    this.disabled = true;
                    this.innerHTML = '<span>✓</span> Request Sent';
                    this.classList.remove('connect-btn');
                    this.classList.add('request-sent');
                    this.style.backgroundColor = '#28a745';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while sending the connection request.');
            });
        });
    });

    // Handle accept/reject buttons
    document.querySelectorAll('.accept-btn, .reject-btn').forEach(button => {
        button.addEventListener('click', function() {
            const requestId = this.dataset.requestId;
            const action = this.classList.contains('accept-btn') ? 'accept' : 'reject';
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/connections/handle_request/${requestId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `action=${action}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Remove the request card
                    const requestCard = this.closest('.pending-request-card');
                    requestCard.remove();
                    
                    // If no more requests, remove the section
                    const requestsSection = document.querySelector('.pending-requests');
                    if (requestsSection && !requestsSection.children.length) {
                        requestsSection.closest('.pending-requests-section').remove();
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while handling the request.');
            });
        });
    });

    // Handle message button clicks
    document.querySelectorAll('.message-btn').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.dataset.userId;
            window.location.href = `/messages/start/${userId}/`;
        });
    });

    // Card flip functionality
    document.querySelectorAll('.profile-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Don't flip if clicking buttons
            if (!e.target.closest('.card-btn')) {
                this.querySelector('.card-inner').classList.toggle('flipped');
            }
        });
    });
}); 