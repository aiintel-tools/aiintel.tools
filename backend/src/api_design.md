# AI Directory Platform - API Design

## Overview

This document outlines the API design for the AI Directory Platform. The API will provide endpoints for all the features of the platform, including user management, AI tool listings, categories, industries, subscriptions, and reviews.

## API Base URL

All API endpoints will be prefixed with `/api/v1` to allow for versioning in the future.

## Authentication

The API will use JWT (JSON Web Tokens) for authentication. Most endpoints will require authentication, except for public endpoints like retrieving public AI tools or categories.

### Authentication Flow

1. User logs in with email and password
2. Server validates credentials and returns a JWT token
3. Client includes the JWT token in the `Authorization` header for subsequent requests
4. Server validates the token and processes the request

## API Endpoints

### Authentication

#### POST /api/v1/auth/register

Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Acme Inc.",
  "job_title": "Product Manager",
  "industry_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "subscription_tier": "Free",
    "token": "jwt_token_here"
  }
}
```

#### POST /api/v1/auth/login

Log in an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "subscription_tier": "Free",
    "is_admin": false,
    "token": "jwt_token_here"
  }
}
```

#### POST /api/v1/auth/refresh

Refresh an expired JWT token.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Token refreshed",
  "data": {
    "token": "new_jwt_token_here"
  }
}
```

### Users

#### GET /api/v1/users/me

Get the current user's profile.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": "Acme Inc.",
    "job_title": "Product Manager",
    "industry": {
      "id": 1,
      "name": "Technology"
    },
    "subscription_tier": "Free",
    "subscription_start_date": "2023-01-01T00:00:00Z",
    "subscription_end_date": null,
    "created_at": "2023-01-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/users/me

Update the current user's profile.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "company": "New Company Inc.",
  "job_title": "Senior Product Manager",
  "industry_id": 2
}
```

**Response:**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "company": "New Company Inc.",
    "job_title": "Senior Product Manager",
    "industry": {
      "id": 2,
      "name": "Finance"
    },
    "subscription_tier": "Free",
    "subscription_start_date": "2023-01-01T00:00:00Z",
    "subscription_end_date": null,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-02-01T00:00:00Z"
  }
}
```

#### GET /api/v1/users

Get a list of all users (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 20)
- `search`: Search term for email, first name, or last name
- `subscription_tier`: Filter by subscription tier

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "user_id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "company": "New Company Inc.",
        "job_title": "Senior Product Manager",
        "industry": {
          "id": 2,
          "name": "Finance"
        },
        "subscription_tier": "Free",
        "created_at": "2023-01-01T00:00:00Z"
      },
      // More users...
    ],
    "pagination": {
      "total": 100,
      "page": 1,
      "limit": 20,
      "pages": 5
    }
  }
}
```

#### GET /api/v1/users/:id

Get a specific user by ID (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "company": "New Company Inc.",
    "job_title": "Senior Product Manager",
    "industry": {
      "id": 2,
      "name": "Finance"
    },
    "subscription_tier": "Free",
    "subscription_start_date": "2023-01-01T00:00:00Z",
    "subscription_end_date": null,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-02-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/users/:id

Update a specific user (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "company": "New Company Inc.",
  "job_title": "Senior Product Manager",
  "industry_id": 2,
  "subscription_tier": "Premium",
  "is_admin": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "company": "New Company Inc.",
    "job_title": "Senior Product Manager",
    "industry": {
      "id": 2,
      "name": "Finance"
    },
    "subscription_tier": "Premium",
    "is_admin": false,
    "subscription_start_date": "2023-01-01T00:00:00Z",
    "subscription_end_date": "2024-01-01T00:00:00Z",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-02-01T00:00:00Z"
  }
}
```

#### DELETE /api/v1/users/:id

Delete a specific user (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

### AI Tools

#### GET /api/v1/tools

Get a list of AI tools.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 20)
- `search`: Search term for tool name or description
- `category_id`: Filter by category ID
- `industry_id`: Filter by industry ID
- `access_level`: Filter by access level (Public, Premium Only, Business Only)
- `sort`: Sort field (name, rating, created_at)
- `order`: Sort order (asc, desc)

**Response:**
```json
{
  "success": true,
  "data": {
    "tools": [
      {
        "id": 1,
        "name": "ChatGPT",
        "description": "AI language model by OpenAI",
        "category": {
          "id": 1,
          "name": "Conversational AI"
        },
        "website_url": "https://chat.openai.com",
        "image_url": "/uploads/tool_images/1_1625097600000.jpg",
        "access_level": "Public",
        "rating": 4.8,
        "industries": [
          {
            "id": 1,
            "name": "Technology"
          },
          {
            "id": 4,
            "name": "Education"
          }
        ],
        "created_at": "2023-01-01T00:00:00Z"
      },
      // More tools...
    ],
    "pagination": {
      "total": 100,
      "page": 1,
      "limit": 20,
      "pages": 5
    }
  }
}
```

#### GET /api/v1/tools/:id

Get a specific AI tool by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "ChatGPT",
    "description": "AI language model by OpenAI",
    "category": {
      "id": 1,
      "name": "Conversational AI"
    },
    "website_url": "https://chat.openai.com",
    "image_url": "/uploads/tool_images/1_1625097600000.jpg",
    "access_level": "Public",
    "rating": 4.8,
    "industries": [
      {
        "id": 1,
        "name": "Technology"
      },
      {
        "id": 4,
        "name": "Education"
      }
    ],
    "reviews": [
      {
        "id": 1,
        "user": {
          "id": 2,
          "first_name": "Jane",
          "last_name": "Doe"
        },
        "rating": 5,
        "comment": "Great tool!",
        "created_at": "2023-01-15T00:00:00Z"
      },
      // More reviews...
    ],
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-02-01T00:00:00Z"
  }
}
```

