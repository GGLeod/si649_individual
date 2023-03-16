#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np
import pprint
import streamlit as st


# In[2]:
st.title("People Who Cannot See a Doctor Due to Cost in the Past 12 Months")

st.write('''
Some studies suggest that people with disabilities get medical care less frequently. This visualization shows the proportion 
of people who cannot see a doctor due to cost in the past 12 months. By comparing the people
with disability and without disability, from the obvious color difference, we can find that in all states in all years, this number of people
with disability is much higher. 

From the bar chart, we can further compare and rank the proportion difference between two groups of all states.
While the US average difference is around 15\% for these years, this number can be much higher in some states. In 2016, the proportion difference 
in North Carolina reaches 24.3%. This number of people with disability (35.7%) is more than three times higher than people without disability (11.4%).
This could be caused by the fact that people with disability typically have less income. Another reason is that people with disability may be subject to 
higher medical cost. Patients with disability may have to go to a farther and more expensive clinic or hospital for the accessible equipments.

In addition, from the line chart, we can see that the proportion for both two groups does not change much from 2016 to 2019. Both proportions
 significently drop in 2020 when covid broke out and people had to spent their money to see a doctor even it was a heavy burden. Hopefully, more 
 measures can be done to overcome the medical barrier of people with disability and it would be great to see the line drops in the future.
''')

st.write("_**Click your interested state and year below!**_")

df=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/not_see_doctor.csv")
df2016=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/2016.csv")
df2017=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/2017.csv")
df2018=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/2018.csv")
df2019=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/2019.csv")
df2020=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/2020.csv")
dfn2016=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/N2016.csv")
dfn2017=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/N2017.csv")
dfn2018=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/N2018.csv")
dfn2019=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/N2019.csv")
dfn2020=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649_individual/main/N2020.csv")
dfn = dfn2016.append(dfn2017, ignore_index=True).append(dfn2018, ignore_index=True).append(dfn2019, ignore_index=True).append(dfn2020, ignore_index=True)
df = df.append(dfn, ignore_index=True)


state_map = data.us_10m.url


# In[3]:

state_id = {
    "Alabama": "1",
    "Alaska": "2",
    "Arizona": "4",
    "Arkansas": "5",
    "California": "6",
    "Colorado": "8",
    "Connecticut": "9",
    "Delaware": "10",
    "District of Columbia": "11",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Idaho": "16",
    "Illinois": "17",
    "Indiana": "18",
    "Iowa": "19",
    "Kansas": "20",
    "Kentucky": "21",
    "Louisiana": "22",
    "Maine": "23",
    "Maryland": "24",
    "Massachusetts": "25",
    "Michigan": "26",
    "Minnesota": "27",
    "Mississippi": "28",
    "Missouri": "29",
    "Montana": "30",
    "Nebraska": "31",
    "Nevada": "32",
    "New Hampshire": "33",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "North Carolina": "37",
    "North Dakota": "38",
    "Ohio": "39",
    "Oklahoma": "40",
    "Oregon": "41",
    "Pennsylvania": "42",
    "Rhode Island": "44",
    "South Carolina": "45",
    "South Dakota": "46",
    "Tennessee": "47",
    "Texas": "48",
    "Utah": "49",
    "Vermont": "50",
    "Virginia": "51",
    "Washington": "53",
    "West Virginia": "54",
    "Wisconsin": "55",
    "Wyoming": "56"
}



# In[4]:


def addId(df):
    df['id']=len(df)*[0] 
    for k in state_id:
        df.loc[df['LocationDesc']==k, 'id'] = int(state_id[k])
    return df


