import os
import http.server as server
from user_backend import *

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""

    def do_OPTIONS(self):
        # self.send_response(200, "ok")
        with open("metadata.json", "r") as f:
            self.wfile.write(f.read().encode('utf-8'))
        # self.send_header('Access-Control-Allow-Origin', '*')
        # self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        # self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # self.end_headers()

    def do_POST(self):
        """Save a file following a HTTP PUT request"""
        # self.send_response(200, "ok")
        # with open("metadata.json", "r") as f:
        #     self.wfile.write(f.read().encode('utf-8'))
        # self.send_header('Access-Control-Allow-Origin', "*")
        # self.end_headers()
        # self.send_response(200, "ok")

        filename = os.path.basename(self.path)
        print(filename + "hey")
        if "update" in filename:
            print(2)
            with open("metadata.json", "r") as f:
                data = f.read()
                self.wfile.write(data.encode('utf-8'))
        elif "-" in filename and "search" in filename.split("-")[0]:
            print(1)
            print(filename.split("-")[1].split(".")[0])
            return_sjon = str(search(filename.split("-")[1].split(".")[0], get_data_from_file()))
            self.wfile.write(return_sjon.replace("'", '"').encode('utf-8'))
        else:
            print(3)
            file_length = int(self.headers['Content-Length'])
            with open(filename, 'wb') as output_file:
                output_file.write(self.rfile.read(file_length))
            add_doc(filename, global_vars.TALPIOT_DRIVE_ID)

if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)