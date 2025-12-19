# Resume Analyzer - Render Deployment Guide

## Project Successfully Pushed to GitHub! ✅
Repository: https://github.com/susanta7029/Resume-Optimizer

---

## 🚀 Deployment Steps for Render

### Step 1: Create a Render Account
1. Go to [Render.com](https://render.com)
2. Sign up for a free account (you can use your GitHub account)

### Step 2: Deploy Django Backend

#### 2.1 Create a New Web Service
1. Click **"New +"** button in the Render dashboard
2. Select **"Web Service"**
3. Connect your GitHub account and select the repository: `susanta7029/Resume-Optimizer`
4. Click **"Connect"**

#### 2.2 Configure the Web Service
Fill in the following details:

- **Name**: `resume-analyzer-backend` (or any name you prefer)
- **Region**: Choose the closest region to you
- **Branch**: `main`
- **Root Directory**: Leave blank (or set to `ats-checker/core` if needed)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r ats-checker/requirements.txt && cd ats-checker/core && python manage.py collectstatic --no-input && python manage.py migrate
  ```
- **Start Command**: 
  ```bash
  cd ats-checker/core && gunicorn core.wsgi:application
  ```

#### 2.3 Set Environment Variables
Click on **"Environment"** tab and add these variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | Click "Generate" to create a random secret key |
| `DEBUG` | `False` |
| `GROQ_API_KEY` | Your Groq API key from https://console.groq.com/ |
| `RENDER_EXTERNAL_HOSTNAME` | (This will be auto-populated after deployment) |

#### 2.4 Deploy
1. Click **"Create Web Service"**
2. Wait for the deployment to complete (this may take 5-10 minutes)
3. Once deployed, note your backend URL (e.g., `https://resume-analyzer-backend.onrender.com`)

### Step 3: Deploy React Frontend

#### 3.1 Create Another Web Service
1. Click **"New +"** again
2. Select **"Web Service"**
3. Select the same repository: `susanta7029/Resume-Optimizer`

#### 3.2 Configure Frontend Service
- **Name**: `resume-analyzer-frontend`
- **Region**: Same as backend
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Runtime**: `Node`
- **Build Command**: 
  ```bash
  npm install && npm run build
  ```
- **Start Command**: 
  ```bash
  npm install -g serve && serve -s build -l 3000
  ```

#### 3.3 Set Frontend Environment Variables
Add this environment variable:

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | Your backend URL from Step 2.4 |

### Step 4: Update Backend CORS Settings
1. Go back to your backend service on Render
2. Add a new environment variable:

| Key | Value |
|-----|-------|
| `RENDER_FRONTEND_URL` | Your frontend URL (e.g., `https://resume-analyzer-frontend.onrender.com`) |

3. Click **"Save Changes"** and the service will redeploy automatically

### Step 5: Update Frontend API Configuration

You need to update the API URL in your frontend code:

1. Edit `frontend/src/services/api.js`
2. Update the `baseURL` to use the environment variable:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
   ```

3. Commit and push this change:
   ```bash
   git add frontend/src/services/api.js
   git commit -m "Update API URL for production"
   git push origin main
   ```

4. Render will automatically redeploy your frontend

---

## 📝 Important Notes

### Free Tier Limitations
- Render's free tier services spin down after 15 minutes of inactivity
- First request after spin down may take 30-60 seconds
- Consider upgrading to a paid plan for production use

### Database Considerations
- Currently using SQLite (not recommended for production)
- For production, upgrade to PostgreSQL:
  1. Create a PostgreSQL database on Render
  2. Add `DATABASE_URL` environment variable
  3. Django will automatically use it (configured in settings.py)

### SpaCy Model Download
If you're using spaCy models, you may need to add this to your build command:
```bash
python -m spacy download en_core_web_sm
```

### Static Files
- Static files are served using WhiteNoise
- All static files are collected during build time

---

## 🔧 Troubleshooting

### If deployment fails:
1. Check the build logs in Render dashboard
2. Verify all environment variables are set correctly
3. Ensure your Groq API key is valid

### If the app doesn't work:
1. Check the service logs for errors
2. Verify CORS settings include your frontend URL
3. Ensure database migrations ran successfully

### Common Issues:
- **500 Error**: Check `DEBUG=False` and SECRET_KEY is set
- **CORS Error**: Verify frontend URL is in `RENDER_FRONTEND_URL`
- **Module Not Found**: Ensure all dependencies are in requirements.txt

---

## ✅ Verification

After deployment, test:
1. Visit your frontend URL
2. Try uploading a resume
3. Check if analysis works correctly

Your app should now be live! 🎉

---

## 🔐 Security Reminders

✅ API keys are stored as environment variables
✅ Secret key is generated securely
✅ DEBUG mode is disabled in production
✅ ALLOWED_HOSTS is configured properly

**Never commit sensitive keys to GitHub!**
