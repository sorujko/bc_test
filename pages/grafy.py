import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
import random

conn = st.connection("gsheets", type=GSheetsConnection)

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





tab1, tab2, tab3, tab4, tab5 = st.tabs(["Spolu", "Ročník", "Mesto/dedina","Bydlisko(okres)","Škola"])

with tab1:
    
    grouped_df = df.groupby(['Pohlavie', 'Preferred Career Field Short']).size().reset_index(name='Count')

    pohlavie_rozdelit = st.toggle(label ='rozdeliť podla pohlavi?', value=False)
    if pohlavie_rozdelit == False :
        fig = go.Figure()
        for gender in grouped_df['Pohlavie'].unique():
            
            color = ''
            if gender =='dievča':
                color = 'red'
            else:
                color = 'blue'
            data = grouped_df[grouped_df['Pohlavie'] == gender]
            fig.add_trace(go.Bar(
                x=data['Preferred Career Field Short'],
                y=data['Count'],
                name=gender,
                marker_color= color
            ))

        # Update layout
        fig.update_layout(
            barmode='group',
            title='Preferred Career Field by Gender',
            xaxis=dict(title='Preferred Career Field Short', tickangle=45),
            yaxis=dict(title='Count'),
            legend=dict(title='Gender')
        )

        
        st.write(fig)
    else:
        genders = df['Pohlavie'].unique()

    # Create a bar graph for each gender
        for gender in genders:
            # Filter DataFrame for the current gender
            filtered_df = df[df['Pohlavie'] == gender]
            
            color = ''
            if gender =='dievča':
                color = 'red'
            else:
                color = 'blue'
            # Group the filtered DataFrame by 'Preferred Career Field Short' and count the occurrences
            grouped_df = filtered_df['Preferred Career Field Short'].value_counts().reset_index()
            grouped_df.columns = ['Preferred Career Field Short', 'Count']
            
            # Create bar graph
            fig = go.Figure(go.Bar(
                x=grouped_df['Preferred Career Field Short'],
                y=grouped_df['Count'],
                name=gender,
                marker_color= color
            ))
            
            # Update layout
            fig.update_layout(
                title=f'Preferred Career Field for {gender}',
                xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                yaxis=dict(title='Count')
            )
            
            # Show the plot
            st.write(fig)

with tab2:
    
    pohlavie_rozdelit_rocnik = st.toggle(label ='rozdeliť podla pohlavi?', value=False, key = 144155) 
    
    if pohlavie_rozdelit_rocnik == False:
        grouped_df = df.groupby(['Grade', 'Pohlavie', 'Preferred Career Field Short']).size().reset_index(name='Count')

        # Get unique grades
        grades = df['Grade'].unique()
        grades = sorted(grades)
        # Create separate graphs for each unique value in the 'Grade' column
        for grade in grades:
            # Create a filtered DataFrame for the current grade
            filtered_df = grouped_df[grouped_df['Grade'] == grade]
            color = ''
            
            # Create a new figure for each grade
            fig = go.Figure()
            
            # Add traces for each gender
            for gender in filtered_df['Pohlavie'].unique():
                # Filter DataFrame for the current gender
                gender_df = filtered_df[filtered_df['Pohlavie'] == gender]
                if gender =='dievča':
                    color = 'red'
                else:
                    color = 'blue'
                
                fig.add_trace(go.Bar(
                    x=gender_df['Preferred Career Field Short'],
                    y=gender_df['Count'],
                    name=gender,
                    marker_color = color
                ))

            # Update layout
            fig.update_layout(
                barmode='group',
                title=f'Preferred Career Field by Gender for Grade {grade}',
                xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                yaxis=dict(title='Count'),
                legend=dict(title='Gender')
            )
            
            # Show the plot
            st.write(fig)
    
    else:
        grouped_df = df.groupby(['Grade', 'Pohlavie', 'Preferred Career Field Short']).size().reset_index(name='Count')

# Get unique grades
        grades = df['Grade'].unique()
        grades = sorted(grades)
        # Create separate graphs for each unique value in the 'Grade' column
        for grade in grades:
            # Create a filtered DataFrame for the current grade
            filtered_df = grouped_df[grouped_df['Grade'] == grade]
            
            # Create separate graphs for boys and girls
            for gender in filtered_df['Pohlavie'].unique():
                if gender =='dievča':
                    color = 'red'
                else:
                    color = 'blue'
                
                # Filter DataFrame for the current gender
                gender_df = filtered_df[filtered_df['Pohlavie'] == gender]
                
                # Create a new figure for each grade, gender combination
                fig = go.Figure()
                
                # Add trace for the current gender
                fig.add_trace(go.Bar(
                    x=gender_df['Preferred Career Field Short'],
                    y=gender_df['Count'],
                    name=gender,
                    marker_color = color
                ))
                
                # Update layout
                fig.update_layout(
                    title=f'Preferred Career Field for {gender} - Grade {grade}',
                    xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                    yaxis=dict(title='Count')
                )
                
                # Show the plot
                st.write(fig)
                
with tab3:
    
    grouped_df = df.groupby(['Location', 'Pohlavie', 'Preferred Career Field Short']).size().reset_index(name='Count')
    
    pohlavie_rozdelit_bydlisko = st.toggle(label ='rozdeliť podla pohlavi?', value=False, key = 14532633) 

# Get unique locations
    locations = df['Location'].unique()

