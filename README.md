# 🌾 Agri Dost Pakistan (زرعی دوست پاکستان)

A premium bilingual (English / Urdu) agriculture e-commerce platform built with **Django REST Framework** + **PostgreSQL** + **Cloudinary** (backend) and **React + Vite + Tailwind CSS** (frontend).

Designed for Pakistani farmers — **mobile-first, premium-quality**, with two ordering paths: **WhatsApp** or a **simple form**.

> **Production-ready** — env-var configuration, PostgreSQL, Cloudinary media storage, one-click Render deployment.

---

## ✨ Features

### Customer Side
- 🌐 **Fully bilingual** — English & Urdu, instant switch with RTL layout & Nastaliq font for Urdu
- 📱 **Mobile-first premium UI** — refined typography (Fraunces + Plus Jakarta Sans), rich gradients, smooth animations
- 🛒 **Two ordering paths:**
  1. **WhatsApp** — pre-fills product details into a chat with you
  2. **Simple form** — Name, Phone, Address (3 fields)
- 🎬 **Hero banners with video support** — autoplay muted MP4 backgrounds OR static images
- 🖼️ Multi-image gallery + product video on every product
- ⭐ Customer testimonials with embedded video
- 📞 Floating WhatsApp button + bottom mobile nav

### Admin Side
- 🔐 JWT-based admin login
- 📊 Premium dashboard with stat cards
- 📦 Products CRUD with multi-image + video upload
- 📋 Orders manager with status workflow (Pending → Contacted → Sale Done / Not Interested)
- 🗂️ Categories, Banners (image OR video), Testimonials with video
- ⚙️ Site settings (WhatsApp number, contact, social links — all editable in EN + UR)

---

## 🛠️ Tech Stack

**Backend**: Django 4.2 · DRF · SimpleJWT · PostgreSQL · Cloudinary · Gunicorn · WhiteNoise
**Frontend**: React 18 · Vite 5 · Tailwind CSS 3 · React Router 6 · React Icons · Axios · React Toastify

---

## 🚀 Quick Local Setup

### Prerequisites
- Python 3.10+ · Node.js 18+ · Git

### Backend

```bash
cd backend

# 1. Virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac — Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env — for local dev you can leave DATABASE_URL blank (uses SQLite)
# and CLOUDINARY_* blank (saves files locally to ./media/)

# 4. Migrate + seed
python manage.py makemigrations api
python manage.py migrate
python setup_data.py

# 5. Run
python manage.py runserver
```

✅ Backend at `http://localhost:8000`

### Frontend (new terminal)

```bash
cd frontend

# 1. Set API URL (only needed for production builds — dev defaults to localhost:8000)
cp .env.example .env

# 2. Install + run
npm install
npm run dev
```

✅ Frontend at `http://localhost:5173`

### Default credentials

```
Username: admin
Password: admin123
```

🔒 **Change it immediately** at `http://localhost:8000/admin/` or with `python manage.py changepassword admin`.

---

## ☁️ Deploying to Production

See **[DEPLOY-RENDER.md](./DEPLOY-RENDER.md)** for a complete step-by-step guide covering:
- Cloudinary account setup (free)
- Render PostgreSQL database
- Render web service deployment (one-click via `render.yaml` or manual)
- Environment variables checklist
- Netlify frontend deployment
- Troubleshooting common issues

---

## 📂 Project Structure

```
agri-dost-pakistan/
├── backend/
│   ├── agri_dost/          # Django settings (env-driven)
│   ├── api/                # Models, serializers, views, URLs
│   ├── manage.py
│   ├── requirements.txt
│   ├── setup_data.py       # Creates admin + sample data
│   ├── build.sh            # Render build script
│   ├── render.yaml         # Render Blueprint config
│   └── .env.example
│
├── frontend/
│   ├── public/
│   │   ├── _redirects      # Netlify SPA routing
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/     # Navbar, Footer, ProductCard, HeroCarousel, ...
│   │   ├── context/        # Language, Auth, Settings
│   │   ├── layouts/        # PublicLayout, AdminLayout
│   │   ├── locales/        # en.js, ur.js
│   │   ├── pages/          # Home, Products, ProductDetail, About, Contact
│   │   │   └── admin/      # All admin pages
│   │   ├── services/       # api.js (axios)
│   │   ├── App.jsx, main.jsx, index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
│
├── README.md
├── DEPLOY-RENDER.md        # Full deployment guide
└── .gitignore
```

---

## 🌍 Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✓ | Django secret key (generate a long random string for production) |
| `DEBUG` | | `True` for dev, `False` for production |
| `ALLOWED_HOSTS` | | Comma-separated, e.g. `localhost,.onrender.com` |
| `DATABASE_URL` | | Postgres URL (blank = uses SQLite locally) |
| `CLOUDINARY_CLOUD_NAME` | | From Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | | From Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | | From Cloudinary dashboard |
| `CORS_ALLOWED_ORIGINS` | | Comma-separated frontend URLs |
| `CSRF_TRUSTED_ORIGINS` | | Same as above |

When **all 3 Cloudinary vars** are set, file uploads automatically go to Cloudinary. When blank, files save locally to `./media/`.

When `DATABASE_URL` is set, Postgres is used. Otherwise, SQLite (perfect for local dev).

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API URL (default `http://localhost:8000/api`) |
| `VITE_MEDIA_URL` | Backend root (only used for non-Cloudinary images) |

---

## 📡 API Quick Reference

All endpoints are under `/api/`.

**Public**: `GET /products/`, `GET /products/:id/`, `GET /products/featured/`, `GET /categories/`, `GET /banners/`, `GET /testimonials/`, `GET /settings/`, `POST /orders/`

**Admin (JWT)**: `POST /auth/login/`, full CRUD on `/products/`, `/orders/`, `/categories/`, `/testimonials/`, `/banners/`, `PATCH /settings/update/`

JWT login flow:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
# Returns { access, refresh, user }
# Use Bearer access token on subsequent requests
```

---

## 🎨 Design System

- **Primary green**: `#247845` (custom palette, lush/agricultural)
- **Gold accent**: `#dba01c` (premium feel)
- **Display font**: Fraunces (serif, distinctive)
- **Body font**: Plus Jakarta Sans (modern, clean)
- **Urdu font**: Noto Nastaliq Urdu (proper Nastaliq style)
- **Shadows**: Custom `soft`, `medium`, `large` for depth
- **All gradients**: Hand-tuned in `tailwind.config.js`

---

## 🤝 Built For

Bitnex Technologies. For modifications:
- All translations in `frontend/src/locales/{en,ur}.js` — edit one place, both work
- All colors/fonts in `frontend/tailwind.config.js`
- All site-wide info (WhatsApp number, contact, about) editable from admin → Site Settings (no code change)

---

**Made with ❤️ for Pakistani Farmers** 🌾
