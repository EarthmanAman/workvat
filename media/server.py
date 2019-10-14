import socket
import re

HOST, PORT = '', 8888

import xml.etree.ElementTree as ET

# create the file structure
# data = ET.Element('data')
# items = ET.SubElement(data, 'items')
# item1 = ET.SubElement(items, 'item')
# item2 = ET.SubElement(items, 'item')
# item1.set('name','item1')
# item2.set('name','item2')
# item1.text = 'item1abc'
# item2.text = 'item2abc'
# mydata = ET.tostring(data)
# myfile = open("items2.xml", "w")
# myfile.write(mydata)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
# print(f'Serving HTTP on port {PORT} ...')
# with open('Hadoop.pdf', 'rb') as file: 
# 	self.wfile.write(file.read()) # Read the file and send the contents 
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    words = request_data.decode('utf-8').rsplit()
    # gets = words[1]
    # first = re.findall('/?first=([0-9]+)', gets)
    # second = re.findall('&second=([0-9]+)', gets)
    # third = re.findall('&third=([0-9]+)', gets)
    # try:
    # 	sumIn = int(first[0]) + int(second[0]) + int(third[0])
    # except:
    # 	sumIn = "Enter"
    mydata = "<xml><number><first name=\"number1\">4</first><second name=\"number2\">item2abc</second></number><addition><sum name=\"sumi\">5</sum></addition></xml>"
    http_response = f"""\
    Content-type: text/html
	HTTP/1.1 200 OK

	The sum of the numbers you entered is:


	{mydata}
	""".encode('utf-8')
    client_connection.sendall(http_response)
    client_connection.close()
