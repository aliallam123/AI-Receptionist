

'''
🔑 3. Turn Filtering

Decide which speaker turns you care about.

If you want your model to act like a receptionist:

Focus on SYSTEM turns (the answers).

Optionally keep USER turns as the context.
'''

''' 🔑 7. Splitting & Balancing

Make sure you have proper train/validation/test splits.

Standard: 80/10/10 split (train/val/test).

Check class balance (e.g., not all examples are restaurant, some hotel too).
'''



'''
🔑 8. Feature Formatting

Convert your cleaned data into a format your model accepts:

For ML/Deep Learning → often a .csv or .parquet with input_text and target_text.

For classical ML → structured features (slots, intents, etc.).

Two possible directions:

Classical ML (baseline):

Input = TF-IDF features of user turns.

Output = intent/response label.

Neural Seq2Seq / Transformers (advanced):

Input = raw text (user history).

Output = raw text (system reply).

👉 Save in .csv or HuggingFace dataset format.
'''

''' 
🔑 9. Sanity Checks

Make sure no empty texts.

Check that your domains and speakers make sense.

Spot-check 5–10 random dialogues manually to confirm preprocessing didn’t break meaning.
'''

''' 
⏳ How long should this take?

Steps 1–4: 2–3 focused sessions (~1 day).

Steps 5–6: Optional, adds ~2 days if you want slot handling.

Steps 7–9: 1 session (~half a day).

So preprocessing is about 3–5 days max if you’re systematic. That’s enough to get you a dataset you can actually model with, without falling into the “paradox of choice.”
'''

Some useful pandas commands for EDA:

🔍 Exploring data

df.head(n) → view first n rows

df.tail(n) → view last n rows

df.shape → (rows, columns)

df.info() → column types & nulls

df.describe() → summary stats for numeric columns

df.columns → list of column names

df.dtypes → data types of each column

🧹 Filtering & selection

df["col"] → select one column

df[["col1","col2"]] → select multiple

df.loc[row_index, "col"] → by label

df.iloc[row_number, col_number] → by position

df[df["col"] == value] → filter rows

df[df["col"].isin(["a","b"])] → multiple matches

df.drop(columns=["col"]) → remove columns

🧠 Transforming

df["new"] = df["a"] + df["b"] → create new column

df.rename(columns={"old":"new"}) → rename

df.sort_values("col", ascending=False) → sort

df.fillna(value) / df.dropna() → handle missing values

df.apply(func) → apply a custom function

📊 Aggregating

df["col"].value_counts() → frequency counts

df.groupby("col").mean() → group and summarise

df.pivot_table(values="x", index="y", aggfunc="mean") → pivot

💾 Import / export

pd.read_csv("file.csv") / df.to_csv("file.csv")

pd.read_json() / df.to_json()

pd.read_excel() / df.to_excel()