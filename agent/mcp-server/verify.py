#!/usr/bin/env python3
"""
MCP 天气服务器验证脚本

验证所有文件是否完整，检查依赖是否可用。
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_python_version() -> bool:
    """检查 Python 版本"""
    version = sys.version_info
    required = (3, 8)
    ok = version >= required
    status = "✅" if ok else "❌"
    print(f"{status} Python 版本: {version.major}.{version.minor}.{version.micro} (需要 >= 3.8)")
    return ok

def check_import(module_name: str) -> bool:
    """检查模块是否可以导入"""
    try:
        spec = importlib.util.find_spec(module_name)
        ok = spec is not None
        status = "✅" if ok else "❌"
        print(f"{status} 模块: {module_name}")
        return ok
    except:
        print(f"❌ 模块: {module_name}")
        return False

def check_api_key() -> bool:
    """检查 API 密钥配置（现在无需 API 密钥）"""
    print("✅ API 密钥: 无需 API 密钥，使用 open-meteo 免费 API")
    return True

def main():
    """主函数"""
    print("🔍 MCP 天气服务器完整性检查")
    print("=" * 50)
    
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 检查文件
    print("\n📁 文件检查:")
    files_to_check = [
        ("weather_server.py", "天气服务主文件"),
        ("server.py", "MCP 服务器文件"),
        ("test_client.py", "测试客户端"),
        ("config.yaml", "配置文件"),
        ("requirements.txt", "依赖文件"),
        ("README.md", "说明文档"),
        ("USAGE.md", "使用指南"),
        ("install.sh", "安装脚本"),
    ]
    
    all_files_ok = True
    for filename, description in files_to_check:
        if not check_file_exists(filename, description):
            all_files_ok = False
    
    # 检查 Python 版本
    print("\n🐍 Python 检查:")
    python_ok = check_python_version()
    
    # 检查 API 密钥
    print("\n🔑 API 密钥检查:")
    api_key_ok = check_api_key()
    
    # 检查依赖
    print("\n📦 依赖检查:")
    dependencies = ["mcp", "httpx", "anyio"]
    deps_ok = True
    for dep in dependencies:
        if not check_import(dep):
            deps_ok = False
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果:")
    
    issues = []
    if not all_files_ok:
        issues.append("缺少必要文件")
    if not python_ok:
        issues.append("Python 版本过低")
    if not api_key_ok:
        issues.append("API 密钥未设置")
    if not deps_ok:
        issues.append("依赖未安装")
    
    if not issues:
        print("✅ 所有检查通过！服务器可以正常运行。")
        print("\n🚀 下一步:")
        print("1. 运行测试: ./test.sh")
        print("2. 启动服务器: ./start_server.sh --stdio")
        print("3. 集成到 AI 助手")
        return 0
    else:
        print(f"❌ 发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"   - {issue}")
        
        print("\n🔧 解决方案:")
        if "缺少必要文件" in issues:
            print("   - 重新运行安装脚本: ./install.sh")
        if "Python 版本过低" in issues:
            print("   - 升级 Python 到 3.8 或更高版本")
        if "API 密钥未设置" in issues:
            print("   - 无需 API 密钥，使用 open-meteo 免费 API")
        if "依赖未安装" in issues:
            print("   - 安装依赖: pip install -r requirements.txt")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
