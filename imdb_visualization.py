# importing neccessary libraries
import pandas as pd 
import numpy as np 
import streamlit as st
import altair as alt 
import matplotlib.pyplot as plt
import psycopg2
#--------------------------------------------------------

# setting page configuration
st.set_page_config(layout='wide')

# connecting python with SQL database
conn = psycopg2.connect(
    host=st.secrets['host'],
    database=st.secrets['database'],
    user=st.secrets['user'],
    password=st.secrets['password'],
    port=st.secrets['port']
)

# creating dataframe
imdb=pd.read_sql('select * from imdb',conn)

#--------------------------------------------------------

# creating header
col1,col2= st.columns([1,3],gap='small')
with col1:
    image='https://1000logos.net/wp-content/uploads/2023/01/IMDb-logo.png'
    st.image(image,width=250)
with col2:
    st.write('IMDb is a comprehensive online database that provides information on movies, TV shows, and the entertainment industry. It offers details on cast and crew, plot summaries, user ratings and reviews, trivia, and more, making it a go-to resource for movie enthusiasts. IMDb also allows users to connect and share thoughts on various titles.')
    st.write('Here are the insights of 10,000 movies and shows present in the imdb data below.')
st.markdown('''---''')

# ---------------------------------------------------------------

# showing dataframe
st.subheader(':orange[DATAFRAME]') 
st.markdown('This dataset consist of ratings for over 10,000 movies and shows.')
st.dataframe(imdb)

# showing statistical descp
st.subheader(':orange[STATISTICAL DESCRIPTION]')
st.table(imdb.describe().T)

#creating columns
col1,col2 = st.columns(2)

# Correlation heatmap
with col1:
    st.subheader(':orange[CORRELATION AMONG VARIABLES]')
#     corr = imdb.corr()
#     corr_long = corr.reset_index().melt(id_vars='index')
#     heatmap = alt.Chart(corr_long).mark_rect().encode(
#         alt.X('index:O',title=''),
#         alt.Y('variable:O',title=''),
#         color=alt.Color('value:Q', scale=alt.Scale(domain=[-1,+1],range=['black','orange','black'])),
#         tooltip=alt.Tooltip('value')
#     ).properties(height=400, width=450)
#     st.altair_chart(heatmap)

# Top five shows and movies based on weighted mean
with col2:
    st.subheader(':orange[TOP 5 MOVIES AND SHOWS]')
    top_movies=imdb.sort_values(by='weighted_rating',ascending=False)[:5]
    top_movies_chart=alt.Chart(top_movies).mark_bar().encode(
        alt.X('weighted_rating'),
        alt.Y('title',sort='-x'),
        tooltip=[alt.Tooltip('title'),alt.Tooltip('votes'),alt.Tooltip('rating'),alt.Tooltip('weighted_rating')],
        color=alt.value('orange')
        ).properties(height=400,width=600)
    st.altair_chart(top_movies_chart)

# Top five shows and movies based on rating alone
with col1:
    st.subheader(':orange[TOP 5 MOVIES AND SHOWS BASED ON] RATINGS ALONE')
    top_movies_by_rating_alone=imdb.sort_values(by=['rating','votes'],ascending=False)[:5]
    top_movies_by_rating_alone_chart=alt.Chart(top_movies_by_rating_alone).mark_bar().encode(
        alt.X('rating'),
        alt.Y('title',sort='-x'),
         tooltip=[alt.Tooltip('title'),alt.Tooltip('votes'),alt.Tooltip('rating'),alt.Tooltip('weighted_rating')],
        color=alt.value('orange')
        ).properties(height=350,width=600)
    st.altair_chart(top_movies_by_rating_alone_chart)

# Top five shows and movies based on votes alone
with col2:
    st.subheader(':orange[TOP 5 MOVIES AND SHOWS BASED ON] VOTINGS ALONE')
    top_movies_by_voting_alone=imdb.sort_values('votes',ascending=False)[:5]
    top_movies_by_voting_alone_chart=alt.Chart(top_movies_by_voting_alone).mark_bar().encode(
        alt.X('votes'),
        alt.Y('title',sort='-x'),
         tooltip=[alt.Tooltip('title'),alt.Tooltip('votes'),alt.Tooltip('rating'),alt.Tooltip('weighted_rating')],
        color=alt.value('orange')
        ).properties(height=350,width=600)
    st.altair_chart(top_movies_by_voting_alone_chart)

# Trend analysis
# Rating trend over year
with col1:
    st.subheader(':orange[RATING TREND OVER YEAR]')
    rating_trend=imdb[(imdb['rating']!=0) & (imdb['year']!=0)].groupby(by='year')['rating'].mean()
    rating_trend_df=pd.DataFrame({'year':rating_trend.index,'rating':rating_trend.values})
    rating_trend_chart=alt.Chart(rating_trend_df).mark_line().encode(
        alt.X('year'),
        alt.Y('rating'),
        color=alt.value('gold')
        ).properties(width=600)
    st.altair_chart(rating_trend_chart)

# Voting trend over year
with col2:
    st.subheader(':orange[VOTING TREND OVER YEAR]')
    voting_trend=imdb[(imdb['votes']!=0) & (imdb['year']!=0)].groupby(by='year')['votes'].mean()
    voting_trend_df=pd.DataFrame({'year':voting_trend.index,'votes':voting_trend.values})
    voting_trend_chart=alt.Chart(voting_trend_df).mark_area().encode(
        alt.X('year'),
        alt.Y('votes'),
        color=alt.value('gold')
        ).properties(width=600)
    st.altair_chart(voting_trend_chart)

