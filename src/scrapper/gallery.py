from .common import ApolloScrapperCommon

class ApolloScrapperGallery:
    def __init__(self):
        self.galleries = [
            "MG", "EA", "1", "7", "8", "9", "10", "11", "12", "13",
            "14", "15", "16", "17", "SV", "PA"
        ]
        self.scrapper = ApolloScrapperCommon()

    def scrap(self, id):
        self.scrapper.write_gallery_json(id, False)
    
    def scrap_all(self):
        for i in self.galleries:
            self.scrap(i)