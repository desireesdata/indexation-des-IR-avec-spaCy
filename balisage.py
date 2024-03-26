import xml.etree.ElementTree as et
import spacy
from spacy import displacy

nlp = spacy.load("fr_core_news_sm")
tree = et.parse("ir_test.xml")
root = tree.getroot()

def get_element_content(element):
    content = ''    
    for child in element:
        content += '<' + child.tag + '>'
        # content += '<persname>'
        content += get_element_content(child)
        # content += '</persname>'
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
                print("ne rien faire")
        content += element.text
    else :
        content+=''
    # content += element.text if element.text else ''
    return content

full_content = get_element_content(root)
print(full_content)