# Weighted rating over year
with col1:
    st.subheader(':orange[WEIGHTED RATING TREND OVER YEAR]')
    weighted_rating_trend=imdb[(imdb['weighted_rating']!=0) & (imdb['year']!=0)].groupby(by='year')['weighted_rating'].mean()
    weighted_rating_trend_df=pd.DataFrame({'year':weighted_rating_trend.index,'weighted_rating':weighted_rating_trend.values})
    weighted_rating_trend_chart=alt.Chart(weighted_rating_trend_df).mark_line().encode(
        alt.X('year'),
        alt.Y('weighted_rating'),
        color=alt.value('chocolate')
        ).properties(width=600)
    st.altair_chart(weighted_rating_trend_chart)

with col2:
    # create word cloud for description column 
    st.subheader(':orange[MOST FREQUENT WORD IN DESCRIPTION]')
    from wordcloud import WordCloud
    import nltk 
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    # Pre-process the movie descriptions to create a frequency table
    desc_list = " ".join(imdb['desc'][imdb['desc']!= 'Not specified'].tolist()).split()
    desc_list = [word for word in desc_list if word.lower() not in stop_words]
    word_counts = pd.Series(desc_list).value_counts()
    # Generate the word cloud
    wordcloud = WordCloud(height=300,width=600).generate_from_frequencies(dict(word_counts))
    # wordcloud.to_file("imdb_wordcloud.png")
    # st.image("imdb_wordcloud.png")
    st.image(wordcloud.to_image())

col1,col2 = st.columns(2)
# most frequent certificates 
with col1:
    st.subheader(':orange[MOST FREQUENT CERTIFICATES]')
    top_certificates=imdb['certificate'].value_counts().reset_index()
    top_certificates.drop([0,4],axis=0,inplace=True)
    top_certificates.rename(columns={'index':'certificate','certificate':'count'},inplace=True)
    top_certificates_5=top_certificates.head()
    certificate_pie= alt.Chart(top_certificates_5).mark_arc(innerRadius=60).encode(
        theta=alt.Theta('count:Q',stack=True),
        color=alt.Color('certificate:N',scale=alt.Scale(domain=list(top_certificates_5 ['certificate']),range=['darkorange','orange','darkgoldenrod','goldenrod','gold']))
        ).properties(height=340,width=325)
    st.altair_chart(certificate_pie)

# most frequent genres
with col2:
    st.subheader(':orange[MOST FREQUENT GENRES]')
    top_genre=imdb['genre'].value_counts().head(5).reset_index()
    top_genre.rename(columns={'index':'genre','genre':'count'},inplace=True)
    genre_pie= alt.Chart(top_genre).mark_arc(innerRadius=60).encode(
        theta=alt.Theta('count:Q',stack=True),
        color=alt.Color('genre:N',scale=alt.Scale(domain=list(top_genre ['genre']),range=['darkorange','orange','darkgoldenrod','goldenrod','gold']))
        ).properties(height=340,width=400)
    st.altair_chart(genre_pie)

# top movies and shows by year
with col1:
    st.subheader(':orange[TOP MOVIES AND SHOWS BY YEAR BASED ON] WEIGHTED RATING')
    year_unique=imdb['year'].unique()
    top_by_year=st.number_input('ENTER YEAR',value=2022,min_value=1913,max_value=2024)
    if top_by_year in year_unique:
        top_movie_of_year=imdb[imdb['year']==top_by_year].sort_values(by='weighted_rating',ascending=False)[:5]
        top_movie_of_year_chart=alt.Chart(top_movie_of_year).mark_bar().encode(
            alt.X('weighted_rating'),
            alt.Y('title',sort='-x'),
            tooltip=[alt.Tooltip('title'),alt.Tooltip('certificate'),alt.Tooltip('votes'),alt.Tooltip('rating'),alt.Tooltip('weighted_rating')],
            color=alt.value('gold')
            ).properties(height=350,width=650)
        st.altair_chart(top_movie_of_year_chart)
    else:
        st.warning('No data available on this particular year. Please enter another year', icon="⚠️")

# top movies and shows based on certificates
with col2:
    st.subheader(':orange[TOP MOVIES AND SHOWS BY YEAR BASED ON] CERTIFICATE')
    certificates_unique=imdb['certificate'].unique()
    top_by_certificate=st.selectbox('SELECT CERTIFICATE',certificates_unique)
    top_movie_by_certificate=imdb[imdb['certificate']==top_by_certificate].sort_values(by='weighted_rating',ascending=False)[:5]
    top_movie_by_certificate_chart=alt.Chart(top_movie_by_certificate).mark_bar().encode(
                alt.X('weighted_rating'),
                alt.Y('title',sort='-x'),
                tooltip=[alt.Tooltip('title'),alt.Tooltip('year'),alt.Tooltip('votes'),alt.Tooltip('rating'),alt.Tooltip('weighted_rating')],
                color=alt.value('orange')
                ).properties(height=350,width=650)
    st.altair_chart(top_movie_by_certificate_chart)

# the end :)
st.write('''---''')

