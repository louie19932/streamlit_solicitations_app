import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title('Solicitations Filter')

uploaded_file = st.file_uploader('sam.gov -> data services -> contract opportunities -> datagov -> ContractOpportunitiesFullCSV.csv',type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,encoding='ISO-8859-1',low_memory=False)

    #clean
    df['PostedDate'] = pd.to_datetime(df.PostedDate, format='ISO8601', utc=True)
    df['PostedDate'] = df.PostedDate.dt.date
    df = df[df['Department/Ind.Agency'] == 'DEPT OF DEFENSE']
    df = df[(df.Awardee.isnull()) | (df.Awardee == 'null') | (df.Awardee == 'null ') | (df.Awardee == None)]

    # Filter by days ago
    days_back = st.text_input('How many days back? (Leave blank for all)', value='')

    if days_back:
        try:
            days_back = int(days_back)
            today = datetime.today().date()
            daysago = today - timedelta(days=days_back)
            df = df[df.PostedDate >= daysago]
            st.write(f'Dates from {df.PostedDate.min()} to {df.PostedDate.max()}')
        except ValueError:
            st.error('Please enter a valid number of days.')
    st.write(df.head())

    # Search titles
    search_terms = st.text_input('Search Titles:')

    if search_terms:
        words = search_terms.lower().split()

        # Only keep rows where at least one word matches
        mask = df['Title'].str.lower().apply(lambda x: all(word in x for word in words))
        filtered_df = df[mask]

        if not filtered_df.empty:
            st.write(f'Number of results: {len(filtered_df)}')
            st.write('')
            st.write('')

            for ind in filtered_df.index:
                st.write(f"**Title**: {filtered_df.Title[ind]}\n")
                st.write(f"**Response Deadline**: {filtered_df.ResponseDeadLine[ind]}\n")
                st.write(filtered_df.Link[ind])
                st.write('---')
        else:
            st.warning('No results found. Try different search terms.')



