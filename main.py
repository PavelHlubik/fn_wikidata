import rdflib
from KbItem import KbItem
import queries

LANGUAGES = ['en', 'cs']
WIKIDATA_IDS_FILE = 'wikidata_ids.txt'
WIKIDATA_DATA_FILE = '100_items_wikidata_subset.nt'


def build_kb_id(wiki_id):
    return f'KB-{wiki_id[1:]}-W'


if __name__ == '__main__':
    rdf_graph = rdflib.Graph()
    rdf_graph.parse(WIKIDATA_DATA_FILE, format="nt")

    with open(WIKIDATA_IDS_FILE, 'r') as f:
        # Read all lines and strip them from newlines
        wiki_ids = map(lambda x: x.strip(), f.readlines())

    for i, wiki_id in enumerate(wiki_ids):
        item = KbItem(kbid=build_kb_id(wiki_id), ids={'wikidata': wiki_id})

        descriptions = queries.get_descriptions(rdf_graph=rdf_graph, wiki_id=wiki_id, languages=LANGUAGES)
        item.descriptions.update(descriptions)

        stdforms = queries.get_stdforms(rdf_graph=rdf_graph, wiki_id=wiki_id, languages=LANGUAGES)
        item.stdforms.update(stdforms)

        labels = queries.get_labels(rdf_graph=rdf_graph, wiki_id=wiki_id, languages=LANGUAGES)
        item.labels.update(labels)

        item.ids['freebase'] = queries.get_freebase_id(rdf_graph=rdf_graph, wiki_id=wiki_id)

        item.save('output', ensure_ascii=False, ensure_hrid=True)