#### POST /api/v1/tools

Create a new AI tool (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
Content-Type: multipart/form-data
```

**Request Body:**
```
name: ChatGPT
description: AI language model by OpenAI
category_id: 1
website_url: https://chat.openai.com
access_level: Public
image: [binary file data]
industry_ids: [1, 4]
```

**Response:**
```json
{
  "success": true,
  "message": "Tool created successfully",
  "data": {
    "id": 1,
    "name": "ChatGPT",
    "description": "AI language model by OpenAI",
    "category": {
      "id": 1,
      "name": "Conversational AI"
    },
    "website_url": "https://chat.openai.com",
    "image_url": "/uploads/tool_images/1_1625097600000.jpg",
    "access_level": "Public",
    "industries": [
      {
        "id": 1,
        "name": "Technology"
      },
      {
        "id": 4,
        "name": "Education"
      }
    ],
    "created_at": "2023-01-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/tools/:id

Update an existing AI tool (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
Content-Type: multipart/form-data
```

**Request Body:**
```
name: ChatGPT
description: Updated description
category_id: 1
website_url: https://chat.openai.com
access_level: Premium Only
image: [binary file data] (optional)
industry_ids: [1, 2, 4]
```

**Response:**
```json
{
  "success": true,
  "message": "Tool updated successfully",
  "data": {
    "id": 1,
    "name": "ChatGPT",
    "description": "Updated description",
    "category": {
      "id": 1,
      "name": "Conversational AI"
    },
    "website_url": "https://chat.openai.com",
    "image_url": "/uploads/tool_images/1_1625097600000.jpg",
    "access_level": "Premium Only",
    "industries": [
      {
        "id": 1,
        "name": "Technology"
      },
      {
        "id": 2,
        "name": "Finance"
      },
      {
        "id": 4,
        "name": "Education"
      }
    ],
    "updated_at": "2023-02-01T00:00:00Z"
  }
}
```

#### DELETE /api/v1/tools/:id

Delete an AI tool (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Tool deleted successfully"
}
```

### Categories

#### GET /api/v1/categories

Get a list of all categories.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Conversational AI",
      "description": "AI tools for natural language conversations",
      "icon": "chat-bubble",
      "tool_count": 15
    },
    {
      "id": 2,
      "name": "Image Generation",
      "description": "AI tools for generating images",
      "icon": "image",
      "tool_count": 10
    },
    // More categories...
  ]
}
```

#### POST /api/v1/categories

Create a new category (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "Video Generation",
  "description": "AI tools for generating videos",
  "icon": "video"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Category created successfully",
  "data": {
    "id": 3,
    "name": "Video Generation",
    "description": "AI tools for generating videos",
    "icon": "video",
    "created_at": "2023-03-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/categories/:id

Update a category (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "Video AI",
  "description": "AI tools for generating and editing videos",
  "icon": "video-camera"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Category updated successfully",
  "data": {
    "id": 3,
    "name": "Video AI",
    "description": "AI tools for generating and editing videos",
    "icon": "video-camera",
    "updated_at": "2023-03-15T00:00:00Z"
  }
}
```

#### DELETE /api/v1/categories/:id

Delete a category (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Category deleted successfully"
}
```

### Industries

#### GET /api/v1/industries

Get a list of all industries.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Technology",
      "description": "Technology and software companies"
    },
    {
      "id": 2,
      "name": "Finance",
      "description": "Financial services and banking"
    },
    // More industries...
  ]
}
```

#### POST /api/v1/industries

Create a new industry (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "Healthcare",
  "description": "Healthcare and medical services"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Industry created successfully",
  "data": {
    "id": 3,
    "name": "Healthcare",
    "description": "Healthcare and medical services",
    "created_at": "2023-03-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/industries/:id

Update an industry (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "name": "Healthcare & Medical",
  "description": "Healthcare, medical services, and biotechnology"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Industry updated successfully",
  "data": {
    "id": 3,
    "name": "Healthcare & Medical",
    "description": "Healthcare, medical services, and biotechnology",
    "updated_at": "2023-03-15T00:00:00Z"
  }
}
```

#### DELETE /api/v1/industries/:id

Delete an industry (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Industry deleted successfully"
}
```

### Reviews

#### GET /api/v1/tools/:id/reviews

Get reviews for a specific AI tool.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 20)
- `sort`: Sort field (rating, created_at)
- `order`: Sort order (asc, desc)

**Response:**
```json
{
  "success": true,
  "data": {
    "reviews": [
      {
        "id": 1,
        "user": {
          "id": 2,
          "first_name": "Jane",
          "last_name": "Doe"
        },
        "rating": 5,
        "comment": "Great tool!",
        "is_verified": true,
        "created_at": "2023-01-15T00:00:00Z"
      },
      // More reviews...
    ],
    "pagination": {
      "total": 50,
      "page": 1,
      "limit": 20,
      "pages": 3
    }
  }
}
```

#### POST /api/v1/tools/:id/reviews

Create a review for an AI tool.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "rating": 5,
  "comment": "This tool has revolutionized my workflow!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review submitted successfully",
  "data": {
    "id": 2,
    "user": {
      "id": 1,
      "first_name": "John",
      "last_name": "Smith"
    },
    "rating": 5,
    "comment": "This tool has revolutionized my workflow!",
    "is_verified": false,
    "created_at": "2023-03-01T00:00:00Z"
  }
}
```

#### PUT /api/v1/reviews/:id

Update a review.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "rating": 4,
  "comment": "Updated review comment"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Review updated successfully",
  "data": {
    "id": 2,
    "user": {
      "id": 1,
      "first_name": "John",
      "last_name": "Smith"
    },
    "rating": 4,
    "comment": "Updated review comment",
    "is_verified": false,
    "updated_at": "2023-03-15T00:00:00Z"
  }
}
```

#### DELETE /api/v1/reviews/:id

Delete a review.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Review deleted successfully"
}
```

#### PUT /api/v1/reviews/:id/verify

Verify a review (admin only).

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Review verified successfully",
  "data": {
    "id": 2,
    "is_verified": true,
    "updated_at": "2023-03-15T00:00:00Z"
  }
}
```

