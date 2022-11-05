import pywikibot

import pandas as pd
import wikitextparser as wtp
import spacy

nlp = spacy.load("en_core_web_trf")

def retrieve_the_page(page_name):
    site = pywikibot.Site('wikipedia:en')
    page = pywikibot.Page(site, f"{page_name}")
    return page

def get_links_for_images_with_names(page):
    images_list = page.imagelinks()
    image_links_dict = {i.title():i.get_file_url() for i in images_list}
    return image_links_dict

def get_table(page):
    pass

def fix_link_protocol(link):
    if link.startswith("//"):
        return f'http:{link}'
    else:
        return link

def get_the_page_link_by_name(name):
    page = pywikibot.Page(site, f"{name}")
    return fix_link_protocol(page.permalink())

def try_to_parse_cell(cell):
    parsed_cell = wtp.parse(cell)
    all_the_text = ''
    if parsed_cell.wikilinks:
        if "File:" in parsed_cell.wikilinks[0].title:
            return parsed_cell.wikilinks[0].title
        else:
            gather_text = [x.text for x in parsed_cell.wikilinks if x.text]
            if gather_text:
                all_the_text += " ".join(gather_text)                
    return all_the_text + " " + parsed_cell.plain_text()    

def parse_with_ner(cell):
    doc = nlp(cell)
    return {(ent.text, ent.label_) for ent in doc.ents}

if __name__ == "__main__":
    the_paintings_list = retrieve_the_page(u'List of paintings by Caravaggio')
