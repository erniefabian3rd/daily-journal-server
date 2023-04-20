import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_entries, get_single_entry, get_entries_by_search, delete_entry, create_journal_entries
from views import get_all_moods, get_single_mood

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server"""
        response = {}
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_entry(id)
                else:
                    self._set_headers(200)
                    response = get_all_entries()
            elif resource == "moods":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_mood(id)
                else:
                    self._set_headers(200)
                    response = get_all_moods()
        
        else:
            (resource, query) = parsed
            if query.get('q') and resource == 'entries':
                self._set_headers(200)
                response = get_entries_by_search(query['q'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        new_entry = None

        if resource == "entries":
            new_entry = create_journal_entries(post_body)
            self.wfile.write(json.dumps(new_entry).encode())

    # def do_PUT(self):
    #     """Handles PUT requests to the server"""
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     post_body = json.loads(post_body)

    #     (resource, id) = self.parse_url(self.path)

    #     success = False
    #     if resource == "animals":
    #         success = update_animal(id, post_body)

    #     if resource == "locations":
    #         update_location(id, post_body)

    #     if resource == "employees":
    #         update_employee(id, post_body)

    #     if resource == "customers":
    #         update_customer(id, post_body)

    #     if success:
    #         self._set_headers(204)
    #     else:
    #         self._set_headers(404)

    #     self.wfile.write("".encode())


    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        """Handles DELETE requests to the server"""
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
