import xml.etree.ElementTree as et
mylist=[]
myquestion=[]
mytree=et.parse("data.xml")
myroot=mytree.getroot()
for x in myroot.findall("Section"):
    
    for y in x.findall("Question"):
        mylist.append(y.get("id"))
        myquestion.append(y.findtext("Text"))
        
        
        
print(len(mylist))
print(len(myquestion))

