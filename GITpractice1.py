import numpy as np
import pandas as pd

dfmaster = pd.read_csv(r'D:\Code\Sales 04_28_2023.csv', header=16)

#splits = (df.notna()).iloc[:,0]
df = dfmaster['Category Name']
cat = df[(~df.str.contains("Total", na=True))]
#tot = df[(df.str.contains("Total", na=False))]

print(cat)

cat_dict = {}
idx = list(cat.index)
for i, index in enumerate(idx):
    if cat.iloc[i] == "TOTAL":
        continue
    cat_dict[str(df.iloc[index])] = dfmaster.iloc[(idx[i]+1):(idx[i+1]-2), 1:]

date = pd.read_csv(r'D:\Code\Sales 04_28_2023.csv').iloc[0, 0]
date = date.replace(" 12:00 AM", "")
date = date.replace(" 11:59 PM", "")
with pd.ExcelWriter(f"D:\Code\{date}.xlsx", mode='w') as writer:
    for key in cat_dict.keys():
        cat_dict[key].to_excel(writer, sheet_name=key.replace("/", "")[:31], index=False)
