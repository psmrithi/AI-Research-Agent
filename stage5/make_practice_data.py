from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # fixed seed: same data every run
states = ["Tamil Nadu", "Karnataka", "Maharashtra", "Delhi"]

rows = []
for state_index, state in enumerate(states):
    base = 500 * (state_index + 1)
    for year in range(2015, 2025):
        rows.append({
            "year": year,
            "state": state,
            "ev_registrations": int(base * 1.6 ** (year - 2015) * rng.uniform(0.9, 1.1)),
            "avg_price_lakh": round(float(rng.uniform(9.0, 16.0)), 2),
        })

df = pd.DataFrame(rows)

# --- Make it messy on purpose ---
df.loc[15, "ev_registrations"] *= 50                    # an outlier
df.loc[[3, 17, 25], "avg_price_lakh"] = np.nan          # missing values
df.loc[[5, 6], "state"] = "tamil nadu "                 # inconsistent names
df.loc[12, "state"] = "KARNATAKA"
df["ev_registrations"] = df["ev_registrations"].apply(lambda v: f"{v:,}")  # numbers as text
df = pd.concat([df, df.iloc[[2, 9]]])                   # duplicate rows
df = df.sample(frac=1, random_state=1).reset_index(drop=True)   # shuffle

out = Path("data/sample")
out.mkdir(parents=True, exist_ok=True)
df.to_csv(out / "practice_ev_registrations_SYNTHETIC.csv", index=False)
df.to_excel(out / "practice_ev_registrations_SYNTHETIC.xlsx", index=False)

print(f"Wrote {len(df)} rows to {out}")