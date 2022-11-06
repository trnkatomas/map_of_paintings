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


def try_to_understand_the_columns(df):
    columns_index = {'painting': ('name', 'title'),
                     'location': ('city', 'gallery', 'country'),
                     'link_to_image': ('image', 'painting'),
                     'technique': ('technique',),
                     'year': ('year',),
                     'dimensions': ('dimensions',)}
    df_columns = [x.lower() for x in df.columns]
    entities_with_indexes = {x:-1 for x in columns_index.keys()}
    for i, column in enumerate(df_columns):
        for e, values in columns_index.items():
            for value in values:
                if value in column:
                    entities_with_indexes.update({e:i})
                    continue
    return entities_with_indexes


def try_to_parse_the_data(listing_page_name):
    the_paintings_list = retrieve_the_page(listing_page_name)
    images_with_links = get_links_for_images_with_names(the_paintings_list)
    assert len(images_with_links) > 0, "There were no links to images on this page"
    page_raw_data = the_paintings_list.get()
    parsed_page = wtp.parse(page_raw_data)
    assert len(parsed_page.tables) > 0, "There was no table on the page"
    images_table = parsed_page.tables[0]
    image_df = pd.DataFrame(images_table.data()[1:], columns=images_table.data()[0])

    parsed_df = image_df.applymap(try_to_parse_cell)
    entities = try_to_understand_the_columns(parsed_df)
    print(entities)
    #parsed_df_with_links = parsed_df.assign(painting_link=lambda x: x.Painting.apply(lambda y: images_with_links.get(y)))
    return parsed_df #_with_links

if __name__ == "__main__":
    carravagio_listing_page = u'List of paintings by Caravaggio'
    durer_listing_page = u'List_of_paintings_by_Albrecht_D%C3%BCrer'
    raphael_listing_page = u'List_of_paintings_by_Raphael'
    listings = [carravagio_listing_page, durer_listing_page, raphael_listing_page]
    for listing in listings:
        df = try_to_parse_the_data(listing)
        #print(df.head())
        print(df.info())
