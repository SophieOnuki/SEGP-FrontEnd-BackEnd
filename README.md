# SEGP-FrontEnd-BackEnd

## Project Overview

This is the FrontEnd and BackEnd implementation for Group 2's SEGP project. The application is an **AI-powered FFB (Fresh Fruit Bunch) Mass Prediction System** that allows users to upload files and get real-time mass predictions using a machine learning model.

**Key Features:**
- Upload and analyze bag files for FFB mass prediction
- Real-time AI predictions using ONNX model
- Interactive dashboard with prediction history
- CSV export functionality
- Responsive web interface

---

## System Requirements

### Hardware & Software Prerequisites
- **Operating System:** Windows, macOS, or Linux
- **Node.js:** v16+ (includes npm)
- **Python:** v3.10 or lower ( **NOT 3.11+** - dependencies not compatible)
- **MySQL:** via MAMP (Mac) or any MySQL installation
- **MAMP:** For easy MySQL database management

### Verify Prerequisites
```powershell
# Check Node.js and npm
node --version
npm --version

# Check Python
python --version
```

---

## Installation & Setup

### Step 1: Clone/Download the Repository

Clone the repository from GitHub:

```powershell
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

If you do not have Git installed, you can also click **Code > Download ZIP** on GitHub, extract the files, and open the project folder.

### Step 2: Install Frontend Dependencies
```powershell
npm install
```

### Step 3: Install Backend Dependencies

Navigate to the backend folder and install Python dependencies:
```powershell
cd src\App\app
pip install -r requirements.txt
```

**Required Backend Dependencies:**
- Flask 2.3.0
- Flask-CORS 4.0.0
- SQLAlchemy 2.0.0
- pymysql 1.1.0
- python-dotenv 1.0.0
- requests 2.31.0

### Step 4: Download AI Model Weights

The AI model uses ONNX format. Ensure the model weights file is:
- Downloaded from the specified source
- Placed in the correct directory as referenced in the backend code
- The model is used by the FFB detection pipeline

---

## Database Setup

### Using MAMP (Recommended)

1. **Download & Install MAMP:**
   - Download from [MAMP website](https://www.mamp.info/)
   - Follow installation instructions for your OS

2. **Start MAMP Services:**
   - Open MAMP application
   - Click "Start Servers" button
   - Verify MySQL is running (status indicator shows green)
   - Default credentials: `root` / `root`

3. **Verify Database Connection:**
   - MAMP will start MySQL on port 3306
   - phpMyAdmin accessible at `http://localhost:8888/phpMyAdmin/`

4. **Database Configuration:**
   - Database name: `ffbs_database`
   - Username: `root`
   - Password: `root`
   - Host: `localhost`
   - Port: `3306`

The tables will be automatically created when the backend runs for the first time.

---

## Running the Application

### Important: Always Start Backend FIRST, Then Frontend

#### Terminal 1: Start Backend Server
```powershell
# Navigate to backend directory
cd src\App\app

# Run the Flask server (debug mode enabled)
python run.py
```

**Expected Output:**
- `Running on http://127.0.0.1:5000/`
- Console logs showing database initialization
- Server ready to receive requests

#### Terminal 2: Start Frontend Development Server
```powershell
# Navigate to project root (open new PowerShell/terminal)
cd <your-repository>

# Start development server
npm run dev
```

