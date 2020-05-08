#
# Create a skelton for magazine json
#

import os
from thumb import get_thumbs

find_dir = "storage/magazines/"

output = "["

for file in os.listdir(find_dir):
    if file.endswith(".json"):
        output += "\n{\n\"id\": \"" + file.replace(".json", "") + "\",\n"
        output += "\"title\": \"\",\n"
        file_path = os.path.join(find_dir, file)
        output += "\"file\": \"" + file_path + "\",\n"
        output += "\"thumbs\": [\n"
        thumbs = get_thumbs(file_path, 10)
        output += thumbs
        output += "]\n},"
output += "]"

f = open("storage/magazines.json", "w+")
f.write(output)
f.close()