# AI Directory Platform - Database Schema Design

## Overview

This document outlines the database schema design for the AI Directory Platform. The schema is designed to support all the features of the platform, including user management, AI tool listings, categories, industries, subscriptions, and reviews.

## Database Tables

### Users

The `users` table stores information about registered users of the platform.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the user |
| email | TEXT | NOT NULL, UNIQUE | User's email address (used for login) |
| password_hash | TEXT | NOT NULL | Hashed password for security |
| first_name | TEXT | NOT NULL | User's first name |
| last_name | TEXT | NOT NULL | User's last name |
| company | TEXT | | User's company name (optional) |
| job_title | TEXT | | User's job title (optional) |
| industry_id | INTEGER | FOREIGN KEY | Reference to the industry the user belongs to |
| subscription_tier | TEXT | NOT NULL | User's subscription tier (Free, Premium, Business) |
| subscription_start_date | DATETIME | | Start date of the current subscription |
| subscription_end_date | DATETIME | | End date of the current subscription |
| is_admin | BOOLEAN | NOT NULL, DEFAULT 0 | Whether the user has admin privileges |
| created_at | DATETIME | NOT NULL | When the user account was created |
| updated_at | DATETIME | NOT NULL | When the user account was last updated |

### AI Tools

The `ai_tools` table stores information about AI tools listed in the directory.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the tool |
| name | TEXT | NOT NULL | Name of the AI tool |
| description | TEXT | NOT NULL | Detailed description of the tool |
| category_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the category the tool belongs to |
| website_url | TEXT | | URL to the tool's website |
| image_path | TEXT | | Path to the tool's image file |
| access_level | TEXT | NOT NULL | Access level required (Public, Premium Only, Business Only) |
| rating | REAL | | Average rating of the tool (1-5) |
| created_at | DATETIME | NOT NULL | When the tool was added to the directory |
| updated_at | DATETIME | NOT NULL | When the tool was last updated |

### Categories

The `categories` table stores the categories that AI tools can belong to.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the category |
| name | TEXT | NOT NULL, UNIQUE | Name of the category |
| description | TEXT | | Description of the category |
| icon | TEXT | | Icon representing the category |
| created_at | DATETIME | NOT NULL | When the category was created |
| updated_at | DATETIME | NOT NULL | When the category was last updated |

### Industries

The `industries` table stores the industries that users and AI tools can be associated with.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the industry |
| name | TEXT | NOT NULL, UNIQUE | Name of the industry |
| description | TEXT | | Description of the industry |
| created_at | DATETIME | NOT NULL | When the industry was created |
| updated_at | DATETIME | NOT NULL | When the industry was last updated |

### Tool Industries

The `tool_industries` table is a junction table that maps the many-to-many relationship between AI tools and industries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the mapping |
| tool_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the AI tool |
| industry_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the industry |
| created_at | DATETIME | NOT NULL | When the mapping was created |

### Reviews

The `reviews` table stores user reviews of AI tools.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the review |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the user who wrote the review |
| tool_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the AI tool being reviewed |
| rating | INTEGER | NOT NULL | Rating given (1-5) |
| comment | TEXT | | Review text |
| is_verified | BOOLEAN | NOT NULL, DEFAULT 0 | Whether the review is verified |
| created_at | DATETIME | NOT NULL | When the review was created |
| updated_at | DATETIME | NOT NULL | When the review was last updated |

### User Favorites

The `user_favorites` table stores the AI tools that users have marked as favorites.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the favorite |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the user |
| tool_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the AI tool |
| created_at | DATETIME | NOT NULL | When the tool was marked as favorite |

### User Activity Logs

The `user_activity_logs` table stores logs of user activity on the platform.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the log entry |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the user |
| activity_type | TEXT | NOT NULL | Type of activity (login, view_tool, add_favorite, etc.) |
| details | TEXT | | Additional details about the activity |
| created_at | DATETIME | NOT NULL | When the activity occurred |

### Payment Transactions

The `payment_transactions` table stores information about subscription payments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the transaction |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Reference to the user |
| amount | REAL | NOT NULL | Amount paid |
| currency | TEXT | NOT NULL | Currency of the payment |
| status | TEXT | NOT NULL | Status of the payment (completed, failed, refunded) |
| payment_method | TEXT | | Payment method used |
| subscription_tier | TEXT | NOT NULL | Subscription tier purchased |
| transaction_date | DATETIME | NOT NULL | When the transaction occurred |
| metadata | TEXT | | Additional metadata about the transaction |

## Relationships

1. **Users to Industries**: Many-to-one relationship. Each user can belong to one industry.
2. **AI Tools to Categories**: Many-to-one relationship. Each AI tool belongs to one category.
3. **AI Tools to Industries**: Many-to-many relationship through the `tool_industries` junction table.
4. **Users to AI Tools (Favorites)**: Many-to-many relationship through the `user_favorites` table.
5. **Users to AI Tools (Reviews)**: Many-to-many relationship through the `reviews` table.
6. **Users to Payment Transactions**: One-to-many relationship. Each user can have multiple payment transactions.
7. **Users to User Activity Logs**: One-to-many relationship. Each user can have multiple activity logs.

## Indexes

To optimize query performance, the following indexes will be created:

1. Index on `users.email` for fast login lookups
2. Index on `ai_tools.category_id` for fast category filtering
3. Index on `ai_tools.access_level` for fast access level filtering
4. Index on `reviews.tool_id` for fast retrieval of reviews for a specific tool
5. Index on `user_favorites.user_id` for fast retrieval of a user's favorites
6. Index on `user_activity_logs.user_id` for fast retrieval of a user's activity
7. Index on `payment_transactions.user_id` for fast retrieval of a user's payment history

## Data Migration Strategy

For the initial deployment, we will create the database schema and populate it with seed data for categories, industries, and sample AI tools. For future updates, we will use migration scripts to handle schema changes without data loss.

## File Storage

For storing AI tool images, we will use a file storage system with the following structure:

```
/uploads
  /tool_images
    /[tool_id]_[timestamp].jpg
```

The `image_path` column in the `ai_tools` table will store the relative path to the image file.

## Security Considerations

1. User passwords will be hashed using bcrypt before storage
2. Database access will be restricted to the application server
3. Input validation will be performed on all user inputs
4. Prepared statements will be used for all database queries to prevent SQL injection
5. Regular backups will be performed to prevent data loss

## Conclusion

This database schema design provides a solid foundation for the AI Directory Platform. It supports all the required features while maintaining good performance and security practices. The schema is also flexible enough to accommodate future enhancements to the platform.

