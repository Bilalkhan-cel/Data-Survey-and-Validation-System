import xml.etree.ElementTree as et
mylist=[]
myquestion=[]
myans=[]
mytree=et.parse("data.xml")
myroot=mytree.getroot()
for x in myroot.findall("Section"):
    
    for z in x.findall("Options"):
        for w in z.findall("Option"):
            myans.append(w.get("value"))
    
    
    for y in x.findall("Question"):
        mylist.append(y.get("id"))
        myquestion.append(y.findtext("Text"))
        
        
        
# print(mylist)
# print(myquestion)
print(myans)



# define a function that retunr the dictionay contains all the question and theri likert ans and and their section same and id name