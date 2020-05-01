from scrapper.gallery import ApolloScrapperGallery
from scrapper.magazine import ApolloScrapperMagazine

#
# Scraping Galleries
#

gallery = ApolloScrapperGallery()
# for scrap gallery by gallery
# gallery.scrap('14')

# for scrap all galleries, use this:
# gallery.scrap_all()

#
# Scraping Magazines
#
mag = ApolloScrapperMagazine()
mag.scrap_all()