import pywikibot

site = pywikibot.Site('wikipedia:en')
page = pywikibot.Page(site, u"List of paintings by Caravaggio")
print(page)

image_links = page.imagelinks()