import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title('Solicitations Filter')

uploaded_file = st.file_uploader('sam.gov -> data services -> contract opportunities -> datagov -> ContractOpportunitiesFullCSV.csv',type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', low_memory=False)

    # Clean
    df['PostedDate'] = pd.to_datetime(df.PostedDate, format='ISO8601', utc=True)
    df['PostedDate'] = df.PostedDate.dt.date
    df = df[df['Department/Ind.Agency'] == 'DEPT OF DEFENSE']
    df = df[(df.Awardee.isnull()) | (df.Awardee == 'null') | (df.Awardee == 'null ') | (df.Awardee == None)]

    # days_back input before proceeding
    days_back_input = st.text_input('How many days back? (Required)', value='')

    if days_back_input:
        try:
            days_back = int(days_back_input)
            today = datetime.today().date()
            daysago = today - timedelta(days=days_back)
            df = df[df.PostedDate >= daysago]
            st.success(f'Dates from {df.PostedDate.min()} to {df.PostedDate.max()}')
            search_terms = st.text_input('Filter Titles (optional):')

            if search_terms:
                words = search_terms.lower().split()
                mask = df['Title'].str.lower().apply(lambda x: all(word in x for word in words))
                filtered_df = df[mask]
            else:
                filtered_df = df

            # Show results
            if not filtered_df.empty:
                st.write(f'Number of results: {len(filtered_df)}')
                st.empty()
                st.empty()
                for idx, row in filtered_df.iterrows():
                    st.write(f"**Title**: {row['Title']}")
                    st.write(f"**Response Deadline**: {row['ResponseDeadLine']}")
                    st.write(f"{row['Link']}")
                    st.write('---')
            else:
                st.warning('No results found. Try different search terms.')

        except ValueError:
            st.error('Please enter a valid number for days back (e.g., 7, 30).')
    else:
        st.warning('Please enter how many days back you want to search.')


