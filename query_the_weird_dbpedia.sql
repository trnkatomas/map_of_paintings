SELECT # (COUNT(*) AS ?count)
 ?painting , ?paintingName, ?artist, ?museum, ?long, ?lat, ?width, ?height, ?year_created, ?medium, ?depiction, ?comment
 {
     ?painting a dbo:Artwork;
                rdfs:label ?paintingName;          
                dbo:museum ?museum.
   OPTIONAL {
        ?painting dbo:author ?artist
   }
   OPTIONAL {
        ?painting dbp:author ?artist
   }
    OPTIONAL {
     ?museum rdfs:label ?museum_label;
                         geo:long ?long; 
                         geo:lat ?lat;
                         a dbo:Museum
   }
     ?artist rdfs:label "Tintoretto"@en 
     OPTIONAL {
        ?painting rdfs:comment ?comment
     }
   OPTIONAL {
        ?painting dbp:year ?year_created;
                  dbp:medium ?medium
   }
   OPTIONAL {
         ?painting  dbp:heightMetric ?height;
                    dbp:widthMetric ?width
    }
    OPTIONAL {
         ?painting  dbp:lengthMetric ?height;
                    dbp:widthMetric ?width
    }
    OPTIONAL {
         ?museum geo:long ?long;
                             geo:lat ?lat
     }
     OPTIONAL {
         ?museum georss:point ?lat;
                             georss:point ?long
     }
     OPTIONAL {
         ?painting foaf:depiction ?depiction
     }
    FILTER 
       ( LANG ( ?paintingName ) = 'en' AND
         LANG ( ?comment ) = 'en' AND
         LANG ( ?museum_label ) = 'en' )
}      
