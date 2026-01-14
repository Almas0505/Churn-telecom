"""
FastAPI service for churn prediction
REST API for making predictions on customer data
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from inference import ChurnPredictor
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="API for predicting customer churn in telecom industry",
    version="1.0.0",
)

# Initialize predictor (lazy loading)
predictor = None


def get_predictor():
    """Get or initialize predictor"""
    global predictor
    if predictor is None:
        try:
            predictor = ChurnPredictor(model_dir='../models')
            predictor.load_artifacts()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not available. Please train the model first."
            )
    return predictor


class CustomerData(BaseModel):
    """Schema for customer data"""
    
    tenure: int = Field(..., ge=0, description="Number of months the customer has stayed")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges")
    TotalCharges: float = Field(..., ge=0, description="Total charges")
    SeniorCitizen: int = Field(..., ge=0, le=1, description="Whether customer is a senior citizen (0 or 1)")
    Partner: int = Field(..., ge=0, le=1, description="Whether customer has a partner (0 or 1)")
    Dependents: int = Field(..., ge=0, le=1, description="Whether customer has dependents (0 or 1)")
    PhoneService: int = Field(..., ge=0, le=1, description="Whether customer has phone service (0 or 1)")
    PaperlessBilling: int = Field(..., ge=0, le=1, description="Whether customer uses paperless billing (0 or 1)")
    
    class Config:
        schema_extra = {
            "example": {
                "tenure": 24,
                "MonthlyCharges": 70.5,
                "TotalCharges": 1692.0,
                "SeniorCitizen": 0,
                "Partner": 1,
                "Dependents": 0,
                "PhoneService": 1,
                "PaperlessBilling": 1
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    
    prediction: int = Field(..., description="Predicted churn (0: No, 1: Yes)")
    churn_probability: float = Field(..., description="Probability of churn (0-1)")
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    message: str = Field(..., description="Human-readable message")


class BatchCustomerData(BaseModel):
    """Schema for batch prediction"""
    
    customers: List[CustomerData]


@app.get("/", tags=["General"])
def root():
    """Root endpoint"""
    return {
        "message": "Churn Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint"""
    try:
        pred = get_predictor()
        return {
            "status": "healthy",
            "model_loaded": pred is not None,
            "model_type": type(pred.model).__name__ if pred.model else None
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_churn(customer: CustomerData):
    """
    Predict churn for a single customer
    
    Args:
        customer: Customer data
        
    Returns:
        Prediction with probability and risk level
    """
    try:
        # Get predictor
        pred = get_predictor()
        
        # Convert to DataFrame
        df = pd.DataFrame([customer.dict()])
        
        # Make prediction
        result = pred.predict_with_details(df)
        
        # Extract results
        prediction = int(result['prediction'].iloc[0])
        probability = float(result['churn_probability'].iloc[0])
        risk = str(result['risk_level'].iloc[0])
        
        # Create message
        if prediction == 1:
            message = f"Customer is likely to churn (probability: {probability:.2%})"
        else:
            message = f"Customer is likely to stay (churn probability: {probability:.2%})"
        
        logger.info(f"Prediction made: {prediction}, probability: {probability:.2%}")
        
        return PredictionResponse(
            prediction=prediction,
            churn_probability=probability,
            risk_level=risk,
            message=message
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch", tags=["Prediction"])
def predict_batch(batch: BatchCustomerData):
    """
    Predict churn for multiple customers
    
    Args:
        batch: Batch of customer data
        
    Returns:
        List of predictions
    """
    try:
        # Get predictor
        pred = get_predictor()
        
        # Convert to DataFrame
        df = pd.DataFrame([customer.dict() for customer in batch.customers])
        
        # Make predictions
        results = pred.predict_with_details(df)
        
        # Format response
        predictions = []
        for idx, row in results.iterrows():
            predictions.append({
                "customer_index": idx,
                "prediction": int(row['prediction']),
                "churn_probability": float(row['churn_probability']),
                "risk_level": str(row['risk_level'])
            })
        
        logger.info(f"Batch prediction made for {len(predictions)} customers")
        
        return {
            "total_customers": len(predictions),
            "predictions": predictions
        }
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/model/info", tags=["Model"])
def model_info():
    """Get information about the loaded model"""
    try:
        pred = get_predictor()
        
        return {
            "model_type": type(pred.model).__name__,
            "num_features": len(pred.feature_names) if pred.feature_names else 0,
            "features": pred.feature_names if pred.feature_names else []
        }
        
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Churn Prediction API...")
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
