import json
import os

PHOTO_PER_PAGE = 20

def create_pagination(file_path, output_directory):
    def write_page(output_directory, page_number, page_data):
        output_path = f"{output_directory}{page_number}.json"
        f = open(output_path, "w+")
        f.write(json.dumps(page_data))
        f.close()
    # check if directory exists and try to create
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    f = open(file_path, 'r')
    gallery_data = json.load(f)
    current_page = 1
    current_page_data = []
    current_count = 0
    for i in range(0, len(gallery_data)):
        item = gallery_data[i]
        current_title = ""
        try:
            current_title = gallery_data[i]['title']
        except:
            pass
        
        current_images = []
        for j in range(0, len(item['gallery'])):
            current_images.append(item['gallery'][j])
            current_count += 1
            if current_count >= PHOTO_PER_PAGE:
                current_page_data.append({
                    "title": current_title,
                    "images": current_images
                })
                write_page(output_directory, current_page, current_page_data)
                current_page_data = []
                current_count = 0
                current_page += 1
                current_images = []
        if current_count > 0:
            current_page_data.append({
                "title": current_title,
                "images": current_images
            })
    # write current_page to json
    if len(current_page_data) > 0:
        write_page(output_directory, current_page, current_page_data)
        current_page += 1
    # write the pagination file
    pagination_data = {
        "count": (current_page - 1)
    }
    pagination_file = f"{output_directory}pagination.json"
    pagination_fp = open(pagination_file, "w+")
    pagination_fp.write(json.dumps(pagination_data))
    pagination_fp.close()