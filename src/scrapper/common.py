import requests
from lxml import html
import json
import os

class ApolloScrapperCommon:
    def __init__(self):
        self.session = requests.session()
        self.url = 'http://www.apolloarchive.com/apg_subject_index.php'

    def get_image_url_from_magazine(self, image_id):
        folder = ""
        if image_id.startswith("AS07"):
            folder = "a410"
        elif image_id.startswith("AS09"):
            folder = 'a410'
        elif image_id.startswith("AS11"):
            folder = "a11"
        elif image_id.startswith("AS12"):
            folder = "a12"
        elif image_id.startswith("AS14"):
            folder = "a14"
        elif image_id.startswith("AS15"):
            folder = "a15"
        elif image_id.startswith("AS16"):
            folder = "a16"
        elif image_id.startswith("AS17"):
            folder = "a17"
        if folder != "":
            # if folder is not empty, get image url from common path format
            url = f"https://www.hq.nasa.gov/office/pao/History/alsj/{folder}/{image_id}"
            hd_url = f"{url}HR.jpg"
            url = f"{url}.jpg"
            return {
                "highres": hd_url,
                "standard": url
            }
        return None

    def get_image_url(self, image_id, is_magazine = False, link_id = 1):
        if is_magazine:
            result = self.get_image_url_from_magazine(image_id)
            if result != None:
                return result
        # if folder is empty or if is not magazine, load from web request
        url = f'http://www.apolloarchive.com/apg_thumbnail.php?ptr={link_id}&imageID={str(image_id)}'
        result = self.session.get(url, headers = dict(referer = url))
        if result.status_code == 200:
            tree = html.fromstring(result.content)
            table_col = tree.xpath("//body/table//td//table//tr/td[last()]")
            if len(table_col) == 0:
                return None
            array_standard = table_col[0].xpath(".//a[text()='Standard']/@href")
            array_highres = table_col[0].xpath(".//a[text()='Hi-Res']/@href")
            if len(array_standard) == 0:
                if len(array_highres) == 0:
                    return None
                else:
                    return {
                        "highres": array_highres[0]
                    }
            else:
                if len(array_highres) == 0:
                    return {
                        "standard": array_standard[0]
                    }
                else:
                    return {
                        "highres": array_highres[0],
                        "standard": array_standard[0]
                    }
        else:
            print('Error in web scrap: ', result.status_code)
            return None

    def get_gallery_images(self, gallery_id, is_magazine = False):
        url = f"{self.url}?gallery={str(gallery_id)}"
        # request page content from url
        result = self.session.get(url, headers = dict(referer = url))
        if result.status_code == 200: # success
            # build html tree, get table rows
            # and instantiate some variables
            tree = html.fromstring(result.content)
            rows = tree.xpath("//table//tr")
            elements = []
            current = []
            current_title = ""
            index = 0
            # iterate each row
            for r in rows:
                # check for title row
                sect = r.xpath("th[@colspan='4']")
                if len(sect) == 0:
                    # check for heading
                    sect = r.xpath("th")
                    if len(sect) == 0:
                        # is a image registry
                        sect = r.xpath("td")
                        if len(sect) == 4:
                            s_id = ""
                            s_cred = ""
                            s_desc = ""
                            s_date = ""
                            s_added = ""
                            s_pid_href = ""
                            array_id = sect[0].xpath("a/text()")
                            if len(array_id) != 0:
                                s_id = array_id[0]
                            href_array = sect[0].xpath("a/@href")
                            if len(href_array) != 0:
                                s_pid_href = href_array[0]
                            array_cred = sect[0].xpath("span[@class='cred']/text()")
                            if len(array_cred) != 0:
                                s_cred = array_cred[0]
                            s_desc = sect[1].text_content()
                            s_date = sect[2].text_content()
                            s_added = sect[3].text_content()
                            link_id = "1"
                            try:
                                link_id = s_pid_href.split("(")[1].split(",")[0].replace("'", "")
                            except:
                                link_id = "1"
                            dict_links = self.get_image_url(s_id, is_magazine, link_id)
                            current.append({
                                "id": s_id,
                                "credits": s_cred,
                                "description": s_desc,
                                "date": s_date,
                                "added": s_added,
                                "links": dict_links
                            })
                else:
                    # is a title row
                    if len(current) > 0 and current_title != "":
                        elements.append({
                            "title": current_title,
                            "gallery": current
                        })
                        current = []
                    current_title = sect[0].text_content()
                print("Parsed: " + str(index + 1) + " of " + str(len(rows)) + " rows")
                index = index + 1
            # iterate over rows terminated, check if has pictures
            # in current array and storage
            if len(current) > 0 and current_title != "":
                elements.append({
                    "title": current_title,
                    "gallery": current
                })
            elif len(current) > 0:
                elements.append({
                    "gallery": current
                })
            return elements
        else:
            return None

    def create_gallery_json(self, gallery_id, is_magazine):
        g = self.get_gallery_images(gallery_id, is_magazine)
        return json.dumps(g)

    def write_gallery_json(self, gallery_id, is_magazine):
        json = self.create_gallery_json(gallery_id, is_magazine)
        gid = gallery_id.replace("/", "-")
        path = "storage/galleries/" + gid + ".json"
        if is_magazine:
            path = "storage/magazines/" + gid + ".json"
        f = open(path, "w+")
        f.write(json)
        f.close()