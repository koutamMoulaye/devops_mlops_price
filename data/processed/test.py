import pandas as pd
import json

df = pd.read_csv("X_train.csv")
sample = df.iloc[0].to_dict()

with open("sample_input.json", "w") as f:
    json.dump(sample, f, indent=2)

print("✅ Exemple JSON généré dans sample_input.json")
