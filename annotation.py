import json
import csv
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def normalize_bounding_boxes(image_annotation, image_width, image_height):
    normalized_boxes = []

    for annotation in image_annotation['annotations']:
        label = annotation['label']
        coordinates = annotation['coordinates']

        # Normalize the bounding box coordinates based on image dimensions
        x_min_normalized = coordinates['x_min'] / image_width
        y_min_normalized = coordinates['y_min'] / image_height
        x_max_normalized = coordinates['x_max'] / image_width
        y_max_normalized = coordinates['y_max'] / image_height

        normalized_boxes.append({
            'label': label,
            'x_min': x_min_normalized,
            'y_min': y_min_normalized,
            'x_max': x_max_normalized,
            'y_max': y_max_normalized
        })

    return normalized_boxes


def save_normalized_bounding_boxes(normalized_boxes, filename):
    # Save the normalized bounding box data to a CSV file
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['label', 'x_min', 'y_min', 'x_max', 'y_max'])
        for box in normalized_boxes:
            csv_writer.writerow([box['label'], box['x_min'], box['y_min'], box['x_max'], box['y_max']])


def convert_bounding_boxes(image_annotation):
    converted_boxes = []

    for annotation in image_annotation['annotations']:
        label = annotation['label']
        coordinates = annotation['coordinates']

        x_min = coordinates['x_min']
        y_min = coordinates['y_min']
        x_max = coordinates['x_max']
        y_max = coordinates['y_max']

        width = x_max - x_min
        height = y_max - y_min

        converted_boxes.append({
            'label': label,
            'x_min': x_min,
            'y_min': y_min,
            'width': width,
            'height': height
        })

    return converted_boxes


def save_converted_json(converted_annotation, filename):
    # Save the converted bounding box data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(converted_annotation, json_file, indent=4)


if __name__ == '__main__':
    """
    Image Annotation
    """
    image_annotation = {
        "image_name": "image.jpg",
        "annotations": [
            {
                "label": "Player",
                "coordinates": {
                    "x_min": 150,
                    "y_min": 20,
                    "x_max": 450,
                    "y_max": 540
                }
            },
            {
                "label": "Ball",
                "coordinates": {
                    "x_min": 410,
                    "y_min": 450,
                    "x_max": 500,
                    "y_max": 540
                }
            }
        ]
    }

    # Create and write the data to the image_annotation.json file
    with open('image_annotation.json', 'w') as json_file:
        json.dump(image_annotation, json_file, indent=4)

    # Load the image
    image = Image.open('image.jpg')
    image_width, image_height = image.size

    normalized_boxes = normalize_bounding_boxes(image_annotation, image_width, image_height)

    # Write the normalized bounding boxes to a CSV file
    save_normalized_bounding_boxes(normalized_boxes, 'normalized_bounding_boxes.csv')

    converted_annotation = {
        "image_name": image_annotation['image_name'],
        "annotations": convert_bounding_boxes(image_annotation)
    }

    save_converted_json(converted_annotation, 'converted_image_annotation.json')

    # Load the JSON annotation file (normalized)
    with open('image_annotation.json', 'r') as json_file:
        image_annotation = json.load(json_file)

    # Load the image
    image_path = image_annotation['image_name']
    image = plt.imread(image_path)

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    # Extract bounding box coordinates (normalized)
    boxes = image_annotation['annotations']

    # Draw bounding boxes on the image
    for box in boxes:
        label = box['label']
        x_min = box['coordinates']['x_min']
        y_min = box['coordinates']['y_min']
        x_max = box['coordinates']['x_max']
        y_max = box['coordinates']['y_max']

        # Create a rectangle patch for the bounding box
        rect = patches.Rectangle(
            (x_min, y_min), x_max - x_min, y_max - y_min, linewidth=1, edgecolor='b', facecolor='none'
        )

        # Add the rectangle to the plot
        ax.add_patch(rect)
        ax.text(x_min, y_min - 10, label, fontsize=12, color='r')

    # Set axis limits
    ax.set_xlim(0, image.shape[1])
    ax.set_ylim(image.shape[0], 0)

    # Show the image with bounding boxes
    plt.show()
