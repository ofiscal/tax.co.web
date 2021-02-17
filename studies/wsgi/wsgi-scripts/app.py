# This is "the WSGI application script file."

# The name "application" cannot be changed without
# configuring mod_wsgi for that.
def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
