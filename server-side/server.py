from http.server import SimpleHTTPRequestHandler, HTTPServer
# from fetch import query
from urllib.parse import urlparse, parse_qs

class HTTPHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        params = parse_qs(urlparse(self.path).query)
        # params = {'lat' : [1,2], 'lng': [3,4]}
        print(params, self.path)
        try:
            res = 4 #query(float(params['lat'][0]), float(params['lng'][0]))
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(res), "utf8"))
        except (ValueError, KeyError) as e:
            self.send_response(400)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("Bad request params", "utf8"))
        return

def run():
  print('starting server...')
  server_address = ('', 8081)
  httpd = HTTPServer(server_address, HTTPHandler)
  httpd.serve_forever()

run()


# from http.server import SimpleHTTPRequestHandler, HTTPServer
# # from fetch import query
# from urllib.parse import urlparse, parse_qs

# class HTTPHandler(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         print(self.path)
#         print(urlparse(self.path))
#         try:
#             self.send_response(200)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#         except:
#             self.send_response(400)
#             self.send_header('Content-type','text/html')
#             self.end_headers()
#         return
#         # params = parse_qs(urlparse(self.path).query)
#         # print(params, self.path)

#         # try:
#         #     res = query(float(params['img'][0]))
#         #     self.send_response(200)
#         #     self.send_header('Content-type', 'text/html')
#         #     self.end_headers()
#         #     self.wfile.write(bytes(str(res), "utf8"))
#         # except:
#         #     self.send_response(400)
#         #     self.send_header('Content-type', 'text/html')
#         #     self.end_headers()
#         #     self.wfile.write(bytes("Bad request params", "utf8"))
#         # return

# def main():
#     server_address = ('0.0.0.0', 8081)
#     print('Serving HTTP on ', server_address, ' ...')
#     httpd = HTTPServer(server_address, HTTPHandler)
#     httpd.serve_forever()

# if __name__ == "__main__":
#     main()