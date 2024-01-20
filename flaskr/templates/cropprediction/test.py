import pandas as pd
df = pd.read_csv('Crop_recommendation.csv')

billy = []

for label in df['label']:
    if not label in billy:
        billy.append(label)

print(billy)