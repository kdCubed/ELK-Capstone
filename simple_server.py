from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import re

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def sanitize_filename(self, filename):
        """
        Remove or replace characters in the filename to prevent directory traversal or other injection attacks.
        """
        # Remove path separators to prevent directory traversal attacks
        filename = filename.replace('/', '').replace('\\', '')
        # Remove or replace other potentially dangerous characters
        filename = re.sub(r'[<>:"|?*]', '', filename)
        # Optional: Limit the filename to a whitelist of known safe characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        return filename

    def do_GET(self):
        # HTML form for file upload
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <head><title>Upload File</title></head>
        <body>
            <form enctype="multipart/form-data" method="post">
                <input name="file" type="file"/>
                <input type="submit" value="Upload"/>
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        # Get the uploaded file
        file_field = form['file']
        if file_field.filename:
            # Ensure the directory exists
            upload_dir = '/usr/share/logstash/data/uploads/'
            os.makedirs(upload_dir, exist_ok=True)

            # Sanitize the filename
            safe_filename = self.sanitize_filename(file_field.filename)

            # It's an uploaded file; save it in a predetermined directory
            file_path = os.path.join(upload_dir, safe_filename)
            with open(file_path, 'wb') as output_file:
                output_file.write(file_field.file.read())
            message = f"File '{safe_filename}' uploaded successfully."
        else:
            message = "No file was uploaded."

        # Respond with an acknowledgment page
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"<html><body><h1>{message}</h1></body></html>".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

