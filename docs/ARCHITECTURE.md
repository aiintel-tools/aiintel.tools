# AI Directory Platform Architecture

## System Overview

The AI Directory Platform is built using a modern web application architecture with a clear separation between frontend and backend components:

- **Frontend**: React-based single-page application (SPA)
- **Backend**: Flask-based RESTful API
- **Database**: SQLite (development) / PostgreSQL (production)

## Frontend Architecture

The frontend is built with React and follows a component-based architecture:

### Key Components

- **App**: Main application component and routing
- **Header**: Navigation and authentication controls
- **HomePage**: Landing page with featured tools and statistics
- **ToolsPage**: Directory browsing with filters and search
- **ToolDetailPage**: Detailed information about specific tools
- **AuthPage**: User registration and login
- **UserDashboard**: User profile, favorites, and subscription management
- **AdminDashboard**: Admin portal for managing users, tools, and content

### State Management

- **Context API**: Used for authentication state and notifications
- **Local State**: Component-specific state using React hooks

## Backend Architecture

The backend follows a modular architecture with clear separation of concerns:

### Key Components

- **Models**: SQLAlchemy ORM models for database entities
- **Routes**: API endpoints organized by resource type
- **Services**: Business logic and data processing
- **Utils**: Helper functions and utilities
- **Config**: Application configuration

### Database Schema

- **Users**: User accounts and authentication
- **AITools**: AI tool listings with details and metadata
- **Categories**: Tool categories for organization
- **Industries**: Industry classifications for tools
- **Reviews**: User reviews and ratings
- **Subscriptions**: User subscription information
- **UserFavorites**: User's saved tools
- **UserActivityLog**: Tracking of user actions

## API Endpoints

### Authentication
- `POST /api/auth/register`: Create new user account
- `POST /api/auth/login`: Authenticate user
- `POST /api/auth/refresh`: Refresh authentication token
- `POST /api/auth/logout`: End user session

### Tools
- `GET /api/tools`: List all tools with filtering
- `GET /api/tools/:id`: Get specific tool details
- `POST /api/tools`: Create new tool (admin)
- `PUT /api/tools/:id`: Update tool (admin)
- `DELETE /api/tools/:id`: Delete tool (admin)

### Users
- `GET /api/users`: List all users (admin)
- `GET /api/users/:id`: Get user details
- `PUT /api/users/:id`: Update user
- `DELETE /api/users/:id`: Delete user

### Categories
- `GET /api/categories`: List all categories
- `POST /api/categories`: Create category (admin)
- `PUT /api/categories/:id`: Update category (admin)
- `DELETE /api/categories/:id`: Delete category (admin)

### Reviews
- `GET /api/tools/:id/reviews`: Get reviews for a tool
- `POST /api/tools/:id/reviews`: Create review
- `PUT /api/reviews/:id`: Update review
- `DELETE /api/reviews/:id`: Delete review

### Subscriptions
- `GET /api/subscriptions`: List subscription plans
- `POST /api/subscriptions`: Create subscription
- `PUT /api/subscriptions/:id`: Update subscription
- `DELETE /api/subscriptions/:id`: Cancel subscription

## Authentication Flow

1. User registers or logs in
2. Backend validates credentials and issues JWT token
3. Frontend stores token in localStorage
4. Token is included in Authorization header for API requests
5. Backend validates token for protected endpoints

## Deployment Architecture

### Development
- Frontend: Vite dev server
- Backend: Flask development server
- Database: SQLite

### Production
- Frontend: Static files served from CDN
- Backend: Gunicorn with Flask application
- Database: PostgreSQL
- File Storage: Cloud storage for uploaded images

