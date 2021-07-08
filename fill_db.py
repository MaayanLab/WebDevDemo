## add pandas on requirements.txt
import sys
import pandas as pd
from app.model import db, Enrichment

## after running init_db.py, you can run this by
## python fill_db.py data/enriched_terms.tsv

filename = sys.argv[1]
df = pd.read_csv(filename, sep="\t", index_col=0)
df = df.loc[~df["Gene Sets"].isna()]

for i in df.index:
	signature_name = i
	shortId = df.at[i, 'shortId']
	userListId = str(df.at[i, 'userListId'])
	try:
		enrichment = Enrichment(signature_name, shortId, userListId)
		db.session.add(enrichment)
		# Commit changes
		db.session.commit()
	except Exception as e:
		print ("Error inserting Enrichment")
		print(e)
		#Rollback if there are errors
		db.session.rollback()