from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
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
        
        extractor = ANN(root)
        file_names, class_names = extractor.get_indices(1000, 0.1)

        data={}

        data['bird_species_1']='Jalen Brunson',
        data['img_url_1']="https://www.si.com/.image/ar_1.91%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cg_faces:center%2Cq_auto:good%2Cw_1200/MjAyOTUwMTU0NTk5Mjc3NTgw/jalen-brunson.jpg"
        data['bird_species_2']='Naz Reid',
        data['img_url_2']="https://cdn.forumcomm.com/dims4/default/4b4d971/2147483647/strip/true/crop/3451x2301+0+0/resize/1599x1066!/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.us-west-2.amazonaws.com%2Fbrightspot%2F0a%2F4f%2Fb11228204ecdbe4003209bd31092%2F2022-12-20t035812z-247368338-mt1usatoday19655624-rtrmadp-3-nba-dallas-mavericks-at-minnesota-timberwolves.JPG"
        data['bird_species_3']='Josh Hart',
        data['img_url_3']="https://www.si.com/.image/t_share/MjAyOTM3Mzc0MTE4NzgxOTY0/josh-hart-knicks.jpg"

        return jsonify(data)
    else:
        return "Please Upload query images first"


@app.route('/upload', methods=['POST'])
def upload():
    global upload_success  
    if not request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    files = request.files.getlist('file[]')  # Get the list of files
    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    uploaded_files = []
    for file in files:
        if file:  # Additional checks can be implemented
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            uploaded_files.append(file.filename)

    if uploaded_files:
        upload_success = True
        response = {'message': 'Query images uploaded successfully.', 'filenames': uploaded_files}
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Failed to upload files'}), 400
    
@app.route('/delete-uploads', methods=['POST'])
def delete_uploads():
    folder = app.config['UPLOAD_FOLDER']
    try:
        shutil.rmtree(folder)  # Remove the entire directory
        os.makedirs(folder)    # Recreate the directory after deletion
        return jsonify({'message': 'All files deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete files', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
