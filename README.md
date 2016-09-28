# Wilddog Python Client

基于 [Wilddog REST API](https://z.wilddog.com/rest/quickstart).

### 安装

请确认你的 Python 版本支持 SNI，推荐使用 2.7.9及以上版本

```bash
$ sudo pip install requests==1.1.0
```

```bash
$ sudo pip install wilddog-python
```
### 示例
```python

from wilddog import WilddogApplication
wilddog = WilddogApplication('https://your_storage.wilddogio.com', None)
result = wilddog.get('/users', None)
print result
{'1': 'John Doe', '2': 'Jane Doe'}
```

### Token生成
Token用于标识用户身份，结合 [规则表达式](https://z.wilddog.com/rule/quickstart) 做数据读写权限的控制。可以使用超级密钥本身做为token，这样的终端将获得管理员权限，读写数据操作不受规则表达式的限制。也可以使用超级密钥进行签名，自行生成标准jwt格式的token。

token格式的文档参见：[https://z.wilddog.com/rule/guide/4](https://z.wilddog.com/rule/guide/4)。

python版token生成工具：[wilddog-token-generator-python](https://github.com/WildDogTeam/wilddog-token-generator-python)。


### API列表
```python

#WilddogAuthentication 构造器
WilddogAuthentication(secret, email, debug=False, admin=False, extra=None)
#Wilddog 构造器
Wilddog(base_url, authentication=None)

#WilddogAuthentication 并不是必须的，你也可以直接设置Token
wilddog.set_token(token)
#读取数据
wilddog.get(url, name, params=None, headers=None, connection=None)                
#异步读取数据
wilddog.get_async(url, name, callback=None, params=None, headers=None)        
#更新数据
wilddog.put(url, name, data, params=None, headers=None, connection=None)     
#异步更新数据
wilddog.put_async(url, name, data, callback=None, params=None, headers=None) 
#push数据
wilddog.post(url, data, params=None, headers=None, connection=None)
#异步push数据
wilddog.post_async(url, data, callback=None, params=None, headers=None)
#追加数据
wilddog.patch(url, data, params=None, headers=None, connection=None)
#异步追加数据
wilddog.patch_async(url, data, callback=None, params=None, headers=None):
#删除数据
wilddog.delete(url, name, params=None, headers=None, connection=None)
#异步删除数据
wilddog.delete_async(url, name, callback=None, params=None, headers=None)

```

详细的Rest API接口描述，请参考 [Wilddog REST API 文档](https://z.wilddog.com/rest/quickstart).


### 单元测试
单元测试代码在/test目录下。测试运行方式如下：

```bash
$ python test/wilddog_test.py
```

```bash
$ python test/jsonutil_test.py
```

### License
MIT
http://wilddog.mit-license.org/