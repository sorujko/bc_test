import streamlit as st

st.title("Redirect Button Example")

# Create a button
if st.button("Go to /grafy"):
    # Redirect to "/grafy" when the button is clicked
    st.markdown('<meta http-equiv="refresh" content="0; URL=/grafy" />', unsafe_allow_html=True)




# Button to clear cache
if st.button("Clear Cache"):
    st.cache_data.clear()

from streamlit_gsheets import GSheetsConnection

conn = st.connection('gsheets', type=GSheetsConnection)

df = conn.read()
    
column_name_mapping = {
    'Kde bývaš? ': 'Location',
    'Pohlavie ' : 'Pohlavie',
    'Z akého okresu pochádzaš?\n(napr. Pezinok)' : 'Bydlisko(okres)',
    'Názov školy \n(napríklad: ZŠ Vajanského Modra)' : 'Škola',
    'Ktorý ročník ZŠ navštevuješ?': 'Grade',
    'Čo najradšej robíš vo svojom voľnom čase?': 'Free Time Activity',
    'Aký je tvoj obľúbený predmet v škole?': 'Favorite School Subject',
    'Ktorá hra ťa baví najviac?': 'Favorite Game',
    'Ktorý film ťa baví najviac?': 'Favorite Movie',
    'Kam by si najradšej cestoval/-a?': 'Dream Travel Destination',
    'Ktorú aktivitu alebo hru hráš veľmi dobre?': 'Skilled Activity/Game',
    'Kedy si bol/-a hrdý/-á na niečo, čo si dokázal/-a urobiť?': 'Proud Achievement',
    'Čo je podľa teba najdôležitejšie na svete?': 'Top World Priority',
    'Prečo je dôležité pomáhať iným?': 'Importance of Helping Others',
    'Čo by si chcel/-a dosiahnuť, aby svet bol lepším miestom?': 'Contribution to a Better World',
    'Ktorá oblasť povolaní sa ti páči?': 'Preferred Career Field',
    'Máš nejaké vysnívané povolanie?\nak áno, napíš, ktoré povolanie je tvoje vysnívané a prečo?': 'Dream Job',
}
 
#rename columns in DataFrame using dictionary
df.rename(columns=column_name_mapping, inplace=True)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df['Preferred Career Field Short'] = df['Preferred Career Field'].str.split('(').str[0].str.strip()
df.drop("Časová pečiatka",axis=1, inplace=True)
df = df.dropna(how='all')
# Print results.


st.dataframe(df)