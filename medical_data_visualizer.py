import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column 
df['overweight'] = (df['weight'] / (df['height'] / 100) **2).apply(lambda x: 1 if x > 25 else 0)


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

zero_one = { 1: 0, 2: 1, 3: 1}
df['cholesterol'] = df['cholesterol'].map(zero_one)
df['gluc'] = df['gluc'].map(zero_one) 

# Draw Categorical Plot
def draw_cat_plot():

    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,  value_vars = ['alco', 'active','cholesterol', 'gluc', 'overweight','smoke'], id_vars = ['cardio'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.

    df_cat = pd.DataFrame(df_cat.groupby(['variable', 'value', 'cardio'])['value'].count()).rename(columns={'value': 'total'}).reset_index()

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot( kind="bar",data=df_cat,  x="variable", y="total", hue="value", col="cardio")
    fig = fig.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():

    # Clean the data
    df_heat = df[(df['ap_lo']<=df['ap_hi']) &
    (df['height'] >= df['height'].quantile(0.025))&
    (df['height'] <= df['height'].quantile(0.975))&
    (df['weight'] >= df['weight'].quantile(0.025))&
    (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap( corr , mask=mask , fmt='.1f', vmax=.3 , linewidths=.5, center=0 , square=True, cbar_kws = {'shrink':0.7,'format':'%.2f'},annot=True)



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
