import json
import os
import numpy
import ujson

class Database:
    """
        A fake database based on JSON and NPY files to store the predictions the models make, which then can be queried against.
    """
    def __init__(self, database_file_path: str) -> None:
        # Filepaths to load data from
        # The image path files are maps from an image path string to a numpy array within the corresponding .npy file
        self.object_predictions_fp = os.path.join(database_file_path, 'objects.json')
        self.predictions_fp = os.path.join(database_file_path, 'predictions.npy')
        self.prediction_image_paths_fp = os.path.join(database_file_path, 'prediction_image_paths.json')
        self.rmac_predictions_fp = os.path.join(database_file_path, 'rmac_preds.npy')
        self.rmac_prediction_image_paths_fp = os.path.join(database_file_path, 'rmac_image_paths.json')
        
        # Loading current data (if any exists)
        self.object_predictions = self.load_json_data(self.object_predictions_fp)
        self.prediction_image_paths = self.load_json_data(self.prediction_image_paths_fp)
        self.predictions = self.load_npy_data(self.predictions_fp)
        self.rmac_predictions = self.load_npy_data(self.rmac_predictions_fp)
        self.rmac_prediction_image_paths = self.load_json_data(self.rmac_prediction_image_paths_fp)

    def store_predictions(self, predictions, image_paths) -> None:
        '''
            Stores and updates predictions by updating the JSON (map from image path to numpy array) and the corresponding .npy file, saving both using numpy.save() and store_json_data.
        '''
        # Adds new predictions to already stored predictions, or creates new file to store predictions.
        if numpy.size(self.predictions, axis=0) > 0:
            self.predictions = numpy.append(self.predictions, predictions, axis=0)
        else:
            self.predictions = predictions
        numpy.save(self.predictions_fp, self.predictions)
        
        image_path_prediction_map = {}
        max_index = len(self.prediction_image_paths)
        for i in range(max_index, max_index + len(image_paths)):
            image_path_prediction_map[image_paths[i - max_index]] = i
        self.prediction_image_paths.update(image_path_prediction_map)

        self.store_json_data(self.prediction_image_paths, self.prediction_image_paths_fp)
    
    def store_rmac_predictions(self, predictions, image_paths) -> None:
        # This is essentially repeated code from store_predictions, but I decided this over a flag to determine where the predictions we provide should be stored.

        if numpy.size(self.rmac_predictions, axis=0) > 0:
            self.rmac_predictions = numpy.append(self.rmac_predictions, predictions, axis=0)
        else:
            self.rmac_predictions = predictions
        numpy.save(self.rmac_predictions_fp, self.rmac_predictions)
        
        image_path_prediction_map = {}
        max_index = len(self.rmac_prediction_image_paths)

        for i in range(max_index, max_index + len(image_paths)):
            image_path_prediction_map[image_paths[i - max_index]] = i
        self.rmac_prediction_image_paths.update(image_path_prediction_map)
        
        self.store_json_data(self.rmac_prediction_image_paths, self.rmac_prediction_image_paths_fp)
        
    def store_object_data(self, object_infos, image_paths):
        # Store inverted index, i.e. we store a map linking object classes to image paths with these images
        for index, current_object_info in enumerate(object_infos):
            for object_class_name in current_object_info.keys():
                if object_class_name not in self.object_predictions:
                    self.object_predictions[object_class_name] = {}
                self.object_predictions[object_class_name][image_paths[index]] = current_object_info[object_class_name]
        self.store_json_data(self.object_predictions, self.object_predictions_fp)
    
    def store_json_data(self, json_data, json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data) + "\n")
    
    def load_json_data(self, json_file_path):
        ''' Tries loading JSON data, where it returns an empty JSON object if nothing is found. '''
        if not os.path.exists(json_file_path):
            return {}
        with open(json_file_path, encoding='utf-8') as json_file:
            try:
                return ujson.load(json_file) # uJSON is faster for loading large JSON files
            except Exception:
                return {}
    
    def load_npy_data(self, npy_file_path):
        ''' Tries loading numpy data, where it returns an empty numpy array if nothing is found. '''
        if not os.path.exists(npy_file_path):
            return numpy.empty((0, 0))
        try:
            return numpy.load(npy_file_path)
        except Exception:
            return numpy.empty((0, 0))