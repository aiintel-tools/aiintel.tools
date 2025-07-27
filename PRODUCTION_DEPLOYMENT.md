# A.I Intel - Production Deployment

## 🚀 Live URLs

### Frontend (React)
- **Production URL**: https://gzspwolk.manus.space
- **Framework**: React + Vite
- **Hosting**: Manus Platform
- **Features**: Responsive design, real-time data from API

### Backend (Flask API)
- **Production URL**: https://aiinteltools-production.up.railway.app
- **Admin Portal**: https://aiinteltools-production.up.railway.app/admin
- **Framework**: Flask + Gunicorn
- **Hosting**: Railway
- **Database**: JSON file storage with persistence

## 🔗 Integration

The frontend and backend are fully integrated:
- Frontend fetches live data from Railway API
- Admin portal changes reflect immediately on frontend
- CORS properly configured for cross-origin requests

## 📊 Features

### Frontend Features
- Homepage with dynamic statistics
- AI tools directory with real-time data
- Pricing page with subscription tiers
- User authentication interface
- Admin portal access via footer link

### Backend Features
- RESTful API endpoints for users, tools, reviews
- Admin portal with full CRUD operations
- Data persistence across deployments
- Edit functionality for users and tools
- Real-time statistics dashboard

## 🛠 Admin Portal Access

1. Go to frontend: https://gzspwolk.manus.space
2. Click "Admin Portal" in footer
3. Redirects to: https://aiinteltools-production.up.railway.app/admin
4. Add/edit users and AI tools
5. Changes appear immediately on frontend

## 📁 Repository Structure

```
aiintel.tools/
├── frontend/           # React application
│   ├── src/
│   ├── public/
│   ├── vercel.json     # Deployment config
│   └── package.json
├── backend/            # Flask API
│   ├── app.py          # Main application
│   ├── data/           # JSON data storage
│   ├── Dockerfile      # Container config
│   └── requirements.txt
└── docs/               # Documentation
```

## 🔄 Deployment Process

### Frontend Deployment
- Deployed via Manus Platform
- Automatic builds from GitHub
- Environment variables configured

### Backend Deployment
- Deployed via Railway
- Automatic deployments from GitHub
- Persistent data storage

## ✅ Production Ready

- ✅ Frontend-backend integration working
- ✅ Admin portal fully functional
- ✅ Real-time data synchronization
- ✅ CORS properly configured
- ✅ Responsive design
- ✅ Data persistence
- ✅ Edit functionality working
- ✅ Professional UI/UX

## 📞 Support

For any issues or updates, refer to the GitHub repository:
https://github.com/aiintel-tools/aiintel.tools

