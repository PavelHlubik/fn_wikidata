from typing import List

import rdflib


w3_rdf_scheme_namespace = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')
schema_namespace = rdflib.Namespace('http://schema.org/')
entity_namespace = rdflib.Namespace('http://www.wikidata.org/entity/')

w3_skos_core_nmsp = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')
freebase_uri = rdflib.URIRef('http://www.wikidata.org/prop/direct/P646')


def get_descriptions(rdf_graph: rdflib.Graph, wiki_id: str, languages: List[str]):
    subject = rdflib.URIRef(entity_namespace + wiki_id)
    descriptions = {}
    for s, p, o in rdf_graph.triples((subject, schema_namespace.description, None)):
        if o.language in languages:
            descriptions[o.language] = o

    return descriptions


def get_stdforms(rdf_graph: rdflib.Graph, wiki_id: str, languages: List[str]):
    subject = rdflib.URIRef(entity_namespace + wiki_id)
    stdforms = {}
    for s, p, o in rdf_graph.triples((subject, w3_rdf_scheme_namespace.label, None)):
        if o.language in languages:
            stdforms[o.language] = o

    return stdforms


def get_labels(rdf_graph: rdflib.Graph, wiki_id: str, languages: List[str]):
    subject = rdflib.URIRef(entity_namespace + wiki_id)

    # Second query for altLabel always returns empty result
    tuples = list(rdf_graph.triples((subject, schema_namespace.alternateName, None))) + \
        list(rdf_graph.triples((subject, w3_skos_core_nmsp.altLabel, None))) + \
        list(rdf_graph.triples((subject, w3_rdf_scheme_namespace.label, None)))

    labels = {}
    for s, p, o in tuples:
        if o.language in languages:
            if o.language not in labels:
                labels[o.language] = {}
            labels[o.language][o] = {'text': o}
            if len(o.split()) <= 1:
                labels[o.language][o]['stability'] = -10

    return labels


def get_freebase_id(rdf_graph: rdflib.Graph, wiki_id: str):
    subject = rdflib.URIRef(entity_namespace + wiki_id)
    freebase_id = ''
    for i, (s, p, o) in enumerate(rdf_graph.triples((subject, freebase_uri, None))):
        if i > 0:
            raise RuntimeError(f'Found more than one freebase ids in given database. Item id: "{wiki_id}",'
                               f'freebase ids: {[freebase_id, o]}.')
        freebase_id = o
    return freebase_id



