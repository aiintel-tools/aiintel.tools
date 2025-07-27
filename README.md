# AI Directory Platform

A comprehensive directory website for AI tools with membership options, allowing business owners to discover, compare, and implement AI tools for their specific industry needs.

## Features

- **AI Tools Directory**: Browse and search through 250+ AI tools organized by category and industry
- **Membership System**: Three-tier subscription model (Free, Premium, Business)
- **Admin Portal**: Manage users, tools, subscriptions, and content
- **User Dashboard**: Track favorites, reviews, and subscription status
- **Implementation Guides**: Detailed guides for implementing AI tools
- **Review System**: Verified user reviews and ratings

## Repository Structure

- `/frontend`: React-based frontend application
- `/backend`: Flask-based backend API
- `/docs`: Documentation and guides

## Getting Started

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Deployment

The application is designed to be deployed as:
- Frontend: Static site hosting (Netlify, Vercel, etc.)
- Backend: Python web server with Gunicorn

## License

[MIT License](LICENSE)

