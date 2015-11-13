# -*- coding: utf-8 -*-

##############################################################################
#  本源文件来自于 Wilddog token generator for python project.                  #
#                                                                            #
#  - https://github.com/WildDogTeam/wilddog-token-generator-python           #
##############################################################################

try:
    basestring
except NameError:  # Python 3
    basestring = str
from base64 import urlsafe_b64encode
import hashlib
import hmac
import sys

try:
    import json
except ImportError:
    import simplejson as json
import calendar
import time
import datetime

__all__ = ['create_token']

TOKEN_VERSION = 0
TOKEN_SEP = '.'

CLAIMS_MAP = {
    'expires': 'exp',
    'notBefore': 'nbf',
    'admin': 'admin',
    'debug': 'debug'
}


def create_token(secret, data, options=None):
    """
    生成JWT格式的token. 
    约定参见文档： https://z.wilddog.com/rule/guide/4
    base64使用的是URL-safe的，以便于token可以做http请求的参数被传递。
  
      token中固定包含的字段：
      "iat" -> 颁发此token的时间戳。
      "d" -> 用户指定的json数据，参见文档。
      
      用户可配置字段 (全部为可选):
      "exp" -> token过期的时间戳。
      "nbf" -> not before，即在此时间戳之前，这个token不生效。
      "admin" -> 如果设置为true，则这个client将获得管理员权限，即不受规则表达式约束，可以读写任意数据 (建议仅在认证服务器时使用)。
      "debug" -> 如果设置为true，client将会接收到规则表达式执行过程的debug信息.
  
    Args:
        secret - Wilddog App的超级密钥。
        data - 一个serializable的json，数据将被包含的token中。
        options - 一个dictionary，可选的key包括："expires", "notBefore", "admin", "debug"。
        
    Returns:
        Wilddog token.
        
    Raises:
        ValueError
    """
    if not isinstance(secret, basestring):
        raise ValueError("wilddog_token_generator.create_token: secret must be a string.")
    if not options and not data:
        raise ValueError(
            "wilddog_token_generator.create_token: data is empty and no options are set.  This token will have no effect on Wilddog.");
    if not options:
        options = {}
    is_admin_token = ('admin' in options and options['admin'] == True)
    _validate_data(data, is_admin_token)
    claims = _create_options_claims(options)
    claims['v'] = TOKEN_VERSION
    claims['iat'] = int(time.time())
    claims['d'] = data

    token = _encode_token(secret, claims)
    if len(token) > 1024:
        raise RuntimeError("wilddog_token_generator.create_token: generated token is too long.")
    return token


def _validate_data(data, is_admin_token):
    if data is not None and not isinstance(data, dict):
        raise ValueError("wilddog_token_generator.create_token: data must be a dictionary")
    contains_uid = (data is not None and 'uid' in data)
    if (not contains_uid and not is_admin_token) or (contains_uid and not isinstance(data['uid'], basestring)):
        raise ValueError("wilddog_token_generator.create_token: data must contain a \"uid\" key that must be a string.")
    if contains_uid and (len(data['uid']) > 256):
        raise ValueError(
            "wilddog_token_generator.create_token: data must contain a \"uid\" key that must not be longer than 256 bytes.")


def _create_options_claims(opts):
    claims = {}
    for k in opts:
        if isinstance(opts[k], datetime.datetime):
            opts[k] = int(calendar.timegm(opts[k].utctimetuple()))
        if k in CLAIMS_MAP:
            claims[CLAIMS_MAP[k]] = opts[k]
        else:
            raise ValueError('Unrecognized Option: %s' % k)
    return claims


if sys.version_info < (2, 7):
    def _encode(bytes_data):
        # Python 2.6 has problems with bytearrays in b64
        encoded = urlsafe_b64encode(bytes(bytes_data))
        return encoded.decode('utf-8').replace('=', '')
else:
    def _encode(bytes):
        encoded = urlsafe_b64encode(bytes)
        return encoded.decode('utf-8').replace('=', '')


def _encode_json(obj):
    return _encode(bytearray(json.dumps(obj, separators=(',', ':')), 'utf-8'))


def _sign(secret, to_sign):
    def portable_bytes(s):
        try:
            return bytes(s, 'utf-8')
        except TypeError:
            return bytes(s)

    return _encode(hmac.new(portable_bytes(secret), portable_bytes(to_sign), hashlib.sha256).digest())


def _encode_token(secret, claims):
    encoded_header = _encode_json({'typ': 'JWT', 'alg': 'HS256'})
    encoded_claims = _encode_json(claims)
    secure_bits = '%s%s%s' % (encoded_header, TOKEN_SEP, encoded_claims)
    sig = _sign(secret, secure_bits)
    return '%s%s%s' % (secure_bits, TOKEN_SEP, sig)
