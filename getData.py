from Bio import Entrez,Medline
import json

def getPapers(myQuery, maxPapers, myEmail ="conrad_heinrich.carl@mailbox.tu-dresden.de"):
    # Get articles from PubMed
    Entrez.email =myEmail
    record =Entrez.read(Entrez.esearch(db="pubmed", term=myQuery, retmax=maxPapers))
    idlist =record["IdList"]
    print("\nThere are %d records for %s."%(len(idlist), myQuery.strip()))
    records =Medline.parse(Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
    retmode="text"))
    # records is iterable, which means that it can be consumed only once.
    # Converting it to a list, makes it permanently accessible.
    return list(records)


def main():
    myQuery = "Nature" #query in title and abstract
    maxPapers =100 #limit the number of papers retrieved
    records =getPapers(myQuery, maxPapers)
    data = []

    for record in records:
        if not "AD" in record or not "PMID" in record:
            continue
        d = {
            "PMID": record['PMID'],
            "AD": record['AD']
        }
        data.append(d)

    # save records to file
    json.dump(data, open("myPapers.json", "w"))

if __name__ == "__main__":
    main()


