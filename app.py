from flask import Flask, request, render_template
from orchestrator import orchestrate
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Save uploaded files
    base_data = request.files['base_data']
    current_data = request.files['current_data']

    base_data_path = os.path.join('uploads', base_data.filename)
    current_data_path = os.path.join('uploads', current_data.filename)

    os.makedirs('uploads', exist_ok=True)
    base_data.save(base_data_path)
    current_data.save(current_data_path)

    # Retrieve Mistral API key
    mistral_api_key = request.form.get('mistral_api_key') or os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        return "Mistral API key is required!", 400

    # Run orchestration
    response = orchestrate(base_data_path, current_data_path, mistral_api_key)

    return render_template('results.html', response=response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
