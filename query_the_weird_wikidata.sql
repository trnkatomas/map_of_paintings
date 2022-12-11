#All paintings for one particular artist with their location
SELECT DISTINCT ?item ?itemLabel ?author ?locationLabel ?coordinates ?image ?height ?width ?materials ?depicts ?genre ?year_inception ?itemDescription  ?sitelinks
WHERE {
    ?item wdt:P31 wd:Q3305213;            # Any instance of a image
          wdt:P276 ?location;             # with a specific location, eg. MOMA wd:Q160236
          wdt:P18 ?image;
          wdt:P170 wd:Q;             # can be a specific author, eg. Edgar Degas Q46373
          wikibase:sitelinks ?sitelinks.
    OPTIONAL { ?location wdt:P31 wd:Q207694 } # art museum
    OPTIONAL { ?location wdt:P31 wd:Q33506 } # museum 
    OPTIONAL { ?location wdt:P31 wd:Q3329412 } # archeological museum 
    OPTIONAL { ?location wdt:P31 wd:Q684740 } # real property     
    OPTIONAL { ?location wdt:P31 wd:Q515 } # city 
    OPTIONAL { ?location wdt:P31 wd:Q5119 } # capital city
    OPTIONAL { ?location wdt:P31 wd:Q1549591 } # big city
    ?location wdt:P625 ?coordinates.
    OPTIONAL {
      ?item wdt:P2048 ?height;
            wdt:P2049 ?width;
    }
    OPTIONAL { ?item wdt:P1071 ?location_of_creation.}
    OPTIONAL { ?item wdt:P180  ?depicts.}
    OPTIONAL { ?item wdt:P186 ?materials.}
    OPTIONAL { ?item wdt:P136 ?genre.}
    OPTIONAL { ?item wdt:P571 ?year_inception. } 
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
ORDER BY DESC(?sitelinks)