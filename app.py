import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('Startup_India_Cleaned.csv')
df['Date']=pd.to_datetime(df['Date'],errors='coerce')
df['year']=df['Date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total investment amount
    total_amount = df['Amount'].sum()

    # highest investment amount
    highest_investment = df.groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(1).values[0]

    # average funding
    average_funding = df.groupby('Startup')['Amount'].sum().mean()

    # total funded startup
    total_startup = df['Startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total_amount) + ' Cr')
    with col2:
        st.metric('Highest Investment',str(highest_investment) + ' Cr')
    with col3:
        st.metric('Average Funding',str(round(average_funding,2)))
    with col4:
        st.metric('total startup',total_startup)

    # top sectors count
    top_5_sectors = df.groupby('Vertical')['Vertical'].count().sort_values(ascending=False).head()
    st.subheader('Top 5 Sector Count')
    fig, ax = plt.subplots()
    ax.pie(top_5_sectors, labels=top_5_sectors.index, autopct='%1.1f%%')
    st.pyplot(fig)

    # top sectors amount
    top_5_sectors_amount = df.groupby('Vertical')['Amount'].sum().sort_values(ascending=False).head()
    st.subheader('Top 5 Sectors Amount')
    fig, ax = plt.subplots()
    ax.bar(top_5_sectors_amount.index,top_5_sectors_amount.values)
    st.pyplot(fig)


def load_startup_details(startup):
    # recent fundings
    st.title(startup)
    recent_fundings = df[df['Startup'].str.contains(startup)][
        ['Date', 'Startup', 'Vertical', 'City', 'Round', 'Amount']].sort_values('Date', ascending=False).head()
    st.subheader('Recent Fundings')
    st.dataframe(recent_fundings)

    col1,col2=st.columns(2)

    with col1:
        # stage wise /round wise amount gathered by company
        startup_stage_wise = df[df['Startup'].str.contains(startup)].groupby('Round')['Amount'].sum()
        st.subheader('Sector wise funds')
        fig, ax = plt.subplots()
        ax.pie(startup_stage_wise, labels=startup_stage_wise.index, autopct='%1.1f%%')
        st.pyplot(fig)

    with col2:
        # investors invested in particular company
        startup_investors = df[df['Startup'].str.contains(startup)].groupby('Investors')['Amount'].sum()
        st.subheader('Investors invested')
        fig, ax = plt.subplots()
        ax.bar(startup_investors.index,startup_investors.values)
        st.pyplot(fig)




def load_invester_details(investor):

    # recent 5 investments
    st.title(investor)
    recent_investment = df[df['Investors'].str.contains(investor)][
        ['Date', 'Startup', 'Vertical', 'City', 'Round', 'Amount']].sort_values('Date', ascending=False).head()
    st.subheader('Recent 5 investment')
    st.dataframe(recent_investment)

    col1,col2 = st.columns(2)

    with col1:
        # biggest investments
        biggest_investments = df[df['Investors'].str.contains(investor)].groupby('Startup')[
            'Amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest investments')
        fig, ax = plt.subplots()
        ax.bar(biggest_investments.index,biggest_investments.values)

        st.pyplot(fig)

    with col2:
        # vertical/sector wise investment , show pie chart
        vertical_wise = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum()
        st.subheader('Sector wise investments')
        fig,ax=plt.subplots()
        ax.pie(vertical_wise,labels=vertical_wise.index,autopct='%1.1f%%')
        st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        # show investment in pie chart for round wise
        round_wise = df[df['Investors'].str.contains(investor)].groupby(['Round'])['Amount'].sum()
        st.subheader('Round wise investments')
        fig, ax = plt.subplots()
        ax.pie(round_wise,labels=round_wise.index, autopct='%1.1f%%')
        st.pyplot(fig)


    with col2:
        # city wise investment done in pie chart
        city_wise = df[df['Investors'].str.contains(investor)].groupby('City')['Amount'].sum()
        st.subheader('City wise investments')
        fig, ax = plt.subplots()
        ax.pie(city_wise,labels=city_wise.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # YoY investment graph

    print(df.info())
    yoy_investment = df[df['Investors'].str.contains(investor)].groupby('year')['Amount'].sum()
    fig, ax = plt.subplots()
    ax.plot(yoy_investment.index, yoy_investment.values)
    st.pyplot(fig)



st.sidebar.title('Startup Funding Analysis')

option1 = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investors'])

if option1=='Overall Analysis':
    load_overall_analysis()
elif option1 == 'Startup':
    st.header('Startup Analysis')
    strup = st.sidebar.selectbox('Select Startup',sorted(set(df['Startup'].str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup')
    if btn1:
        load_startup_details(strup)
else:
    invest = st.sidebar.selectbox('Select Investor',sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor')
    if btn2:
        load_invester_details(invest)