# Create separate graphs for each unique value in the 'Location' column
    if pohlavie_rozdelit_bydlisko == False:
        for location in locations:
            # Create a filtered DataFrame for the current location
            filtered_df = grouped_df[grouped_df['Location'] == location]
            
            # Create a new figure for each location
            fig = go.Figure()
            
            # Add traces for each gender
            for gender in filtered_df['Pohlavie'].unique():
                if gender =='dievča':
                    color = 'red'
                else:
                    color = 'blue'
                # Filter DataFrame for the current gender
                gender_df = filtered_df[filtered_df['Pohlavie'] == gender]
                
                fig.add_trace(go.Bar(
                    x=gender_df['Preferred Career Field Short'],
                    y=gender_df['Count'],
                    name=gender,
                    marker_color = color
                ))

            # Update layout
            fig.update_layout(
                barmode='group',
                title=f'Preferred Career Field by Gender for Location {location}',
                xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                yaxis=dict(title='Count'),
                legend=dict(title='Gender')
            )
            
            # Show the plot
            st.write(fig)
    else:
        grouped_df = df.groupby(['Location', 'Pohlavie', 'Preferred Career Field Short']).size().reset_index(name='Count')

# Get unique locations
        locations = df['Location'].unique()

        # Create separate graphs for each unique value in the 'Location' column
        for location in locations:
            # Create a filtered DataFrame for the current location
            filtered_df = grouped_df[grouped_df['Location'] == location]
            
            # Create separate graphs for each gender
            for gender in filtered_df['Pohlavie'].unique():
                # Filter DataFrame for the current gender
                gender_df = filtered_df[filtered_df['Pohlavie'] == gender]
                
                if gender =='dievča':
                    color = 'red'
                else:
                    color = 'blue'
                    
                # Create a new figure for each location and gender
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=gender_df['Preferred Career Field Short'],
                    y=gender_df['Count'],
                    name=gender,
                    marker_color = color
                ))

                # Update layout
                fig.update_layout(
                    barmode='group',
                    title=f'Preferred Career Field for {gender} - Location {location}',
                    xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                    yaxis=dict(title='Count'),
                    legend=dict(title='Gender')
                )
                
                # Show the plot
                st.write(fig)

with tab4:
    grouped_df = df.groupby(['Bydlisko(okres)', 'Preferred Career Field Short']).size().reset_index(name='Count')

    bydlisko_rozdelit = st.toggle(label='rozdeliť podľa bydliska?', value=False)
    if bydlisko_rozdelit == False:
        fig = go.Figure()
        for bydlisko in grouped_df['Bydlisko(okres)'].unique():
            color = 'blue'  # Default color
            data = grouped_df[grouped_df['Bydlisko(okres)'] == bydlisko]
            fig.add_trace(go.Bar(
                x=data['Preferred Career Field Short'],
                y=data['Count'],
                name=bydlisko,
                marker_color=color
            ))

        # Update layout
        fig.update_layout(
            barmode='group',
            title='Preferred Career Field by Location',
            xaxis=dict(title='Preferred Career Field Short', tickangle=45),
            yaxis=dict(title='Count'),
            legend=dict(title='Location')
        )

        st.write(fig)
    else:
        locations = df['Bydlisko(okres)'].unique()

        # Create a bar graph for each location
        for location in locations:
            # Filter DataFrame for the current location
            filtered_df = df[df['Bydlisko(okres)'] == location]
            
            # Group the filtered DataFrame by 'Preferred Career Field Short' and count the occurrences
            grouped_df = filtered_df['Preferred Career Field Short'].value_counts().reset_index()
            grouped_df.columns = ['Preferred Career Field Short', 'Count']
            
            # Create bar graph
            fig = go.Figure(go.Bar(
                x=grouped_df['Preferred Career Field Short'],
                y=grouped_df['Count'],
                name=location,
                marker_color='blue'
            ))
            
            # Update layout
            fig.update_layout(
                title=f'Preferred Career Field for {location}',
                xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                yaxis=dict(title='Count')
            )
            
            # Show the plot
            st.write(fig)

with tab5:
    grouped_df = df.groupby(['Škola', 'Preferred Career Field Short']).size().reset_index(name='Count')

    skola_rozdelit = st.toggle(label='rozdeliť podľa školy?', value=False)
    if skola_rozdelit == False:
        fig = go.Figure()
        for skola in grouped_df['Škola'].unique():
            # Generating a random color for each school
            color = '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
            data = grouped_df[grouped_df['Škola'] == skola]
            fig.add_trace(go.Bar(
                x=data['Preferred Career Field Short'],
                y=data['Count'],
                name=skola,
                marker_color=color
            ))

        # Update layout
        fig.update_layout(
            barmode='group',
            title='Preferred Career Field by School',
            xaxis=dict(title='Preferred Career Field Short', tickangle=45),
            yaxis=dict(title='Count'),
            legend=dict(title='School')
        )

        st.write(fig)
    else:
        schools = df['Škola'].unique()

        # Create a bar graph for each school
        for school in schools:
            # Filter DataFrame for the current school
            filtered_df = df[df['Škola'] == school]
            
            # Group the filtered DataFrame by 'Preferred Career Field Short' and count the occurrences
            grouped_df = filtered_df['Preferred Career Field Short'].value_counts().reset_index()
            grouped_df.columns = ['Preferred Career Field Short', 'Count']
            
            # Generating a random color for each school
            color = '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])
            
            # Create bar graph
            fig = go.Figure(go.Bar(
                x=grouped_df['Preferred Career Field Short'],
                y=grouped_df['Count'],
                name=school,
                marker_color=color
            ))
            
            # Update layout
            fig.update_layout(
                title=f'Preferred Career Field for {school}',
                xaxis=dict(title='Preferred Career Field Short', tickangle=45),
                yaxis=dict(title='Count')
            )
            
            # Show the plot
            st.write(fig)
