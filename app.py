import streamlit as st
import pandas as pd
import altair as alt
import ast

df = pd.read_csv("all_pokemon_data.csv")

# make the string into a list thru 
df['types'] = df['types'].apply(ast.literal_eval)
#trying to get the primary type of the pokemon, which is the first type in the list - used lambda to get first type
df['primary_type'] = df['types'].apply(lambda x: x[0] if isinstance(x, list) and x else None)

st.title("Pokémon Weight Distribution by Type")

# Dropdown to filter by the types, default is what shows up automatically
selected_types = st.multiselect(
    "Select one or more Pokémon types to compare:",
    options=df['primary_type'].dropna().unique(),
    default=["fire", "water", "grass"]
)

# give me the rows where primary type in the list -> the 'picker'
filtered_df = df[df['primary_type'].isin(selected_types)]

# Altair Histogram - creating the chart
hist_chart = alt.Chart(filtered_df).mark_bar(opacity=0.75).encode(
    x=alt.X('weight:Q', bin=alt.Bin(maxbins=30), title='Weight (hectograms)'),
    y=alt.Y('count()', title='Number of Pokémon'),
    color=alt.Color('primary_type:N', legend=alt.Legend(title="Type"))
).properties(
    width=700,
    height=400,
    title='Histogram: Pokémon Weights by Type'
)

st.altair_chart(hist_chart, use_container_width=True)

st.markdown("""
**What this chart shows:**  
The histogram is showing the the distribution of Pokémon weights by looking at their primary type in groupings. In this visual, you can select one or more types and compare how weight of the Pokémon is distributed by them.

**Insights:**  
- The histogram is showing the distribution of Pokémon weights by looking at their primary type in groupings.  
- You can select one or more types to see how the weights are spread out across those categories.  
- Most Pokémon tend to weigh less than 1,000 hectograms (which is about 100 kg).  
- Some types show a wide range of weights — for example, water types include both light ones like Goldeen and very heavy ones like Wailord.  
- This chart helps you compare which types tend to be heavier or lighter overall.
""")
# Section Header
st.header("Common Pokémon Abilities")

# Parse and flatten all abilities
from collections import Counter

# convert string to list 
df['abilities'] = df['abilities'].apply(ast.literal_eval)
#make one big list of abilities
all_abilities = [ability for sublist in df['abilities'] for ability in sublist]
#creates a dictionary with ability:count of number of pokemon
ability_counts = Counter(all_abilities)

# gives me 10 most frequent abilities out of all our pokemons
ability_df = pd.DataFrame(ability_counts.most_common(10), columns=["Ability", "Count"])

# Plot
ability_chart = alt.Chart(ability_df).mark_bar().encode(
    x=alt.X("Count:Q"),
    y=alt.Y("Ability:N", sort='-x'),
    color=alt.value("#1f77b4")
).properties(
    width=600,
    height=400,
    title="Top 10 Most Common Pokémon Abilities"
)

st.altair_chart(ability_chart, use_container_width=True)

# Caption
st.markdown("""
**What this chart shows:**  
This bar chart shows the 10 most common abilities that Pokémon have across the entire dataset.

**Insights:**  
- Certain abilities like **swift-swim** and **sturdy** appear frequently.
- These abilities may be shared by multiple species, which could explain why they are so common.
- This view helps you quickly see which abilities show up the most and might play bigger roles in Pokémon battles or gameplay strategy.
""")

