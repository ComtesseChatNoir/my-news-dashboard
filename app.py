File "/usr/local/lib/python3.14/http/client.py", line 971, in _get_hostport
    port = int(host[i+1:])
ValueError
During handling of the above exception, another exception occurred:
File "/mount/src/my-news-dashboard/app.py", line 48, in <module>
    feed = feedparser.parse(google_news_url)
File "/home/adminuser/venv/lib/python3.14/site-packages/feedparser/api.py", line 216, in parse
    data = _open_resource(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers, result)
File "/home/adminuser/venv/lib/python3.14/site-packages/feedparser/api.py", line 115, in _open_resource
    return http.get(url_file_stream_or_string, etag, modified, agent, referrer, handlers, request_headers, result)
           ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/feedparser/http.py", line 171, in get
    f = opener.open(request)
File "/usr/local/lib/python3.14/urllib/request.py", line 487, in open
    response = self._open(req, data)
File "/usr/local/lib/python3.14/urllib/request.py", line 504, in _open
    result = self._call_chain(self.handle_open, protocol, protocol +
                              '_open', req)
File "/usr/local/lib/python3.14/urllib/request.py", line 464, in _call_chain
    result = func(*args)
File "/usr/local/lib/python3.14/urllib/request.py", line 1381, in https_open
    return self.do_open(http.client.HTTPSConnection, req,
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        context=self._context)
                        ^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.14/urllib/request.py", line 1303, in do_open
    h = http_class(host, timeout=req.timeout, **http_conn_args)
File "/usr/local/lib/python3.14/http/client.py", line 1510, in __init__
    super(HTTPSConnection, self).__init__(host, port, timeout,
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
                                          source_address,
                                          ^^^^^^^^^^^^^^^
                                          blocksize=blocksize)
                                          ^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.14/http/client.py", line 921, in __init__
    (self.host, self.port) = self._get_hostport(host, port)
                             ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
File "/usr/local/lib/python3.14/http/client.py", line 976, in _get_hostport
    raise InvalidURL("nonnumeric port: '%s'" % host[i+1:])