def getChart(df, df2016, dfn2016, interested_year):

    df = addId(df)
    df = df[(df['id']!=0) | (df['LocationAbbr']=="US")]
    # for index, row in df.iterrows():
    #     print(row['LocationDesc'], row['id'])

    df2016 = addId(df2016)
    dfn2016 = addId(dfn2016)
    df2016['Data_Value2'] = dfn2016['Data_Value'] 
    df2016['diff'] = df2016['Data_Value']-df2016['Data_Value2']
    df2016 = df2016[(df2016['id']!=0) | (df2016['LocationAbbr']=="US")]



    # df2016 = df2016.drop(df2016[df2016.diff=='0'].index)
    # df2016.sample(5)
        


    # In[16]:


    selection = alt.selection_single(fields=['id'])
    opacity = alt.condition(selection, alt.value(1.0), alt.value(0.2))

    slider=alt.binding_range(
        min=1,
        max=56,
        step=1,
        name="range shown"
        )

    selector = alt.selection_single(
        bind=slider,
        fields= ["cutoff"],
        init={"cutoff":15}
        )


    states = alt.topo_feature(state_map, 'states')
    map_chart = alt.Chart(states, title="proportion cannot see a doctor (disability)").mark_geoshape().encode(
        color=alt.Color('Data_Value:Q', title="percentage (%)"),
        opacity=opacity,
        tooltip=[alt.Tooltip('Data_Value:Q', title='rate (%)'), alt.Tooltip('LocationDesc:N', title='State')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df2016, key='id', fields=['Data_Value'])
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df2016, key='id', fields=['LocationDesc'])
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df2016, key='id', fields=['diff'])
    ).project(
        'albersUsa'
    ).add_selection(selection)

    map_chart_N = alt.Chart(states, title="proportion cannot see a doctor (no disability)").mark_geoshape().encode(
        color='Data_Value:Q',
        opacity=opacity,
        tooltip=[alt.Tooltip('Data_Value:Q', title='rate (%)'), alt.Tooltip('LocationDesc:N', title='State')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(dfn2016, key='id', fields=['Data_Value'])
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(dfn2016, key='id', fields=['LocationDesc'])
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df2016, key='id', fields=['diff'])
    ).project(
        'albersUsa'
    ).add_selection(selection)


    # (map_chart |  map_chart_N)
    # # (bar_chart+rule_chart)
    # ((map_chart |  map_chart_N) & (bar_chart+rule_chart+text | line_chart+point_chart)).configure_view(width=350)


    # In[17]:


    bar_chart = alt.Chart(df2016).mark_bar().encode(
        x=alt.X("diff", title="proportion difference between people with and without disability (%)"),
        y=alt.Y('LocationDesc', sort=alt.EncodingSortField(field='diff', order='ascending'), title=None),
        opacity = opacity,
        color=alt.value('lightgrey'),
        tooltip=[
            alt.Tooltip('Data_Value:Q', title='with diasability (%)'), 
            alt.Tooltip('Data_Value2:Q', title='without disability (%)'),  
            alt.Tooltip("diff", title="difference (%)")
        ]
        
    ).transform_window(
        rank='rank(diff)',
        sort=[alt.SortField('diff', order='descending')],
        
    ).transform_filter(
        (alt.datum.rank <= selector.cutoff)
    ).transform_filter(
        (alt.datum.LocationAbbr !='US')
    ).add_selection(selection).add_selection(selector)


    rule_chart = alt.Chart(df2016).mark_rule(size=3, color='firebrick').encode(
        x='diff:Q',
    ).transform_filter(
        (alt.datum.LocationAbbr =='US')
    )

    text = rule_chart.mark_text(
        fontSize=14,
        align='left',
        baseline='middle',
        color='firebrick',
        text="US average: " + '%.1f' % float(df2016['diff'][0]),
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        # text=alt.Text('diff:Q', format='.2f')
    ).transform_filter(
        (alt.datum.LocationAbbr =='US')
    )


    # bar_chart+rule_chart+text 


    # In[26]:


    line_chart = alt.Chart(df).mark_line().encode(
        x="Year:O",
        y=alt.Y("average(Data_Value):Q", title="proportion (%)"),
        color=alt.Color('Stratification1:N', title="group")
    ).add_selection(selection).transform_filter(selection).transform_filter(selection)

    point_chart = alt.Chart(df).mark_circle().encode(
        x="Year:O",
        y="average(Data_Value):Q",
        color='Stratification1:N',
        size=alt.condition(alt.datum.Year==interested_year, alt.value(300), alt.value(100))
    ).transform_filter(selection)
    # line_chart+point_chart


    # In[27]:


    final = ((map_chart |  map_chart_N) & (bar_chart+rule_chart+text | line_chart+point_chart)).configure_view(width=300)
    return final


tab1, tab2, tab3, tab4, tab5 = st.tabs(['2016','2017','2018','2019','2020'])

with tab1:
    st.altair_chart(getChart(df, df2016, dfn2016, 2016), use_container_width=True)
with tab2:
    st.altair_chart(getChart(df, df2017, dfn2017, 2017), use_container_width=True)
with tab3:
    st.altair_chart(getChart(df, df2018, dfn2018, 2018), use_container_width=True)
with tab4:
    st.altair_chart(getChart(df, df2019, dfn2019, 2019), use_container_width=True)
with tab5:
    st.altair_chart(getChart(df, df2020, dfn2020, 2020), use_container_width=True)



# In[ ]:


