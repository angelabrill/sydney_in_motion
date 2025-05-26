import pandas as pd

age_df = pd.read_csv('data/median_age.csv')
age_df['Area'] = age_df['Area'].str.upper()
print(age_df.head())

suburb_df = pd.read_csv('data/sydney_sa2_data.csv')
suburb_df = suburb_df['nsw_loca_2']
print(suburb_df.head())

df = pd.merge(suburb_df, age_df, left_on='nsw_loca_2',right_on='Area',how='outer')
df.to_csv("data/age_suburb.csv")




