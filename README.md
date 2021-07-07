# Transformace Wikidata -> Knowledgebase

Účelem tohoto projektu je transformovat data z 
RDF databáze Wikidata do standardizovaných souborů ve formátu
`json`. Projekt je rozdělen do 3 souborů.

`KbItem.py` implementuje třídu reprezentující jeden item
z Knowledge base. Účelem je držet data pohromadě, plus zapouzdřené
ukládání. Deserializace není implementovaná, jelikož ji zadání nezmiňuje.

`main.py` obsahuje hlavní smyčku přes ID ze souboru `wikidata_ids.txt` a 
postupně vyplňuje jednu instanci KbItem.

`queries.py` obsahuje vlastní práci s RDF databází. Používám
čistě python api nabízené knihovnou `rdflib`, tedy ne SPARQL. 
Kód jsem se ovšem snažil strukturovat tak, aby eventuální přechod
na SPARQL nebyl moc složitý - mělo by stačit změnit těla funkcí
v tomto souboru.