### User Favorites

#### GET /api/v1/users/me/favorites

Get the current user's favorite AI tools.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of items per page (default: 20)

**Response:**
```json
{
  "success": true,
  "data": {
    "favorites": [
      {
        "id": 1,
        "tool": {
          "id": 1,
          "name": "ChatGPT",
          "description": "AI language model by OpenAI",
          "category": {
            "id": 1,
            "name": "Conversational AI"
          },
          "image_url": "/uploads/tool_images/1_1625097600000.jpg",
          "access_level": "Public",
          "rating": 4.8
        },
        "created_at": "2023-02-01T00:00:00Z"
      },
      // More favorites...
    ],
    "pagination": {
      "total": 10,
      "page": 1,
      "limit": 20,
      "pages": 1
    }
  }
}
```

#### POST /api/v1/tools/:id/favorite

Add an AI tool to the user's favorites.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Tool added to favorites",
  "data": {
    "id": 2,
    "tool_id": 2,
    "created_at": "2023-03-01T00:00:00Z"
  }
}
```

#### DELETE /api/v1/tools/:id/favorite

Remove an AI tool from the user's favorites.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "message": "Tool removed from favorites"
}
```

### Subscriptions

#### GET /api/v1/subscriptions/plans

Get available subscription plans.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "free",
      "name": "Free",
      "description": "Basic access to the AI Directory",
      "price": 0,
      "currency": "USD",
      "interval": "month",
      "features": [
        "Browse all AI tools",
        "Basic search and filters",
        "Tool ratings and reviews",
        "Community support"
      ]
    },
    {
      "id": "premium",
      "name": "Premium",
      "description": "Enhanced access with additional features",
      "price": 9.99,
      "currency": "USD",
      "interval": "month",
      "features": [
        "Everything in Free",
        "Advanced search filters",
        "Save favorite tools",
        "Write reviews",
        "Priority support",
        "Export tool lists"
      ]
    },
    {
      "id": "business",
      "name": "Business",
      "description": "Complete access for professional use",
      "price": 29.99,
      "currency": "USD",
      "interval": "month",
      "features": [
        "Everything in Premium",
        "Team collaboration",
        "Custom categories",
        "API access",
        "Analytics dashboard",
        "Dedicated support"
      ]
    }
  ]
}
```

#### POST /api/v1/subscriptions/subscribe

Subscribe to a plan.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "plan_id": "premium",
  "payment_method_id": "pm_card_visa"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Subscription created successfully",
  "data": {
    "subscription_id": "sub_123456",
    "plan": {
      "id": "premium",
      "name": "Premium"
    },
    "status": "active",
    "current_period_start": "2023-03-01T00:00:00Z",
    "current_period_end": "2023-04-01T00:00:00Z"
  }
}
```

