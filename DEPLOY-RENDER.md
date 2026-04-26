# 🚀 Deploying Agri Dost Pakistan to Render.com

This guide walks you through deploying the **Django backend** to Render with **PostgreSQL** + **Cloudinary** for media. The React frontend will be deployed separately (Netlify/Vercel are easiest — instructions at the end).

---

## 📋 What You'll Need (5 minutes to gather)

1. **Render account** — Free tier at [render.com](https://render.com)
2. **GitHub account** — Your code must be in a Git repo
3. **Cloudinary account** — Free tier at [cloudinary.com](https://cloudinary.com)
4. **Postgres database on Render** — We'll create this in Step 2

---

## 🌥️ Step 1: Get Your Cloudinary Credentials

Cloudinary stores all your product images, videos, banners, and testimonial videos. Render's filesystem is **ephemeral** (files get wiped on each deploy), so cloud storage is mandatory.

1. Sign up at [cloudinary.com](https://cloudinary.com) → **Free plan** (25 GB storage, plenty for thousands of products)
2. From the dashboard, copy these 3 values (top of the page):
   - **Cloud name** (e.g., `dxyz123abc`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `aBcDeFgHiJkLmNoPqRsTuVwXyZ_-`)
3. Save these — we'll paste them into Render in Step 4.

---

## 🐘 Step 2: Create the PostgreSQL Database on Render

1. Log in to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** (top right) → **PostgreSQL**
3. Fill in:
   - **Name**: `agri-dost-db`
   - **Database**: `agridost` (or leave auto-generated)
   - **User**: leave auto-generated
   - **Region**: Pick the one closest to Pakistan — **Singapore** or **Frankfurt** is best
   - **PostgreSQL Version**: 16 (default)
   - **Plan**: **Free** (90 days, then $7/month — for production, upgrade)
4. Click **Create Database**
5. Wait ~1 minute for status to become **Available**
6. Scroll down to **Connections** and copy the **Internal Database URL** (looks like `postgresql://user:pass@dpg-xxx.singapore-postgres.render.com/agridost`)
7. Save this — you'll paste it into the web service in Step 4

> 💡 **Internal vs External URL:** Use the **Internal** URL when your web service runs on Render (faster, free bandwidth). Only use the **External** URL if connecting from your laptop.

---

## 📦 Step 3: Push Your Code to GitHub

If your code isn't on GitHub yet:

```bash
cd agri-dost-pakistan
git init
git add .
git commit -m "Initial commit"

# Create a new repo on github.com first, then:
git remote add origin https://github.com/YOUR-USERNAME/agri-dost-pakistan.git
git branch -M main
git push -u origin main
```

> ⚠️ **Make sure `.env` is NOT committed.** The included `.gitignore` excludes it, but double-check before pushing.

---

## 🌐 Step 4: Deploy the Backend Web Service

### Option A: One-Click Deploy with `render.yaml` (Recommended)

The project includes a `backend/render.yaml` file that pre-configures everything.

1. Go to [dashboard.render.com](https://dashboard.render.com) → **New +** → **Blueprint**
2. Connect your GitHub account if you haven't already
3. Pick the `agri-dost-pakistan` repo → click **Connect**
4. Render reads `render.yaml` and shows the planned service. Click **Apply**
5. Skip ahead to the **"Set environment variables"** section below

### Option B: Manual Setup

1. **New +** → **Web Service**
2. Connect your GitHub repo
3. Fill in:
   - **Name**: `agri-dost-backend`
   - **Region**: Same as your database (Singapore/Frankfurt)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn agri_dost.wsgi:application`
   - **Plan**: **Free** (good enough to start)
4. Click **Advanced** to expand environment variables (next section)

### Set environment variables (both options)

Click **Environment** in the left sidebar of the web service page. Add **each** of these:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.7` | |
| `SECRET_KEY` | *(click "Generate")* | Long random string |
| `DEBUG` | `False` | **Must be False in production** |
| `ALLOWED_HOSTS` | `.onrender.com` | Or your custom domain |
| `DATABASE_URL` | *(paste Internal URL from Step 2)* | The Postgres URL |
| `CLOUDINARY_CLOUD_NAME` | *(from Step 1)* | |
| `CLOUDINARY_API_KEY` | *(from Step 1)* | |
| `CLOUDINARY_API_SECRET` | *(from Step 1)* | |
| `CORS_ALLOW_ALL` | `False` | Lock CORS in production |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.netlify.app` | Your frontend URL (add later) |
| `CSRF_TRUSTED_ORIGINS` | `https://your-frontend.netlify.app` | Same as above |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |

Click **Save Changes** — Render will redeploy automatically.

---

## ✅ Step 5: Watch the Deployment

1. Click the **Logs** tab on your web service
2. You should see:
   ```
   ==> Installing Python dependencies
   ==> Collecting static files
   ==> Running database migrations
   Operations to perform:
     Apply all migrations: admin, api, auth, ...
   ==> Build complete!
   [INFO] Starting gunicorn ...
   [INFO] Listening at: http://0.0.0.0:10000
   ```
3. When status turns green (**Live**), open the URL Render gives you (e.g., `https://agri-dost-backend.onrender.com`)
4. Visit `https://agri-dost-backend.onrender.com/api/products/` — you should see `{"count":0,"next":null,...}`

**It works! 🎉**

---

## 🔐 Step 6: Create Your Admin User

Render's free tier does **not** give you a persistent shell. Instead, use the one-time setup script:

### Method 1: Render Shell (paid plans only)

If you upgrade to a paid plan, click **Shell** in the service sidebar and run:
```bash
python setup_data.py
```

### Method 2: Run setup once via build hook (free tier)

1. Go to your service → **Settings** → find **Build Command**
2. Temporarily change it to:
   ```bash
   ./build.sh && python setup_data.py
   ```
3. Click **Save Changes** — this triggers a new deploy
4. Once deployed, go back and **change the Build Command back to** `./build.sh`
5. Save again

This creates the admin user (`admin` / `admin123`) and seed data **once**. Login at `https://your-backend.onrender.com/admin/` and **change the password immediately**.

### Method 3: Local one-time creation (cleanest)

From your laptop, run setup pointing at the production database:
```bash
cd backend
# Set DATABASE_URL temporarily to your EXTERNAL Postgres URL from Step 2
DATABASE_URL="postgresql://user:pass@external-host/agridost" python setup_data.py
```

---

## 🎨 Step 7: Deploy the Frontend (Netlify — recommended)

The React frontend is a static site. Easiest free option:

1. Sign up at [netlify.com](https://netlify.com) → **Add new site** → **Import existing project**
2. Connect GitHub → select your repo
3. Configure build:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
4. Click **Show advanced** → **New variable**:
   - `VITE_API_URL` = `https://agri-dost-backend.onrender.com/api`
   - `VITE_MEDIA_URL` = `https://agri-dost-backend.onrender.com`
5. Click **Deploy**

After deploy, copy your Netlify URL (e.g., `https://agri-dost-pakistan.netlify.app`) and:
1. Go back to Render → your backend service → Environment
2. Update `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` to that URL
3. Save (triggers a redeploy)

### Add `_redirects` for client-side routing

Create `frontend/public/_redirects` with this single line:
```
/*    /index.html   200
```

This makes Netlify serve `index.html` for all routes (so `/admin/login` works on direct visit). Already included in this project.

---

## 🐛 Troubleshooting

### "Application failed to respond" / 502 Bad Gateway
- Check the **Logs** tab. Common cause: missing environment variable. Make sure `DATABASE_URL` and `SECRET_KEY` are set.

### Images don't show up
- Check that `CLOUDINARY_*` variables are set correctly (no extra spaces).
- After uploading a product image from admin, the URL should look like `https://res.cloudinary.com/your-cloud/image/upload/...`
- If it still saves locally (`/media/...`), the Cloudinary credentials are wrong.

### CORS errors in browser console
- The frontend's URL must be in `CORS_ALLOWED_ORIGINS` exactly (with `https://`, no trailing slash).
- Example: `https://agri-dost-pakistan.netlify.app` (NOT `https://agri-dost-pakistan.netlify.app/`)

### "psycopg2 / postgres" error in build logs
- This is fixed by the `psycopg2-binary` package in `requirements.txt`. If you see it, make sure you didn't change that line.

### Free Postgres database expired (after 90 days)
- Render will email you. Either upgrade to **Starter** ($7/mo) or export → import to a new free DB.
- Export: `pg_dump $OLD_DATABASE_URL > backup.sql`
- Import to new DB: `psql $NEW_DATABASE_URL < backup.sql`

### Static files (admin CSS) not loading
- The build script runs `collectstatic` automatically. If admin CSS is broken, check the build log for that step.
- WhiteNoise is configured to serve them — make sure `whitenoise` is in `requirements.txt`.

### Free tier sleeps after 15 min of inactivity
- First request after sleep takes 30-60 seconds (cold start). For a production farmer-facing site, upgrade to **Starter** ($7/mo) — it never sleeps.

---

## 📊 Cost Summary (when you outgrow free tier)

| Service | Free Tier | Paid (production-grade) |
|---------|-----------|------------------------|
| Render Web Service | Sleeps after 15min idle | $7/mo (always on) |
| Render Postgres | 90-day expiry, 1GB | $7/mo (1GB, persistent) |
| Cloudinary | 25GB storage, 25GB bandwidth | $0 — free tier is generous |
| Netlify | 100GB bandwidth | Free is plenty |
| **Total** | **$0** | **~$14/mo** |

---

## ✅ Production Checklist

Before sharing the link with customers:

- [ ] Changed default admin password (NOT `admin123`)
- [ ] `DEBUG=False` set on Render
- [ ] Real WhatsApp number set in admin → Site Settings
- [ ] At least 1 hero banner uploaded
- [ ] At least 5 products with real images uploaded
- [ ] About text + contact info set (English AND Urdu)
- [ ] CORS origins locked to your real frontend URL
- [ ] Test the WhatsApp button on a real phone
- [ ] Test the order form — submit a test order, see it in admin

Good luck! 🌾
