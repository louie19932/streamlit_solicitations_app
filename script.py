from logging import exception
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

st.title('Sam.gov Contracts Filter')

def flatten(xss):
    return [x for xs in xss for x in xs]

def descr_words(df,idx,pattern):
    pattern = pattern.split('|')
    n = len(pattern)
    for i in range (n):
        if pattern[i].lower() in df['Description'][idx].lower():
            st.write(f'*description: {pattern[i]}')

def title_words(df,idx,pattern):
    pattern = pattern.split('|')
    n = len(pattern)
    for i in range(n):
        if pattern[i].lower() in df['Title'][idx].lower():
            st.write(f'*title: {pattern[i]}')

def read_file(pattern):
    uploaded_file = st.file_uploader('sam.gov -> data services -> contract opportunities -> datagov -> ContractOpportunitiesFullCSV.csv', type='csv')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', low_memory=False)
        # clean
        df['PostedDate'] = pd.to_datetime(df.PostedDate, format='ISO8601', utc=True)
        df['PostedDate'] = df.PostedDate.dt.date
        df = df[df['Department/Ind.Agency'] == 'DEPT OF DEFENSE']
        df = df[(df.Awardee.isnull()) | (df.Awardee == 'null') | (df.Awardee == 'null ') | (df.Awardee == None)]
        df = df[(df.Title.str.contains(pattern, case=False)) | (df.Description.str.contains(pattern, case=False))]
        # days back
        days_back_input = st.text_input('How many days back? (Required)', value='')
        if days_back_input:
            try:
                days_back = int(days_back_input)
                if days_back > 99999:
                    days_back = 99999
                elif days_back < 0:
                    days_back = 0
                today = datetime.today().date()
                daysago = today - timedelta(days=days_back)
                df = df[df.PostedDate >= daysago]
                st.success(f'Dates from {df.PostedDate.min()} to {df.PostedDate.max()}')
                search_terms = st.text_input('Filter Titles (optional):')
                if search_terms:
                    search_words = search_terms.lower().split()
                    mask = df['Title'].str.lower().apply(lambda x: any(word in x for word in search_words))
                    filtered_df = df[mask]
                else:
                    filtered_df = df
                # show results
                if not filtered_df.empty:
                    st.write(f'Number of results: {len(filtered_df)}')
                    for idx, row in filtered_df.iterrows():
                        st.write(f"**Title**: {row['Title']}")
                        st.write(f"**Response Deadline**: {row['ResponseDeadLine']}")
                        descr_words(df,idx,pattern)
                        title_words(df,idx,pattern)
                        st.write(f"{row['Link']}")
                        st.write('---')
                else:
                    st.warning('No results found. Try different search terms.')
            except ValueError:
                st.error('Enter a valid number for days back (e.g., 7, 30).')
        else:
            st.warning('Enter how many days back you want to search.')

def keyword_function():
    try:
        words = [' rf ', ' passive ', ' spectral ', ' sensing ', ' electromagnetic ', ' unmanned ',
                 ' sensor ', ' satellite ', ' surveillance ', ' situational ', ' unintended ', ' radiation ',
                 ' signal ', ' denoising ', ' tracking ', ' counterfeit ', ' awareness ', ' detection ',
                 ' space domain ', ' cyber ', ' anomaly ', ' monitoring ', ' cctv ']
        pattern = '|'.join(words)
        st.write(f'default keywords:\n{pattern} ')
        st.write(f'number of keywords:{len(pattern.split('|'))}')
        add_words = st.text_area("Add comma-separated keywords (optional)")
        if len(add_words)!=0:
            words = [words]
            add_words = add_words.split(",")
            words.append(add_words)
            words = list(flatten(words))
            pattern = '|'.join(words)
            st.write(f'keywords:\n{pattern}')
            st.write(f'number of keywords:{len(pattern.split('|'))}')
            read_file(pattern)
        else:
            read_file(pattern)
    except Exception as e:
        print(e)

if __name__=="__main__":
    keyword_function()






