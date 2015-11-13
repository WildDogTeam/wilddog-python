# coding=utf-8
try:
    import urlparse
except ImportError:
    # py3k
    from urllib import parse as urlparse

import json

from wilddog_token_generator import create_token
from decorators import http_connection

from async import process_pool
from jsonutil import JSONEncoder

__all__ = ['WilddogAuthentication', 'WilddogApplication']


@http_connection(60)
def make_get_request(url, params, headers, connection):
    """
    向指定 wilddog 节点发送一个 GET 请求，超时时间60s。
    `url`: wilddog 节点的全路径。
    `params`: Python dict，作为查询参数附加到URL之后。
    `headers`: Python dict. HTTP 请求头信息。
    `connection`: 预置的连接对象，如未指定默认将由`decorators.http_connection`提供。
    函数的返回值是一个由 JSON 解析器反序列化而来的 Python dict。 不过，当请求的响应状态
    码不是2x或者403时，将会抛出requests.HTTPError
    connection = connection_pool.get_available_connection()
    response = make_get_request('http://wilddog.localhost/users', {'print': silent'},
                                {'X_WILDDOG_SOMETHING': 'Hi'}, connection)
    response => {'1': 'John Doe', '2': 'Jane Doe'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.get(url, params=params, headers=headers, timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()


@http_connection(60)
def make_put_request(url, data, params, headers, connection):
    """
    向指定 wilddog 节点发送一个 PUT 请求，超时时间60s。
    `url`: wilddog 节点的全路径。
    `data`: 可序列化为 JSON 的 dict，将会存储到远程服务器上。
    `params`: Python dict，作为查询参数附加到URL之后。
    `headers`: Python dict. HTTP 请求头信息。
    `connection`: 预置的连接对象，如未指定默认将由`decorators.http_connection`提供。
    函数的返回值是一个由 JSON 解析器反序列化而来的 Python dict。 不过，当请求的响应状态
    码不是2x或者403时，将会抛出requests.HTTPError
    connection = connection_pool.get_available_connection()
    response = make_put_request('http://wilddog.localhost/users',
                                '{"1": "Ozgur Vatansever"}',
                                {'X_WILDDOG_SOMETHING': 'Hi'}, connection)
    response => {'1': 'Ozgur Vatansever'} or {'error': 'Permission denied.'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.put(url, data=data, params=params, headers=headers,
                              timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()


@http_connection(60)
def make_post_request(url, data, params, headers, connection):
    """
    向指定 wilddog 节点发送一个 POST 请求，超时时间60s。
    `url`: wilddog 节点的全路径。
    `data`: 可序列化为 JSON 的 dict，将会存储到远程服务器上。
    `params`: Python dict，作为查询参数附加到URL之后。
    `headers`: Python dict. HTTP 请求头信息。
    `connection`:预置的连接对象，如未指定默认将由`decorators.http_connection`提供。
    函数的返回值是一个由 JSON 解析器反序列化而来的 Python dict。 不过，当请求的响应状态
    码不是2x或者403时，将会抛出requests.HTTPError
    connection = connection_pool.get_available_connection()
    response = make_put_request('http://wilddog.localhost/users/',
       '{"Ozgur Vatansever"}', {'X_WILDDOG_SOMETHING': 'Hi'}, connection)
    response => {u'name': u'-Inw6zol_2f5ThHwVcSe'} or {'error': 'Permission denied.'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.post(url, data=data, params=params, headers=headers,
                               timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()


@http_connection(60)
def make_patch_request(url, data, params, headers, connection):
    """
    向指定 wilddog 节点发送一个 PATCH 请求，超时时间60s。
    `url`: wilddog 节点的全路径。
    `data`: 可序列化为 JSON 的 dict，将会存储到远程服务器上。
    `params`: Python dict，作为查询参数附加到URL之后。
    `headers`: Python dict. HTTP 请求头信息。
    `connection`:预置的连接对象，如未指定默认将由`decorators.http_connection`提供。
    函数的返回值是一个由 JSON 解析器反序列化而来的 Python dict。 不过，当请求的响应状态
    码不是2x或者403时，将会抛出requests.HTTPError
    connection = connection_pool.get_available_connection()
    response = make_put_request('http://wilddog.localhost/users/1',
       '{"Ozgur Vatansever"}', {'X_WILDDOG_SOMETHING': 'Hi'}, connection)
    response => {'Ozgur Vatansever'} or {'error': 'Permission denied.'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.patch(url, data=data, params=params, headers=headers,
                                timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()


@http_connection(60)
def make_delete_request(url, params, headers, connection):
    """
    向指定 wilddog 节点发送一个 DELETE 请求，超时时间60s。
    `url`: wilddog 节点的全路径。
    `params`: Python dict，作为查询参数附加到URL之后。
    `headers`: Python dict. HTTP 请求头信息。
    `connection`:预置的连接对象，如未指定默认将由`decorators.http_connection`提供。
    函数的返回值是一个由 JSON 解析器反序列化而来的 Python dict。不过，当请求的响应状态
    码不是2x或者403时，将会抛出requests.HTTPError
    connection = connection_pool.get_available_connection()
    response = make_put_request('http://wilddog.localhost/users/1',
                                {'X_WILDDOG_SOMETHING': 'Hi'}, connection)
    response => NULL or {'error': 'Permission denied.'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.delete(url, params=params, headers=headers, timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()


class WilddogUser(object):
    """
    封装已验证用户鉴权信息的类，把它想作是一个保存鉴权相关信息的容器就行了
    """

    def __init__(self, email, wilddog_auth_token, provider, id=None):
        self.email = email
        self.wilddog_auth_token = wilddog_auth_token
        self.provider = provider
        self.id = id


class WilddogAuthentication(object):
    """
    封装了 Wilddog SimpleLogin 机制的类。事实上这个类并没有触发任何连接，只是简
    单的模拟了鉴权操作。另外，属性中的 email 和 password 是完全没什么用处的，它
    们永远不会出现在服务端的``auth``变量中
    """

    def __init__(self, secret, email, debug=False, admin=False, extra=None):
        self.secret = secret
        self.debug = debug
        self.admin = admin
        self.email = email
        self.provider = 'password'
        self.extra = (extra or {}).copy()
        self.extra.update({'debug': debug, 'admin': admin,
                           'email': self.email, 'provider': self.provider})

    def get_user(self):
        """
        获取已验证用户信息的方法。返回的用户信息中包含token、email 和 provider
        """
        token = create_token(self.secret, self.extra)
        user_id = self.extra.get('uid')
        return WilddogUser(self.email, token, self.provider, user_id)


class WilddogApplication(object):
    """
    实际在后端与 Wilddog 进行 HTTP 通信的类。它完全实现了由 Wilddog 所定义的
    RESTful 接口规范。数据在两端使用 JSON 格式传输。这个类需要一个 dsn 作为后端通信的
    基础 url。如有必要，authentication 中的 consideration 信息将会在构造 HTTP 请
    求时放入请求的 consideration 中。
    这里也提供了每种 HTTP 请求方法的异步版本。异步调用利用了 async 模块下定义的on-demand
    process pool
    auth = WilddogAuthentication(WILDDOG_SECRET, 'wilddog@wilddog.com', 'fbpw')
    wilddog = WilddogApplication('https://wilddog.localhost', auth)
    That's all there is. Then you start connecting with the backend:
    json_dict = wilddog.get('/users', '1', {'print': 'pretty'})
    print json_dict
    {'1': 'John Doe', '2': 'Jane Doe', ...}
    Async version is:
    wilddog.get('/users', '1', {'print': 'pretty'}, callback=log_json_dict)
    The callback method is fed with the returning response.
    """
    NAME_EXTENSION = '.json'
    URL_SEPERATOR = '/'
    HEADERS = {'typ': 'JWT', 'alg': 'HS256'}

    def __init__(self, dsn, authentication=None):
        assert dsn.startswith('https://'), 'DSN must be a secure URL'
        self.token = None
        self.dsn = dsn
        self.authentication = authentication

    def set_token(self, token):
        """
        如果在构造对象时未指定 authentication，可以在后续流程中调用此方法直接设置 token
        :param token: 生成好的超级密钥
        """
        if (token is None) or (not isinstance(token, basestring)):
            raise ValueError("token must not be None and must be a string.")
        self.token = token

    def _build_endpoint_url(self, url, name=None):
        """
        使用指定的 url 构造全路径和快照名称。
        例子:
        full_url = _build_endpoint_url('/users', '1')
        full_url => 'http://wilddog.localhost/users/1.json'
        """
        if not url.endswith(self.URL_SEPERATOR):
            url += self.URL_SEPERATOR
        if name is None:
            name = ''
        return '%s%s%s' % (urlparse.urljoin(self.dsn, url), name,
                           self.NAME_EXTENSION)

    def _authenticate(self, params, headers):
        """
        指定请求所使用的鉴权信息。
        `params` 当前请求的查询参数。
        `headers` 当前的请求头信息。
        如果在构造对象时既未指定 authentication，也未调用 set_token 方法设置 token，那么这个方法什么都不会做。
        """
        if self.authentication:
            user = self.authentication.get_user()
            params.update({'auth': user.wilddog_auth_token})
            headers.update(self.HEADERS)
        elif self.token:
            params.update({'auth': self.token})
            headers.update(self.HEADERS)

    @http_connection(60)
    def get(self, url, name, params=None, headers=None, connection=None):
        """
        同步 GET。
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        return make_get_request(endpoint, params, headers, connection=connection)

    def get_async(self, url, name, callback=None, params=None, headers=None):
        """
        异步 GET。
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        process_pool.apply_async(make_get_request,
                                 args=(endpoint, params, headers), callback=callback)

    @http_connection(60)
    def put(self, url, name, data, params=None, headers=None, connection=None):
        """
        同步 PUT 请求。这里不会有返回值从服务端过来，因为请求将会使用``silent``
        参数构造。``data``必须是一个 JSON 对象。
        """
        assert name, 'Snapshot name must be specified'
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        return make_put_request(endpoint, data, params, headers,
                                connection=connection)

    def put_async(self, url, name, data, callback=None, params=None, headers=None):
        """
        异步 PUT。
        """
        if name is None: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        process_pool.apply_async(make_put_request,
                                 args=(endpoint, data, params, headers),
                                 callback=callback)

    @http_connection(60)
    def post(self, url, data, params=None, headers=None, connection=None):
        """
        Synchronous POST request. ``data`` must be a JSONable value.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        return make_post_request(endpoint, data, params, headers,
                                 connection=connection)

    def post_async(self, url, data, callback=None, params=None, headers=None):
        """
        Asynchronous POST request with the process pool.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        process_pool.apply_async(make_post_request,
                                 args=(endpoint, data, params, headers),
                                 callback=callback)

    @http_connection(60)
    def patch(self, url, data, params=None, headers=None, connection=None):
        """
        Synchronous POST request. ``data`` must be a JSONable value.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        return make_patch_request(endpoint, data, params, headers,
                                  connection=connection)

    def patch_async(self, url, data, callback=None, params=None, headers=None):
        """
        Asynchronous PATCH request with the process pool.
        """
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        data = json.dumps(data, cls=JSONEncoder)
        process_pool.apply_async(make_patch_request,
                                 args=(endpoint, data, params, headers),
                                 callback=callback)

    @http_connection(60)
    def delete(self, url, name, params=None, headers=None, connection=None):
        """
        Synchronous DELETE request. ``data`` must be a JSONable value.
        """
        if not name: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        return make_delete_request(endpoint, params, headers, connection=connection)

    def delete_async(self, url, name, callback=None, params=None, headers=None):
        """
        Asynchronous DELETE request with the process pool.
        """
        if not name: name = ''
        params = params or {}
        headers = headers or {}
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        process_pool.apply_async(make_delete_request,
                                 args=(endpoint, params, headers), callback=callback)
