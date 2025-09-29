pytest 会递归查找当前目录及子目录下所有以 `test_` 开始 或者 `_test` 结尾的python脚本，执行其中符合规则的函数和方法，不需要显示调用。

# 测试范围
1. 文件名以 `test_*.py` 和 `*_test.py` 命名
2. 以 `test_` 开头的函数
3. 以 `Test` 开头的类
4. 以 `test_` 开头的方法

# 使用
* `pytest folder_name`  直接运行文件夹内符合规则的所有用例
* `pytest test_file.py`  执行某个py文件中的用例
* `pytest test_file.py::test_func`  执行模块内的某个函数（节点运行）
* `pytest test_file.py::TestClass::test_method`  执行模块内测试类的某个方法（节点运行）
* `pytest test_file.py::TestClass`  执行模块内某个测试类（节点运行）
* `pytest test_file.py::TestClass test_file2.py::test_mothod`  多节点运行，中间用空格隔开
***
* `pytest -k pass`  匹配用例名称的表达式，含有 "pass" 的被执行，其他的 deselected
* `pytest -k "pass or fail"`  组合匹配，含有 "pass" 和 “fail”的被执行
* `pytest -k "not pass" `  排除运行，不含“pass”的被执行
***
* `pytest -m finished `  标记表达式，运行用 `@pytest.mark.finished` 标记的用例
* `pytest -m "finished and not merged"`  多个标记逻辑匹配，运行含有 finished 不含 merged 标记的用例
***
* `pytest -v`  运行时显示详细信息
* `pytest -s`  显示打印消息
* `pytest -x`  遇到错误就停止运行
* `pytest -x --maxfail=2`  遇到两个错误就停止运行
* `pytest --setup-show`  跟踪固件运行
* `pytest -v --reruns 5 --reruns-delay 1`  运行失败的用例间隔1s重新运行5次 `pip install pytest-rerunfailures`
* `pytest -n 3`  3个cpu并行执行测试用例，需保证测试用例可随机执行, `pip install pytest-xdist` 分布式执行插件，多个cpu或主机执行
* `pytest -v -n auto`  自动侦测系统里cpu的数目
* `pytest --count=2`  重复运行测试 `pip install pytest-repeat`
* `pytest --html=./report/report.html`  生成报告，此报告中css是独立的，分享时会丢失样式，pip install pytest-html
* `pytest --html=report.html --self-containd-html`  合并css到html报告中，除了passed所有行都被展开
* `pytest --durations=10`  获取最慢的10个用例的执行耗时


# Fixture
Fixture（固件）是一些函数，pytest 会在执行函数之前或者之后加载运行它们，相当于预处理和后处理。  

`fixture（scope='function'，params=None，autouse=False，ids=None，name=None)`
* `scope`：有四个级别参数 `function`（默认），`class`，`module`，`session`
* `params`：一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它。
* `autouse`：如果True，则为所有测试激活fixture func可以看到它。如果为False则显示需要参考来激活fixture。当用例很多的时候，每次都传这个参数，会很繁琐，可以设置为True开启自动使用fixture功能，这样用例就不用每次都去传参了。
* ids：每个字符串id的列表，每个字符串对应于params这样他们就是测试ID的一部分。如果没有提供ID它们将从params自动生成。
* name：fixture的名称。这默认为装饰函数的名称。

