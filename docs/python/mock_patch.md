### patch instance method
```py
from unittest import mock

with mock.patch.object(client.VmToolsClient, "batch_get_svt_info") as mock_batch_get_svt_info:
    mock_batch_get_svt_info.return_value = []
    mock_batch_get_svt_info.assert_called_once_with()
    mock_batch_get_svt_info.assert_called_with()
```

### patch class method
```py
from unittest import mock

with mock.patch.object(dhcp.DHCPProxy, "is_enable_dhcp") as mock_is_enable_dhcp:
    mock_is_enable_dhcp.return_value = True
    mock_is_enable_dhcp.assert_called_once_with()
    mock_is_enable_dhcp.assert_called_with()
```

### patch property or property method
```py
from unittest import mock

@mock.patch.object(svt_reports_dao.SVTReportsDAO, "COLLECTION_NAME", new="svt_reports_mock")
def test_get_svt_report_by_uuid(self):
    pass
```

### 测试 logging 调用
```py
from unittest import mock

with mock.patch("logging.warn") as mock_warn:
    mock_warn.call_count == 2
    mock_warn.assert_called_once_with("warn msg")
    mock_warn.assert_called_with("warn meg")
```
