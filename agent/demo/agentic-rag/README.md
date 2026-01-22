# Agentic RAG System

An educational implementation of an Agentic Retrieval-Augmented Generation (RAG) system with ReAct pattern, supporting multiple LLM providers and knowledge base backends.

对比传统 Non-Agentic RAG 与 Agentic RAG 的性能差异。展示 Agent 如何通过 ReAct 模式主导迭代式信息检索，在处理复杂司法问答时显著提升答案质量。

核心概念：Agentic RAG、ReAct 循环、迭代检索、主动探索

## 🌟 Features

- **Agentic RAG with ReAct Pattern**: Uses reasoning and tool-calling to iteratively search and retrieve information
- **Non-Agentic RAG Mode**: Simple retrieval + LLM response for comparison
- **Multiple LLM Provider Support**: 
  - Kimi/Moonshot
  - Doubao
  - SiliconFlow
  - OpenAI
  - OpenRouter
  - Groq
  - Together AI
  - DeepSeek
- **Flexible Knowledge Base**:
  - Local retrieval pipeline (requires ../retrieval-pipeline)
  - Dify knowledge base API
- **Document Chunking**: Configurable chunking with paragraph boundary respect
- **Evaluation Framework**: Comprehensive evaluation with Chinese legal dataset
- **Conversation History**: Support for follow-up questions
- **Verbose Logging**: Detailed logging to understand agent reasoning

## 📦 Installation

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Set environment variables in `.env` file:

```bash
# LLM API Keys (set the one you're using)
MOONSHOT_API_KEY=your_kimi_api_key
ARK_API_KEY=your_doubao_api_key
SILICONFLOW_API_KEY=your_siliconflow_api_key
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
GROQ_API_KEY=your_groq_api_key
TOGETHER_API_KEY=your_together_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# Knowledge Base Configuration (optional, defaults to local)
KB_TYPE=local  # Options: "local", "dify"
DIFY_API_KEY=your_dify_api_key  # if using Dify
DIFY_DATASET_ID=your_dataset_id  # optional

# LLM Configuration (optional)
LLM_PROVIDER=kimi  # default provider
LLM_MODEL=kimi-k2-0905-preview  # optional, uses provider defaults
```

## 🚀 Usage

### 1. Start the Retrieval Pipeline

First, start the retrieval pipeline server (required for local knowledge base):

```bash
# In a separate terminal
cd ../retrieval-pipeline
python main.py
# Server will run on http://localhost:4242
```

### 2. Index Documents

#### Option A: Index Chinese Law Documents (Pre-included)

```bash
# Index the included Chinese law documents
python index_local_laws.py

# With specific categories
python index_local_laws.py --categories 宪法 民法典

# With document limit
python index_local_laws.py --max-docs 10
```

#### Option B: Index Custom Documents

```bash
# Index a single file
python main.py --index path/to/document.txt

# Index a directory
python main.py --index path/to/documents/

# Custom chunk size
python main.py --index documents/ --chunk-size 2048
```

### 3. Run the Agentic RAG System

#### Interactive Mode (Default)

```bash
# Start in agentic mode (default)
python main.py

# Start in non-agentic mode  
python main.py --mode non-agentic

# Enable verbose logging (default is enabled)
python main.py --verbose

# Disable verbose logging
python main.py --no-verbose
```

In interactive mode:
- Type your questions and press Enter
- Type 'quit' or 'exit' to stop
- Type 'clear' to clear conversation history
- Type 'mode' to switch between agentic/non-agentic modes

#### Single Query

```bash
# Agentic mode
python main.py --query "宪法第一条是什么？" --mode agentic

# Non-agentic mode
python main.py --query "盗窃罪的立案标准是什么？" --mode non-agentic

# Compare both modes
python main.py --query "故意杀人罪判几年？" --mode compare
```

#### Batch Processing

```bash
# Create a file with queries (one per line)
echo "故意杀人罪判几年？
盗窃罪的立案标准是什么？
醉酒驾驶如何处罚？" > queries.txt

# Run batch
python main.py --batch queries.txt --output results.json

# Batch with specific mode
python main.py --batch queries.txt --mode non-agentic
```

#### With Different Providers

```bash
python main.py --provider openai --model gpt-4o-2024-11-20
python main.py --provider doubao --model doubao-seed-1-6-thinking-250715
python main.py --provider siliconflow --query "你好"
```

### 4. Run Evaluation

```bash
# Build evaluation dataset
cd evaluation
python dataset_builder.py

# Run evaluation
python evaluate.py

# With specific configuration
python evaluate.py --provider kimi --kb-type local --output custom_results
```

