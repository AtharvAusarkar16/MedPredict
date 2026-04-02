# Deploying to Render

## Prerequisites
- GitHub account with this repository pushed to it
- Render account (render.com)

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Verify All Files Are Present
Before deploying, ensure you have these critical files in your repository:
- ✅ `hospital_stay_model.pkl` - Your trained model
- ✅ `model_features.pkl` - Feature names
- ✅ `model_scaler.pkl` - Feature scaler
- ✅ `HospitalSynthetic1_cleaned (1).csv` - Analytics data
- ✅ `render.yaml` - Deployment configuration (created)
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Flask application (updated)

**⚠️ Important:** If any of these pickle/CSV files are missing, the deployment will fail. Add them to git:
```bash
git add hospital_stay_model.pkl model_features.pkl model_scaler.pkl "HospitalSynthetic1_cleaned (1).csv"
git commit -m "Add model and data files"
git push origin main
```

### 3. Create a Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub (recommended for easy integration)

### 4. Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select this repository
4. Fill in the configuration:
   - **Name:** `hospital-stay-predictor` (or your choice)
   - **Environment:** `Python 3`
   - **Region:** `Oregon` (or closest to you)
   - **Branch:** `main`
   - **Runtime:** `python-3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. Choose **Free Tier** or **Paid Plan**
6. Click **"Deploy"**

### 5. Set Environment Variables (Optional)
If needed, go to **Settings** → **Environment** to add:
- `FLASK_ENV=production` (Render does this automatically)

### 6. Monitor Deployment
- Render will automatically build and start your app
- Watch the **Logs** tab for any errors
- Once status shows "Live", your app is running!

## Your Live URL
Once deployed, your app will be accessible at:
```
https://hospital-stay-predictor.onrender.com
```

## Troubleshooting

### Build Fails - "ModuleNotFoundError"
- Check `requirements.txt` has all dependencies
- Run `pip freeze > requirements.txt` locally to update

### App Crashes - "No such file or directory"
- Ensure model files (`.pkl`) and CSV are committed to GitHub
- File paths must be relative (not absolute)

### 404 on Routes
- Check logs for errors in app.py
- Verify templates are in `templates/` folder
- Verify static files are in `static/` folder

### Port Issues
- Don't hardcode ports - the app now uses PORT env variable ✅

## Free Tier Limitations
- App spins down after 15 min of inactivity (takes ~30s to wake up)
- Limited to 0.5GB RAM
- Great for dev/demo purposes

## Upgrading to Paid
If you need always-on service, upgrade in Render's **Settings** → **Plan**.

---

For more help: https://render.com/docs/deploy-flask
