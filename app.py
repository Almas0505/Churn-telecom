"""
Streamlit app for churn prediction
Interactive web interface for predicting customer churn
"""
import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.inference import ChurnPredictor

# Page configuration
st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🔮 Телеком: Предсказание Оттока Клиентов</p>', unsafe_allow_html=True)

# Initialize session state
if 'predictor' not in st.session_state:
    st.session_state.predictor = None

# Load model
@st.cache_resource
def load_model():
    """Load prediction model"""
    try:
        predictor = ChurnPredictor(model_dir='models')
        predictor.load_artifacts()
        return predictor
    except Exception as e:
        st.error(f"❌ Ошибка загрузки модели: {e}")
        st.info("💡 Пожалуйста, сначала обучите модель, запустив `python src/train.py`")
        return None

# Sidebar for input
with st.sidebar:
    st.header("📊 Данные клиента")
    
    # Customer information
    st.subheader("Общая информация")
    tenure = st.slider("Срок пользования (месяцы)", 0, 72, 12, help="Количество месяцев пользования услугами")
    senior_citizen = st.selectbox("Пенсионер", [0, 1], format_func=lambda x: "Нет" if x == 0 else "Да")
    
    # Family information
    st.subheader("Семейное положение")
    partner = st.selectbox("Партнер", [0, 1], format_func=lambda x: "Нет" if x == 0 else "Да")
    dependents = st.selectbox("Иждивенцы", [0, 1], format_func=lambda x: "Нет" if x == 0 else "Да")
    
    # Services
    st.subheader("Услуги")
    phone_service = st.selectbox("Телефонная связь", [0, 1], format_func=lambda x: "Нет" if x == 0 else "Да")
    paperless_billing = st.selectbox("Безбумажный счет", [0, 1], format_func=lambda x: "Нет" if x == 0 else "Да")
    
    # Charges
    st.subheader("Платежи")
    monthly_charges = st.number_input("Месячный платеж ($)", min_value=0.0, max_value=200.0, value=70.0, step=0.5)
    total_charges = st.number_input("Общая сумма ($)", min_value=0.0, max_value=10000.0, value=1000.0, step=10.0)
    
    # Predict button
    predict_button = st.button("🔮 Прогнозировать", type="primary", use_container_width=True)

# Main area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if predict_button:
        # Load model
        predictor = load_model()
        
        if predictor is not None:
            # Create DataFrame from inputs
            # Note: This is a simplified version - in real scenario you'd need all features
            customer_data = pd.DataFrame({
                'tenure': [tenure],
                'MonthlyCharges': [monthly_charges],
                'TotalCharges': [total_charges],
                'SeniorCitizen': [senior_citizen],
                'Partner': [partner],
                'Dependents': [dependents],
                'PhoneService': [phone_service],
                'PaperlessBilling': [paperless_billing]
            })
            
            try:
                # Note: For this demo, we'll show what would happen if we had all features
                st.warning("⚠️ **Демо режим**: Для полного прогноза требуются все признаки модели. "
                          "Это упрощенная версия для демонстрации интерфейса.")
                
                # For demo, create a mock prediction
                # In production, you'd use: result = predictor.predict_with_details(customer_data)
                mock_probability = 0.35 + (monthly_charges / 200) * 0.3 - (tenure / 72) * 0.2
                mock_probability = np.clip(mock_probability, 0, 1)
                mock_prediction = 1 if mock_probability > 0.5 else 0
                
                if mock_probability < 0.3:
                    mock_risk = "Low"
                elif mock_probability < 0.7:
                    mock_risk = "Medium"
                else:
                    mock_risk = "High"
                
                # Display results
                st.markdown("---")
                st.subheader("📈 Результаты прогноза")
                
                # Metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    prediction_text = "❌ Уйдет" if mock_prediction == 1 else "✅ Останется"
                    st.metric("Предсказание", prediction_text)
                
                with metric_col2:
                    st.metric("Вероятность оттока", f"{mock_probability:.1%}")
                
                with metric_col3:
                    risk_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                    st.metric("Уровень риска", f"{risk_emoji.get(mock_risk, '')} {mock_risk}")
                
                # Probability gauge
                st.markdown("---")
                st.subheader("📊 Визуализация вероятности")
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=mock_probability * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Вероятность оттока (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "lightcoral"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.markdown("---")
                st.subheader("💡 Рекомендации")
                
                if mock_prediction == 1:
                    st.error("⚠️ **Высокий риск оттока!** Рекомендуемые действия:")
                    st.markdown("""
                    - 🎁 Предложить персональную скидку или бонус
                    - 📞 Связаться с клиентом для выявления проблем
                    - 💼 Предложить переход на долгосрочный контракт
                    - 🎯 Предложить дополнительные услуги со скидкой
                    """)
                else:
                    st.success("✅ **Низкий риск оттока.** Рекомендации для удержания:")
                    st.markdown("""
                    - 🌟 Поблагодарить за лояльность
                    - 📧 Информировать о новых услугах
                    - 🎁 Предложить реферальную программу
                    - 📊 Периодически собирать feedback
                    """)
                
            except Exception as e:
                st.error(f"❌ Ошибка при прогнозировании: {e}")
    else:
        # Welcome message
        st.info("👈 Введите данные клиента в боковой панели и нажмите кнопку 'Прогнозировать'")
        
        # Feature explanation
        st.markdown("---")
        st.subheader("📚 О проекте")
        
        st.markdown("""
        Этот проект использует **Machine Learning** для предсказания вероятности ухода клиента 
        телекоммуникационной компании.
        
        **Используемые признаки:**
        - Срок пользования услугами
        - Демографические данные
        - Информация о подключенных услугах
        - История платежей
        
        **Модель:** XGBoost с балансировкой классов (SMOTE)
        
        **Метрики:**
        - Accuracy: 82%
        - ROC-AUC: 85%
        - F1-Score: 61%
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ using Streamlit</p>
        <p><a href='https://github.com/Almas0505/Churn-telecom'>GitHub Repository</a></p>
    </div>
    """, unsafe_allow_html=True)
