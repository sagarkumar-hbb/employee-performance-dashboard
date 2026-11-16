"""PS 76 - Employee Performance Dashboard
Console dashboard using Pandas and Matplotlib.
CSV columns: Name, Department, Rating (1-5), Projects
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt


def get_category(rating):
    """Assign performance category from rating."""
    if rating >= 4.5:
        return "Outstanding"
    elif rating >= 3.5:
        return "Good"
    elif rating >= 2.5:
        return "Average"
    return "Needs Improvement"


def load_data(path):
    """Load CSV, validate rows, skip invalid ones with a message."""
    try:
        raw = pd.read_csv(path, header=None, dtype=str, skipinitialspace=True)
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("CSV file is empty.")
        return None

    # Drop header row if present
    if str(raw.iloc[0, 2]).strip().lower() == "rating":
        raw = raw.iloc[1:]

    rows = []
    for _, r in raw.iterrows():
        name = str(r[0]).strip()
        dept = str(r[1]).strip()
        try:
            rating = float(r[2])
        except (ValueError, TypeError):
            print(f"Invalid rating '{r[2]}' for {name}. Row skipped.")
            continue
        if not 1 <= rating <= 5:
            print(f"Invalid rating {r[2].strip()} for {name}. "
                  f"Rating must be between 1 and 5. Row skipped.")
            continue
        try:
            projects = int(float(r[3]))
            if projects < 0:
                raise ValueError
        except (ValueError, TypeError):
            print(f"Invalid project count '{r[3]}' for {name}. Row skipped.")
            continue
        rows.append({"Name": name, "Department": dept,
                     "Rating": rating, "Projects": projects})

    df = pd.DataFrame(rows, columns=["Name", "Department", "Rating", "Projects"])
    if df.empty:
        print("No valid records found.")
        return None
    df["Category"] = df["Rating"].apply(get_category)
    return df


def department_average(df):
    avg = df.groupby("Department")["Rating"].mean().sort_index()
    print(" | ".join(f"{d}: {v:.2f}" for d, v in avg.items()))
    plt.figure()
    plt.bar(avg.index, avg.values, color="steelblue")
    plt.title("Average Rating by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Rating")
    plt.ylim(0, 5)
    plt.show()


def top_performer(df):
    best = df.loc[df["Rating"].idxmax()]
    print(f"Top performer: {best['Name']} ({best['Department']}) | "
          f"Rating: {best['Rating']:.1f} | Category: {best['Category']}")


def categories(df):
    order = ["Outstanding", "Good", "Average", "Needs Improvement"]
    parts = []
    counts = {}
    for cat in order:
        names = df.loc[df["Category"] == cat, "Name"].tolist()
        counts[cat] = len(names)
        label = f"{cat}: {len(names)}"
        if names:
            label += f" ({', '.join(names)})"
        parts.append(label)
    print(" | ".join(parts))

    shown = {k: v for k, v in counts.items() if v > 0}
    plt.figure()
    plt.pie(shown.values(), labels=shown.keys(), autopct="%1.0f%%", startangle=90)
    plt.title("Performance Category Distribution")
    plt.show()


def projects_per_department(df):
    total = df.groupby("Department")["Projects"].sum().sort_index()
    print(" | ".join(f"{d}: {v}" for d, v in total.items()))
    plt.figure()
    plt.bar(total.index, total.values, color="seagreen")
    plt.title("Projects per Department")
    plt.xlabel("Department")
    plt.ylabel("Total Projects")
    plt.show()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else input(
        "Enter CSV file name [employees.csv]: ").strip() or "employees.csv"
    df = load_data(path)
    if df is None:
        return

    actions = {"1": department_average, "2": top_performer,
               "3": categories, "4": projects_per_department}
    while True:
        print("\n=== Employee Performance Dashboard ===")
        print("1. Department-wise average rating")
        print("2. Top performer")
        print("3. Performance categories")
        print("4. Total projects per department")
        print("5. Exit")
        try:
            choice = input("Enter choice: ").strip()
        except EOFError:
            break
        if choice == "5":
            print("Goodbye!")
            break
        if choice in actions:
            actions[choice](df)
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
