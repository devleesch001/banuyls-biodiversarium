from io import BytesIO
import requests

IA_URL = "http://10.3.2.105:80"

def get_labels(content):
    files = {
        'file': ('test file.png', BytesIO(content))
    }
    
    r = requests.post(f"{IA_URL}/v1/image-detection/", files=files)

    detections = []
    for object in r.json()["detection"]:
        conf = object["conf"]
        detection = object["class_name"]
        positions = {
            "topleft":{"x":object["x1"], "y":object["y1"]},
            "bottomright":{"x":object["x2"], "y":object["y2"]}
        }
        detections.append({"detection":detection, "position":positions, "certainty":conf})
    return detections