## 📁 Project Structure

```
agentic-rag/
├── config.py              # Configuration classes
├── agent.py               # Main AgenticRAG implementation
├── tools.py               # Knowledge base tools
├── chunking.py            # Document chunking and indexing
├── main.py                # Main entry point
├── index_local_laws.py    # Index Chinese law documents
├── quickstart.py          # Quick demo script
├── test_simple.py         # Simple test script
├── requirements.txt       # Dependencies
├── README.md              # This file
├── document_store.json    # Local document storage
├── laws/                  # Chinese law documents
│   ├── 1-宪法/
│   ├── 2-宪法相关法/
│   ├── 3-民法典/
│   ├── 3-民法商法/
│   ├── 4-行政法/
│   ├── 5-经济法/
│   ├── 6-社会法/
│   ├── 7-刑法/
│   └── 8-诉讼与非诉讼程序法/
└── evaluation/
    ├── dataset_builder.py # Build evaluation dataset
    └── evaluate.py        # Evaluation framework
```

## 🧠 How It Works

### Agentic RAG Mode

The agent uses the ReAct (Reasoning + Acting) pattern:

1. **Reasoning**: Analyzes what information is needed to answer the question
2. **Tool Calling**: Uses `knowledge_base_search` tool to find relevant chunks
3. **Iterative Search**: May perform multiple searches with refined queries
4. **Document Retrieval**: Can fetch complete documents with `get_document` for context
5. **Answer Synthesis**: Combines retrieved information with citations
6. **Conversation Memory**: Maintains context for follow-up questions

Example flow:
```
User: 宪法第一条是什么？
Agent: [Thinks] Need to find information about Article 1 of the Constitution
       [Tool] knowledge_base_search("宪法第一条")
       [Result] Found relevant chunks about constitutional articles
       [Answer] Based on the retrieved information, Article 1 states...
```

### Non-Agentic RAG Mode

Simple retrieval-augmented generation:

1. **Direct Search**: Searches once with the user's query as-is
2. **Context Injection**: Puts top-K results in the prompt
3. **Single Response**: LLM answers based on provided context
4. **No Iteration**: Single-shot approach without refinement

## 📊 Configuration Options

### Top-K Results

Control how many search results to retrieve:

```python
# In config.py or via environment
local_top_k = 3  # Number of results to retrieve
```

### Verbose Mode

See detailed agent reasoning:

```bash
# Enable verbose (default)
python main.py --verbose

# Disable for cleaner output
python main.py --no-verbose
```

### LLM Temperature

Control response randomness:

```python
# In config.py
temperature = 0.7  # 0.0 = deterministic, 1.0 = more creative
```

## 🎯 Evaluation Results

The system includes an evaluation framework that compares both modes:

### Metrics
- **Success Rate**: Whether the answer contains key legal concepts
- **Response Time**: Time to generate response
- **Retrieval Quality**: Relevance of retrieved chunks
- **Citation Coverage**: Proper source attribution

### Expected Patterns

**Agentic RAG** typically shows:
- ✅ Better coverage of complex multi-faceted questions
- ✅ More accurate citations through explicit tool use  
- ✅ Ability to refine searches based on initial results
- ⚠️ Slower response time (multiple LLM calls)

**Non-Agentic RAG** typically shows:
- ✅ Faster responses (single retrieval step)
- ✅ Good performance on simple, direct questions
- ⚠️ May miss relevant information with poor query formulation
- ⚠️ Limited ability to handle ambiguous queries

## 🔧 Troubleshooting

### Retrieval Pipeline Not Responding

```bash
# Check if the service is running
curl http://localhost:4242/health

# If not, start it:
cd ../retrieval-pipeline
python main.py
```

### No Search Results

1. Ensure documents are indexed:
```bash
python index_local_laws.py
```

2. Check document store:
```bash
ls -la document_store.json
```

3. Verify retrieval pipeline has documents:
```bash
curl http://localhost:4242/stats
```

### API Key Issues

```bash
# Check if environment variable is set
echo $MOONSHOT_API_KEY

# Or use .env file
cat .env | grep API_KEY
```

### Indexing Errors

- Ensure retrieval pipeline is running before indexing
- Check file encodings (UTF-8 expected)
- Verify network connectivity to localhost:4242

## 🤝 Contributing

Areas for potential enhancement:

- Additional evaluation metrics
- More sophisticated chunking strategies
- Better reranking algorithms
- Additional knowledge base backends (RAPTOR, GraphRAG)
- Multi-language support
- Query expansion techniques
- Hybrid retrieval strategies

## 📄 License

This is an educational project for learning purposes.
