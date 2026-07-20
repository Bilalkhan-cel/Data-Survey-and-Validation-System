import xml.etree.ElementTree as et

coloums = []


def extract_columns(path):
    try:
        mytree = et.parse(path)
        myroot = mytree.getroot()
        for x in myroot.findall("Section"):
            for y in x.findall("Question"):
                coloums.append(y.get("id"))
        return coloums
    except Exception as e:
        return f"Coloums Extraction Failed   Error={e}  Kindly check your XML format"


def extract_images(path):
    img = {}
    try:
        mytree = et.parse(path)
        myroot = mytree.getroot()
        for x in myroot.findall("Section"):
            for y in x.findall("Question"):
                for z in y.findall("image"):

                    img[y.get("id")] = {
                        "src": z.attrib["src"],
                        "width": z.attrib.get("width"),
                        "height": z.attrib.get("height"),
                    }

        return img
    except Exception as e:
        return f"Coloums Extraction Failed   Error={e}  Kindly check your XML format"


def extract_questions_ans_value(path):
    try:
        mytree = et.parse(path)
        myroot = mytree.getroot()

        questions = {}

        for section in myroot.findall("Section"):

            options = []

            # Section-level options
            for z in section.findall("Options"):
                for w in z.findall("Option"):
                    options.append({w.get("value"): w.text})

            for question in section.findall("Question"):

                text = question.findtext("Text")

                # Check if this question has its own Options
                question_options = question.find("Options")

                if question_options is not None:
                    q_options = []
                    for w in question_options.findall("Option"):
                        q_options.append({w.get("value"): w.text})
                    questions[text] = q_options
                else:
                    questions[text] = options.copy()

        return questions

    except Exception as e:
        return f"Questions Extraction Failed. Error = {e}"


# imges = extract_images("data.xml")
# print(imges)
