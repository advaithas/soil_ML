import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import ttk

# Load soil data
data = pd.read_csv('soil_data.csv')

# Load crop mineral requirement data
crop_requirements = pd.read_csv('crop_requirements.csv')  # Update the filename as needed

# Fit the StandardScaler using nutrient features
nutrient_features = ['Nitrogen', 'Phosphorus', 'Potassium']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data[nutrient_features])
y = data['MineralPercentage']
model = LinearRegression()
model.fit(X_scaled, y)

# Crop-specific fertilizer recommendations
def recommend_fertilizer_for_crop(crop, nutrient_levels):
    recommended_fertilizer = {}
    
    if crop in crop_requirements['Crop'].values:
        required_nutrients = crop_requirements[crop_requirements['Crop'] == crop].iloc[0, 1:]
        for nutrient, required_level in required_nutrients.items():
            if nutrient in nutrient_levels:
                deficit = required_level - nutrient_levels[nutrient]
                recommended_fertilizer[nutrient] = max(0, deficit)
            else:
                recommended_fertilizer[nutrient] = required_level
    
    return recommended_fertilizer

# GUI using tkinter
def plot_graph():
    crop = crop_var.get()
    if crop in crop_requirements['Crop'].values:
        required_nutrients = crop_requirements[crop_requirements['Crop'] == crop].iloc[0, 1:]
        plt.figure(figsize=(8, 5))
        plt.bar(required_nutrients.index, required_nutrients.values, color=['r', 'g', 'b'])
        plt.xlabel('Nutrient')
        plt.ylabel('Required Level')
        plt.title(f'{crop} Nutrient Requirements')
        plt.show()
    else:
        print(f"No nutrient requirements found for {crop}.")

def recommend_fertilizer():
    crop = crop_var.get()
    nutrient_levels = {nutrient: nutrient_vars[i].get() for i, nutrient in enumerate(nutrient_labels)}
    
    # Transform nutrient levels using the fitted scaler
    nutrient_levels_scaled = scaler.transform(np.array([nutrient_levels[nutrient] for nutrient in nutrient_features]).reshape(1, -1))
    
    recommended_fertilizer = recommend_fertilizer_for_crop(crop, nutrient_levels_scaled)
    
    if recommended_fertilizer:
        result_label.config(text="Recommended Fertilizer:")
        recommendation_text = ""
        for nutrient, quantity in recommended_fertilizer.items():
            recommendation_text += f"{nutrient}: {quantity:.2f} kg per acre\n"
        recommendation_label.config(text=recommendation_text)
    else:
        result_label.config(text="No specific fertilizer recommendation.")
        recommendation_label.config(text="")

# Create the main application window
root = tk.Tk()
root.title("Crop Nutrient Management")

# Create a label for crop selection
crop_label = tk.Label(root, text="Select Crop:")
crop_label.pack()

# Create a dropdown menu for crop selection
crop_var = tk.StringVar()
crop_names = crop_requirements['Crop'].tolist()
crop_dropdown = ttk.Combobox(root, textvariable=crop_var, values=crop_names, state="readonly")
crop_dropdown.pack()

# Create labels and entry widgets for nutrient levels
nutrient_labels = ['Nitrogen', 'Phosphorus', 'Potassium']
nutrient_vars = []

for nutrient in nutrient_labels:
    nutrient_frame = tk.Frame(root)
    nutrient_frame.pack()
    nutrient_label = tk.Label(nutrient_frame, text=f"{nutrient} Level:")
    nutrient_label.pack(side=tk.LEFT)
    nutrient_var = tk.DoubleVar(value=0.0)
    nutrient_entry = tk.Entry(nutrient_frame, textvariable=nutrient_var)
    nutrient_entry.pack(side=tk.LEFT)
    nutrient_vars.append(nutrient_var)

# Create buttons for plotting nutrient graph and recommending fertilizer
buttons_frame = tk.Frame(root)
buttons_frame.pack()

plot_button = tk.Button(buttons_frame, text="Plot Nutrient Graph", command=plot_graph)
plot_button.pack(side=tk.LEFT, padx=10)

recommend_button = tk.Button(buttons_frame, text="Recommend Fertilizer", command=recommend_fertilizer)
recommend_button.pack(side=tk.LEFT, padx=10)

# Create labels to display results
result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
result_label.pack(pady=10)

recommendation_label = tk.Label(root, text="", font=("Helvetica", 12))
recommendation_label.pack()

# Start the main event loop
root.mainloop()
