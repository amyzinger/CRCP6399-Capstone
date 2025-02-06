import pandas as pd
import numpy as np

# Read all datasets
waggle_df = pd.read_csv('Berlin2019_waggle_phases.csv')
followers_df = pd.read_csv('Berlin2019_followers.csv')
feeders_df = pd.read_csv('Berlin2019_feeder_experiment_log.csv')

# Convert timestamps to datetime
waggle_df['timestamp'] = pd.to_datetime(waggle_df['timestamp'])

# Select a 15-minute window of dance data
start_time = '2019-08-30 08:00:00'
end_time = '2019-08-30 08:15:00'
selected_dances = waggle_df[
    (waggle_df['timestamp'] >= start_time) & 
    (waggle_df['timestamp'] <= end_time)
]

# Normalize coordinates to be positive
x_min = selected_dances['x_median'].min()
y_min = selected_dances['y_median'].min()

dance_points = selected_dances.copy()
dance_points['x'] = dance_points['x_median'] - x_min
dance_points['y'] = dance_points['y_median'] - y_min

# Create CSVs for each layer
# Layer 1: Dance points
dance_points[['x', 'y']].to_csv('dance_points.csv', index=False)

# Layer 2: Food sources
# Parse coordinates from string format and convert to x,y
def parse_coordinates(coord_str):
    if pd.isna(coord_str):
        return None, None
    try:
        lat, lon = map(float, coord_str.split(','))
        # Convert to same scale as dance coordinates for visual consistency
        x = (lon - 13.29) * 1000  # Arbitrary scaling, adjust as needed
        y = (lat - 52.45) * 1000
        return x, y
    except:
        return None, None

feeder_coords = feeders_df['coordinates'].apply(parse_coordinates).tolist()
feeder_points = pd.DataFrame(feeder_coords, columns=['x', 'y']).dropna()
feeder_points.to_csv('feeder_points.csv', index=False)

print("Files created:")
print("1. dance_points.csv - Layer 1 (Front)")
print("2. feeder_points.csv - Layer 2 (Middle)")
print("\nNumber of points in each file:")
print(f"Dance points: {len(dance_points)}")
print(f"Feeder points: {len(feeder_points)}")

print("\nCoordinate ranges (after normalization):")
print(f"Dance points X range: 0 to {dance_points['x'].max():.2f}")
print(f"Dance points Y range: 0 to {dance_points['y'].max():.2f}")
