import os
import json


class KbItem(object):
    EMPTY_STR_VALUE = 'empty'

    def __init__(self, kbid: str = EMPTY_STR_VALUE, hrid: str = EMPTY_STR_VALUE,
                 descriptions=None, labels=None, ids=None,
                 stdforms=None, rankings=None, item_type: str = EMPTY_STR_VALUE):
        self.kbid = kbid
        self.hrid = hrid

        self.descriptions = {} if descriptions is None else descriptions

        self.ids = {
                'freebase': KbItem.EMPTY_STR_VALUE,
                'wikidata': KbItem.EMPTY_STR_VALUE
            }
        if ids is not None:
            self.ids.update(ids)

        self.labels = {
                'cs': {},
                'en': {}
            }
        if labels is not None:
            self.labels.update(labels)

        self.stdforms = {
                'cs': self.EMPTY_STR_VALUE,
                'en': self.EMPTY_STR_VALUE
            }
        if stdforms is not None:
            self.stdforms.update(stdforms)

        self.rankings = rankings
        if rankings is None:
            self.rankings = {
                "wikilinks": -1
            }
        self.type = item_type

    def infer_hrid(self):
        if self.kbid == self.EMPTY_STR_VALUE or self.stdforms['en'] == self.EMPTY_STR_VALUE:
            raise RuntimeError(f'Cannot infer hrid because either kbid or english stdform is not set.'
                               f'kbid={self.kbid}')

        self.hrid = f'{self.stdforms["en"]} ({self.kbid})'

    def to_json(self):
        return self.__dict__

    def save(self, directory, ensure_ascii=True, ensure_hrid=True):
        if self.kbid == KbItem.EMPTY_STR_VALUE:
            raise RuntimeError(f'Field "kbid" is not initialized. This must be done before saving.')
        output_path = os.path.join(directory, f'{self.kbid}.json')

        if ensure_hrid and self.hrid == self.EMPTY_STR_VALUE:
            self.infer_hrid()

        with open(output_path, 'w', encoding='utf8') as f:
            json.dump(self.to_json(), f, indent=4, ensure_ascii=ensure_ascii)


if __name__ == '__main__':

    item = KbItem()
    with open('kbitem_test.json', 'w') as f:
        json.dump(item.to_json(), f, indent=4)
