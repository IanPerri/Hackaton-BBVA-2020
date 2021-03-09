# Libraries
import tweepy
import pandas as pd
import numpy as np
import pickle
import tensorflow
from tensorflow import keras

import re
import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import requests
from bs4 import BeautifulSoup
from instagramy import InstagramUser
from py3pin.Pinterest import Pinterest

# Input Tokens of Development Twitter
flag = True
while flag:
    try:
        
        CONSUME_KEY = input('Consume Key: ')
        CONSUME_SECRET = input('Consume Secret: ')
        ACCESS_TOKEN = input('Acces Token: ')
        ACCESS_TOKEN_SECRET = input('Acces Token Secret: ')

        # Authorization
        auth = tweepy.OAuthHandler(CONSUME_KEY, CONSUME_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        # Querry Try
        data = api.me()
        flag = False
    except:
        # Error Message
        print('Incorrect tokens, try again')
        print('')
        
# Pinterest
        
flag = True
while flag:
    try:
        
        email = input('Pinterest Email: ')
        password = input('Pinterest Password: ')
        username = input('Pinterest User Name: ')

        # Authorization
        pinterest = Pinterest(email=email, 
                      password=password, 
                      username=username, 
                      cred_root='cred root dir')

        user_profile = pinterest.get_user_overview('grupobbva')
        flag = False
    except:
        # Error Message
        print('Incorrect tokens, try again')
        print('')
        
# Number of desire tweets        
num_tweets = 70

# Screen Names
sn_bbva = ['@BBVAInnovation', '@BBVA_Mex', '@bbva', '@BBVAresponde_es', '@BBVARe_mx', '@BBVA_Colombia', '@BBVASeguros_mx',
          '@BBVAProvincial', '@BBVAResearch', '@bbva_argentina', '@BBVA_espana', '@Citibanamex', '@SantanderMx']
sn_banco = ['bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'citibanamex', 'santander']
sn_pais = ['GLOBAL', 'MX', 'GLOBAL', 'ES', 'MX', 'COL', 'MX', 'GLOBAL', 'GLOBAL', 'AR', 'ES', 'MX', 'MX', 'MX']



# Data Frame
tweet = tweepy.Cursor(api.user_timeline, screen_name = '@bbva_peru', tweet_mode = "extended", include_rts = False).items(num_tweets)
tl = pd.DataFrame(t.__dict__ for t in tweet)
tl['banco'] = ['bbva' for x in range(len(tl))]
tl['pais'] = ['PE' for x in range(len(tl))]
tl['procedencia'] = ['oficial' for x in range(len(tl))]
tl['tema'] =  ['banco' for x in range(len(tl))]


# Screen Name and number of desired tweets inputs
flag2 = True
while flag2:
    try:
        for i in range(len(sn_bbva)):
        # Querry
            tweet = tweepy.Cursor(api.user_timeline, screen_name = sn_bbva[i], 
                                  tweet_mode = "extended", include_rts = False).items(num_tweets)
            tl_aux = pd.DataFrame(t.__dict__ for t in tweet)
            tl_aux['banco'] = [sn_banco[i] for x in range(len(tl_aux))]
            tl_aux['pais'] = [sn_pais[i] for x in range(len(tl_aux))]
            tl_aux['procedencia'] = ['oficial' for x in range(len(tl_aux))]
            tl_aux['tema'] =  ['banco' for x in range(len(tl_aux))]
            tl = pd.concat([tl, tl_aux])
        flag2 = False
    except:
        # Error Message
        print('Incorrect screen name or integer, try again')
        print('')


# Querries
q_bbva = ['bbva mexico', 'bbva tarjeta', 'bbva credito', 'bbva españa', 'bbva perú', 'bbva servico', 'bbva colombia',
          'bbva pago', 'bbva telefono', 'bbva sucursal', 'bbva viral', 'bbva cobrar', 'bbva cuenta', 'bbva app',
         'santander mexico', 'santander tarjeta', 'santander servicio', 'santander app', 'citibanamex tarjeta',
         'citibanamex mexico', 'citibanamex servicio', 'citibanamex app', 'coronavirus bbva', 'pandemia bbva', 'sanitaria bbva']

q_banco = ['bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva', 'bbva',
          'santander', 'santander', 'santander', 'santander', 'citibanamex', 'citibanamex', 'citibanamex', 'citibanamex',
          'bbva', 'bbva', 'bbva']

q_pais = ['MX', 'GLOBAL', 'GLOBAL', 'ES', 'PE', 'GLOBAL', 'COL', 'GLOBAL', 'GLOBAL', 'GLOBAL', 'GLOBAL', 'GLOBAL', 'GLOBAL',
          'GLOBAL', 'MX', 'GLOBAL', 'GLOBAL', 'GLOBAL','GLOBAL', 'MX', 'GLOBAL', 'GLOBAL', 'GLOBAL', 'GLOBAL', 'GLOBAL']

q_tema = ['MX', 'tarjeta', 'credito', 'ES', 'PE', 'servicio', 'CL', 'pago', 'telefono', 'sucursal', 'viral', 'cobrar', 'cuenta',
          'app', 'MX', 'tarjeta', 'servicio', 'app','tarjeta', 'MX', 'servicio', 'app', 'coronavirus', 'coronavirus', 'coronavirus']


# Data Frame
tweet2 = tweepy.Cursor(api.search, q = 'bbva', tweet_mode = "extended", lang = 'es').items(num_tweets)
bbva = pd.DataFrame(t.__dict__ for t in tweet2)
bbva['banco'] = ['bbva' for x in range(len(bbva))]
bbva['pais'] = ['GLOBAL' for x in range(len(bbva))]
bbva['procedencia'] = ['usuario' for x in range(len(bbva))]
bbva['tema'] =  ['banco' for x in range(len(bbva))]

flag2 = True
while flag2:
    try:
        for i in range(len(q_bbva)):
            tweet2 = tweepy.Cursor(api.search, q = q_bbva[i], tweet_mode = "extended", lang = 'es').items(num_tweets)
            bbva_aux = pd.DataFrame(t.__dict__ for t in tweet2)
            bbva_aux['banco'] = [q_banco[i] for x in range(len(bbva_aux))]
            bbva_aux['pais'] = [q_pais[i] for x in range(len(bbva_aux))]
            bbva_aux['procedencia'] = ['usuario' for x in range(len(bbva_aux))]
            bbva_aux['tema'] = [q_tema[i] for x in range(len(bbva_aux))]
            bbva = pd.concat([bbva, bbva_aux])
            
        flag2 = False
    except: # Exception
        print('Querry not found or too many tweets requested, try again')
        print('')

bbva = bbva[["author", "created_at", "entities", "favorite_count", "full_text", 'lang', 'retweet_count', 'source', 'banco', 'pais', 'procedencia', 'tema']]
tl = tl[["author", "created_at", "entities", "favorite_count", "full_text", 'lang', 'retweet_count', 'source', 'banco', 'pais', 'procedencia', 'tema']]

df = pd.concat([bbva, tl])

# Extracting name and location
s_name = [x.screen_name for x in df.author]
locat = [x.location for x in df.author]
follo = [x.followers_count for x in df.author]
friends = [x.friends_count for x in df.author]
veri = [x.verified for x in df.author]

# Adding extracted features
df["screen_Name"] = s_name
df["location"] = locat
df["followers"] = follo
df["friends"] = friends
df["verified"] = veri

# Dropping Author feature
df.drop('author', axis = 1, inplace=True)

# Extrating hashtags from tweets
hashtags = []
for x in df.entities:
    try:
        hashtags.append(dict(x["hashtags"][0])["text"])
    except:
        hashtags.append("NONE")

# Dummy Variable if tweet has a mention
mentions = []
for x in df.entities:
    try:
        aux = dict(x["user_mentions"][0])["screen_name"]
        mentions.append(1)
    except:
        mentions.append(0)

# Adding new features
df["hashtag"] = hashtags
df["mention"] = mentions

# Ordering Features
df = df[["screen_Name", "location", "created_at", "lang", "full_text", "favorite_count", 
         "retweet_count", "hashtag", "mention", "source", "followers", "friends", "verified", 'banco', 'pais', 
         'procedencia', 'tema']]

def process_tweet(tweet):
    """Process tweet function.
    Input:
        tweet: a string containing a tweet
    Output:
        tweets_clean: a list of words containing the processed tweet

    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('spanish')
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
            # tweets_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)

    return tweets_clean

preprocess_list = np.array([process_tweet(x) for x in df.full_text])

# Neural Network
model = tensorflow.keras.models.load_model("C:/Users/olver/Documents/Edgar/Hackathon_BBVA/Models/Modelo_Ian_7.h5")

# Tokenizer
with open('C:/Users/olver/Documents/Edgar/Hackathon_BBVA/Models/tokenizer_bbva3.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Sequence convertion
maxlen = 100
sequences = tokenizer.texts_to_sequences(preprocess_list)
data = keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen)

# Prediction
predict = (model.predict_proba(data)[:,1] >= 0.448)

polarity = []

for i in predict:
    if i:
        polarity.append('Negativo')
    else:
        polarity.append('Positivo')
        
# Sentiments append
df['Sentiment'] = polarity
df.reset_index(drop = True, inplace = True)

# Adding Characters
df['caracteres'] = [len(x) for x in df.full_text]
df['id'] = [str(df.screen_Name[i] + '_' + str(df.created_at[i]) + '_' + str(df.caracteres[i])).replace(" ", ";") for i in range(len(df))]

# Reset Index
df.drop_duplicates('id', inplace = True)
df.reset_index(drop = True, inplace = True)

df_final = df[['id', 'screen_Name', 'location', 'created_at', 'lang', 'full_text',
       'favorite_count', 'retweet_count', 'hashtag', 'mention', 'source',
       'followers', 'friends', 'verified', 'banco', 'pais', 'Sentiment',
       'caracteres', 'procedencia', 'tema']]

#Engagement per post
engage=[]
engage=np.array([((df_final.iloc[x].retweet_count + df_final.iloc[x].favorite_count)/(df_final.iloc[x].followers + 0.0001))*100 for x in range(df.shape[0])])
df_final['Engagement'] = engage

# Droping BBVA League
df_final = df_final[~df_final.full_text.str.contains("@LigaBBVAMX")]
df_final.reset_index(drop = True, inplace = True)
df_final['red_social'] = ['twitter' for x in range(len(df_final))]

# Other Social Network

user_profile = pinterest.get_user_overview('grupobbva')
BBVA_BOARDS= pinterest.search(scope='boards', query='bbva')
BBVA_PINS = pinterest.search(scope='pins', query='bbva')
engage_bbva = (len(BBVA_BOARDS) + len(BBVA_PINS) + user_profile['profile_reach'])/user_profile['follower_count']

# Intagram
bancos = ["bbva_mex", "citibanamex", "santander_mex"]
instametric = []
datas = []

for cuenta in bancos:
    html = requests.get('https://www.instagram.com/' + cuenta + '/')
    soup = BeautifulSoup(html.text, 'lxml')
    item = soup.select_one("meta[property='og:description']")
    
    user = InstagramUser(cuenta)
    name = user.username
    biografia = user.biography
    seguidores = user.number_of_followers
    seguidos = user.number_of_followings

    posts = user.number_of_posts
    datosins = [name, biografia, seguidores, seguidos, posts]
    #obtenemos las métricas generales de cada banco
    instametric.append(datosins)
    
    instapost = pd.DataFrame(user.posts)
    instapost.insert(0, "Banco", [cuenta for i in range(12)] )
    datas.append(instapost)
    instapostF = pd.concat(datas)

instapostF = instapostF.drop(['url'], axis=1)

instametric = pd.DataFrame(instametric)
instametric.columns = ['Banco','Biografía','Seguidores','Seguidos','Post']
foll = dict(zip(instametric.Banco, instametric.Seguidores))

instapostF['followers'] = [foll[x] for x in instapostF.Banco]
instapostF.reset_index(drop = True, inplace = True)

eng = []
for i in range(len(instapostF)):
    eng.append((instapostF.comment[i] + instapostF.likes[i])/instapostF.followers[i])
    
instapostF['engagement'] = eng

# New Ids
ids = []
for i in range(len(instapostF)):
    ids.append(str(instapostF.Banco[i]) + str(instapostF.timestamp[i]))
    
instapostF['id'] = ids

# Dictionary bank engagement
pint_dict = dict(zip(instapostF['Banco'].unique(), [engage_bbva, 0, 0]))

# Pinterest 
instapostF['Pinterest'] = [pint_dict[x] for x in instapostF.Banco]

# Saving file
try:
    base = pd.read_excel('BBVA.xlsx', sheet_name = 'BBVA')
    base_final = pd.concat([df_final, base])
    
    base_final.drop_duplicates('id', inplace = True)
    base_final.reset_index(drop = True, inplace = True)
    
    x = pd.ExcelWriter('BBVA.xlsx', engine = 'openpyxl')
    base_final.to_excel(x, sheet_name = 'BBVA', index = False)
    x.save()
    
except:
    x = pd.ExcelWriter('BBVA.xlsx', engine = 'openpyxl')
    df_final.to_excel(x, sheet_name = 'BBVA', index = False)
    x.save()
