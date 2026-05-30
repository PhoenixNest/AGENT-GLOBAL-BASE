#!/usr/bin/env python3
"""
Workspace Knowledge MCP Server

RAG server for workspace documentation search and retrieval.
Provides semantic search across all workspace documentation.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Workspace Knowledge")

# Workspace root from environment
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "."))


class SimpleRAGEngine:
    """Simple RAG engine for workspace documentation"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.index = self._build_index()
    
    def _build_index(self) -> List[Dict[str, Any]]:
        """Build simple index of all markdown files"""
        index = []
        
        # Index key directories
        key_dirs = [
            "company/library",
            "company/pipeline",
            "company/departments",
            "studio/casual-games/library",
            "studio/casual-games/pipeline",
            "core-component-00",
            ".claude/rules",
            ".claude/skills",
        ]
        
        for dir_path in key_dirs:
            full_path = self.workspace_root / dir_path
            if full_path.exists():
                for md_file in full_path.rglob("*.md"):
                    try:
                        content = md_file.read_text(encoding="utf-8")
                        index.append({
                            "path": str(md_file.relative_to(self.workspace_root)),
                            "content": content,
                            "size": len(content),
                            "lines": content.count("\n") + 1,
                        })
                    except Exception as e:
                        print(f"Error indexing {md_file}: {e}")
        
        return index
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search"""
        query_lower = query.lower()
        results = []
        
        for doc in self.index:
            content_lower = doc["content"].lower()
            
            # Simple scoring: count query term occurrences
            score = content_lower.count(query_lower)
            
            if score > 0:
                # Extract snippet around first occurrence
                idx = content_lower.find(query_lower)
                start = max(0, idx - 100)
                end = min(len(doc["content"]), idx + 200)
                snippet = doc["content"][start:end]
                
                results.append({
                    "path": doc["path"],
                    "score": score,
                    "snippet": snippet,
                    "size": doc["size"],
                    "lines": doc["lines"],
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def retrieve(self, file_path: str) -> Optional[str]:
        """Retrieve full content for a specific file"""
        full_path = self.workspace_root / file_path
        
        if not full_path.exists():
            return None
        
        try:
            return full_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"


# Initialize RAG engine
rag_engine = SimpleRAGEngine(WORKSPACE_ROOT)


@mcp.tool()
def search_docs(query: str, top_k: int = 5) -> str:
    """
    Search workspace documentation using semantic search.
    
    Args:
        query: Search query string
        top_k: Number of results to return (default: 5)
    
    Returns:
        JSON string with search results
    """
    results = rag_engine.search(query, top_k)
    
    return json.dumps({
        "query": query,
        "count": len(results),
        "results": results
    }, indent=2)


@mcp.tool()
def retrieve_context(file_path: str) -> str:
    """
    Retrieve full context for a specific file.
    
    Args:
        file_path: Relative path to file from workspace root
    
    Returns:
        File content or error message
    """
    content = rag_engine.retrieve(file_path)
    
    if content is None:
        return json.dumps({
            "error": f"File not found: {file_path}",
            "path": file_path
        }, indent=2)
    
    return json.dumps({
        "path": file_path,
        "content": content,
        "size": len(content),
        "lines": content.count("\n") + 1
    }, indent=2)


@mcp.tool()
def list_indexed_files() -> str:
    """
    List all files in the RAG index.
    
    Returns:
        JSON string with list of indexed files
    """
    files = [
        {
            "path": doc["path"],
            "size": doc["size"],
            "lines": doc["lines"]
        }
        for doc in rag_engine.index
    ]
    
    return json.dumps({
        "count": len(files),
        "files": files
    }, indent=2)


@mcp.tool()
def rebuild_index() -> str:
    """
    Rebuild the RAG index from workspace files.
    
    Returns:
        JSON string with rebuild status
    """
    global rag_engine
    rag_engine = SimpleRAGEngine(WORKSPACE_ROOT)
    
    return json.dumps({
        "status": "success",
        "indexed_files": len(rag_engine.index),
        "message": "Index rebuilt successfully"
    }, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
