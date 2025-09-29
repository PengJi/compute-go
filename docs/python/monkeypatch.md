### patch self method
```py
monkeypatch.setattr("crab.client.CrabClient.get_current_user", lambda x, y: {"role": 0})


def mock_read_bytes(self, path, timeout=None):  # 这里参数必须一致
    return "2.12.0"
monkeypatch.setattr("svt.qga.QEMUGuestAgent.read_bytes", mock_read_bytes)
```

### patch class method
```py
@classmethod
def mock_allow_thaw(cls, vm_uuid):
    return False

monkeypatch.setattr("SVTFileSystemWrapper.allow_thaw", mock_allow_thaw)

# 或者

def batch_get_svt_static_data_mock(self, uuid):
    return []
monkeypatch.setattr(
    "SVTStaticDataWrapper.batch_get_svt_static_data",
    classmethod(batch_get_svt_static_data_mock),
)
```

### patch class staticmethod
```py
@staticmethod
def mock_allow_thaw(vm_uuid):
    return False
monkeypatch.setattr("SVTFileSystemWrapper.allow_thaw", mock_allow_thaw)

# 或者

def mock_allow_thaw(cls, vm_uuid):
    return False
monkeypatch.setattr("SVTFileSystemWrapper.allow_thaw", staticmethod(mock_allow_thaw))
```

### patch property
```py
def mock_platform(self):
    return "windows"

monkeypatch.setattr("svt.qga.QEMUGuestAgent.platform", property(mock_platform))
```
