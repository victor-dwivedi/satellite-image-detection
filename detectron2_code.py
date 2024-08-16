import cv2
import numpy as np
import torch
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

class Detectron2Model:
    def __init__(self):
        # Set up the Detectron2 configuration
        self.cfg = get_cfg()
        config_path = "G:/My Drive/models/Detectron2_models/config.yaml"  # Relative path to your config file
        weights_path = "G:/My Drive/models/Detectron2_models/model_final.pth"  # Relative path to your weights file
        
        # Merge from file and set model weights
        self.cfg.merge_from_file(config_path)
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = weights_path
        self.predictor = DefaultPredictor(self.cfg)

    def predict(self, image_path):
        # Load the image
        im = cv2.imread(image_path)
        outputs = self.predictor(im)

        # Visualization
        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=0.8)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        
        
        # Save the result
        result_path = image_path.replace('.jpg', '_result.png')
        cv2.imwrite(result_path, out.get_image()[:, :, ::-1])
        
        return result_path
