# Deployment Guide for Render

## Prerequisites
1. GitHub repository with your code
2. Render account (render.com)
3. Neon database credentials

## Steps to Deploy

### 1. Push to GitHub
Make sure all your code is pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create New Web Service on Render
1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Select your repository: `Data-Visualisation-OECD-Agricultural`

### 3. Configure Service Settings
- **Name**: `oecd-agricultural-dashboard`
- **Environment**: `Python 3`
- **Build Command**: `pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt`
- **Start Command**: `gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --preload`

### 4. Set Environment Variables
In the Render dashboard, add these environment variables:

```
NEON_HOST=ep-fragrant-sky-a1dbmhdl-pooler.ap-southeast-1.aws.neon.tech
NEON_DATABASE=neondb
NEON_USER=neondb_owner
NEON_PASSWORD=npg_xA9rZyENj4YJ
NEON_PORT=5432
```

### 5. Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Your app will be available at: `https://your-service-name.onrender.com`

## Alternative: Using render.yaml (Infrastructure as Code)
If you want to use the `render.yaml` file:

1. In your Render dashboard, go to "Blueprint"
2. Click "New Blueprint Instance"
3. Connect your GitHub repo
4. Render will read the `render.yaml` file and create services automatically
5. You'll still need to manually add the database environment variables for security

## Important Notes

- **Database**: Your app connects to Neon PostgreSQL database
- **Cold Starts**: Free tier on Render may have cold starts (app sleeps after inactivity)
- **Logs**: Check deployment logs in Render dashboard if there are issues
- **SSL**: Render provides HTTPS automatically

## Troubleshooting

### Common Issues:
1. **Build Fails**: Check that all dependencies are in `requirements.txt`
2. **App Won't Start**: Verify the start command points to `app:server`
3. **Database Connection**: Ensure environment variables are set correctly
4. **Import Errors**: Make sure all your Python files are committed to Git

### Gunicorn "Application object must be callable" Error:
If you see this error, it means the server object isn't properly exposed. The fix:

1. **Ensure server is exposed at module level**:
   ```python
   from dash import Dash
   app = Dash(__name__)
   server = app.server  # This line is critical
   ```

2. **Don't load heavy imports at module level** - defer them until needed
3. **Handle database connection failures gracefully**
4. **Use the corrected Procfile**:
   ```
   web: gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --preload
   ```

### Updated Start Command:
Use this in your Render settings:
```
gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --preload
```

### Health Check
Your app includes a health check endpoint. Once deployed, you can test:
```
GET https://your-app.onrender.com/health
```

## Performance Optimization
- Consider upgrading to paid plan for better performance
- Monitor memory usage and adjust worker count if needed
- Use caching strategies for database queries if needed

## Security Notes
- Database credentials are sensitive - never commit them to Git
- Use Render's environment variables for secrets
- Consider using environment-specific configurations
