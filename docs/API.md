# AI Directory API Documentation

## Base URL

```
https://api.aiintel.tools
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Headers

```
Authorization: Bearer <token>
```

### Endpoints

#### Register

```
POST /api/auth/register
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Example Inc.",
  "industry": "Technology"
}
```

Response:
```json
{
  "message": "User registered successfully",
  "user_id": 123,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login

```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "message": "Login successful",
  "user_id": 123,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## AI Tools

### List Tools

```
GET /api/tools
```

Query parameters:
- `category`: Filter by category ID
- `industry`: Filter by industry ID
- `access_level`: Filter by access level (public, premium, business)
- `search`: Search term
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

Response:
```json
{
  "tools": [
    {
      "id": 1,
      "name": "ChatGPT",
      "category": "Conversational AI",
      "description": "Advanced AI chatbot for conversations and content creation",
      "website_url": "https://chat.openai.com",
      "access_level": "public",
      "rating": 4.8,
      "image_url": "https://example.com/images/chatgpt.png",
      "business_utility": "Automate customer support and generate content efficiently",
      "price_point": {
        "free_tier": true,
        "starting_price": 20,
        "pricing_model": "monthly subscription"
      }
    }
  ],
  "total": 253,
  "page": 1,
  "pages": 13
}
```

### Get Tool Details

```
GET /api/tools/:id
```

Response:
```json
{
  "id": 1,
  "name": "ChatGPT",
  "category": "Conversational AI",
  "description": "Advanced AI chatbot for conversations and content creation",
  "website_url": "https://chat.openai.com",
  "access_level": "public",
  "rating": 4.8,
  "image_url": "https://example.com/images/chatgpt.png",
  "business_utility": "Automate customer support and generate content efficiently",
  "price_point": {
    "free_tier": true,
    "starting_price": 20,
    "pricing_model": "monthly subscription"
  },
  "industries": ["Technology", "Marketing", "Education", "Healthcare"],
  "reviews_count": 156,
  "guides": [
    {
      "id": 1,
      "title": "Getting Started with ChatGPT",
      "description": "Learn how to set up and use ChatGPT effectively"
    }
  ]
}
```

### Create Tool (Admin)

```
POST /api/tools
```

Request body:
```json
{
  "name": "New AI Tool",
  "category_id": 1,
  "description": "Description of the tool",
  "website_url": "https://example.com",
  "access_level": "premium",
  "image": "[Base64 encoded image]",
  "business_utility": "How this tool helps businesses",
  "price_point": {
    "free_tier": false,
    "starting_price": 29,
    "pricing_model": "monthly subscription"
  },
  "industry_ids": [1, 3, 5]
}
```

Response:
```json
{
  "message": "Tool created successfully",
  "tool_id": 254
}
```

### Update Tool (Admin)

```
PUT /api/tools/:id
```

Request body: Same as create tool

Response:
```json
{
  "message": "Tool updated successfully"
}
```

### Delete Tool (Admin)

```
DELETE /api/tools/:id
```

Response:
```json
{
  "message": "Tool deleted successfully"
}
```

## Tool Guides

### List Guides for Tool

```
GET /api/tools/:id/guides
```

Response:
```json
{
  "guides": [
    {
      "id": 1,
      "title": "Getting Started with ChatGPT",
      "description": "Learn how to set up and use ChatGPT effectively",
      "content": "Markdown content goes here...",
      "created_at": "2025-07-15T10:30:00Z"
    }
  ]
}
```

### Create Guide (Admin)

```
POST /api/tools/:id/guides
```

Request body:
```json
{
  "title": "Advanced ChatGPT Prompting",
  "description": "Learn advanced prompting techniques",
  "content": "Markdown content goes here..."
}
```

Response:
```json
{
  "message": "Guide created successfully",
  "guide_id": 5
}
```

## Users

### Get User Profile

```
GET /api/users/me
```

Response:
```json
{
  "id": 123,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Example Inc.",
  "industry": "Technology",
  "subscription": {
    "plan": "premium",
    "status": "active",
    "expires_at": "2026-07-27"
  },
  "favorites_count": 15,
  "reviews_count": 8
}
```

### Update User Profile

```
PUT /api/users/me
```

Request body:
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "company": "New Company Inc.",
  "industry": "Marketing"
}
```

Response:
```json
{
  "message": "Profile updated successfully"
}
```

## User Favorites

### List User Favorites

```
GET /api/users/me/favorites
```

Response:
```json
{
  "favorites": [
    {
      "id": 1,
      "tool_id": 5,
      "tool_name": "ChatGPT",
      "category": "Conversational AI",
      "added_at": "2025-07-15T10:30:00Z"
    }
  ]
}
```

### Add Favorite

```
POST /api/users/me/favorites
```

Request body:
```json
{
  "tool_id": 10
}
```

Response:
```json
{
  "message": "Tool added to favorites"
}
```

### Remove Favorite

```
DELETE /api/users/me/favorites/:tool_id
```

Response:
```json
{
  "message": "Tool removed from favorites"
}
```

## Reviews

### Create Review

```
POST /api/tools/:id/reviews
```

Request body:
```json
{
  "rating": 4.5,
  "content": "This tool has been very helpful for our business..."
}
```

Response:
```json
{
  "message": "Review submitted successfully",
  "review_id": 42
}
```

### Update Review

```
PUT /api/reviews/:id
```

Request body:
```json
{
  "rating": 5.0,
  "content": "Updated review content..."
}
```

Response:
```json
{
  "message": "Review updated successfully"
}
```

## Subscriptions

### List Subscription Plans

```
GET /api/subscription-plans
```

Response:
```json
{
  "plans": [
    {
      "id": "free",
      "name": "Free",
      "price": 0,
      "billing_cycle": "monthly",
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
      "price": 9,
      "billing_cycle": "monthly",
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
      "price": 29,
      "billing_cycle": "monthly",
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

### Create Subscription

```
POST /api/subscriptions
```

Request body:
```json
{
  "plan_id": "premium",
  "payment_method_id": "pm_card_visa"
}
```

Response:
```json
{
  "message": "Subscription created successfully",
  "subscription_id": "sub_12345",
  "status": "active",
  "current_period_end": "2025-08-27T00:00:00Z"
}
```

### Cancel Subscription

```
DELETE /api/subscriptions/:id
```

Response:
```json
{
  "message": "Subscription cancelled successfully",
  "end_date": "2025-08-27T00:00:00Z"
}
```

## Admin Endpoints

### List Users (Admin)

```
GET /api/admin/users
```

Query parameters:
- `search`: Search by name or email
- `subscription`: Filter by subscription type
- `page`: Page number
- `per_page`: Items per page

Response:
```json
{
  "users": [
    {
      "id": 123,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "company": "Example Inc.",
      "subscription": {
        "plan": "premium",
        "status": "active"
      },
      "created_at": "2025-06-15T10:30:00Z"
    }
  ],
  "total": 15482,
  "page": 1,
  "pages": 775
}
```

### Dashboard Statistics (Admin)

```
GET /api/admin/statistics
```

Response:
```json
{
  "users": {
    "total": 15482,
    "growth": 12,
    "by_plan": {
      "free": 12500,
      "premium": 2500,
      "business": 482
    }
  },
  "tools": {
    "total": 253,
    "by_category": {
      "Conversational AI": 45,
      "Image Generation": 38,
      "Code Assistant": 25
    }
  },
  "reviews": {
    "total": 8743,
    "average_rating": 4.6
  },
  "revenue": {
    "monthly": 12850,
    "growth": 8.5
  }
}
```

