import pandas as pd
import matplotlib.pyplot as plt

# Read the files
events = pd.read_csv("events.csv")
attendance = pd.read_csv("attendance.csv")

# Clean column names
events.columns = events.columns.str.strip()
attendance.columns = attendance.columns.str.strip()

# Remove duplicate attendance records
attendance = attendance.drop_duplicates()

# Fill missing values
attendance["First_Time_Visitor"] = attendance["First_Time_Visitor"].fillna("No")
attendance["Age_Group"] = attendance["Age_Group"].fillna("Unknown")

# Merge the two tables
merged = attendance.merge(events, on="Event_ID", how="left")

# Create summary report
summary = merged.groupby(
    ["Event_Name", "Promotion_Channel"]
).agg(
    Total_Attendance=("Attendee_Name", "count"),
    First_Time_Visitors=("First_Time_Visitor", lambda x: (x == "Yes").sum())
).reset_index()

# Calculate visitor rate
summary["Visitor_Rate"] = (
    summary["First_Time_Visitors"] /
    summary["Total_Attendance"] * 100
).round(1)

# Create a bar chart
# Create a professional-looking chart
plt.figure(figsize=(14,7))

bars = plt.bar(
    summary["Event_Name"],
    summary["Total_Attendance"]
)

plt.title(
    "Church Event Attendance",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Church Events", fontsize=12)
plt.ylabel("Number of Attendees", fontsize=12)

# Rotate labels so they are readable
plt.xticks(rotation=35, ha="right")

# Add attendance numbers above each bar
for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.05,
        str(int(height)),
        ha="center",
        fontsize=11,
        fontweight="bold"
    )

# Add light horizontal grid lines
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "attendance_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# Business Question 1:
# Which event had the highest attendance?
highest_attendance = summary.sort_values(
    by="Total_Attendance",
    ascending=False
).head(1)

# Business Question 2:
# Which event had the highest first-time visitors?
highest_visitors = summary.sort_values(
    by="First_Time_Visitors",
    ascending=False
).head(1)

# Business Question 3:
# Which event had the highest visitor rate?
highest_visitor_rate = summary.sort_values(
    by="Visitor_Rate",
    ascending=False
).head(1)

# Save Excel Report
with pd.ExcelWriter("church_event_report_v2.xlsx") as writer:
    merged.to_excel(writer, sheet_name="Cleaned Data", index=False)
    summary.to_excel(writer, sheet_name="Summary Report", index=False)
    highest_attendance.to_excel(writer, sheet_name="Highest Attendance", index=False)
    highest_visitors.to_excel(writer, sheet_name="Most Visitors", index=False)
    highest_visitor_rate.to_excel(writer, sheet_name="Highest Visitor Rate", index=False)

print(summary)
print("Report created successfully!")
print("Files created: church_event_report_v2.xlsx and attendance_chart.png")


print("Highest Attendance Event:")
print(highest_attendance)

print("\nHighest First-Time Visitors Event:")
print(highest_visitors)

print("\nHighest Visitor Rate Event:")
print(highest_visitor_rate)

