import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Load data
applicants = pd.read_csv('applicants.csv')
events = pd.read_csv('events.csv')
sessions = pd.read_csv('sessions.csv')

# Merge data
merged_data = pd.merge(applicants, events, on=['session_id', 'applicant_id'])
merged_data = pd.merge(merged_data, sessions, on=['session_id', 'applicant_id'])

# Convert event datetime to datetime objects
merged_data['event_datetime'] = pd.to_datetime(merged_data['event_datetime'])

# Print count of events before filtering
print("Number of events before filtering:", len(merged_data))

# Print event types and their timestamps before filtering
print("Event types and timestamps before filtering:")
print(merged_data[['event_type', 'event_datetime']])

# Filter relevant events
relevant_events = merged_data[(merged_data['event_type'] == 'Ally entered underwriting') |
                              (merged_data['event_type'] == 'Ally submitted test results')]

# Print count of events after filtering
print("Number of events after filtering:", len(relevant_events))

# Print event types and their timestamps after filtering
print("Event types and timestamps after filtering:")
print(relevant_events[['event_type', 'event_datetime']])

# Group by session_id and event_type, then aggregate datetime values
grouped_data = relevant_events.groupby(['session_id', 'event_type'])['event_datetime'].min().unstack()

# Convert columns to datetime objects
grouped_data['Ally submitted test results'] = pd.to_datetime(grouped_data['Ally submitted test results'])
grouped_data['Ally entered underwriting'] = pd.to_datetime(grouped_data['Ally entered underwriting'])

# Calculate time differences
grouped_data['time_to_submit'] = (grouped_data['Ally submitted test results'] -
                                   grouped_data['Ally entered underwriting']).dt.total_seconds() / 3600  # Convert to hours

# Merge with session status to ensure we only include relevant sessions
time_data = pd.merge(grouped_data, sessions[['session_id', 'session_status']], on='session_id')

# Filter out sessions that were not completed or dropped off
time_data = time_data[time_data['session_status'].isin(['completed', 'drop-off'])]

# Separate data into before and after the change
change_date = pd.to_datetime('2259-03-15')
before_change = time_data[time_data['Ally entered underwriting'].dt.tz_localize(None) < change_date]['time_to_submit']
after_change = time_data[time_data['Ally entered underwriting'].dt.tz_localize(None) >= change_date]['time_to_submit']

# Count of events before and after the change
count_before_change = len(before_change)
count_after_change = len(after_change)

# Average time it took for each group
avg_time_before_change = before_change.mean()
avg_time_after_change = after_change.mean()

# Perform statistical test
t_stat, p_val = stats.ttest_ind(before_change.dropna(), after_change.dropna())

# Print results
print(f'Test results before change: Count={count_before_change}, Average Time={avg_time_before_change}')
print(f'Test results after change: Count={count_after_change}, Average Time={avg_time_after_change}')
print(f'T-test statistic: {t_stat}, P-value: {p_val}')
if not pd.isnull(p_val) and p_val < 0.05:
    print("There is a statistically significant difference in the time to submit test results before and after the change.")
else:
    print("There is no statistically significant difference in the time to submit test results before and after the change.")

# Plotting
plt.figure(figsize=(12, 8))

# Plot histogram
plt.subplot(1, 2, 1)
plt.hist([before_change.dropna(), after_change.dropna()], color=['#800020', '#90EE90'], alpha=0.7, bins=20,
         label=['Before Change', 'After Change'])
plt.title('Distribution of Time to Submit Test Results', fontweight='bold', color='turquoise')
plt.xlabel('Time (hours)', fontweight='bold')
plt.ylabel('Frequency', fontweight='bold')
plt.text(0.15, 0.45, f'\n\n\nTest results before change: Count={count_before_change}, Average Time={avg_time_before_change:.2f}',
         transform=plt.gca().transAxes, fontweight='bold', fontsize=10, color='#800020')
plt.text(0.15, 0.4, f'Test results after change: Count={count_after_change}, Average Time={avg_time_after_change:.2f}',
         transform=plt.gca().transAxes, fontweight='bold', fontsize=10, color='#90EE90')
plt.legend()
plt.grid(True)

# Calculate time saved percentage
time_saved_percentage = ((avg_time_before_change - avg_time_after_change) / avg_time_before_change) * 100

# Plot pie chart
plt.subplot(1, 2, 2)
labels = ['Time Saved', 'Time Spent']
sizes = [time_saved_percentage, 100 - time_saved_percentage]
colors = ['#90EE90', '#800020']
explode = (0.1, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140,
        textprops={'fontweight': 'bold'})
plt.axis('equal')
plt.title('Time Saved Percentage', fontweight='bold', color='turquoise')

plt.show()
