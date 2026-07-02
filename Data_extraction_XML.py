import xml.etree.ElementTree as et
coloums=[]
questions=[]




def extract_columns(path):
    try:
        mytree=et.parse(path)
        myroot=mytree.getroot()
        for x in myroot.findall("Section"):
            for y in x.findall("Question"):
              coloums.append(y.get("id"))
        return coloums
    except Exception as e:
        return f"Coloums Extraction Failed   Error={e}  Kindly check your XML format"
    
    
def extract_questions(path):
    
    try:
        mytree=et.parse(path)
        myroot=mytree.getroot()
        for x in myroot.findall("Section"):
            for y in x.findall("Question"):
              questions.append(y.findtext("Text"))
        return questions
    except Exception as e:
        return f"Coloums Extraction Failed   Error={e}  Kindly check your XML format"
    
    

        
      

    
    
    
        
        
        


