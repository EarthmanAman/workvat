from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import xml.etree.ElementTree as ET

# create the file structure
data = ET.Element('xml')
numbers = ET.SubElement(data, 'numbers')
sumIn = ET.SubElement(data, 'addition')
sumIn1 = sumIn = ET.SubElement(sumIn, 'sum')
number1 = ET.SubElement(numbers, 'num')
number2 = ET.SubElement(numbers, 'num')
number1.set('name','number1')
number2.set('name','number2')
sumIn1.set('name','sum')

print("Listening at port :8080")
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        # self.send_header('Content-Disposition', 'attachment; filename="Hadoop.pdf"')
        self.end_headers()
        gets = self.path
        first = re.findall('/?first=([0-9]+)', gets)
        second = re.findall('&second=([0-9]+)', gets)
        number1.text = first[0]
        number2.text = second[0]
        sumIn1.text = str(int(first[0]) + int(second[0]))
        mydata = ET.tostring(data)
        with open("addition.xml", "wb") as myfile:
        	myfile.write(mydata)
        with open('addition.xml', 'r') as file: 
        	self.wfile.write(file.read().encode('utf-8')) # Read the file and send the contents 


myServer = HTTPServer(('localhost', 8080), MyServer)
myServer.serve_forever()
myServer.server_close()