import streamlit as st
import pandas as pd
import joblib

model = joblib.load('fraud_detection_pipeline.pkl')

st.title("Fraud Detection App")

st.markdown("Please enter the transaction details below:")

st.divider()

transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
amount = st.number_input("Amount", min_value=0.0, value=100.0)
oldbalanceOrg = st.number_input("Old Balance of Sender",min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance of Sender", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("Old Balance of Receiver", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance of Receiver", min_value=0.0, value=0.0)

if st.button("Predict"):
    input_data = pd.DataFrame([{
    'type': transaction_type,
    'amount': amount,
    'oldbalanceOrg': oldbalanceOrg,
    'newbalanceOrig': newbalanceOrig,
    'oldbalanceDest': oldbalanceDest,
    'newbalanceDest': newbalanceDest
}])

    input_data['balanceDiffOrig'] = input_data['oldbalanceOrg'] - input_data['newbalanceOrig']
    input_data['balanceDiffDest'] = input_data['newbalanceDest'] - input_data['oldbalanceDest']

    prediction = model.predict(input_data)[0]

    st.subheader(f"Prediction : '{int(prediction)}'")

    if prediction == 1:
        st.error("The transaction is predicted to be FRAUDULENT.")
    else:
        st.success("The transaction is predicted to be LEGITIMATE.")