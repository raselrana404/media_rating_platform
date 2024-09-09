# Media Rating Platform

## Overview
**Media Rating Platform** is a REST API built using Python, Django, and Django Rest Framework (DRF). The primary goal of this project is to explore and understand the core concepts of DRF. While certain best practices such as using a custom user model, following strict API patterns, and implementing advanced functionality are not emphasized, the project is designed to showcase how DRF works in practice.

## Objective
The main objective of this project is to provide hands-on experience with building a REST API using DRF. The focus is on understanding key DRF components and features rather than adhering to advanced design patterns.

## Key Concepts Covered
1. **DRF Views**:
   - `APIView`, `GenericAPIView`, and Concrete Views
2. **Serializers**:
   - Basic serializers, Nested serializers, and Serializer relationships
3. **Permissions**:
   - Basic permissions and Custom permissions
4. **Authentication**:
   - Token-based authentication and JWT authentication using `djangorestframework-simplejwt`
5. **Throttling**:
   - Throttling for both anonymous users and authenticated users
6. **Pagination**:
   - Page Number Pagination, Limit Offset Pagination, and Cursor Pagination
7. **Filtering**, **Searching**, and **Ordering**
8. **Basic Testing**:
   - Demonstrating testing approaches with DRF APIs

> **Note**: The project includes extensive comments that contain real code examples, which are commented out. These examples are provided to cover various topics and serve as reference material for understanding different concepts.

## Features
- **User Management**:
   - Users can register, login, and logout.
   - Only superusers can promote users to admin/staff roles.
- **Streaming Platform Management**:
   - Admins can create, edit, and delete streaming platforms (like Netflix, Hulu, etc.).
- **Watchlist Management**:
   - Admins can create, edit, and delete watchlist items (e.g., movies, TV shows).
- **Review Management**:
   - Users can leave a review for each watchlist item (one review per item).
   - Only the review owner or an admin can update or delete the review.

## Tech Stack / Requirements
- **Python**
- **Django**
- **Django Rest Framework**
- **djangorestframework-simplejwt** (for JWT-based authentication)
- **Code Editor** (Recommended: Visual Studio Code)

## Level
This project is suited for **Intermediate Learners** who have some experience with Python and Django and are looking to gain a deeper understanding of DRF.

## Tips
After learning the basics covered in this project, it is recommended to consult the [official DRF documentation](https://www.django-rest-framework.org/) to further expand your knowledge and apply best practices.

## How to Run the Project

1. **Download or Clone the Project**:
   - Download the source code or use the following command to clone the repository via terminal:
     ```bash
     git clone [repository-url]
     ```

2. **Set up a Virtual Environment**:
   - Navigate to the project folder and create a virtual environment:
     - On Linux/macOS:
       ```bash
       python3 -m venv venv
       ```
     - On Windows:
       ```bash
       python -m venv venv
       ```

3. **Install Required Packages**:
   - Activate your virtual environment and install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Apply Migrations**:
   - Navigate to the project root directory and run the following commands to apply the database migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Create a Superuser**:
   - Create a superuser to access the Django admin panel:
     ```bash
     python manage.py createsuperuser
     ```

6. **Run the Development Server**:
   - Start the Django development server (port is optional, default is 8000):
     ```bash
     python manage.py runserver
     ```

7. **Access the Admin Panel**:
   - Go to the link displayed in the terminal or open `localhost:[portnumber]/admin` in your browser to create some Streaming Platforms and Watchlists.

8. **Explore the API**:
   - After creating the necessary data, you can interact with the API using any API client (e.g., Postman) or via the Django Rest Framework’s web interface.

---

Enjoy exploring the Django Rest Framework! 🎉
