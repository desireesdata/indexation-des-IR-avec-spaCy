

# Indexation des IR avec spaCy

Projet pour l'automatisation des instruments de recherche avec Python et sa librairie *spaCy*. Il s'agit d'effectuer, sur un fichier XML/EAD, certaines tâches répétitives propres à l'indexation : 1) détecter les noms propres au sein d'un texte; 2) entourer les entités détectées avec les balises adéquates.

Je présenterai d'abord ici le cahier des charges et l'état actuel du projet; et les tâches à réaliser pour perfectionner l'automatisation de l'indexation.

## 1. Cahier des charges

L'archiviste qui rédige un instrument de recherche en XML prend soin de respecter les normes internationales (notamment ISAD-G) via la grammaire EAD. Il doit donc rendre compte de l'arborescence documentaire d'un fonds d'archives en conformité avec les standards internationaux. Ainsi, les balises qui vont être utilisées seront `<geogname>` s'il s'agit d'un lieu géographique; `<persname>` s'il s'agit d'un nom; et `<corpname>` s'il s'agit d'une institution publique, ou d'un organisme privé. S'il existe d'autres balises de structurations de données dans le dictionnaire EAD permettant une indexation plus fine, ces trois catégories de métadonnées seront dans un premier temps suffisantes.

La reconnaissance des entités nommées reposera sur l'analyse de l'ensemble du contenu XML avec Python et la librairie SpaCy. Dans un premier temps, sera utilisé la pipeline pré-entraînée de spaCy "`fr_core_news_sm`". Cela implique de faire des tests sur des instruments de recherche fictifs, composés d'entités nommées importantes (ex: les présidents de la République; les grandes villes de France; les institutions historiques comme le Louvre).

La modification du fichier XML de façon complète ou partielle (par exemple à l'intérieur du bloc `<bioghist>`) doit être réversible; on peut effectuer des opérations sur les branches de l'arborescence de l'instrument de recherche et sur ses éléments selon une logique récursive.

## 2. Tests sur des chaînes de caractères puis sur un fichier XML

Avec un programme rudimentaire, j'ai d'abord testé une esquisse de solution pour analyser et modifier du texte simulant du XML. Après avoir importé spaCy et initialisé les variables, on va effectuer des opérations sur une simple chaîne de caractère (ci-dessous `text_xml`):

```python
# [...] On a importé spaCy et déclaré la variable text_xml
doc = nlp(text_xml)
for ent in doc.ents:
    if ent.label_ == "PER":
        text_xml = text_xml.replace(ent.text, "<persname>%s</persname>" % (ent.text))
    elif ent.label_ == "LOC":
        text_xml = text_xml.replace(ent.text, "<geogname>%s</geogname>" % (ent.text))
    elif ent.label_ == "ORG":
        text_xml = text_xml.replace(ent.text, "<corpname>%s</corpname>" % (ent.text))
```

Ensuite, avec la librairie `etree`, j'ai effectué ces modifications sur un véritable fichier XML parsé, dans une fonction récursive (extrait du programme):

```python
def get_element_content(element):
    content = ''    
    for child in element:
        content += '<' + child.tag + '>'
        content += get_element_content(child)
        content += '</' + child.tag + '>'
    if element.text:
        doc = nlp(element.text)
        for ent in doc.ents:
            if ent.label_ == "PER":
                element.text = element.text.replace(ent.text, "<persname>%s</persname>" % (ent.text))
            elif ent.label_ == "LOC":
                element.text = element.text.replace(ent.text, "<geogname>%s</geognamename>" % (ent.text))
            elif ent.label_ == "ORG":
                element.text = element.text.replace(ent.text, "<corpname>%s</corpname>" % (ent.text))
            else :
                print("vide")
        content += element.text
    else :
        content+=''
    return content

full_content = get_element_content(root)
```

De cette manière, j'ai pu copier le contenu d'un document XML, le modifier et réaliser un export d'un instrument de recherche indexé grâce au balisage automatique des entités nommées.

## 3. Aller plus loin

A ce stade, il est donc possible de produire des instruments de recherche dont l'indexation a été automatisée avec spaCy. Cependant, l'analyse des données est loin d'être satisfaisante car on utilise un modèle pré-entraîné qui ne reconnaît pas, par exemple, les institutions publiques françaises et ses représentants.

Pour entraîner le modèle, j'envisage d'utiliser les jeux de données disponibles de data.gouv.fr. Par exemple, dans un projet d'indexation des instruments de recherche de fonds de la série O des Archives Départementales ou des sous-séries F des Archives Nationales, on pourra utiliser le `.csv` des dossiers des préfets et préfètes depuis 1800.

Les données de data.gouv.fr comprennent la colonne `wikidata`; cela permettant d'ajouter au XML des fiches d'autorité :

```xml
<persname normal="Poubelle, Eugène" source="wikidata" authfilenumber="https://www.wikidata.org/wiki/Q166668">Eugène Poubelle</persname>
```
