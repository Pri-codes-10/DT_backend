# Digital Twin Health Backend

A FastAPI-based backend service for digital twin health monitoring with LoRA-fine-tuned machine learning models.

## Features

- **LoRA Fine-tuning**: Efficient model adaptation using Low-Rank Adaptation
- **Database Integration**: SQLAlchemy ORM with support for PostgreSQL, MySQL, SQLite
- **Health Predictions**: ML-powered patient health status predictions
- **Patient Management**: CRUD operations for patient records
- **Vital Signs Tracking**: Store and analyze patient vital signs
- **RESTful API**: FastAPI-based REST endpoints with automatic documentation
- **Logging**: Comprehensive application logging
- **Configuration Management**: Environment-based configuration

## Project Structure

```
digital-twin-backend/
├── app/
│   ├── models/               # ML models and LoRA implementation
│   │   ├── lora_model.py     # LoRA model wrapper
│   │   └── predictor.py      # Health prediction models
│   ├── db/                   # Database layer
│   │   ├── database.py       # Database manager
│   │   └── models.py         # SQLAlchemy models
│   ├── routes/               # API routes
│   │   ├── patients.py       # Patient endpoints
│   │   └── predictions.py    # Prediction endpoints
│   └── utils/                # Utility functions
│       └── helpers.py        # Helper functions
├── config/
│   └── config.py             # Configuration management
├── logs/                     # Application logs
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd digital-twin-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## Running the Application

```bash
python main.py
```

Or with Uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API documentation will be available at: `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /health` - Check application and database health

### Patients
- `POST /api/v1/patients` - Create new patient
- `GET /api/v1/patients/{patient_id}` - Get patient details
- `PUT /api/v1/patients/{patient_id}` - Update patient
- `DELETE /api/v1/patients/{patient_id}` - Delete patient
- `GET /api/v1/patients` - List all patients

### Predictions
- `POST /api/v1/predictions/predict` - Get health prediction
- `GET /api/v1/predictions/patient/{patient_id}` - Get patient predictions
- `POST /api/v1/predictions/vitals` - Record vital signs

## Configuration

All configuration can be managed through environment variables in the `.env` file:

- **Database**: `DATABASE_URL`
- **LoRA Settings**: `LORA_RANK`, `LORA_ALPHA`, `LORA_DROPOUT`
- **API Settings**: `API_HOST`, `API_PORT`
- **Logging**: `LOG_LEVEL`, `LOG_FILE`

## Database Models

### Patient
Stores patient information including demographics and contact details.

### VitalSigns
Tracks patient vital measurements (heart rate, BP, etc.).

### HealthPrediction
Stores prediction results from the ML model with confidence scores.

### ModelMetadata
Tracks LoRA model versions and configurations.

## Development

### Run Tests
```bash
pytest
```

### Format Code
```bash
black app/ config/ main.py
```

### Type Checking
```bash
mypy app/ config/ main.py
```

### Lint Code
```bash
flake8 app/ config/ main.py
```

## Next Steps

1. **Implement Database Migrations**: Set up Alembic for database versioning
2. **Implement Routes**: Complete the API route implementations
3. **Add Authentication**: Implement JWT-based authentication
4. **Model Integration**: Integrate your trained LoRA models
5. **Testing**: Add comprehensive unit and integration tests
6. **Docker**: Create Dockerfile for containerization
7. **Documentation**: Add API documentation and usage examples

## Requirements

- Python 3.9+
- PostgreSQL 12+ (or SQLite for development)
- PyTorch 2.0+
- CUDA support (optional, for GPU acceleration)

## License

[Add your license here]

## Support

For issues and questions, please open an issue in the repository.
