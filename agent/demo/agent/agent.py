"""
System-Hint Enhanced AI Agent
An agent that demonstrates advanced trajectory management with system hints,
including timestamps, tool call tracking, TODO lists, and detailed error messages.
"""

import json
import os
import sys
import platform
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from openai import OpenAI
import traceback

from agent.config import SystemHintConfig
from agent.tools import (
    ToolCall,
    get_tool_definitions,
    read_file,
    write_file,
    code_interpreter,
    execute_command,
    rewrite_todo_list,
    update_todo_status,
    TodoItem,
    TodoStatus,
    KnowledgeBaseTools
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SystemHintAgent:
    """
    AI Agent with enhanced system hints for better trajectory management
    """
    
    def __init__(self, api_key: str, provider: str = "deepseek",
                 model: Optional[str] = None, config: Optional[SystemHintConfig] = None,
                 verbose: bool = True):
        """
        Initialize the agent
        
        Args:
            api_key: API key for the LLM provider
            provider: LLM provider ('deepseek')
            model: Optional model override
            config: System hint configuration
            verbose: If True, log full details
        """
        self.provider = provider.lower()
        self.verbose = verbose
        self.config = config or SystemHintConfig()
        
        # Configure client based on provider
        if self.provider == "deepseek":
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
            self.model = model or "deepseek-chat"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # Initialize tracking
        self.tool_call_counts: Dict[str, int] = {}
        self.tool_calls: List[ToolCall] = []
        self.todo_list: List[TodoItem] = []
        self.next_todo_id = 1
        
        # Initialize conversation history
        self.conversation_history = []
        self.simulated_time = datetime.now()  # For demo time simulation
        self._init_system_prompt()
        
        # Track current working directory
        self.current_directory = os.getcwd()
        
        # Track last messages sent to LLM
        self.last_llm_messages = None

        # Initialize knowledge base tools
        self.kb_tools = KnowledgeBaseTools(self.config.knowledge_base)
        
        logger.info(f"System-Hint Agent initialized with provider: {self.provider}, model: {self.model}")
    
    def _init_system_prompt(self):
        """Initialize the system prompt for the conversation"""
        system_content = """You are an intelligent assistant with access to various tools for file operations, code execution, and system commands.

Your task is to complete the given objectives efficiently using the available tools. Think step by step and use tools as needed.

## Role Clarification:
- You are an assistant that responds to user queries. Do NOT generate user-like questions.
- Do NOT demonstrate rules by creating example questions. Simply follow the rules when answering.
- Your responses should always be in the assistant role, never mimic user questions.

## TODO List Management Rules:
- For any complex task with 3+ distinct steps, immediately create a TODO list using `rewrite_todo_list`
- Break down the user's request into specific, actionable TODO items
- Update TODO items to 'in_progress' when starting work on them using `update_todo_status`
- Mark items as 'completed' immediately after finishing them
- Only have ONE item 'in_progress' at a time
- If you encounter errors or need to change approach, update relevant TODOs to 'cancelled' and add new ones
- Use the TODO list as your primary planning and tracking mechanism
- Reference TODO items by their ID when discussing progress

## Key Behaviors:
1. ALWAYS start complex tasks by creating a TODO list
2. Pay attention to timestamps to understand the timeline of events
3. Notice tool call numbers (e.g., "Tool call #3") to avoid repetitive loops - if you see high numbers, change strategy
4. Learn from detailed error messages to fix issues and adapt your approach
5. Be aware of your current directory and system environment shown in system state
6. When exploring projects, systematically read key files (README, main.py, agent.py) to understand structure
7. For questions about Intel CPU instructions, architecture, or technical specifications, you MUST search the knowledge base and ONLY answer based on found information. Do not rely on general knowledge or assumptions. If the information is not available, clearly state that you cannot answer based on the available knowledge.
   - Use `knowledge_base_search` to search for relevant information
   - Use `get_document` to retrieve complete documents when you need more context
   - You may need multiple searches with different queries to fully answer a question
8. **Reasoning Process**: Think step-by-step:
   - First, understand what information is needed
   - Search for relevant information
   - If needed, retrieve full documents for context
   - Synthesize the information to answer the question
   - Include proper citations
9. **Be Accurate**: Never make up information. If something is unclear or not found, say so explicitly.

## Error Handling:
- Read error messages carefully - they contain specific information about what went wrong
- Use the suggestions provided in error messages to fix issues
- If a tool fails multiple times (check the call number), try a different approach
- Common fixes: check file paths, verify current directory, ensure proper permissions

Important: When you have completed all tasks, clearly state "FINAL ANSWER:" followed by a comprehensive summary of what was accomplished."""
        
        self.conversation_history = [
            {
                "role": "system",
                "content": system_content
            }
        ]
    
    def _get_system_state(self) -> str:
        """Get current system state information"""
        if not self.config.enable_system_state:
            return ""
        
        # Detect OS
        system = platform.system()
        if system == "Windows":
            shell_type = "Windows Command Prompt or PowerShell"
        elif system == "Darwin":
            shell_type = "macOS Terminal (zsh/bash)"
        else:
            shell_type = f"Linux Shell ({os.environ.get('SHELL', 'bash')})"
        
        state_info = [
            f"Current Time: {self._get_timestamp()}",
            f"Current Directory: {self.current_directory}",
            f"System: {system} ({platform.release()})",
            f"Shell Environment: {shell_type}",
            f"Python Version: {sys.version.split()[0]}"
        ]
        
        return "\n".join(state_info)
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        if self.config.simulate_time_delay:
            # For demo: simulate time passing
            return self.simulated_time.strftime(self.config.timestamp_format)
        return datetime.now().strftime(self.config.timestamp_format)
    
    def _advance_simulated_time(self, hours: int = 0, minutes: int = 0, seconds: int = 30):
        """Advance simulated time for demo purposes"""
        if self.config.simulate_time_delay:
            self.simulated_time += timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    def _save_trajectory(self, iteration: int, final_answer: Optional[str] = None):
        """Save current trajectory to JSON file for debugging"""
        if not self.config.save_trajectory:
            return
        
        trajectory_data = {
            "timestamp": datetime.now().isoformat(),
            "iteration": iteration,
            "provider": self.provider,
            "model": self.model,
            "conversation_history": self.conversation_history,
            # Note: last_llm_messages is for debugging only - it shows what was sent to LLM
            # including system hints that are not part of the actual conversation
            "last_llm_messages": self.last_llm_messages,
            "tool_calls": [
                {
                    "tool_name": call.tool_name,
                    "arguments": call.arguments,
                    "result": call.result,
                    "error": call.error,
                    "call_number": call.call_number,
                    "timestamp": call.timestamp,
                    "duration_ms": call.duration_ms
                }
                for call in self.tool_calls
            ],
            "todo_list": [
                {
                    "id": item.id,
                    "content": item.content,
                    "status": item.status.value,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                }
                for item in self.todo_list
            ],
            "current_directory": self.current_directory,
            "final_answer": final_answer,
            "config": {
                "enable_timestamps": self.config.enable_timestamps,
                "enable_tool_counter": self.config.enable_tool_counter,
                "enable_todo_list": self.config.enable_todo_list,
                "enable_detailed_errors": self.config.enable_detailed_errors,
                "enable_system_state": self.config.enable_system_state,
                "timestamp_format": self.config.timestamp_format,
                "simulate_time_delay": self.config.simulate_time_delay
            }
        }
        
        try:
            # Save to file, overwriting each time to capture latest state
            with open(self.config.trajectory_file, 'w', encoding='utf-8') as f:
                json.dump(trajectory_data, f, indent=2, ensure_ascii=False)
            
            if self.verbose:
                logger.info(f"Trajectory saved to {self.config.trajectory_file} (iteration {iteration})")
        except Exception as e:
            logger.warning(f"Failed to save trajectory: {e}")
    
    def _format_todo_list(self) -> str:
        """Format TODO list for display"""
        if not self.todo_list:
            return "TODO List: Empty"
        
        lines = ["TODO List:"]
        for item in self.todo_list:
            status_symbol = {
                TodoStatus.PENDING: "⏳",
                TodoStatus.IN_PROGRESS: "🔄",
                TodoStatus.COMPLETED: "✅",
                TodoStatus.CANCELLED: "❌"
            }.get(item.status, "❓")
            
            lines.append(f"  [{item.id}] {status_symbol} {item.content} ({item.status.value})")
        
        return "\n".join(lines)
    
    def _get_system_hint(self, include_system_state: bool = True) -> Optional[str]:
        """Get system hint content with current state
        
        Args:
            include_system_state: Whether to include system state in the hint
        """
        if not any([self.config.enable_system_state, self.config.enable_todo_list]):
            return None
        
        hint_parts = []
        
        if self.config.enable_system_state and include_system_state:
            hint_parts.append("=== SYSTEM STATE ===")
            hint_parts.append(self._get_system_state())
            hint_parts.append("")
        
        if self.config.enable_todo_list and self.todo_list:
            hint_parts.append("=== CURRENT TASKS ===")
            hint_parts.append(self._format_todo_list())
            hint_parts.append("")
        
        if hint_parts:
            return "\n".join(hint_parts)
        return None
        
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[Any, Optional[str]]:
        """
        Execute a tool and return the result with detailed error information
        
        Returns:
            Tuple of (result, error_detail)
        """
        start_time = datetime.now()
        
        try:
            if tool_name == "read_file":
                result = read_file(**arguments, current_directory=self.current_directory)
            elif tool_name == "write_file":
                result = write_file(**arguments, current_directory=self.current_directory)
            elif tool_name == "code_interpreter":
                result = code_interpreter(**arguments)
            elif tool_name == "execute_command":
                result = execute_command(**arguments, current_directory=self.current_directory)
                # Update current directory if 'cd' command was successful
                if result.get("success") and result.get("new_directory"):
                    self.current_directory = result["new_directory"]
            elif tool_name == "rewrite_todo_list":
                result = rewrite_todo_list(**arguments, todo_list=self.todo_list, next_todo_id=self.next_todo_id)
                # Update internal state from result
                if result["success"]:
                    self.next_todo_id = result["next_todo_id"]
                    # Convert dicts back to TodoItem objects
                    self.todo_list = [
                        TodoItem(
                            id=item["id"],
                            content=item["content"],
                            status=TodoStatus(item["status"]),
                            created_at=item["created_at"],
                            updated_at=item["updated_at"]
                        )
                        for item in result["todo_list"]
                    ]
            elif tool_name == "update_todo_status":
                result = update_todo_status(**arguments, todo_list=self.todo_list)
                # Update internal state from result
                if result["success"]:
                    # Convert dicts back to TodoItem objects
                    self.todo_list = [
                        TodoItem(
                            id=item["id"],
                            content=item["content"],
                            status=TodoStatus(item["status"]),
                            created_at=item["created_at"],
                            updated_at=item["updated_at"]
                        )
                        for item in result["todo_list"]
                    ]

            elif tool_name == "knowledge_base_search":
                query = arguments.get("query", "")
                results = self.kb_tools.knowledge_base_search(query)
                
                # Log full trajectory when verbose
                if self.config.agent.verbose:
                    logger.info("=" * 80)
                    logger.info(f"TOOL EXECUTION: {tool_name}")
                    logger.info("-" * 80)
                    logger.info(f"Query: {query}")
                    logger.info("-" * 80)
                
                if not results:
                    if self.config.agent.verbose:
                        logger.info("Results: No relevant documents found")
                        logger.info("=" * 80)
                    result = {"status": "no_results", "message": "No relevant documents found"}
                else:
                    # Format results for agent - KEEP ALL RESULTS
                    formatted_results = []
                    for i, r in enumerate(results, 1):
                        formatted_results.append({
                            "doc_id": r["doc_id"],
                            "chunk_id": r["chunk_id"],
                            "text": r["text"],
                            "score": r["score"]
                        })
                        
                        # Log each result in full detail
                        if self.config.agent.verbose:
                            logger.info(f"Result {i}/{len(results)}:")
                            logger.info(f"  Document ID: {r['doc_id']}")
                            logger.info(f"  Chunk ID: {r['chunk_id']}")
                            logger.info(f"  Score: {r['score']:.4f}")
                            logger.info(f"  Text (full):\n{'-' * 40}")
                            logger.info(r['text'])
                            logger.info("-" * 40)
                    
                    if self.config.agent.verbose:
                        logger.info(f"Total results found: {len(results)}")
                        logger.info("=" * 80)
                    
                    result = {
                        "status": "success",
                        "results": formatted_results[:3],  # Limit to top 3 for LLM context
                        "total_found": len(results),
                        "all_results": formatted_results  # Keep all for logging
                    }
                
            elif tool_name == "get_document":
                doc_id = arguments.get("doc_id", "")
                
                # Log full trajectory when verbose
                if self.config.agent.verbose:
                    logger.info("=" * 80)
                    logger.info(f"TOOL EXECUTION: {tool_name}")
                    logger.info("-" * 80)
                    logger.info(f"Document ID: {doc_id}")
                    logger.info("-" * 80)
                
                document = self.kb_tools.get_document(doc_id)
                
                if "error" in document:
                    if self.config.agent.verbose:
                        logger.info(f"Error: {document['error']}")
                        logger.info("=" * 80)
                    result = {"status": "error", "message": document["error"]}
                else:
                    # Log full document content
                    if self.config.agent.verbose:
                        logger.info("Document Retrieved:")
                        logger.info(f"  Doc ID: {document.get('doc_id', doc_id)}")
                        if document.get('metadata'):
                            logger.info(f"  Metadata: {json.dumps(document['metadata'], indent=2, ensure_ascii=False)}")
                        logger.info("  Content (full):\n" + "=" * 40)
                        logger.info(document.get('content', ''))
                        logger.info("=" * 80)
                    
                    result = {
                        "status": "success",
                        "document": {
                            "doc_id": document.get("doc_id", doc_id),
                            "content": document.get("content", ""),
                            "metadata": document.get("metadata", {})
                        }
                    }

            else:
                error = f"Unknown tool: {tool_name}"
                return {"error": error}, error
            
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            logger.info(f"Tool '{tool_name}' executed in {duration_ms}ms")
            return result, None
            
        except Exception as e:
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Get detailed error information
            error_detail = self._get_detailed_error(e, tool_name, arguments)
            
            if self.config.enable_detailed_errors:
                return {"error": error_detail}, error_detail
            else:
                return {"error": str(e)}, str(e)
    
    def _get_detailed_error(self, exception: Exception, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Get detailed error information for debugging"""
        error_parts = [
            f"Tool '{tool_name}' failed with {type(exception).__name__}: {str(exception)}",
            f"Arguments: {json.dumps(arguments, indent=2)}",
        ]
        
        # Add traceback for debugging
        if self.verbose:
            tb = traceback.format_exc()
            error_parts.append(f"Traceback:\n{tb}")
        
        # Add suggestions based on error type
        suggestions = self._get_error_suggestions(exception, tool_name)
        if suggestions:
            error_parts.append(f"Suggestions: {suggestions}")
        
        return "\n".join(error_parts)
    
    def _get_error_suggestions(self, exception: Exception, tool_name: str) -> str:
        """Get suggestions for fixing common errors"""
        error_str = str(exception).lower()
        exception_type = type(exception).__name__
        
        suggestions = []
        
        if "permission" in error_str or exception_type == "PermissionError":
            suggestions.append("Check file/directory permissions")
            suggestions.append("Try using a different directory or running with appropriate permissions")
        elif "not found" in error_str or "no such file" in error_str or exception_type == "FileNotFoundError":
            suggestions.append("Verify the file/directory path exists")
            suggestions.append("Check the current working directory")
            suggestions.append("Use absolute paths or create the file/directory first")
        elif "syntax" in error_str or exception_type == "SyntaxError":
            suggestions.append("Check the code syntax")
            suggestions.append("Ensure proper indentation and valid Python syntax")
        elif "timeout" in error_str:
            suggestions.append("The operation took too long")
            suggestions.append("Try with simpler input or break into smaller steps")
        elif "import" in error_str or exception_type == "ImportError":
            suggestions.append("Required module not available in restricted environment")
            suggestions.append("Use only built-in Python modules")
        
        return " | ".join(suggestions) if suggestions else ""
    
    def execute_task(self, task: str, max_iterations: int = 20) -> Dict[str, Any]:
        """
        Execute a task using available tools with system hints
        
        Args:
            task: The task to execute
            max_iterations: Maximum number of tool calls
            
        Returns:
            Task execution result
        """
        # Add timestamp to user message if enabled
        if self.config.enable_timestamps:
            timestamp_prefix = f"[{self._get_timestamp()}] "
            task = timestamp_prefix + task
        
        # Add user message
        self.conversation_history.append({"role": "user", "content": task})
        
        iteration = 0
        final_answer = None
        consecutive_text_only = 0  # Track consecutive text-only responses
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}/{max_iterations}")
            
            # Simulate time passing for demo
            self._advance_simulated_time(seconds=5)
            
            # Save trajectory at the start of each iteration
            self._save_trajectory(iteration)
            
            try:
                # Prepare messages for the model - add system hint as last user message
                messages_to_send = self.conversation_history.copy()
                
                # Only add full system hint on first iteration or when tools were used
                # This prevents repetitive system state updates in text-only conversations
                include_full_state = (iteration == 1 or consecutive_text_only == 0)
                system_hint = self._get_system_hint(include_system_state=include_full_state)
                if system_hint:
                    messages_to_send.append({"role": "user", "content": system_hint})
                
                # Store the messages being sent to LLM for trajectory logging
                self.last_llm_messages = messages_to_send
                
                # Call the model
                print("🔥🔥🔥🔥🔥🔥🔥messages_to_send: ", messages_to_send)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages_to_send,
                    tools=get_tool_definitions(),
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=8192
                )
                
                message = response.choices[0].message
                
                # Check for final answer
                if message.content and "FINAL ANSWER:" in message.content:
                    print("🎯🎯🎯🎯🎯🎯: ", message.content)
                    final_answer = message.content.split("FINAL ANSWER:")[1].strip()
                    logger.info(f"Final answer found: {final_answer[:100]}...")
                    self.conversation_history.append(message.model_dump())
                    # Save final trajectory
                    self._save_trajectory(iteration, final_answer)
                    break
                
                # Handle tool calls
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    print("🧨🧨🧨🧨🧨🧨🧨message.tool_calls: ", message.content)
                    self.conversation_history.append(message.model_dump())
                    consecutive_text_only = 0  # Reset counter when tools are used
                    
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        # Track tool call count
                        if self.config.enable_tool_counter:
                            self.tool_call_counts[function_name] = self.tool_call_counts.get(function_name, 0) + 1
                            call_number = self.tool_call_counts[function_name]
                        else:
                            call_number = 1
                        
                        logger.info(f"Executing tool: {function_name} (call #{call_number})")
                        
                        # Print tool arguments in a concise format
                        args_str = json.dumps(function_args)
                        if len(args_str) > 200:
                            logger.info(f"  📥 Args: {args_str[:200]}...")
                        else:
                            logger.info(f"  📥 Args: {args_str}")
                        
                        # Execute the tool
                        result, error = self._execute_tool(function_name, function_args)
                        
                        # Print tool result in a concise format
                        if error:
                            error_preview = str(error).replace('\n', ' ')[:150]
                            logger.info(f"  ❌ Error: {error_preview}")
                        else:
                            if isinstance(result, dict):
                                if result.get('success'):
                                    # Show key information for successful operations
                                    if 'output' in result and result['output']:
                                        output_preview = str(result['output']).replace('\n', ' ')[:100]
                                        logger.info(f"  ✅ Success: {output_preview}...")
                                    elif 'content' in result:
                                        # Handle read_file results
                                        if result.get('partial_read'):
                                            logger.info(f"  ✅ Success: Read lines {result.get('begin_line', 1)}-{result.get('end_line', 0)} ({result.get('lines_read', 0)} lines) from {result.get('total_lines', 0)} total")
                                        else:
                                            logger.info(f"  ✅ Success: Read {result.get('lines', 0)} lines, {result.get('size_bytes', 0)} bytes")
                                    elif 'file_path' in result:
                                        logger.info(f"  ✅ Success: File operation on {result['file_path']}")
                                    else:
                                        logger.info("  ✅ Success: Operation completed")
                                elif result.get('success') is False:
                                    # Handle explicit failures (like binary file detection)
                                    if result.get('is_binary'):
                                        logger.info(f"  ⚠️ Binary file detected: {result.get('file_path', 'unknown')}")
                                    else:
                                        logger.info(f"  ⚠️ Failed: {result.get('error', 'Unknown error')[:100]}")
                                else:
                                    logger.info("  ✅ Success: Operation completed")
                            else:
                                result_preview = str(result).replace('\n', ' ')[:150]
                                logger.info(f"  ✅ Result: {result_preview}")
                        
                        # Record tool call
                        tool_call_record = ToolCall(
                            tool_name=function_name,
                            arguments=function_args,
                            result=result if not error else None,
                            error=error,
                            call_number=call_number
                        )
                        self.tool_calls.append(tool_call_record)
                        
                        # Prepare tool result message
                        tool_content = json.dumps(result)
                        
                        # Add metadata to tool result if enabled
                        metadata_parts = []
                        
                        if self.config.enable_timestamps:
                            metadata_parts.append(f"[{self._get_timestamp()}]")
                        
                        if self.config.enable_tool_counter:
                            metadata_parts.append(f"[Tool call #{call_number} for '{function_name}']")
                        
                        if metadata_parts:
                            tool_content = " ".join(metadata_parts) + "\n" + tool_content
                        
                        # Add tool result
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_content
                        })
                    
                elif message.content:
                    print("♨️♨️♨️♨️♨️♨️♨️message.content: ", message.content)
                    
                    # Clean the message content - remove any timestamp prefix that LLM might have incorrectly added
                    cleaned_content = message.content
                    # Remove timestamp pattern like "[2026-01-26 20:49:36] " from the beginning
                    import re
                    timestamp_pattern = r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] '
                    cleaned_content = re.sub(timestamp_pattern, '', cleaned_content)
                    
                    # Create cleaned message
                    cleaned_message = message.model_dump()
                    if cleaned_content != message.content:
                        logger.info(f"Cleaned timestamp from assistant message: '{message.content[:50]}...' -> '{cleaned_content[:50]}...'")
                        cleaned_message["content"] = cleaned_content
                    
                    # Regular assistant message
                    self.conversation_history.append(cleaned_message)
                    
                    # Check if we're stuck in text-only loop
                    consecutive_text_only += 1
                    if consecutive_text_only >= 3:
                        logger.warning(f"Detected {consecutive_text_only} consecutive text-only responses. Generating final answer.")
                        final_answer = cleaned_content
                        # Save final trajectory
                        self._save_trajectory(iteration, final_answer)
                        break
                    
            except Exception as e:
                logger.error(f"Error during task execution: {str(e)}")
                # Save trajectory even on error
                self._save_trajectory(iteration)
                return {
                    "error": str(e),
                    "tool_calls": self.tool_calls,
                    "iterations": iteration,
                    "trajectory_file": self.config.trajectory_file if self.config.save_trajectory else None
                }
        
        # Save final trajectory before returning
        self._save_trajectory(iteration, final_answer)
        
        return {
            "final_answer": final_answer,
            "tool_calls": self.tool_calls,
            "todo_list": [
                {
                    "id": item.id,
                    "content": item.content,
                    "status": item.status.value
                }
                for item in self.todo_list
            ],
            "iterations": iteration,
            "success": final_answer is not None,
            "trajectory_file": self.config.trajectory_file if self.config.save_trajectory else None
        }
    
    def reset(self):
        """Reset the agent's state"""
        self.tool_call_counts = {}
        self.tool_calls = []
        self.todo_list = []
        self.next_todo_id = 1
        self.current_directory = os.getcwd()
        self.simulated_time = datetime.now()
        self.last_llm_messages = None
        self._init_system_prompt()
        logger.info("Agent state reset")