[pytest框架之fixture详细使用方法及举例](https://blog.csdn.net/Z1998hx0919/article/details/118227331)

示例（test_pytest.py）
```python
# scope、auto使用
@pytest.fixture(scope = "function", autouse=True)
def function_scope():
    pass

@pytest.fixture(scope = "module")
def module_scope():
    pass

@pytest.fixture(scope = "session")
def session_scope():
    pass

@pytest.fixture(scope = "class")
def class_scope():
    pass

# yield 使用
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nsession start: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('\nsession finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('session Total time cost: {:.3f}s'.format(finished - start))

def test_1():
    time.sleep(1)

def test_2():
    time.sleep(2)
```

执行：`pytest --setup-show -s`  
执行结果：
```
test_pytest.py
session start: 2020-04-16 17:29:02

SETUP    S timer_session_scope
    SETUP    M module_scope
      SETUP    C class_scope
        SETUP    F function_scope
        test_pytest_study.py::test_3 (fixtures used: class_scope, function_scope, module_scope, timer_session_scope).
        TEARDOWN F function_scope
      TEARDOWN C class_scope
      SETUP    C class_scope
        SETUP    F function_scope
        test_pytest_study.py::test_4 (fixtures used: class_scope, function_scope, module_scope, timer_session_scope).
        TEARDOWN F function_scope
      TEARDOWN C class_scope
    TEARDOWN M module_scope
session finished: 2020-04-16 17:29:05
session Total time cost: 3.087s

TEARDOWN S timer_session_scope
```

## 集中管理 fixture
使用文件 `conftest.py` 集中管理，在不同层级定义，作用于在其所在的目录和子目录，pytest会自动调用。

示例（conftest.py）
```python
# conftest.py
# conding=utf-8
import pytest

@pytest.fixture()
def postcode():
    print("执行postcode fixture")
    return "010"
```

使用（test_demo.py）
```python
# coding=utf-8
import pytest

class TestDemo():

    def test_postcode(self, postcode):
        assert postcode == "010"

if __name__=="__main__":
    pytest.main(["--setup-show", "-s", "test_demo.py"])
```

执行
```shell
python test_demo.py
```

## 固件参数化
固件参数化需要使用 pytest 内置的固件 request，并通过 request.param 获取参数。
```python
# test_demo.py
@pytest.fixture(params=[
    ("user1", "passwd1"),
    ("user2", "passwd2")
    ])
def param(request):
    return request.param

@pytest.fixture(autouse=True)
def login(param):
    print("\n登录成功 %s %s" %param)
    yield
    print("\n退出成功 %s %s" %param)

def test_api():
    assert 1 == 1
```

执行
```shell
pytest -s -v test_demo.py
运行结果：
test_demo.py::test_api[param0]
登录成功 user1 passwd1
PASSED
退出成功 user1 passwd1

test_demo.py::test_api[param1]
登录成功 user2 passwd2
PASSED
退出成功 user2 passwd2
```


# mark
`mark` 即标签

## 使用方法
1. 注册标签名或使用内置标签
2. 在测试用例、测试类、模块文件前面加上 @pytest.mark 标签名

## 内置标签
### 1.参数化
`@pytest.mark.parametrize(argnames, argvalues)`
示例
```python
import hashlib

@pytest.mark.parametrize("x", list(range(10)))
def test_somethins(x):
    time.sleep(1)

# 执行多次
@pytest.mark.parametrize("passwd",["123456", "abcdefgfs", "as52345fasdf4"])
def test_passwd_length(passwd):
    assert len(passwd) >= 8

# 执行多次
@pytest.mark.parametrize('user, passwd',[('jack', 'abcdefgh'),('tom', 'a123456a')])
def test_passwd_md5(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }
    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]

# 如果觉得每组测试的默认参数显示不清晰，可以使用 pytest.param 的 id 参数进行自定义
@pytest.mark.parametrize("user, passwd",
                       [pytest.param("jack", "abcdefgh", id = "User<Jack>"),
                        pytest.param("tom", "a123456a", id = "User<Tom>")])
def test_passwd_md5_id(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }
    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]
```

### 2.无条件跳过用例
`@pytest.mark.skip(reason="xxx")`

### 3.有条件跳过用例
`@pytest.mark.skipif(version < 0.3, reason = "not supported until 0.3")`

### 4.预测执行失败进行提示标记
`@pytest.mark.xfail(version < 0.3, reason = "not supported until 0.3")`
运行结果为 x ，通过 xpassed, 失败 xfailed

## 注册标签名
### 注册方法
* 在 `conftest.py` 文件中添加代码
```python
# 单个标签文件内容
def pytest_configure(config):
    config.addinivalue_line("markers", "demo:demo标签名称")

# 多个标签文件内容
def pytest_configure(config):
    marker_list = ["p0:p0级别用例", "p1:p1级别用例", "p2:p2级别用例"]  # 标签名称
    for markers in marker_list:
        config.addinivalue_line("markers", markers)
```

* 项目中添加 `pytest.ini` 配置文件
```shell
[pytest]
markers = 
    p0:p0级别用例
    p1:p1级别用例
    p2:p2级别用例
```

### 使用
```python
import pytest

@pytest.mark.p0
def test_mark01():
    print("函数级别的mark_p0")

@pytest.mark.p1
def test_mark02():
    print("函数级别的mark_p1")

@pytest.mark.P2
class TestDemo:
    def test_mark03(self):
        print("mark_p2")

    def test_mark04(self):
        print("mark_p2")
```

### 运行方式
1. 命令行运行
`pytest -m "p0 and p1"`

2. 文件运行
`pytest.main(["-m", "P0", "--html=report.html"])`


# 其他使用示例
### 抛出异常
```py
with pytest.raises(SVTInvalidArgument) as excinfo:
    SVTPropertiesWrapper(vm_uuid, conn, "192.168.1.1").update_svt_properties(
        properties["properties"], ["hostname"], ""
    )
assert "Hostname can not be empty" in str(excinfo.value)
assert excinfo.value.user_code = ERROR_CODE
```
