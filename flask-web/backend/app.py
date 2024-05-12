from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from src.ann import ANN

# CORS(app, resources={r"/upload": {"origins": ["http://localhost:8081"]}})
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # CORS policy applies to all routes, and allows all domains to access your Flask application
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
upload_success = False


@app.route('/get', methods=['GET'])
def get_data():
    if upload_success:
        root = app.config['UPLOAD_FOLDER']
        files = os.listdir(root)
        paths = [os.path.join(root, f) for f in files]
        
        extractor = ANN(paths)
        fusional_features = extractor._get_fusional_features()
        data={}
        data['bird_species']='small chicken',
        data['img_url']="https://www.si.com/.image/ar_1.91%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cg_faces:center%2Cq_auto:good%2Cw_1200/MjAyOTUwMTU0NTk5Mjc3NTgw/jalen-brunson.jpg"
        return jsonify(data)
    else:
        return "Please Upload query images first"


@app.route('/upload', methods=['POST'])
def upload():
    global upload_success  
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Here you can add your machine learning preprocessing
        response = {'message': f'File uploaded successfully.', 'filename': file.filename}
        upload_success = True
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
