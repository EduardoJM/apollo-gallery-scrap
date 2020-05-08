from pagination import create_pagination
from information import get_escaped_magazines

magazines = get_escaped_magazines()

for m in magazines:
    input_file = f"storage/magazines/{m}.json"
    output_path = f"storage/magazines/{m}/"
    create_pagination(input_file, output_path)