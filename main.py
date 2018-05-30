#!/usr/bin/python

import SimpleHTTPServer, SocketServer, logging, subprocess, sys, os, re, mimetypes
import argparse as argparse

# Stop traceback on ctrl-c
sys.tracebacklimit = 0

parser = argparse.ArgumentParser()

parser.add_argument("-p", nargs='?', default=6969)
parser.add_argument("-d", nargs='?', default=None)

args = parser.parse_args()

PORT = int(args.p)

serve_listing = "serve"
serve_files = []

for root, dirs, files in os.walk(serve_listing):
    for f in files:
        serve_files.append(os.path.join(root, f).replace("serve/", ""))
print ("Files to serve:")
for f in serve_files:
    print f

ANSI_COLOR_RED      = "\x1b[31m"
ANSI_COLOR_GREEN    = "\x1b[32m"
ANSI_COLOR_YELLOW   = "\x1b[33m"
ANSI_COLOR_BLUE     = "\x1b[34m"
ANSI_COLOR_MAGENTA  = "\x1b[35m"
ANSI_COLOR_CYAN     = "\x1b[36m"
ANSI_COLOR_RESET    = "\x1b[0m"

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_HEAD(self):
        self.server_version = "nginx"
        self.sys_version = ""

        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_GET(self):
        # Suppress information leakage & Deal with CORS

        self.server_version = "nginx"
        self.sys_version = ""

        rows, columns = subprocess.check_output(['stty', 'size']).split()

        print ("="*int(columns))
        print ("> %sRequested GET path: %s%s" % (ANSI_COLOR_MAGENTA, self.path, ANSI_COLOR_RESET))
        for h in self.headers:
            print ("> %s%s%s: %s" % (ANSI_COLOR_GREEN, h, ANSI_COLOR_RESET, self.headers[h]))

        path = self.path[1:]
        path = re.sub("\?(.|\n)*", "", path)

        if path in serve_files:
            fp = "serve/%s" % path
            d = open(fp).read()
            t = mimetypes.guess_type(fp)[0] if not mimetypes.guess_type(fp)[0] == None else "text/plain"

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", t)
            self.send_header("Content-length", len(d))
            self.end_headers()
            self.wfile.write(d)

            return

        if args.d != None:
            fp = "serve/%s" % args.d
            d = open(fp).read()
            t = mimetypes.guess_type(fp)[0] if not mimetypes.guess_type(fp)[0] == None else "text/plain"

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", t)
            self.send_header("Content-length", len(d))
            self.end_headers()
            self.wfile.write(d)

            return

        self.send_response(404)
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_POST(self):
        # Suppress information leakage & Deal with CORS

        self.server_version = "nginx"
        self.sys_version = ""

        rows, columns = subprocess.check_output(['stty', 'size']).split()

        print ("="*int(columns))
        print ("> %sRequested POST path: %s%s" % (ANSI_COLOR_MAGENTA, self.path, ANSI_COLOR_RESET))
        for h in self.headers:
            print ("> %s%s%s: %s" % (ANSI_COLOR_BLUE, h, ANSI_COLOR_RESET, self.headers[h]))

        data = self.rfile.read(int(self.headers['Content-Length']))

        print (data)

        self.send_response(200)



Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()
