import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Auto Loan Calculator')

purchase_price = st.slider('Purchase Price', 0, 70000)
st.text_input('',value=str(purchase_price))

loan_term = st.slider('Loan Term"(months)', 1, 84)
st.text_input('',value=str(loan_term))

interest_rate = st.slider('Interest Rate', 0.00, 20.00)
st.text_input('',value=str(interest_rate))

def calculate_loan_payment(purchase_price, loan_term, interest_rate):
    monthly_interest_rate = interest_rate / 100 / 12
    total_payment = loan_term
    monthly_payment = purchase_price * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -total_payment)
    remaining_balance = purchase_price
    table_data = []

    for i in range(1, total_payment + 1):
        interest = remaining_balance * monthly_interest_rate
        principal = monthly_payment - interest
        remaining_balance -= principal
        total_payment = monthly_payment * i
        table_data.append([i, round(monthly_payment, 2), round(principal, 2), round(interest, 2), round(total_payment,2), round(remaining_balance, 2)])
    return table_data
    

if st.button('Calculate'):
    loan_schedule = calculate_loan_payment(purchase_price, loan_term, interest_rate)
    df = pd.DataFrame(loan_schedule, columns=['Payment #', 'Monthly Payment', 'Principal', 'Interest', 'Total Payment', 'Remaining Balance']).set_index('Payment #')
    total_row = pd.DataFrame({'Monthly Payment': df['Monthly Payment'].sum(), 'Principal': df['Principal'].sum(), 'Interest': df['Interest'].sum(), 'Total Payment': [''], 'Remaining Balance': ['']}, index=['Total'])
    df = pd.concat([df, total_row])
    st.write('Payment Schedule')
    st.write(df)
    # st.write('| Payment # | Monthly Payment | Principal | Interest | Total Payment | Remaining Balance')
    # st.write('| --- | --- | --- | --- | --- | --- |')
    # for row in loan_schedule:
    #     st.write(f'| {row[0]} | {row[1]:,.2f} | {row[2]:,.2f} | {row[3]:,.2f} | {row[4]:,.2f} | {row[5]:,.2f} |')
  
# plotting principal and interest
    payments_data = pd.DataFrame({'Payment Type': ['Principal', 'Interest'], 'Total': [df['Principal'].sum(), df['Interest'].sum()]})
    fig, ax = plt.subplots()
    ax.bar(payments_data['Payment Type'], payments_data['Total'])
    colors = {'Principal': 'blue', 'Interest': 'red'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    ax.legend(handles, labels)
    st.pyplot(fig)
    st.write('Principal and Interest Breakdown')
    # st.write(payments_data)
    st.write('Total Interest Paid:', round(df['Interest'].sum(), 2))
    st.write('Total Principal Paid:', round(df['Principal'].sum(), 2))
    st.write('Monthly Payment:', round(df['Monthly Payment'].iloc[0], 2))
