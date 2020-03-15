from lxml import etree
from io import StringIO
import sys

filename_xml = sys.argv[1]
#filename_xsd = sys.argv[2]
filename_xsd = './Jefferson/schema/gdml.xsd'

print(filename_xml)
xml_file = etree.parse(filename_xml)
xml_validator = etree.XMLSchema(file=filename_xsd)

is_valid = xml_validator.validate(xml_file)
print(is_valid)

xml_validator.assertValid(xml_file)

print ('domain_name: ' + error.domain_name)
print ('domain: ' + str(error.domain))
print ('filename: ' + error.filename)
print ('level: ' + str(error.level))
print ('level_name: ' + error.level_name)
print ('line: ' + str(error.line))
print ('message: ' + error.message)
print ('type: ' + str(error.type))
print ('type_name: ' + error.type_name)
