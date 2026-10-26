# 状态栏
## claude-code-statusline-pro
在项目根目录或家目录创建 .claude/settings.json
```json
{
  "statusLine": {
    "type": "command", 
    "command": "npx ccsp@latest"
  }
}
```

[claude-code-statusline-pro](https://github.com/Wangnov/claude-code-statusline-pro)


## claude-code-statusline-pro-aicodeditor
在项目根目录或家目录创建 .claude/settings.json：
```json
{
  "statusLine": {
    "type": "command", 
    "command": "npx claude-code-statusline-pro-aicodeditor@latest"
    // 或使用原版：npx claude-code-statusline-pro@latest
  }
}
```
配置
```bash
npx claude-code-statusline-pro-aicodeditor@latest --preset PMBTUS --theme powerline
```
[状态栏优化](https://github.com/HorizonWing/claude-code-statusline-pro-aicodeditor)
