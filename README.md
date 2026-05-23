# AI Crop Recommendation and Farmer Advisory System

A comprehensive AI-powered web application that provides intelligent crop recommendations, pest/disease detection, market insights, and farmer advisory services to help maximize agricultural yield and profits.

## 🌟 Features

### Core Functionality
- **Smart Crop Recommendations**: AI-powered suggestions based on soil, weather, and location data
- **Pest & Disease Detection**: Upload images to instantly identify pests and diseases with treatment recommendations
- **Market Intelligence**: Real-time market prices and trends for informed selling decisions
- **Weather Monitoring**: Localized weather forecasts and alerts
- **SMS Notifications**: Automated alerts for weather events, market changes, and farming reminders

### Technical Features
- **Multilingual Support**: English, Hindi, and Telugu interfaces
- **Mobile-First Design**: Responsive UI optimized for farmers
- **Real-time Data**: Integration with external APIs for soil and weather data
- **Machine Learning**: Trained models for crop recommendations and image classification
- **Secure Authentication**: JWT-based user authentication
- **Scalable Architecture**: Microservices-ready with Docker deployment

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **ML Models**: scikit-learn, TensorFlow for image classification
- **External APIs**: OpenWeather, SoilGrids integration
- **SMS Service**: Twilio integration for notifications

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **UI Library**: TailwindCSS for responsive design
- **State Management**: Pinia for application state
- **Internationalization**: Vue i18n for multilingual support
- **HTTP Client**: Axios for API communication

### Database Schema
- **Farmers**: User profiles and authentication
- **Soil Data**: Soil composition and quality metrics
- **Weather Data**: Historical and forecast weather information
- **Crop History**: Past crop cultivation records
- **Market Data**: Price trends and market information
- **Detections**: Pest and disease detection records
- **Notifications**: SMS and alert management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (optional, SQLite for development)
- Docker & Docker Compose (for containerized deployment)

### Kaggle Setup

1. Install the Kaggle CLI dependency (already in requirements.txt for backend):
   ```bash
   pip install kaggle
   ```
2. Provide Kaggle credentials by either method:
   - Place `kaggle.json` at:
     - Windows: `%USERPROFILE%\.kaggle\kaggle.json`
     - Linux/Mac: `~/.kaggle/kaggle.json`
     Ensure permissions on Linux/Mac: `chmod 600 ~/.kaggle/kaggle.json`.
   - Or set environment variables:
     ```bash
     set KAGGLE_USERNAME=your_username
     set KAGGLE_KEY=your_key
     ```
3. Datasets will be downloaded automatically into `datasets/` on first training run.

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-crop-recommendation-system
   ```

2. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set environment variables
   cp env.example .env
   # Edit .env with your configuration
   
   # Run the backend
   cd backend
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   # Install Node.js dependencies
   cd frontend
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Train models with Kaggle datasets**
   ```bash
   # This will auto-download datasets into datasets/ and save models into models/
   python backend/ml/train_all.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Deployment