**Expected Output:**
- `VITE v6.4.1 ready in XXX ms`
- `Local: http://localhost:5173` (or http://localhost:3000)
- Browser should automatically open the web app

### Access the Application
- **Frontend:** http://localhost:3000 (or http://localhost:5173)
- **Backend API:** http://localhost:5000
- **Database Admin:** http://localhost:8888/phpMyAdmin/

---

## Project Structure

```
SEGP-FrontEnd-BackEnd/
├── package.json              # Frontend dependencies
├── vite.config.ts           # Vite configuration
├── src/
│   ├── App.tsx              # Main React component
│   ├── main.tsx             # Entry point
│   ├── components/          # React UI components
│   │   ├── DashboardPage.tsx
│   │   ├── UploadBagButton.tsx
│   │   ├── PredictionHistory.tsx
│   │   └── ...
│   ├── services/
│   │   └── api.ts           # Backend API calls
│   ├── styles/              # CSS/styling
│   └── App/                 # Backend folder
│       ├── app/
│       │   ├── app.py       # Flask app configuration
│       │   ├── run.py       # Backend entry point 
│       │   ├── models.py    # Database models
│       │   ├── ffb_pipeline_final.py  # AI prediction pipeline
│       │   ├── routes/      # API endpoints
│       │   ├── requirements.txt
│       │   └── uploads/     # Uploaded files storage
│       └── ffb_detection/   # ML model files
├── build/                   # Production build (generated)
└── README.md
```

---

## How It Works

1. **User uploads a BAG file** via the web interface
2. **Frontend sends request** to backend API at `http://localhost:5000`
3. **Backend processes file** and runs through FFB detection pipeline
4. **AI model (ONNX)** predicts the mass of the Fresh Fruit Bunch
5. **Predictions stored** in MySQL database
6. **Results displayed** in real-time on dashboard
7. **User can export** prediction history as CSV

---

## Development Notes

### Frontend Stack
- **Framework:** React 18.3.1
- **Build Tool:** Vite 6.4.1
- **UI Components:** Radix UI
- **Charts:** Recharts, Plotly.js
- **HTTP Client:** Axios

### Backend Stack
- **Framework:** Flask 2.3.0
- **Database:** MySQL with SQLAlchemy ORM
- **API:** RESTful endpoints with CORS support
- **ML Model:** ONNX format (pre-loaded)

### Default Ports
- Frontend: `3000` (or `5173` with Vite default)
- Backend: `5000`
- MySQL: `3306`
- phpMyAdmin: `8888`

---

## Troubleshooting

### Issue: "Connection refused" on Backend Startup
**Solution:**
- Ensure MySQL is running (start MAMP services first)
- Verify database credentials in `src/App/app/__init__.py`
- Check if port 5000 is not in use: `netstat -ano | findstr :5000`

### Issue: "Module not found" Python Error
**Solution:**
- Verify Python version: `python --version` (must be ≤3.10)
- Reinstall dependencies: `pip install -r requirements.txt`
- Try using virtual environment: `python -m venv venv` then activate

### Issue: Frontend not connecting to Backend
**Solution:**
- Ensure backend is running on port 5000
- Check CORS settings in `src/App/app/__init__.py`
- Verify API endpoint in `src/services/api.ts`
- Open browser DevTools (F12) to check console for errors

### Issue: "MAMP won't start"
**Solution:**
- Check if MySQL is already running on port 3306
- Restart MAMP application
- Try restarting your computer

### Issue: Model weights not found
**Solution:**
- Verify ONNX model file is in the correct directory
- Check file path in `src/App/app/ffb_pipeline_final.py`
- Ensure file hasn't been deleted or moved

---

## Common Commands Reference

```powershell
# Terminal 1: Backend
cd src\App\app
python run.py                    # Start backend server

# Terminal 2: Frontend
npm install                      # Install dependencies
npm run dev                      # Start development server
npm run build                    # Build for production

# Database
# (Via phpMyAdmin at http://localhost:8888/phpMyAdmin/)
# Username: root
# Password: root
```

---

## Contributing & Support

- **Non-technical Users:** Follow the setup guide step-by-step
- **Technical Examiners:** Refer to component documentation in code comments
- **Issues:** Check troubleshooting section above first

---

## Additional Resources

- See `Guidelines.md` in `src/guidelines/` for detailed feature documentation
- See `Attributions.md` in `src/` for library credits
- Backend code comments explain prediction pipeline logic

---

**Last Updated:** April 2026 | Group 2 SEGP Project


  
  