#### GET /api/v1/subscriptions/me

Get the current user's subscription.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "subscription_id": "sub_123456",
    "plan": {
      "id": "premium",
      "name": "Premium"
    },
    "status": "active",
    "current_period_start": "2023-03-01T00:00:00Z",
    "current_period_end": "2023-04-01T00:00:00Z",
    "cancel_at_period_end": false,
    "payment_method": {
      "brand": "visa",
      "last4": "4242",
      "exp_month": 12,
      "exp_year": 2025
    }
  }
}
```

#### POST /api/v1/subscriptions/cancel

Cancel the current user's subscription.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Request Body:**
```json
{
  "cancel_immediately": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Subscription will be canceled at the end of the billing period",
  "data": {
    "subscription_id": "sub_123456",
    "status": "active",
    "cancel_at_period_end": true,
    "current_period_end": "2023-04-01T00:00:00Z"
  }
}
```

### Admin Dashboard

#### GET /api/v1/admin/dashboard

Get admin dashboard statistics.

**Request Headers:**
```
Authorization: Bearer jwt_token_here
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": {
      "total": 1500,
      "new_this_month": 120,
      "growth_percentage": 8.7
    },
    "tools": {
      "total": 253,
      "new_this_month": 15,
      "growth_percentage": 6.3
    },
    "reviews": {
      "total": 8743,
      "new_this_month": 432,
      "growth_percentage": 5.2
    },
    "revenue": {
      "total_monthly": 12850,
      "growth_percentage": 12.4,
      "by_plan": {
        "premium": 5850,
        "business": 7000
      }
    },
    "popular_tools": [
      {
        "id": 1,
        "name": "ChatGPT",
        "views": 3500,
        "favorites": 850,
        "reviews": 320
      },
      // More tools...
    ],
    "recent_activities": [
      {
        "id": 1,
        "type": "new_user",
        "user": {
          "id": 1500,
          "first_name": "Alice",
          "last_name": "Johnson"
        },
        "created_at": "2023-03-15T12:30:00Z"
      },
      // More activities...
    ]
  }
}
```

## Error Handling

All API endpoints will return consistent error responses with appropriate HTTP status codes.

**Example Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "details": null
  }
}
```

Common error codes:
- `INVALID_CREDENTIALS`: Invalid email or password
- `UNAUTHORIZED`: User is not authorized to access the resource
- `FORBIDDEN`: User does not have permission to perform the action
- `NOT_FOUND`: Resource not found
- `VALIDATION_ERROR`: Request validation failed
- `INTERNAL_ERROR`: Internal server error

## Rate Limiting

To prevent abuse, the API will implement rate limiting:

- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers will be included in all responses:
- `X-RateLimit-Limit`: Maximum number of requests allowed per minute
- `X-RateLimit-Remaining`: Number of requests remaining in the current minute
- `X-RateLimit-Reset`: Time in seconds until the rate limit resets

## Versioning

The API will be versioned using URL prefixes (e.g., `/api/v1`). When breaking changes are introduced, a new version will be created (e.g., `/api/v2`).

## CORS

The API will support Cross-Origin Resource Sharing (CORS) to allow requests from the frontend application. The following headers will be included in all responses:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Conclusion

This API design provides a comprehensive set of endpoints for the AI Directory Platform. It supports all the required features while maintaining good security practices and performance considerations. The design is also flexible enough to accommodate future enhancements to the platform.

