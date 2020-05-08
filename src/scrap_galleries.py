#
# Scraping Galleries
#
from scrapper.gallery import ApolloScrapperGallery

gallery = ApolloScrapperGallery()
# for scrap gallery by gallery
gallery.scrap('14')

# for scrap all galleries, use this:
# gallery.scrap_all()