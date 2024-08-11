from bs4 import BeautifulSoup
from statistics import median, variance
from collections import Counter
import psycopg2

# Load the HTML file
with open('python_class_question.html', 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Extract color data from the table
color_data = []
rows = soup.find_all('tr')[1:]  # Skip header row
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 1:
        colors = cells[1].text.split(', ')
        color_data.extend(colors)

print(color_data)

# Analyze colors
color_counter = Counter(color_data)
total_colors = sum(color_counter.values())

def mean_color(color_counter):
    most_common_color = color_counter.most_common(1)[0][0]
    return most_common_color

def most_frequent_color(color_counter):
    return color_counter.most_common(1)[0][0]

def median_color(color_counter):
    # Use frequencies for median calculation
    frequencies = list(color_counter.values())
    return median(frequencies)

def get_variance(color_counter):
    color_values = list(color_counter.values())
    return variance(color_values) if len(color_values) > 1 else 0

def probability_of_red(color_counter):
    red_count = color_counter.get('RED', 0)
    return red_count / total_colors

mean_color_result = mean_color(color_counter)
most_frequent_color_result = most_frequent_color(color_counter)
median_color_result = median_color(color_counter)
variance_result = get_variance(color_counter)
probability_red_result = probability_of_red(color_counter)

print(f"Mean Color: {mean_color_result}")
print(f"Most Frequent Color: {most_frequent_color_result}")
print(f"Median Color Frequency: {median_color_result}")
print(f"Variance of Colors: {variance_result}")
print(f"Probability of Red: {probability_red_result:.2f}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="your_database",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS color_frequencies (
    color VARCHAR(50) PRIMARY KEY,
    frequency INT
)
''')

# Insert data
for color, freq in color_counter.items():
    cursor.execute('''
    INSERT INTO color_frequencies (color, frequency)
    VALUES (%s, %s)
    ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency
    ''', (color, freq))

conn.commit()
cursor.close()
conn.close()
