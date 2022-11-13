from collections import Counter

import pandas as pd
import pywikibot
import spacy
import wikitextparser as wtp

nlp = spacy.load("en_core_web_trf")


def retrieve_the_page(page_name):
    site = pywikibot.Site("wikipedia:en")
    page = pywikibot.Page(site, f"{page_name}")
    return page


def get_links_for_images_with_names(page):
    images_list = page.imagelinks()
    image_links_dict = {i.title(): i.get_file_url() for i in images_list}
    return image_links_dict


def get_table(page):
    pass


def fix_link_protocol(link):
    if link.startswith("//"):
        return f"http:{link}"
    else:
        return link


def get_the_page_link_by_name(name):
    page = pywikibot.Page(site, f"{name}")
    return fix_link_protocol(page.permalink())


def try_to_parse_cell(cell):
    parsed_cell = wtp.parse(cell)
    all_the_text = ""
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


def get_instances_for_link(link):
    page = pywikibot.Page(site, f"{link}")
    data_item = page.data_item()
    is_instance_of = data_item.claims.get("P31")
    return [instance.getTarget().getID() for instance in is_instance_of]


def get_coordinates(data_item):
    coordinates = data_item.coordinates(primary_only=True)
    if not coordinates:
        coordinates = data_item.coordinates()
        if coordinates:
            coordinates = coordinates[0]
        else:
            return None
    return coordinates


def get_entity(wiki_entities):
    city = {"Q515", "Q1549591", "Q5119"}
    museum = {"Q33506", "Q3329412", "Q684740", "Q207694"}
    entities = []
    for wiki_entity in wiki_entities:
        if wiki_entity in city:
            entities.append("city")
        elif wiki_entity in museum:
            entities.append("museum")
    # do simple majority vote for really weird edge cases
    return Counter(entities).most_common(1)[0][0]


def get_painting():
    parsed = wtp.parse(
        "{{sort|{{nts|1592}}|c. [[1592 in art|1592–1593]]}}:<br>''[[Boy Peeling a Fruit|Boy Peeling Fruit]]''"
    )
    page = pywikibot.Page(site, f"{parsed.wikilinks[1].text}")
    painting = page.data_item()
    paintint_claims = painting.claims
    interesting_properties = {
        "height": "P2048",
        "width": "P2049",
        "location_of_creation": "P1071",
        "depicts": "P180",
        "materials": "P186",
        "genre": "P136",
        "year": "P571",
    }
    actual_data = {}
    for k, v in interesting_properties.items():
        actual_data.update({k: paintint_claims.get(v)})


def retrieve_links(cell):
    parsed_cell = wtp.parse(cell)
    for link in parsed_cell.wikilinks:
        page = pywikibot.Page(site, f"{link.title}")
        if page.exists():
            data_item = page.data_item()
            coordinates = get_coordinates(data_item)
            what_it_is_it = get_instances_for_link(f"{link.title}")
            custom_entity = get_entity(what_it_is_it)
            yield {
                link.target: {
                    "cooridinates": coordinates,
                    "wiki_entity": what_it_is_it,
                    "entity": custom_entity,
                }
            }


def fix_the_dimensions(dimensions):
    dims = []
    for x in dimensions:
        val, entity_type = x
        if entity_type == "QUANTITY":
            splited = val.split()
            for v in splited:
                v = "".join([y for y in v if y.isnumeric() or y == "."])
                dims.append(v)
    return tuple([x for x in dims if x])


def try_to_understand_the_columns(df):
    columns_index = {
        "painting": ("name", "title"),
        "location": ("city", "gallery", "country"),
        "link_to_image": ("image", "painting"),
        "technique": ("technique",),
        "year": ("year",),
        "dimensions": ("dimensions",),
    }
    df_columns = [x.lower() for x in df.columns]
    entities_with_indexes = {x: -1 for x in columns_index.keys()}
    for i, column in enumerate(df_columns):
        for e, values in columns_index.items():
            for value in values:
                if value in column:
                    entities_with_indexes.update({e: i})
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
    # parsed_df_with_links = parsed_df.assign(painting_link=lambda x: x.Painting.apply(lambda y: images_with_links.get(y)))
    return parsed_df  # _with_links


if __name__ == "__main__":
    carravagio_listing_page = "List of paintings by Caravaggio"
    durer_listing_page = "List_of_paintings_by_Albrecht_D%C3%BCrer"
    raphael_listing_page = "List_of_paintings_by_Raphael"
    listings = [carravagio_listing_page, durer_listing_page, raphael_listing_page]
    for listing in listings:
        df = try_to_parse_the_data(listing)
        # print(df.head())
        print(df.info())
