from app.models import db, Geneset
try:
    gs = Geneset("STAT3 STAT1")
    db.session.add(gs)
    db.session.commit()
except Exception as e:
    print ("Error inserting gs")
    #Rollback if there are errors
    db.session.rollback()

# Will produce an error, why?
try:
    gs = Geneset("STAT1 STAT3")
    db.session.add(gs)
    db.session.commit()
except Exception as e:
    print ("Error inserting gs1")
    #Rollback if there are errors
    db.session.rollback()

# View db contents
genesets = Geneset.query.all()
print(genesets)