from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import keras.utils as image
import numpy as np
import faiss
import keras
import os
import cv2
from .db_manager import DatabaseManager


class ANN():
    def __init__(self, query_paths):
        self.query_paths = query_paths
    
    def _model_init(self):
        base_model = VGG16(weights='imagenet', input_shape=(224, 224, 3))
        intermediate_layer_model = keras.Model(inputs=base_model.input,
                                       outputs=base_model.get_layer("fc1").output)
        return intermediate_layer_model
    
    def _extract_features(self, img_path):
        model = self._model_init()
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array_expanded = np.expand_dims(img_array, axis=0)
        img_preprocessed = preprocess_input(img_array_expanded)
        features = model.predict(img_preprocessed)
        return features.flatten()

    def _get_base_features(self, db_manager):
        all_feature_vectors = db_manager.get_all_feature_vectors()
        return all_feature_vectors # Should be numpy array of shape (N, 4096)
    
    def _get_query_features(self):
        files = os.listdir(self.query_paths)
        sift = cv2.SIFT.create()
        features_cnn_q = []
        sift_features = []
        
        for f in files:
            path = os.path.join(self.query_paths, f)
            if path.endswith(('.png', '.jpg')):
                # Extract CNN features
                feat = self._extract_features(path)
                features_cnn_q.append(feat)
                # Extract SIFT features
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                _, descriptors = sift.detectAndCompute(img, None)
                sift_features.append(descriptors)

        features_sift_q = np.concatenate(sift_features)
        features_cnn_q = np.array(features_cnn_q)
        return features_sift_q, features_cnn_q

    
    def _compute_ann(self, features_all, features_cnn_q):
        dimension = features_all.shape[1]
        index = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity
        index.add(features_all)  # Add the dataset to the index
        # Perform the search
        k = 50  # Number of nearest neighbors to find
        D, I = index.search(features_cnn_q, k)
        return I, D

    def get_indices(self, cnn_ratio, sift_ratio):
        db_manager = DatabaseManager(host='localhost', user='root', password='Lbb15853111953', dbname='sample_bird')
        features_all = self._get_base_features(db_manager)
        features_sift_q, features_cnn_q = self._get_query_features()
        Index, Distance = self._compute_ann(features_all,features_cnn_q)
        indices = Index.flatten()
        distances = Distance.flatten()

        scoring_dict = {}
        sift = cv2.SIFT.create()
        
        for key, value in zip(indices, distances):
            cnn_score = 1/value
            # print(cnn_score)
            # base_path = '../../..'
            f, _, _ = db_manager.fetch_data_by_id(key)
            # f = os.path.join(base_path, f)

            img = cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            if f.endswith(('.png', '.jpg', '.jpeg')):
                _, descriptors = sift.detectAndCompute(img, None)
            else:
                return "Error in uploaded images."
            index_params = dict(algorithm = 1, trees = 5)
            search_params = dict()
            # Create the FLANN matcher
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors, features_sift_q, k=2)
            good_matches = 0
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches+=1

            sift_score = good_matches/min(len(descriptors), len(features_sift_q))
            # print(sift_score)

            score = cnn_ratio*cnn_score + sift_ratio*sift_score
            if key in scoring_dict:
                scoring_dict[key] += score
            else:
                scoring_dict[key] = score
            
        top_three_indecies = [key for key, _ in sorted(scoring_dict.items(), key=lambda item: item[1], reverse=True)[:3]]

        file_names = []
        class_names = []
        for i in top_three_indecies:
            filename, classname, _ = db_manager.fetch_data_by_id(i)
            file_names.append(filename)
            class_names.append(classname)

        return file_names, class_names
    
