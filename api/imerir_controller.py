from io import BytesIO
import requests

def get_labels(content):
    files = {
        'file': ('test file.png', BytesIO(content))
    }
    
    r = requests.post("http://10.3.2.105:5000/v1/object-detection", files=files)

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
