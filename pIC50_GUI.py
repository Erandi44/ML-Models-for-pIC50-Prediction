import tkinter as tk
from tkinter import messagebox
import joblib
from rdkit import Chem
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Chem import Descriptors
import pandas as pd

# Load the trained RandomForestRegressor model
model = joblib.load('bioactivity/final_rf_model.pkl')

# Load the feature names that were used during training
feature_names = joblib.load('bioactivity/feature_names.pkl')

# Function to generate only the descriptors used during training
def generate_descriptors(smiles, feature_names):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES input")
    
    # Get all RDKit descriptors
    calculator = MoleculeDescriptors.MolecularDescriptorCalculator([desc[0] for desc in Descriptors.descList])
    all_descriptors = list(calculator.CalcDescriptors(mol))
    
    # Create a DataFrame of all descriptors
    descriptor_df = pd.DataFrame([all_descriptors], columns=[desc[0] for desc in Descriptors.descList])
    
    # Select only the descriptors that were used in training
    selected_descriptors = descriptor_df[feature_names].values[0]
    
    return selected_descriptors

# Function to predict pIC50 using the RandomForest model
def predict_pIC50():
    smiles = entry.get()
    try:
        descriptors = generate_descriptors(smiles, feature_names)  # Convert SMILES to descriptors
        prediction = model.predict([descriptors])[0]
        result_label.config(text=f"Predicted pIC50: {prediction:.2f}")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")

# Build the Tkinter GUI
root = tk.Tk()
root.title("pIC50 Prediction from SMILES")

# Input label and entry box for SMILES
tk.Label(root, text="Enter SMILES:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# Predict button
tk.Button(root, text="Predict pIC50", command=predict_pIC50).pack(pady=10)

# Label to show the prediction result
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Start the GUI main loop
root.mainloop()

