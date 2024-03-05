import torch

class ObjectAnalyzer:

    def __init__(self) -> None:
        self.model = torch.hub.load(
            './models/yolov5',
            'custom', 
            path="./models/yolov5/runs/train/exp/weights/best.pt", 
            source="local"
        )

    def analyze_objects(self, image):
        results = self.model(image)
        return eval(results.pandas().xyxy[0].to_json(orient='records'))