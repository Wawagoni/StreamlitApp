import streamlit
import os
model_path = os.path.join(os.getcwd(), 'random_forest_model.joblib')
streamlit.write(os.path.exists(model_path))
