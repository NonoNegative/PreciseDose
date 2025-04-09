import onnx
import onnxruntime as ort
import numpy as np

# Load the ONNX model
model = onnx.load("assets\\nn\\Oral.onnx")

# model summary
print("\nONNX Model Information")
print("=" * 40)
print("Model Metadata")
print(f"  - IR Version: {model.ir_version}")
print(f"  - Producer Name: {model.producer_name or 'N/A'}")
print(f"  - Domain: {model.domain or 'N/A'}")
print(f"  - Model Version: {model.model_version}")
print(f"  - Doc String: {model.doc_string.strip() or 'N/A'}")
print(("=" * 40) + '\n')

def predict_dosage(input_array, onnx):
    
    session = ort.InferenceSession(f"assets\\nn\\Oral.onnx", providers=['CPUExecutionProvider'])

    input_header = ['Gender', 'Age', 'Systolic BP', 'Diastolic BP', 'BMI', 'Temperature']

    input_data = np.array([input_array], dtype=np.float32)

    # Get the input and output names from the model
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    prediction = session.run([output_name], {input_name: input_data})

    for i in range(len(input_header)-1):
        print(f"{input_header[i]}: {input_array[i]}")

    if onnx == 'Oral.onnx':
        print(f"Predicted dosage: {prediction[0][0][0]} mL")
        return prediction[0][0][0]
    else:
        session = ort.InferenceSession(f"assets\\nn\\{onnx}", providers=['CPUExecutionProvider'])

        input_header = ['Oral dosage']

        input_data = np.array([[prediction[0][0][0]]], dtype=np.float32)

        # Get the input and output names from the model
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name

        prediction = session.run([output_name], {input_name: input_data})

        for i in range(len(input_header)-1):
            print(f"{input_header[i]}: {input_array[i]}")

        print(f"Predicted dosage: {prediction[0][0][0]} mL")
        return prediction[0][0][0]
