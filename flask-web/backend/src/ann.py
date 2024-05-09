from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.layers import Conv2D, LeakyReLU,MaxPooling2D,Flatten,Dense,Dropout
from keras.models import Model
import keras.utils as image
import numpy as np
import faiss


class ANN():
    def __init__(self, paths):
        self.paths = paths
    
    def _model_init(self):
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        # Replace ReLU with LeakyReLU
        x = base_model.input
        for layer in base_model.layers:
            if isinstance(layer, Conv2D):
                # Creates a new layer with the same configuration as the current layer, but without the activation function
                new_layer = Conv2D(
                    filters=layer.filters,
                    kernel_size=layer.kernel_size,
                    strides=layer.strides,
                    padding=layer.padding,
                    activation=None,  
                    name=layer.name
                )
                
                new_layer.build(layer.input_shape)
                new_layer.set_weights(layer.get_weights())
                
                x = new_layer(x)
                
                # add LeakyReLU
                x = LeakyReLU(alpha=0.01)(x)
                
            elif isinstance(layer, MaxPooling2D):
                x = layer(x)


        # Add the full connection layer
        x = Flatten()(x)  
        x = Dense(4096)(x)
        x = LeakyReLU(alpha=0.01)(x)
        x = Dropout(0.5)(x)

        # feature vector 4096
        return Model(inputs=base_model.input, outputs=x)
    
    def _extract_features(self, model, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array_expanded = np.expand_dims(img_array, axis=0)
        img_preprocessed = preprocess_input(img_array_expanded)
        features = model.predict(img_preprocessed)
        return features.flatten()
    
    def _get_fusional_features(self):
        LeakyReLU_model = self._model_init()
        features_list = []
        for path in self.paths:
            features = self._extract_features(LeakyReLU_model, path)
            features_list.append(features)
        features_array = np.array(features_list)
        return np.mean(features_array, axis=0).reshape((1, 4096))

    
    def _get_base_features(self):
        base_features = []
        # TODO: Implement function
        return base_features # Should be numpy array of shape (N, 4096)
        
    def get_indices(self):
        base_features = self._get_base_features()
        query_features = self._get_fusional_features()
        dimension = base_features.shape[1]
        index = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity
        index.add(base_features)  # Add the dataset to the index

        # Perform the search
        k = 12  # Number of nearest neighbors to find
        _, I = index.search(query_features, k)

        return I[0]
    
