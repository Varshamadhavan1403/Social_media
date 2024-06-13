# Social Networking API using Django Rest Framework

## Problem Statement

Create an API for a social networking application using Django Rest Framework with the following functionalities.

### Constraints
- Use any database of your choice.Here sqlite3 has been used.
- You are free to design Request/Response fields/formats.

## User Login/Signup
- Users should be able to login with their email and password (email should be case insensitive).
- Users should be able to signup with their email only (no OTP verification required, valid email format is sufficient).
- Except for signup and login, every API should be called for authenticated users only.

## API Functionalities

### 1. User Search
- API to search other users by email and name (paginate up to 10 records per page).
  - If search keyword matches exact email, return user associated with the email.
  - If the search keyword contains any part of the name, return a list of all users.
    - e.g., Amarendra, Amar, Aman, Abhirama are three users and if users search with "am", then all of these users should be shown in the search result because "am" substring is part of all of these names.
  - There will be only one search keyword that will search either by name or email.

### 2. Friend Requests
- API to send/accept/reject friend requests.
- API to list friends (list of users who have accepted friend request).
- List pending friend requests (received friend request).
- Users can not send more than 3 friend requests within a minute.

## Technologies Used
- Django
- Django Rest Framework
- [Database of your choice]-[sqlite3 is used]

## Setup Instructions
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.


## Usage
1. Run the Django development server.
2. [Instructions for API usage and endpoints]

## Contributors
- [Varsha Madhavan]

## API URLS
1. Registration
    http://127.0.0.1:8000/register/
2. Login
    http://127.0.0.1:8000/login/
3. Send friend request
    http://127.0.0.1:8000/friend-request/send/
4. Search friends
    http://127.0.0.1:8000/search/?<query parameter>
5. Respond to friend request
    http://127.0.0.1:8000/friend-request/respond/id/
6. Pending friend requests
    http://127.0.0.1:8000/friend-requests/pending/
7. View friends   
    http://127.0.0.1:8000/friends/
    
