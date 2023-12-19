import tkinter as tk
from tkinter import ttk
from tkinter import Label

# Sample data (Replace this with your actual dataset)
data = {
  'age': ['10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99'],
  'menopause': ['lt40', 'ge40', 'premeno'],
  'tumor-size': ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',
                 '55-59'],
  'inv-nodes': ['0-2', '3-5', '6-8', '9-11', '12-14', '15-17', '18-20', '21-23', '24-26', '27-29', '30-32', '33-35',
                '36-39'],
  'node-caps': ['yes', 'no'],
  'deg-malig': ['1', '2', '3'],
  'breast': ['left', 'right'],
  'breast-quad': ['left-up', 'left-low', 'right-up', 'right-low', 'central'],
  'irradiat': ['yes', 'no']
}

# Initialize Tkinter
root = tk.Tk()
root.title("Predicción de la recurrencia del cáncer de mama")


# Function to predict
from tkinter import Label


def predict():
  selected_symptoms = {key: var.get() for key, var in dropdowns.items()}

  # Example prediction result
  prediction_result = "no-recurrence-events"  # Default prediction

  print(selected_symptoms)  # Printing selected symptoms for reference

  # Initialize points with 100
  points = 100

  # Fetch the selected age, degree of malignancy, breast quadrant, and tumor size
  age_selected = selected_symptoms.get('age', '')
  deg_malig = selected_symptoms.get('deg-malig', '')
  breast_quad = selected_symptoms.get('breast-quad', '')
  tumor_size = selected_symptoms.get('tumor-size', '')
  irradiat = selected_symptoms.get('irradiat', '')

  # Deduct points based on the selected degree of malignancy
  if deg_malig == '2':
     points -= 20
  elif deg_malig == '3':
     points -= 25

  # Deduct points if age is older than 50-59
  if age_selected in [ '60-69', '70-79', '80-89', '90-99']:
     points -= 25

  # Deduct points if the breast quadrant is 'left-up' or 'right-up'
  if breast_quad in ['left-up', 'right-up']:
     points -= 15

  # Deduct points if tumor size more than 40-44
  if tumor_size in ['45-49', '50-54', '55-59']:
     points -= 10

  if irradiat == 'no':
     points -= 5

  # Check if points fall below 70
  if points < 75:
     prediction_result = "recurrence-events"
     root.configure(bg="#FFEBEE")  # Red color scheme for recurrence events
  else:
     root.configure(bg="#E8F5E9")  # Green color scheme for no recurrence

  # Display prediction result in the interface
  prediction_label.config(text=f"Prediccion: {prediction_result}")
  prediction_label.pack()

  difference = 100 - points
  answer_label = tk.Label(root, text=f"Porcentaje: {difference}%", font=("Arial", 12))
  answer_label.pack()

# Assuming 'root' is your Tkinter root window
prediction_label = Label(root, text="", font=("Arial", 12))

# Title
title_label = tk.Label(root, text="Predicción de recurrencia del cáncer de mama", font=("Arial", 20, "bold"), fg="#4CAF50")
title_label.pack(pady=10)

# Store the dropdowns
dropdowns = {}

# Create Dropdowns for symptoms
for key, values in data.items():
  frame = tk.Frame(root)
  frame.pack()

  label = tk.Label(frame, text=key.capitalize(), font=("Arial", 12, "bold"), width=10, anchor="w")
  label.grid(row=0, column=0, pady=5, padx=5)

  style = ttk.Style()
  style.theme_use('clam')  # Choose any theme - 'clam', 'alt', 'default', 'classic'
  dropdowns[key] = tk.StringVar(root)
  dropdowns[key].set(values[0])  # Set default value

  # Use ttk.Combobox for enhanced appearance
  option_menu = ttk.Combobox(frame, textvariable=dropdowns[key], values=values, state="readonly", width=15)
  option_menu['font'] = ('Arial', 10)
  option_menu.grid(row=0, column=1, pady=5, padx=5)

# Button to predict
predict_button = tk.Button(root, text="Predict", command=predict, bg="#4CAF50", fg="white", relief="flat",
                         font=("Arial", 12, "bold"), padx=20)
predict_button.pack(pady=20)

# Set window size
root.geometry("630x600")

root.mainloop()



