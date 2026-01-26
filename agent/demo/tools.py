"""Tools for knowledge base interaction and system operations"""

import json
import logging
import requests
import os
import subprocess
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from config import KnowledgeBaseConfig, KnowledgeBaseType
from agent.indexer_raptor import RaptorIndexer
from agent.indexer_graphrag import GraphRAGIndexer
from agent.config import get_raptor_config, get_graphrag_config


logger = logging.getLogger(__name__)


# TODO list related classes
class TodoStatus(str, Enum):
    """Status of a TODO item"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class TodoItem:
    """Represents a TODO item"""
    id: int
    content: str
    status: TodoStatus
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class SearchResult:
    """Search result from knowledge base"""
    doc_id: str
    chunk_id: str
    text: str
    score: float
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "text": self.text,
            "score": self.score,
            "metadata": self.metadata or {}
        }


class KnowledgeBaseTools:
    """Tools for interacting with knowledge base"""
    
    def __init__(self, config: KnowledgeBaseConfig):
        self.config = config
        self.document_store = {}  # In-memory store for documents
        
        # Load document store if exists
        try:
            with open(config.document_store_path, 'r', encoding='utf-8') as f:
                self.document_store = json.load(f)
        except FileNotFoundError:
            logger.info("No existing document store found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading document store: {e}")
    
    def save_document_store(self):
        """Save document store to disk"""
        try:
            with open(self.config.document_store_path, 'w', encoding='utf-8') as f:
                json.dump(self.document_store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving document store: {e}")
    
    def knowledge_base_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the knowledge base with a natural language query.
        
        Args:
            query: Natural language query string
            
        Returns:
            List of matching document chunks with scores
        """
        try:
            if self.config.type == KnowledgeBaseType.LOCAL:
                return self._search_local(query)
            elif self.config.type == KnowledgeBaseType.DIFY:
                return self._search_dify(query)
            elif self.config.type == KnowledgeBaseType.RAPTOR:
                return self._search_raptor(query)
            elif self.config.type == KnowledgeBaseType.GRAPHRAG:
                return self._search_graphrag(query)
            else:
                raise ValueError(f"Unsupported knowledge base type: {self.config.type}")
        except Exception as e:
            logger.error(f"Error in knowledge base search: {e}")
            return []
    
    def _search_local(self, query: str) -> List[Dict[str, Any]]:
        """Search using local retrieval pipeline"""
        try:
            response = requests.post(
                f"{self.config.local_base_url}/search",
                json={
                    "query": query,
                    "mode": "hybrid",
                    "top_k": self.config.local_top_k,
                    "rerank": True
                }
            )
            response.raise_for_status()
            
            results = []
            data = response.json()
            
            # The retrieval pipeline returns results in different keys based on mode
            # For hybrid mode, we want the reranked_results
            search_results = data.get("reranked_results", [])
            
            # If no reranked results, fall back to dense or sparse results
            if not search_results:
                search_results = data.get("dense_results", [])
            if not search_results:
                search_results = data.get("sparse_results", [])
                
            for item in search_results:
                # Extract doc_id and chunk_id from the result
                doc_id = item.get("doc_id", "")
                chunk_id = item.get("chunk_id", f"{doc_id}_chunk_{len(results)}")
                
                # Get the text field and score based on result type
                text = item.get("text", "")
                score = item.get("rerank_score", item.get("score", 0.0))
                
                result = SearchResult(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    text=text,
                    score=score,
                    metadata=item.get("metadata", {})
                )
                results.append(result.to_dict())
            
            logger.info(f"Local search returned {len(results)} results")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to local retrieval pipeline: {e}")
            return []
     
    def _search_raptor(self, query: str) -> List[Dict[str, Any]]:
        """Search using RAPTOR tree-based index via function call"""
        
        try:
            # Initialize RAPTOR indexer with configuration
            raptor_config = get_raptor_config()
            
            # Override configuration from knowledge base config if needed
            if hasattr(self.config, 'raptor_model_name'):
                raptor_config.model_name = self.config.raptor_model_name
            if hasattr(self.config, 'raptor_base_url'):
                raptor_config.base_url = self.config.raptor_base_url
            
            # Create RAPTOR indexer instance
            raptor_indexer = RaptorIndexer(raptor_config)
            
            # Load the index if it exists
            index_path = raptor_config.index_dir / "raptor_index.pkl"
            if index_path.exists():
                raptor_indexer.load_index(index_path)
            else:
                logger.warning(f"RAPTOR index not found at {index_path}")
                return self._search_raptor_via_http(query)
            
            # Perform search using function call
            search_results = raptor_indexer.search(query, top_k=self.config.raptor_top_k)
            
            # Convert results to standard format
            results = []
            for i, item in enumerate(search_results):
                doc_id = item.get("node_id", f"raptor_node_{i}")
                chunk_id = f"{doc_id}_level_{item.get('level', 0)}"
                
                # Use summary if available, otherwise use text
                text_content = item.get("summary", item.get("text", ""))
                
                result = SearchResult(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    text=text_content,
                    score=item.get("score", 0.0),
                    metadata={
                        "level": item.get("level", 0),
                        "source": "raptor"
                    }
                )
                results.append(result.to_dict())
            
            logger.info(f"RAPTOR search (function call) returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in RAPTOR function call search: {e}")
            # Fall back to HTTP API
            return self._search_raptor_via_http(query)
    
    def _search_raptor_via_http(self, query: str) -> List[Dict[str, Any]]:
        """Search using RAPTOR tree-based index via HTTP API (fallback)"""
        try:
            response = requests.post(
                f"{self.config.raptor_base_url}/query",
                json={
                    "query": query,
                    "index_type": "raptor",
                    "top_k": self.config.raptor_top_k
                }
            )
            response.raise_for_status()
            
            results = []
            data = response.json()
            
            for i, item in enumerate(data.get("results", [])):
                # RAPTOR returns tree nodes with levels and summaries
                doc_id = item.get("node_id", f"raptor_node_{i}")
                chunk_id = f"{doc_id}_level_{item.get('level', 0)}"
                
                # Use summary if available, otherwise use text
                text_content = item.get("summary", item.get("text", ""))
                
                result = SearchResult(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    text=text_content,
                    score=item.get("score", 0.0),
                    metadata={
                        "level": item.get("level", 0),
                        "source": "raptor"
                    }
                )
                results.append(result.to_dict())
            
            logger.info(f"RAPTOR search (HTTP) returned {len(results)} results")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to RAPTOR index via HTTP: {e}")
            return []
    
    def _search_graphrag(self, query: str) -> List[Dict[str, Any]]:
        """Search using GraphRAG knowledge graph index via direct function call"""
        
        try:
            graphrag_config = get_graphrag_config()
            
            # Override configuration from knowledge base config if needed
            if hasattr(self.config, 'graphrag_model_name'):
                graphrag_config.llm_model = self.config.graphrag_model_name
            if hasattr(self.config, 'graphrag_base_url'):
                graphrag_config.base_url = self.config.graphrag_base_url
            if hasattr(self.config, 'graphrag_search_type'):
                search_type = self.config.graphrag_search_type
            else:
                search_type = "hybrid"
            
            # Create GraphRAG indexer instance
            graphrag_indexer = GraphRAGIndexer(graphrag_config)
            
            # Load the index if it exists
            index_path = graphrag_config.index_dir / "graphrag_index.pkl"
            if index_path.exists():
                graphrag_indexer.load_index(index_path)
            else:
                logger.warning(f"GraphRAG index not found at {index_path}")
                return self._search_graphrag_via_http(query)
            
            # Perform search using function call
            search_results = graphrag_indexer.search(
                query,
                top_k=self.config.graphrag_top_k,
                search_type=search_type
            )
            
            # Convert results to standard format
            results = []
            for i, item in enumerate(search_results):
                result_type = item.get("type", "unknown")
                
                if result_type == "entity":
                    doc_id = item.get("id", f"entity_{i}")
                    chunk_id = f"{doc_id}_{item.get('entity_type', 'unknown')}"
                    text_content = f"{item.get('name', '')}. {item.get('description', '')}"
                    metadata = {
                        "type": "entity",
                        "entity_type": item.get("entity_type"),
                        "related_entities": item.get("related_entities", [])
                    }
                else:  # community
                    doc_id = item.get("id", f"community_{i}")
                    chunk_id = f"{doc_id}_level_{item.get('level', 0)}"
                    text_content = item.get("summary", "")
                    metadata = {
                        "type": "community",
                        "level": item.get("level", 0),
                        "entity_count": item.get("entity_count", 0),
                        "sample_entities": item.get("sample_entities", [])
                    }
                
                result = SearchResult(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    text=text_content,
                    score=item.get("score", 0.0),
                    metadata={**metadata, "source": "graphrag"}
                )
                results.append(result.to_dict())
            
            logger.info(f"GraphRAG search (function call) returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in GraphRAG function call search: {e}")
            # Fall back to HTTP API
            return self._search_graphrag_via_http(query)
    
    def _search_graphrag_via_http(self, query: str) -> List[Dict[str, Any]]:
        """Search using GraphRAG knowledge graph index via HTTP API (fallback)"""
        try:
            response = requests.post(
                f"{self.config.graphrag_base_url}/query",
                json={
                    "query": query,
                    "index_type": "graphrag",
                    "top_k": self.config.graphrag_top_k,
                    "search_type": self.config.graphrag_search_type
                }
            )
            response.raise_for_status()
            
            results = []
            data = response.json()
            
            for i, item in enumerate(data.get("results", [])):
                # GraphRAG returns entities or communities
                result_type = item.get("type", "unknown")
                
                if result_type == "entity":
                    doc_id = item.get("id", f"entity_{i}")
                    chunk_id = f"{doc_id}_{item.get('entity_type', 'unknown')}"
                    text_content = f"{item.get('name', '')}. {item.get('description', '')}"
                    metadata = {
                        "type": "entity",
                        "entity_type": item.get("entity_type"),
                        "related_entities": item.get("related_entities", [])
                    }
                else:  # community
                    doc_id = item.get("id", f"community_{i}")
                    chunk_id = f"{doc_id}_level_{item.get('level', 0)}"
                    text_content = item.get("summary", "")
                    metadata = {
                        "type": "community",
                        "level": item.get("level", 0),
                        "entity_count": item.get("entity_count", 0),
                        "sample_entities": item.get("sample_entities", [])
                    }
                
                result = SearchResult(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    text=text_content,
                    score=item.get("score", 0.0),
                    metadata={**metadata, "source": "graphrag"}
                )
                results.append(result.to_dict())
            
            logger.info(f"GraphRAG search (HTTP) returned {len(results)} results")
            return results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to GraphRAG index via HTTP: {e}")
            return []
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieve the entire document from the knowledge base.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Full document content and metadata
        """
        try:
            # First check local document store
            if doc_id in self.document_store:
                return self.document_store[doc_id]
            
            if self.config.type == KnowledgeBaseType.LOCAL:
                return self._get_document_local(doc_id)
            elif self.config.type == KnowledgeBaseType.DIFY:
                return self._get_document_dify(doc_id)
            elif self.config.type == KnowledgeBaseType.RAPTOR:
                return self._get_document_raptor(doc_id)
            elif self.config.type == KnowledgeBaseType.GRAPHRAG:
                return self._get_document_graphrag(doc_id)
            else:
                raise ValueError(f"Unsupported knowledge base type: {self.config.type}")
        except Exception as e:
            logger.error(f"Error retrieving document {doc_id}: {e}")
            return {"error": f"Document {doc_id} not found"}
    
    def _get_document_local(self, doc_id: str) -> Dict[str, Any]:
        """Get document from local retrieval pipeline"""
        try:
            response = requests.get(
                f"{self.config.local_base_url}/documents/{doc_id}"
            )
            
            if response.status_code == 404:
                return {"error": f"Document {doc_id} not found"}
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting document from local pipeline: {e}")
            return {"error": str(e)}
    
    def _get_document_raptor_via_http(self, doc_id: str) -> Dict[str, Any]:
        """Get document/node from RAPTOR index"""
        try:
            # For RAPTOR, we perform a targeted search for the specific node
            response = requests.post(
                f"{self.config.raptor_base_url}/query",
                json={
                    "query": f"node:{doc_id}",  # Specific node query
                    "index_type": "raptor",
                    "top_k": 1
                }
            )
            
            if response.status_code == 404:
                return {"error": f"Document {doc_id} not found"}
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                return {
                    "doc_id": doc_id,
                    "content": result.get("text", ""),
                    "metadata": {
                        "summary": result.get("summary", ""),
                        "level": result.get("level", 0),
                        "source": "raptor"
                    }
                }
            
            return {"error": f"Document {doc_id} not found"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting document from RAPTOR: {e}")
            return {"error": str(e)}
    
    def _get_document_graphrag_via_http(self, doc_id: str) -> Dict[str, Any]:
        """Get entity or community from GraphRAG index"""
        try:
            # For GraphRAG, we perform a targeted search for the specific entity/community
            response = requests.post(
                f"{self.config.graphrag_base_url}/query",
                json={
                    "query": f"id:{doc_id}",  # Specific ID query
                    "index_type": "graphrag",
                    "top_k": 1,
                    "search_type": "hybrid"
                }
            )
            
            if response.status_code == 404:
                return {"error": f"Document {doc_id} not found"}
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                content = ""
                metadata = {"source": "graphrag"}
                
                if result.get("type") == "entity":
                    content = f"{result.get('name', '')}\n\n{result.get('description', '')}"
                    metadata.update({
                        "type": "entity",
                        "entity_type": result.get("entity_type"),
                        "related_entities": result.get("related_entities", [])
                    })
                else:  # community
                    content = result.get("summary", "")
                    metadata.update({
                        "type": "community",
                        "level": result.get("level", 0),
                        "entity_count": result.get("entity_count", 0),
                        "sample_entities": result.get("sample_entities", [])
                    })
                
                return {
                    "doc_id": doc_id,
                    "content": content,
                    "metadata": metadata
                }
            
            return {"error": f"Document {doc_id} not found"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting document from GraphRAG: {e}")
            return {"error": str(e)}
    
    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None):
        """Add a document to the local store"""
        self.document_store[doc_id] = {
            "doc_id": doc_id,
            "content": content,
            "metadata": metadata or {}
        }
        self.save_document_store()


# System tool implementations
def read_file(file_path: str, begin_line: Optional[int] = None,
              number_lines: Optional[int] = None, current_directory: str = ".") -> Dict[str, Any]:
    """Read file contents with optional line-based reading"""
    try:
        # Resolve path relative to current directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(current_directory, file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check if it's a binary file
        try:
            with open(file_path, 'rb') as f:
                # Read first 1024 bytes to check for binary content
                chunk = f.read(1024)
                # Check for null bytes (common in binary files)
                if b'\x00' in chunk:
                    return {
                        "success": False,
                        "error": "Cannot read binary file. This tool only supports text files.",
                        "file_path": file_path,
                        "is_binary": True
                    }
                # Also check if it's valid UTF-8
                try:
                    chunk.decode('utf-8')
                except UnicodeDecodeError:
                    return {
                        "success": False,
                        "error": "File is not a valid text file (encoding error).",
                        "file_path": file_path,
                        "is_binary": True
                    }
        except Exception:
            # If we can't read it as binary, probably permission issue
            raise
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            if begin_line is not None or number_lines is not None:
                # Line-based reading
                all_lines = f.readlines()
                total_lines = len(all_lines)
                
                # Calculate line range
                start_line = (begin_line - 1) if begin_line is not None else 0
                if start_line < 0:
                    start_line = 0
                if start_line >= total_lines:
                    return {
                        "success": False,
                        "error": f"begin_line {begin_line} is beyond file length ({total_lines} lines)",
                        "file_path": file_path,
                        "total_lines": total_lines
                    }
                
                if number_lines is not None:
                    end_line = min(start_line + number_lines, total_lines)
                else:
                    end_line = total_lines
                
                # Get the requested lines
                selected_lines = all_lines[start_line:end_line]
                content = ''.join(selected_lines)
                
                # Get file info
                stat = os.stat(file_path)
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "content": content,
                    "size_bytes": stat.st_size,
                    "total_lines": total_lines,
                    "begin_line": start_line + 1,  # Convert back to 1-based
                    "end_line": end_line,
                    "lines_read": len(selected_lines),
                    "partial_read": True
                }
            else:
                # Full file reading
                content = f.read()
                
                # Get file info
                stat = os.stat(file_path)
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "content": content,
                    "size_bytes": stat.st_size,
                    "lines": len(content.splitlines()),
                    "partial_read": False
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }


def write_file(file_path: str, content: str, current_directory: str = ".") -> Dict[str, Any]:
    """Write content to file"""
    try:
        # Resolve path relative to current directory
        if not os.path.isabs(file_path):
            file_path = os.path.join(current_directory, file_path)
        
        # Create directory if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": file_path,
            "bytes_written": len(content.encode('utf-8')),
            "lines_written": len(content.splitlines())
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file_path": file_path
        }


def code_interpreter(code: str) -> Dict[str, Any]:
    """Execute Python code in restricted environment"""
    try:
        # Capture output
        import io
        import contextlib
        
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
            exec(code)
        
        # Get output
        stdout = output_buffer.getvalue()
        stderr = error_buffer.getvalue()
        
        return {
            "success": True,
            "stdout": stdout,
            "stderr": stderr,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": str(e)
        }


def execute_command(command: str, working_dir: Optional[str] = None,
                    current_directory: str = ".") -> Dict[str, Any]:
    """Execute shell command"""
    try:
        # Use current directory if not specified
        if working_dir is None:
            working_dir = current_directory
        elif not os.path.isabs(working_dir):
            working_dir = os.path.join(current_directory, working_dir)
        
        # Update current directory if 'cd' command
        if command.strip().startswith('cd '):
            new_dir = command.strip()[3:].strip()
            if not os.path.isabs(new_dir):
                new_dir = os.path.join(current_directory, new_dir)
            
            if os.path.isdir(new_dir):
                return {
                    "success": True,
                    "command": command,
                    "output": f"Changed directory to: {os.path.abspath(new_dir)}",
                    "return_code": 0,
                    "new_directory": os.path.abspath(new_dir)
                }
            else:
                raise FileNotFoundError(f"Directory not found: {new_dir}")
        
        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=working_dir,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "command": command,
            "output": result.stdout,
            "error": result.stderr if result.stderr else None,
            "return_code": result.returncode,
            "working_dir": working_dir
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after 30 seconds: {command}",
            "command": command,
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": command,
            "return_code": -1
        }


def rewrite_todo_list(items: List[str], todo_list: List[TodoItem],
                      next_todo_id: int) -> Dict[str, Any]:
    """Rewrite TODO list with new pending items"""
    # Keep completed and cancelled items
    kept_items = [
        item for item in todo_list
        if item.status in [TodoStatus.COMPLETED, TodoStatus.CANCELLED]
    ]
    
    # Create new pending items
    new_items = []
    for content in items:
        new_items.append(TodoItem(
            id=next_todo_id,
            content=content,
            status=TodoStatus.PENDING
        ))
        next_todo_id += 1
    
    # Update TODO list
    updated_todo_list = kept_items + new_items
    
    return {
        "success": True,
        "kept_items": len(kept_items),
        "new_items": len(new_items),
        "total_items": len(updated_todo_list),
        "next_todo_id": next_todo_id,
        "todo_list": [item.to_dict() for item in updated_todo_list]
    }


def update_todo_status(updates: List[Dict[str, Any]], todo_list: List[TodoItem]) -> Dict[str, Any]:
    """Update status of TODO items"""
    updated_count = 0
    
    for update in updates:
        item_id = update["id"]
        new_status = TodoStatus(update["status"])
        
        for item in todo_list:
            if item.id == item_id:
                item.status = new_status
                item.updated_at = datetime.now().isoformat()
                updated_count += 1
                break
    
    return {
        "success": True,
        "updated_items": updated_count,
        "total_items": len(todo_list),
        "todo_list": [item.to_dict() for item in todo_list]
    }


# Tool function definitions for agent
def get_tool_definitions() -> List[Dict[str, Any]]:
    """Get OpenAI-format tool definitions"""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a text file. Returns error for binary files. Supports partial reading for large files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to read (absolute or relative to current directory)"
                        },
                        "begin_line": {
                            "type": "integer",
                            "description": "Optional: Line number to start reading from (1-based indexing). E.g., begin_line=10 starts from line 10."
                        },
                        "number_lines": {
                            "type": "integer",
                            "description": "Optional: Number of lines to read from begin_line. E.g., number_lines=50 reads 50 lines."
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file (creates or overwrites)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "code_interpreter",
                "description": "Execute Python code in a restricted environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute"
                        }
                    },
                    "required": ["code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "execute_command",
                "description": "Execute a shell command in the current directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Shell command to execute"
                        },
                        "working_dir": {
                            "type": "string",
                            "description": "Optional working directory for the command (defaults to current directory)"
                        }
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "rewrite_todo_list",
                "description": "Rewrite the TODO list with new pending items (keeps completed/cancelled items)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of new TODO items to add as pending"
                        }
                    },
                    "required": ["items"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_todo_status",
                "description": "Update the status of existing TODO items",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "updates": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "integer",
                                        "description": "TODO item ID"
                                    },
                                    "status": {
                                        "type": "string",
                                        "enum": ["pending", "in_progress", "completed", "cancelled"],
                                        "description": "New status for the item"
                                    }
                                },
                                "required": ["id", "status"]
                            },
                            "description": "List of TODO items to update with their new status"
                        }
                    },
                    "required": ["updates"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "knowledge_base_search",
                "description": "Search the knowledge base for relevant information using a natural language query. Returns top-matching document chunks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language search query to find relevant information"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_document",
                "description": "Retrieve the complete content of a specific document from the knowledge base using its document ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "doc_id": {
                            "type": "string",
                            "description": "The unique identifier of the document to retrieve"
                        }
                    },
                    "required": ["doc_id"]
                }
            }
        }
    ]
