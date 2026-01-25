# 本地LLM服务集成使用指南

## 概述

现在 `raptor_indexer.py` 和 `graphrag_indexer.py` 已经支持调用本地LLM服务（如 vLLM 或 Ollama）。这使得你可以在本地运行大语言模型，而不需要依赖远程API服务。

## 配置选项

### 环境变量配置

在 `.env` 文件中添加以下配置：

```bash
# 启用本地LLM服务
RAPTOR_USE_LOCAL_LLM=true
GRAPHRAG_USE_LOCAL_LLM=true

# 本地LLM服务地址（默认：vLLM/Ollama的OpenAI兼容接口）
RAPTOR_LOCAL_LLM_BASE_URL=http://localhost:8000/v1
GRAPHRAG_LOCAL_LLM_BASE_URL=http://localhost:8000/v1

# 本地LLM API密钥（vLLM/Ollama通常不需要，使用"EMPTY"）
RAPTOR_LOCAL_LLM_API_KEY=EMPTY
GRAPHRAG_LOCAL_LLM_API_KEY=EMPTY

# 模型名称（使用本地部署的模型）
RAPTOR_MODEL=Qwen/Qwen3-0.6B
GRAPHRAG_MODEL=Qwen/Qwen3-0.6B
```

### 配置说明

1. **`*_USE_LOCAL_LLM`**: 设置为 `true` 启用本地LLM，`false` 使用远程API
2. **`*_LOCAL_LLM_BASE_URL`**: 本地LLM服务的OpenAI兼容API地址
   - vLLM: `http://localhost:8000/v1`
   - Ollama: `http://localhost:11434/v1`
3. **`*_LOCAL_LLM_API_KEY`**: 本地服务通常不需要API密钥，使用 `"EMPTY"`
4. **`*_MODEL`**: 本地部署的模型名称

## 使用示例

### 示例1：使用本地vLLM服务

```bash
# 启动vLLM服务（在另一个终端）
cd /home/jipeng/compute-go/agent/demo/local_llm_serving
python server.py

# 配置环境变量
export RAPTOR_USE_LOCAL_LLM=true
export GRAPHRAG_USE_LOCAL_LLM=true
export RAPTOR_LOCAL_LLM_BASE_URL=http://localhost:8000/v1
export GRAPHRAG_LOCAL_LLM_BASE_URL=http://localhost:8000/v1
export RAPTOR_MODEL=Qwen/Qwen3-0.6B
export GRAPHRAG_MODEL=Qwen/Qwen3-0.6B

# 运行测试
python test_indexing.py
```

### 示例2：使用本地Ollama服务

```bash
# 启动Ollama服务
ollama serve

# 拉取模型
ollama pull qwen3:0.6b

# 配置环境变量
export RAPTOR_USE_LOCAL_LLM=true
export GRAPHRAG_USE_LOCAL_LLM=true
export RAPTOR_LOCAL_LLM_BASE_URL=http://localhost:11434/v1
export GRAPHRAG_LOCAL_LLM_BASE_URL=http://localhost:11434/v1
export RAPTOR_MODEL=qwen3:0.6b
export GRAPHRAG_MODEL=qwen3:0.6b

# 运行测试
python test_indexing.py
```

### 示例3：切换回远程API

```bash
# 禁用本地LLM，使用远程API
export RAPTOR_USE_LOCAL_LLM=false
export GRAPHRAG_USE_LOCAL_LLM=false
export RAPTOR_BASE_URL=https://api.deepseek.com
export GRAPHRAG_BASE_URL=https://api.deepseek.com
export OPENAI_API_KEY=your-deepseek-api-key
export RAPTOR_MODEL=deepseek-chat
export GRAPHRAG_MODEL=deepseek-chat

# 运行测试
python test_indexing.py
```

## 代码修改说明

### 1. 配置类更新 (`config.py`)

添加了本地LLM配置字段：
- `use_local_llm`: 是否使用本地LLM
- `local_llm_base_url`: 本地LLM服务地址
- `local_llm_api_key`: 本地LLM API密钥

### 2. 客户端初始化更新

在 `raptor_indexer.py` 和 `graphrag_indexer.py` 中添加了 `_initialize_client()` 方法，根据配置选择初始化方式：

```python
def _initialize_client(self, config):
    """Initialize OpenAI client for either remote API or local LLM service."""
    client_kwargs = {}
    
    if config.use_local_llm:
        logger.info("Using local LLM service")
        client_kwargs["api_key"] = config.local_llm_api_key or "EMPTY"
        client_kwargs["base_url"] = config.local_llm_base_url
    else:
        client_kwargs["api_key"] = config.openai_api_key
        if config.base_url:
            client_kwargs["base_url"] = config.base_url
    
    return OpenAI(**client_kwargs)
```

### 3. 向后兼容性

修改保持了完全向后兼容性：
- 默认情况下 `use_local_llm=false`，使用原有逻辑
- 原有配置和环境变量仍然有效
- 新增配置不会影响现有功能

## 支持的本地LLM服务

### 1. **vLLM**
- 高性能推理引擎
- 支持多种模型格式
- OpenAI兼容API
- 默认地址：`http://localhost:8000/v1`

### 2. **Ollama**
- 易于使用的本地模型运行器
- 支持多种模型
- OpenAI兼容API
- 默认地址：`http://localhost:11434/v1`

### 3. **其他OpenAI兼容服务**
- LM Studio
- Text Generation WebUI
- 任何提供OpenAI兼容API的本地服务

## 故障排除

### 常见问题

1. **连接失败**
   ```
   Error: Connection error
   ```
   **解决方案**：确保本地LLM服务正在运行，并且地址正确。

2. **模型不存在**
   ```
   Error: Model not found
   ```
   **解决方案**：检查模型名称是否正确，确保模型已下载/部署。

3. **API密钥错误**
   ```
   Error: Invalid API key
   ```
   **解决方案**：本地服务通常使用 `"EMPTY"` 作为API密钥。

### 调试步骤

1. 检查服务状态：
   ```bash
   curl http://localhost:8000/v1/models
   ```

2. 测试简单请求：
   ```bash
   curl http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "Qwen/Qwen3-0.6B",
       "messages": [{"role": "user", "content": "Hello"}],
       "max_tokens": 10
     }'
   ```

3. 查看日志：
   ```bash
   # 查看vLLM日志
   tail -f vllm_server.log
   
   # 查看应用日志
   tail -f test_indexing.log
   ```

## 性能考虑

1. **模型选择**：本地运行较小的模型（如 0.6B-7B 参数）以获得更好的性能
2. **硬件要求**：确保有足够的GPU内存或系统内存
3. **批处理**：考虑调整批处理大小以优化性能
4. **缓存**：利用本地服务的缓存机制提高响应速度

## 扩展功能

未来可以扩展的功能：
1. **负载均衡**：支持多个本地LLM实例
2. **故障转移**：本地服务失败时自动切换到远程API
3. **模型管理**：动态加载/卸载模型
4. **性能监控**：监控本地LLM的性能指标

通过这个集成，你现在可以在本地环境中完全运行RAPTOR和GraphRAG索引，保护数据隐私并减少API成本。
