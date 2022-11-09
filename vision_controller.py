import io
from PIL import Image

# Imports the Google Cloud client library
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def get_labels(imgBytes):
    # Converts to Vision's Image format
    image = vision.Image(content=imgBytes)

    # Get objects bouding boxes
    objects = client.object_localization(
        image=image
    ).localized_object_annotations

    # Get a PIL image to crop in the loop
    img_stream = io.BytesIO(imgBytes)
    pImage = Image.open(img_stream)

    objects_formatted = []
    print(f'objects count: {len(objects)}')
    for object_ in objects:
        xs = []
        ys = []
        for vertex in object_.bounding_poly.normalized_vertices:
            xs.append(vertex.x * pImage.width)
            ys.append(vertex.y * pImage.height)

        top_x = xs[0]
        top_y = ys[0]

        if xs[3] < top_x:
            top_x = xs[3]
        if ys[1] < top_y:
            top_y = ys[1]
        
        bot_x = xs[2]
        bot_y = xs[2]

        if xs[1] > bot_x:
            bot_x = xs[1]
        if ys[3] > bot_y:
            bot_y = ys[3]

        box = (
            top_x,
            top_y,
            bot_x,
            bot_y
        )

        pImage_crop = pImage.crop(box)

        content_crop = io.BytesIO()
        pImage_crop.save(content_crop, format='PNG')
        content_crop = content_crop.getvalue()

        img_crop = vision.Image(content=content_crop)

        # labels = client.label_detection(
        #     image=img_crop
        # ).label_annotations

        feature_label_detection = vision.Feature()
        feature_label_detection.type_ = vision.Feature.Type.LABEL_DETECTION
        feature_label_detection.max_results = 25
        labels = client.annotate_image({
            'image': img_crop,
            'features': [feature_label_detection]
        })

        objects_labels = []
        for la in labels.label_annotations:
            objects_labels.append(la.description)

        obj = {}
        obj["labels"] = [l.description for l in labels.label_annotations]
        obj["score"] = object_.score
        obj["rect"] = []
        for vertex in object_.bounding_poly.normalized_vertices:
            obj["rect"].append({
                'x': vertex.x,
                'y': vertex.y
            })
        objects_formatted.append(obj)

    