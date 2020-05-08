from pagination import create_pagination
from information import galleries

for gallery_id in galleries:
    input_file = f"storage/galleries/{gallery_id}.json"
    output_path = f"storage/galleries/{gallery_id}/"
    create_pagination(input_file, output_path)