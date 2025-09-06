# 🚀 Render Deployment Guide

## Deploy SmartSEO Analyzer to Render

### Option 1: One-Click Deploy

Click the button below to deploy directly to Render:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/JasonRobertDestiny/SmartSEO_Analyzer)

### Option 2: Manual Deployment

1. **Fork this repository** (if you haven't already)

2. **Sign up for Render** at [render.com](https://render.com)

3. **Connect your GitHub account** to Render

4. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `SmartSEO_Analyzer`
   - Choose your deployment branch: `main`

5. **Configure the service**:
   - **Name**: `smartseo-analyzer` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
   - **Instance Type**: `Free` (or upgrade as needed)

6. **Set Environment Variables** (Optional for AI features):
   - Add `SILICONFLOW_API_KEY` with your API key value
   - Add `FLASK_ENV` set to `production`

7. **Deploy**: Click "Create Web Service"

### Environment Variables

To enable AI analysis features, set these environment variables in Render:

| Variable | Description | Required |
|----------|-------------|----------|
| `SILICONFLOW_API_KEY` | Your SiliconFlow API key for AI analysis | Optional |
| `FLASK_ENV` | Set to `production` for production deployment | Recommended |
| `PORT` | Port number (automatically set by Render) | Auto |

### After Deployment

1. **Access your app**: Your app will be available at `https://your-app-name.onrender.com`

2. **Test the functionality**:
   - Try analyzing a website
   - Test both basic and AI-enhanced analysis
   - Download HTML reports

3. **Monitor logs**: Check the logs in Render dashboard for any issues

### Configuration Files

The following files are configured for Render deployment:

- `Procfile`: Defines the web process
- `requirements.txt`: Python dependencies
- `runtime.txt`: Python version specification
- `render.yaml`: Render service configuration
- `web_app.py`: Modified for production environment

### Troubleshooting

**Common Issues:**

1. **Build Failures**: Check that all dependencies are listed in `requirements.txt`
2. **Start Failures**: Verify the start command in Procfile
3. **AI Features Not Working**: Ensure `SILICONFLOW_API_KEY` is set correctly
4. **Slow Performance**: Consider upgrading from free tier for better performance

**Log Access:**
- View logs in Render dashboard under "Logs" tab
- Use `print()` statements for debugging

### Scaling and Performance

**Free Tier Limitations:**
- 512 MB RAM
- Shared CPU
- Sleeps after 15 minutes of inactivity
- 750 hours/month

**Upgrade Options:**
- Starter: $7/month - 512 MB RAM, dedicated CPU
- Standard: $25/month - 2 GB RAM, more CPU power
- Pro: $85/month - 4 GB RAM, high-performance CPU

### Custom Domain

To use a custom domain:
1. Go to your service settings in Render
2. Add your custom domain
3. Configure DNS settings as instructed
4. Render will automatically provide SSL certificate

### Continuous Deployment

The app is configured for automatic deployment:
- Any push to the `main` branch triggers a new deployment
- Build and deployment status visible in Render dashboard
- Rollback available if deployment fails

### Support

For deployment issues:
1. Check Render's [documentation](https://render.com/docs)
2. Review logs in Render dashboard
3. Submit issues to the GitHub repository
