import pandas as pd
from app.model import db, Tissue, Synonym

df = pd.read_csv("data/UBERON.csv")
df = df[df.Obsolete == False]
df.Definitions[df.Definitions.isna()] = ''
df.Synonyms[df.Synonyms.isna()] = ''

for i in df.index:
    entry = df.loc[i]
    class_id = entry["Class ID"]
    label = entry["Preferred Label"]
    synonyms = entry["Synonyms"].split("|")
    definitions = entry["Definitions"]
    try:
        tissue = Tissue(class_id, label, definitions)
        db.session.add(tissue)
        for syn in synonyms:
            synonym = Synonym(tissue.uuid, syn)
            db.session.add(synonym)
        db.session.commit()
    except Exception as e:
        print ("Error inserting tissue")
        print(e)
        #Rollback if there are errors
        db.session.rollback()
