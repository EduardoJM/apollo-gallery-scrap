#
# Util for create random thumbs for the galleries
#

import json
import random
import math
from thumb import get_thumbs

file_path = "storage/galleries/PA.json"
photo_count = 10
print (get_thumbs(file_path, photo_count))