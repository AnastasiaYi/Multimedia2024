import pymysql
import os
import re
import numpy as np

class DatabaseManager:
    def __init__(self, host, user, password, dbname):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=dbname)
        self.cursor = self.connection.cursor()
    
    def get_all_feature_vectors(self):
        query = "SELECT features FROM bird_table"
        all_features = [] 
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()  # Fetch all results in tuple format
            for result in results:
                features_text = result[0]
                if features_text:
                    features = [float(num) for num in features_text.split(',')]
                    all_features.append(features)
            print("length of all feature vectors",len(all_features))
            print("length of feature vector for one image",len(all_features[0]))
            # print("first five",all_features[9][:5])
            return np.array(all_features)
        except Exception as e:
            print("An error occurred:", e)
            return None

    def fetch_data_by_id(self, id):
        query = "SELECT filename, features FROM bird_table WHERE id = %s"
        try:
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            if result:
                filename, features_text = result
                features = [float(num) for num in features_text.split(',')] # convert text into list
                filepath = self.get_file_full_path(filename)
                class_name = self.get_class_name(filename)
                # print("Filepath:", filepath)
                print("Features:", len(features), type(features))
                return filepath, class_name, features
            else:
                print("No data found for ID:", id)
                return None
        except Exception as e:
            print("An error occurred:", e)
            return None
    
    def get_file_full_path(self, filename):
        # base_path = "/Users/jeffreylu/Desktop/24s1/mutimedia "
        base_path = '../../..'
        final_path = os.path.join(base_path,filename)
        print("image full path:", final_path)
        return final_path
    def get_class_name(self, filename):
        # TODO: extract class name based on file name 
        class_name = "class_name"
        print("class_name:",class_name)
        return class_name    

    def close(self):
        self.cursor.close()
        self.connection.close()


db_manager = DatabaseManager(host='localhost', user='root', password='Lbb15853111953', dbname='sample_bird')
# 输入图片id，去数据库里取图片的路径和feature vectors
filename, features, class_name = db_manager.fetch_data_by_id(5)
all_feature_vectors = db_manager.get_all_feature_vectors()
db_manager.close()

