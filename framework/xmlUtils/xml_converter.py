import json
import xmltodict

class XMLConverter:

    @staticmethod
    def from_xml_to_dict(data, condit = None):
        if condit:
            return eval(str(json.dumps(dict(xmltodict.parse(data)))).replace(*condit))
        else: return xmltodict.parse(data)

    def is_xml(data):
        try: 
            xmltodict.parse(data) 
            return True
        except: return False