1. **Using Docker Compose**
   ```bash
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

2. **Using Docker**
   ```bash
   # Build the image
   docker build -t ai-crop-system .
   
   # Run the container
   docker run -p 8000:8000 ai-crop-system
   ```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new farmer
- `POST /api/auth/login` - Login farmer
- `GET /api/auth/me` - Get current farmer info

### v2 Endpoints
- `GET /api/recommend/{farmer_id}` - Crop recommendation + yield + price forecast
- `GET /api/fertilizer/{farmer_id}` - Fertilizer suggestion
- `POST /api/disease-detect` - Disease classification from image
- `POST /api/pest-detect` - Pest classification from image
- `GET /api/market/{commodity}` - Commodity historical + forecast (baseline)
- `POST /api/faq` - Farming FAQ chatbot (baseline)

### Detection
- `POST /api/detection/pest` - Detect pest from image
- `POST /api/detection/disease` - Detect disease from image
- `GET /api/detection/pest/history` - Get pest detection history
- `GET /api/detection/disease/history` - Get disease detection history

### Market
- `GET /api/market/prices/{crop_name}` - Get crop prices
- `GET /api/market/trends` - Get market trends

### Weather & Soil
Legacy (still available):
- `POST /api/weather/fetch` - Fetch weather data
- `POST /api/soil/fetch` - Fetch soil data

### Notifications
- `POST /api/notifications/send` - Send notification
- `POST /api/notifications/weather-alert` - Send weather alert
- `POST /api/notifications/market-alert` - Send market alert
- `GET /api/notifications/history` - Get notification history

## 🤖 Machine Learning Models

### Crop Recommendation Model
- **Algorithm**: Random Forest Classifier
- **Features**: Soil pH, nutrients, weather conditions, season, location
- **Output**: Crop recommendations with confidence scores and yield predictions

### Pest & Disease Detection
- **Algorithm**: Convolutional Neural Network (CNN)
- **Input**: Plant images (JPG/PNG)
- **Output**: Pest/disease type, confidence score, treatment recommendations

### Yield Prediction
- **Algorithm**: Random Forest Regressor
- **Features**: Soil data, weather patterns, historical yields
- **Output**: Expected yield in kg/acre

## 🌐 External API Integration

### Weather Data
- **Provider**: OpenWeather API
- **Data**: Temperature, humidity, rainfall, wind speed, pressure
- **Update Frequency**: Real-time with 7-day forecasts

### Soil Data
- **Provider**: SoilGrids API / Bhuvan API
- **Data**: pH levels, nutrient content, soil type, moisture
- **Coverage**: Global soil composition data

### SMS Notifications
- **Provider**: Twilio
- **Features**: Weather alerts, market updates, farming reminders
- **Languages**: English, Hindi, Telugu

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/farmers_db

# Security
SECRET_KEY=your-secret-key-here

# External APIs
OPENWEATHER_API_KEY=your-openweather-key
SOILGRIDS_API_KEY=your-soilgrids-key

# SMS Service
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

### Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended
- **Migrations**: Alembic for database schema management

## 📱 Mobile Responsiveness

The application is designed with a mobile-first approach:
- **Responsive Design**: Works on all screen sizes
- **Touch-Friendly**: Optimized for touch interactions
- **Offline Capability**: Basic functionality without internet
- **Progressive Web App**: Installable on mobile devices

## 🌍 Internationalization

### Supported Languages
- **English**: Primary language
- **Hindi**: हिन्दी support
- **Telugu**: తెలుగు support

### Adding New Languages
1. Create new locale file in `frontend/src/locales/`
2. Add language option in `NavBar.vue`
3. Update i18n configuration in `main.js`

## 🧪 Testing

### Backend Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend
```

### Frontend Testing
```bash
# Run tests
npm test

# Run e2e tests
npm run test:e2e
```

## 🚀 Deployment

### Production Deployment
1. **Set up production database**
2. **Configure environment variables**
3. **Set up reverse proxy (Nginx)**
4. **Configure SSL certificates**
5. **Set up monitoring and logging**

### Cloud Deployment Options
- **AWS**: EC2, RDS, S3, CloudFront
- **Google Cloud**: Compute Engine, Cloud SQL, Cloud Storage
- **Azure**: Virtual Machines, Azure Database, Blob Storage
- **Heroku**: Easy deployment with add-ons
- **DigitalOcean**: Droplets with managed databases

## 📈 Performance Optimization

### Backend Optimizations
- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Background tasks for heavy operations
- **API Rate Limiting**: Prevent abuse and ensure fair usage

### Frontend Optimizations
- **Code Splitting**: Lazy loading of components
- **Image Optimization**: Compressed images and lazy loading
- **Caching**: Service worker for offline functionality
- **Bundle Optimization**: Tree shaking and minification

## 🔒 Security Features

- **Authentication**: JWT-based secure authentication
- **Password Hashing**: bcrypt for password security
- **Input Validation**: Pydantic models for data validation
- **CORS Protection**: Configured for production security
- **File Upload Security**: Validated file types and sizes
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 📊 Monitoring and Logging

### Application Monitoring
- **Health Checks**: `/health` endpoint for service monitoring
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Response time and throughput monitoring
- **User Analytics**: Usage patterns and feature adoption

### Logging
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Automatic log file management
- **Centralized Logging**: ELK stack or similar for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/Vue code
- Write tests for new features
- Update documentation as needed
- Follow conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenWeather API** for weather data
- **SoilGrids** for soil composition data
- **Twilio** for SMS services
- **Vue.js** and **FastAPI** communities
- **TensorFlow** and **scikit-learn** for ML capabilities

## 📞 Support

For support and questions:
- **Email**: support@aicrop.com
- **Documentation**: [Project Wiki](wiki-url)
- **Issues**: [GitHub Issues](issues-url)

## 🔮 Future Roadmap

### Phase 1 (Current)
- ✅ Basic crop recommendations
- ✅ Pest/disease detection
- ✅ Market price tracking
- ✅ Weather monitoring
- ✅ SMS notifications

### Phase 2 (Next 3 months)
- [ ] Advanced ML models with more training data
- [ ] Mobile app (React Native)
- [ ] IoT sensor integration
- [ ] Satellite imagery analysis
- [ ] Blockchain-based supply chain tracking

### Phase 3 (Next 6 months)
- [ ] Drone integration for field monitoring
- [ ] Advanced analytics dashboard
- [ ] Integration with government schemes
- [ ] Multi-tenant architecture
- [ ] API marketplace for third-party integrations

---

**Built with ❤️ for farmers worldwide**

