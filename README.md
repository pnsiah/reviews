# Movie Review Platform - CS50 Final Project

## Project Overview

This project is a **movie and TV show review platform** built as part of my CS50 final project. The application allows users to search for movies and TV shows, explore trending and popular titles, view detailed information about individual items, and leave reviews for their favorite content. The platform is designed to provide users with an engaging and interactive experience while exploring the world of entertainment.

## Key Features

1. **User Registration and Authentication**:

   - New users can register with a unique username, email, and password.
   - Passwords are securely hashed using `werkzeug.security` before being stored in the database.
   - Registered users can log in and access personalized features like adding reviews or editing their profiles.

2. **Trending and Popular Movies**:

   - The homepage displays trending and popular movies fetched dynamically using The Movie Database (TMDb) API.
   - Users can explore the most talked-about content with ease.

3. **Search Functionality**:

   - Users can search for movies, TV shows, or both using a multi-search feature.
   - Results are displayed dynamically with pagination for seamless navigation through large datasets.

4. **Detailed Movie and TV Show Pages**:

   - Each movie or TV show has its dedicated page with detailed information such as release date, rating, and synopsis.
   - Reviews from other users are displayed, including their usernames, profile pictures, and the review content.

5. **Review System**:

   - Logged-in users can leave reviews for movies or TV shows, including a title and detailed content.
   - Reviews are displayed alongside the relevant content and stored in a SQLite database.

6. **Genre-Based Browsing**:

   - Users can browse movies and TV shows by genre, making it easier to find content that matches their preferences.

7. **User Profiles**:

   - Each user has a profile page where they can update their username, email, and profile picture.
   - Profile pictures are resized and stored securely on the server.

8. **Responsive Design**:
   - The application features responsive templates that work seamlessly on desktop and mobile devices.

## Tools and Technologies

### Backend:

- **Flask**: The core framework used to build the application, handle routing, and manage server-side logic.
- **SQLite**: A lightweight database for managing user accounts, reviews, and other application data.
- **Flask-Session**: For session management, storing user login states, and handling session data securely.

### Frontend:

- **Jinja2**: Used for dynamic HTML templating.
- **Bootstrap**: Provides responsive design and user interface elements.

### External APIs:

- **TMDb API**: Used to fetch movie and TV show data, including details, trending content, genres, and search results.

### Other Tools:

- **Werkzeug**: For password hashing and authentication.
- **Pillow**: For processing and resizing user-uploaded profile pictures.

## Database Design

1. **Users**:

   - Stores user account details such as `id`, `username`, `email`, `password`, `image_file`, and `created_at`.

2. **Movie Reviews**:

   - Contains reviews for movies, including `id`, `author_id`, `movie_id`, `title`, `content`, and `created_at`.

3. **TV Reviews**:
   - Stores reviews for TV shows with similar fields as the movie reviews table.

## Core Functionalities Explained

### User Authentication

- Registration and login routes ensure secure handling of user data.
- Passwords are hashed with `generate_password_hash` and verified during login.

### API Integration

- The TMDb API provides real-time data on trending and popular titles.
- Functions like `fetch_data` handle API requests and parse responses.

### Reviews and Ratings

- Users can leave reviews for movies and TV shows.
- Reviews are stored in a database and displayed alongside relevant content.

### User Profiles

- Users can update their profiles and upload profile pictures.
- Images are resized and securely stored using the `Pillow` library.

### Custom Filters and Utilities

- `format_year` filter extracts the year from a release date string.
- `rating_to_stars` converts numeric ratings into a star-based visual representation.

## Challenges and Solutions

1. **API Data Parsing**:

   - Added error handling for unexpected API response formats or missing data.

2. **Session Management**:

   - Utilized Flask’s `@app.context_processor` to inject session data into templates globally.

3. **Profile Picture Uploads**:

   - Resized and stored images with unique filenames for secure handling.

4. **Dynamic Pagination**:
   - Implemented pagination to fetch and display large datasets seamlessly.

## Future Improvements

1. **Improved Search**:

   - Add filters for year, rating, and other parameters in the search functionality.

2. **Social Features**:

   - Allow users to follow each other and see reviews from their network.

3. **Advanced Profile Customization**:

   - Include a bio and favorite genres in user profiles.

4. **Deployment**:

   - Host the platform on a service like Heroku or AWS for public access.

5. **Review Editing**:
   - Allow users to edit their reviews directly from the movie or TV show page for better flexibility and content management.

## Conclusion

This project demonstrates the integration of Flask, external APIs, and modern web development techniques to create a feature-rich movie review platform. The application combines real-time data, user interaction, and responsive design to provide an engaging experience. This journey helped me deepen my understanding of full-stack development and solve real-world challenges.

---

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=pnsiah&show_icons=true&theme=radical)
