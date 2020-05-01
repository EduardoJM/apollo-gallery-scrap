import json
import random
import math

def get_thumbs(file_path, photo_count):
    f = open(file_path)
    data = json.load(f)
    images = []
    l = len(data)
    part_count = math.ceil(photo_count / l)
    for i in range(0, l):
        in_data = data[i]
        photo_array = in_data["gallery"]
        part_parsed = []
        for j in range(0, part_count):
            num = random.randint(0, len(photo_array) - 1)
            while num in part_parsed:
                num = random.randint(0, len(photo_array) - 1)
            part_parsed.append(num)
            images.append(f"\"{photo_array[num]['links']['standard']}\"")
    display_str = ",\n".join(images)
    return display_str