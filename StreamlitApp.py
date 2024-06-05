import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

# Get the absolute path to the model file
model_path = os.path.abspath('random_forest_model.joblib')

# Load the trained model
model = joblib.load(model_path)

# Title and header
st.title('Pipeline Anomaly Danger Level Prediction')
st.header('Input the characteristics of the anomaly:')

# Input fields for anomaly characteristics
length = st.number_input('Length', min_value=0.0, step=0.1)
width = st.number_input('Width', min_value=0.0, step=0.1)
depth = st.number_input('Depth', min_value=0.0, step=0.1)
ERF = st.number_input('ERF', min_value=0.0, step=0.1)

# Predict button
if st.button('Predict Danger Level'):
    try:
        # Validate input values
        if length <= 0 or width <= 0 or depth <= 0 or ERF <= 0:
            st.error('Please enter positive values for all inputs.')
        else:
            # Prepare input data for prediction
            input_data = np.array([[length, width, depth, ERF]])
            # Make prediction
            prediction = model.predict(input_data)[0]
            # Display prediction
            st.write(f'The predicted danger level is: {prediction}')
    except Exception as e:
        st.error(f"Error in making prediction: {e}")

# Header for file upload
st.header('Or upload an Excel file to process multiple anomalies:')
uploaded_file = st.file_uploader('Choose an Excel file', type='xlsx')

# Handle uploaded file
if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)
        df.dropna(inplace=True)  # Remove rows with missing values

        if df.empty:
            st.error("The uploaded file contains only NaN values or all rows with NaN values were removed.")
        else:
            # Display uploaded data
            st.write('Uploaded Data:')
            st.write(df.head())

            # Column selection for each attribute
            length_col = st.selectbox('Length Column', df.columns)
            width_col = st.selectbox('Width Column', df.columns)
            depth_col = st.selectbox('Depth Column', df.columns)
            erf_col = st.selectbox('ERF Column', df.columns)

            # Validate selected columns
            if length_col and width_col and depth_col and erf_col:
                try:
                    # Prepare input data for prediction
                    input_data = df[[length_col, width_col, depth_col, erf_col]].values
                    # Make predictions
                    predictions = model.predict(input_data)
                    # Add predictions to DataFrame
                    df['DangerLevel'] = predictions

                    # Ask for desired file name
                    file_name = st.text_input('Enter the desired file name', 'processed_anomalies.xlsx')

                    # Create the 'temp' directory if it doesn't exist
                    os.makedirs('temp', exist_ok=True)

                    # Save the DataFrame to a temporary file
                    temp_file_path = os.path.join('temp', file_name)
                    df.to_excel(temp_file_path, index=False)

                    # Download button for processed file
                    st.download_button(
                        label='Download Processed Excel File',
                        data=open(temp_file_path, 'rb').read(),
                        file_name=file_name,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        onclick="this.href = 'data:application/octet-stream;base64,' + btoa(this.download)"
                    )
                except KeyError as e:
                    st.error(f"Error in column selection: {e}")
                except Exception as e:
                    st.error(f"Error in processing file: {e}")
            else:
                st.error('Please select valid columns for all attributes.')
    except Exception as e:
        st.error(f"Error in reading file: {e}")
