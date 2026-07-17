# RAG System Integrations

## Overview

This guide documents integrations for converting various data sources into a searchable RAG system. The integration layer handles document ingestion, chunking strategies, and metadata extraction.

## Quick Reference Matrix

| Data Source         | Integration Complexity | Recommended Connector | Format Support         | Real-time Sync  |
| ------------------- | ---------------------- | --------------------- | ---------------------- | --------------- |
| Markdown files      | Easy                   | File watcher + parser | `.md` only             | Yes (polling)   |
| PDF documents       | Medium                 | PDF parser library    | `.pdf` with text layer | No (batch)      |
| Confluence/Wiki     | Medium                 | REST API connector    | Multiple formats       | Yes (webhook)   |
| SharePoint/OneDrive | Medium                 | Azure integration     | `.docx`, `.pdf`, `.md` | Polling         |
| Git repositories    | Easy                   | LFS + commit hooks    | Source files only      | Near real-time  |
| REST API endpoints  | Hard                   | Scrape + parse HTML   | HTML → markdown        | Webhook/polling |
| Database tables     | Medium                 | Direct SQL connector  | Structured data        | Yes (CDC)       |

## Integration Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        Markdown[Markdown Files]
        PDF[PDF Documents]
        Confluence[Confluence/Wiki]
        SharePoint[SharePoint/OneDrive]
        GitRepo[Git Repository]
        RESTAPI[REST API Endpoint]
        Database[SQL Database]
    end

    subgraph "Ingestion Pipeline"
        Parser[Document Parser]
        Chunker[Chunking Engine]
        Extractor[META Data Extractor]
    end

    subgraph "Vector Storage"
        IndexBuilder[Index Builder]
        VectorDB[(Vector DB)]
    end

    subgraph "Access Control"
        ACL[ACL Store]
    end

    Markdown --> Parser
    PDF --> Parser
    Confluence --> Parser
    SharePoint --> Parser
    GitRepo --> Parser
    RESTAPI --> Parser
    Database --> Parser

    Parser --> Chunker
    Chunker --> Extractor
    Extractor --> IndexBuilder
    IndexBuilder --> VectorDB
    IndexBuilder --> ACL
```

## 1. Markdown File Integration

### Simple File Watcher Implementation

```python
"""
markdown_ingest.py - Ingest markdown files into RAG system
"""
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Any


class MarkdownIngestor:
    """Ingests markdown files and creates embeddings."""

    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding = embedding_model

    async def ingest_directory(self, directory_path: str, recursive: bool = True) -> int:
        """Ingest all markdown files in a directory.

        Args:
            directory_path: Path to directory containing .md files
            recursive: Whether to recurse into subdirectories

        Returns:
            Number of document chunks created
        """
        import aiofiles
        from pathlib import PurePath

        chunk_count = 0

        # Find all markdown files
        if recursive:
            patterns = ["**/*.md"]
        else:
            patterns = ["*.md"]

        md_files = list(Path(directory_path).glob("".join(patterns)))

        for md_file in md_files:
            chunks = await self._parse_markdown(md_file)

            for i, chunk in enumerate(chunks):
                # Create embedding
                embedding = self.embedding(chunk["text"])

                # Store with metadata
                vector_id = f"{md_file.stem}_{i}"
                await self.vector_db.upsert(
                    id=vector_id,
                    embedding=embedding,
                    metadata={
                        "source": str(md_file),
                        "chunk_index": i,
                        "file_hash": chunk.get("hash", ""),
                        **chunk.get("metadata", {})
                    }
                )

                chunk_count += 1

        return chunk_count

    async def _parse_markdown(self, filepath: Path) -> List[Dict[str, Any]]:
        """Parse markdown file into chunks.

        Returns list of dicts with text, metadata, and hash.
        """
        # Read content
        content = await aiofiles.open(filepath, mode="r", encoding="utf-8")
        async for line in content:
            pass  # Load full content

        # Split into chunks (500 token overlap 100)
        chunks = self._split_into_chunks(content, chunk_size=500, overlap=100)

        return chunks
```

### File Watcher for Real-time Updates

```python
"""
file_watcher.py - Watch markdown directories for changes
"""
import asyncio
import time
from pathlib import Path
from typing import Dict


class MarkdownFileWatcher:
    """Watches markdown files and triggers re-indexing on changes."""

    def __init__(self, ingestor, poll_interval_seconds: int = 30):
        self.ingestor = ingestor
        self.poll_interval = poll_interval
        self.file_hashes: Dict[Path, str] = {}

    async def start(self, directories: List[str]):
        """Start watching directories for changes."""
        while True:
            changed_files = self._check_for_changes(directories)

            if changed_files:
                await self.ingestor.update(changed_files)

            await asyncio.sleep(self.poll_interval)

    def _check_for_changes(self, directories: List[str]) -> list:
        """Check for file changes using content hashing."""
        changed = []

        for directory in directories:
            for md_file in Path(directory).glob("*.md"):
                current_hash = self._compute_hash(md_file)
                previous_hash = self.file_hashes.get(md_file, None)

                if current_hash != previous_hash:
                    changed.append(str(md_file))
                    self.file_hashes[md_file] = current_hash

        return changed
```

### Chunking Strategy for Markdown

| Strategy             | When to Use                        | Example Use Case             |
| -------------------- | ---------------------------------- | ---------------------------- |
| **Heading-based**    | Documentation with clear hierarchy | API docs, tutorials          |
| **Fixed tokens**     | Uniform content density            | General knowledge base       |
| **Semantic split**   | Variable sentence length           | Technical documentation      |
| **Code-block aware** | Markdown with code examples        | Developer docs, README files |

### Heading-Based Chunking Example

```python
def chunk_markdown_by_headings(content: str, heading_levels: List[int] = [1, 2, 3]) -> List[Dict]:
    """Split markdown by headings for better semantic coherence."""
    import re

    chunks = []

    # Split by heading level
    patterns = {
        h_level: rf'(#{h_level}+)[ \\n]+([^\\n]+)'
            for h_level in heading_levels
    }

    sections = {}
    current_section = {"text": "", "headings": []}

    for line in content.split('\\n'):
        for level, pattern in patterns.items():
            if re.match(pattern, line):
                # Save previous section
                if current_section["text"].strip():
                    sections[level] = current_section

                # Start new section
                current_section = {
                    "headings": [line],
                    "text": ""
                }

        else:
            current_section["text"] += line + "\\n"

    # Add final section
    sections[1] = current_section

    # Process each section into chunks
    for level, section in sections.items():
        section_chunks = split_text(
            section["text"],
            chunk_size=500,
            overlap=100
        )

        for i, chunk in enumerate(section_chunks):
            chunks.append({
                "text": chunk,
                "headings": section["headings"],
                "heading_level": level
            })

    return chunks
```

## 2. PDF Document Integration

### PDF Text Extraction and Chunking

| Parser Library     | Accuracy | Speed     | Best Use Case              |
| ------------------ | -------- | --------- | -------------------------- |
| **pdfplumber**     | High     | Medium    | Tables + text extraction   |
| **PyMuPDF (fitz)** | High     | Fast      | General PDF processing     |
| **pymupdf**        | Medium   | Very fast | Quick previews             |
| **tabula-py**      | Variable | Slow      | Table-heavy documents only |

### PDF Ingestion Implementation

```python
"""
pdf_ingestor.py - Ingest PDF documents into RAG system
"""
import fitz  # PyMuPDF
from typing import List, Dict, Any


class PDFIngestor:
    """Ingests PDF documents with intelligent chunking."""

    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding = embedding_model

    async def ingest_pdf(
        self,
        pdf_path: str,
        page_range: tuple = (0, -1)  # (start, end), inclusive
    ) -> int:
        """Ingest a single PDF file.

        Args:
            pdf_path: Path to PDF file
            page_range: Tuple of (start_page, end_page), -1 means last page

        Returns:
            Number of chunks created
        """
        doc = fitz.open(pdf_path)
        start_page, end_page = page_range

        # Filter out pages with minimal text (headers/footers only)
        valid_pages = []
        for page_num in range(max(start_page, 0), min(end_page + 1, len(doc))):
            page_text = doc[page_num].get_text("text")
            if len(page_text.strip()) > 50:  # Minimum text threshold
                valid_pages.append(page_num)

        chunks_created = 0

        for page_num in valid_pages:
            page = doc[page_num]

            # Get page content with structure preserved
            content = self._extract_page_content(page, page_num)

            # Chunk the content
            chunked_content = self._chunk_pdf_content(content, chunk_size=500)

            for i, chunk in enumerate(chunked_content):
                embedding = self.embedding(chunk["text"])

                metadata = {
                    "source": f"{pdf_path}::{page_num + 1}",
                    "page_number": page_num + 1,
                    "chunk_index": i,
                    "file_hash": chunk.get("hash", ""),
                    **chunk.get("metadata", {})
                }

                await self.vector_db.upsert(
                    id=f"{pdf_path}_{page_num}_chunk_{i}",
                    embedding=embedding,
                    metadata=metadata
                )

                chunks_created += 1

        doc.close()
        return chunks_created

    def _extract_page_content(self, page, page_num: int) -> str:
        """Extract content from a PDF page preserving structure."""
        # Get text blocks with positions for semantic understanding
        blocks = page.get_text("dict", flags=fitz.PDF_TEXTFLAGS_HYPERLINKS)

        content_parts = []
        for block in blocks["blocks"]:
            lines = block.get("lines", [])
            line_texts = [line["lines"][0]["text"].strip()
                        for line in lines if line.get("lines")]

            text = "\\n\\n".join(line_texts)

            if text:
                content_parts.append({
                    "text": text,
                    "position": block.get("bbox"),
                    "height": len(block["lines"])
                })

        return "\\n\\n".join([p["text"] for p in content_parts])[:5000]  # Max 5k chars per page

    def _chunk_pdf_content(
        self,
        content: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> List[Dict[str, Any]]:
        """Split PDF content into overlapping chunks."""
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\\n\\n", "\\n", " ", ""]
        )

        return text_splitter.split_text(content)
```

## 3. Git Repository Integration

### Git LFS + Commit Hook Integration

| Feature            | Implementation Complexity | Performance Impact    | Recommended Approach              |
| ------------------ | ------------------------- | --------------------- | --------------------------------- |
| Raw source files   | Easy                      | Minimal               | Full repository indexing          |
| Git LFS objects    | Medium                    | Low (only text files) | Skip .gitattributes ignored files |
| Pull request diffs | Easy                      | Minimal               | Real-time PR monitoring           |
| Commit history     | Hard                      | High                  | Incremental indexing only         |

### Git Repository Parser

```python
"""
git_ingestor.py - Ingest git repositories into RAG system
"""
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class GitIngestor:
    """Ingests git repository contents with version awareness."""

    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding = embedding_model

    async def ingest_repository(
        self,
        repo_path: str,
        commit_hash: str = "HEAD"
    ) -> int:
        """Ingest all text files from a git repository at a specific commit.

        Args:
            repo_path: Path to git repository
            commit_hash: Git commit hash (or 'HEAD' for latest)

        Returns:
            Number of chunks created/updated
        """
        import re

        # Run git ls-tree to get file list at commit
        result = subprocess.run(
            f"git -C {repo_path} ls-tree -r --name-only {commit_hash}",
            shell=True,
            capture_output=True,
            text=True
        )

        files = [f for f in result.stdout.strip().split('\\n') if f]

        chunks_created = 0

        for file_path in files:
            file_full_path = Path(repo_path) / file_path

            # Skip binary files and git internals
            if self._is_excluded(file_path):
                continue

            try:
                content = file_full_path.read_text(encoding="utf-8")

                chunks = self._split_content(content, file_path)

                for i, chunk in enumerate(chunks):
                    embedding = self.embedding(chunk["text"])

                    # Create ID with file path for uniqueness
                    vector_id = f"{file_path}::{i}"

                    await self.vector_db.upsert(
                        id=vector_id,
                        embedding=embedding,
                        metadata={
                            "source": str(file_full_path),
                            "commit_hash": commit_hash,
                            "file_extension": file_path.split(".")[-1],
                            **chunk.get("metadata", {})
                        }
                    )

                    chunks_created += 1

            except Exception as e:
                print(f"Failed to ingest {file_path}: {e}")

        return chunks_created

    def _is_excluded(self, file_path: str) -> bool:
        """Check if file should be excluded from indexing."""
        exclude_patterns = [".git/", ".env", "*.pyc", "*.pem",
                          "__pycache__/", "node_modules/", ".DS_Store"]

        for pattern in exclude_patterns:
            if pattern in file_path:
                return True

        return False

    def _split_content(
        self,
        content: str,
        filepath: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> List[Dict[str, Any]]:
        """Split file content into chunks with metadata."""
        from langchain.text_splitter import CharacterTextSplitter

        # Create appropriate splitter based on file type
        ext = filepath.split(".")[-1] if "." in filepath else ""

        text_splitter = None
        if ext == "md":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                length_function=len,
                separators=["\\n\\n", "\\n", ".", ",", ""]
            )
        else:
            text_splitter = CharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                length_function=len,
                separators=[" ", ""]
            )

        chunks = text_splitter.split_text(content)

        return [
            {
                "text": chunk,
                "metadata": {
                    "source": str(filepath),
                    "file_extension": ext,
                    **{"path": filepath}
                }
            } for chunk in chunks
        ]
```

## 4. Confluence/Wiki Integration

### REST API Connector for Confluence

| Authentication Method     | Complexity | Recommended For           |
| ------------------------- | ---------- | ------------------------- |
| Basic Auth                | Easy       | Personal/small wiki use   |
| OAuth2 Client Credentials | Medium     | Enterprise deployment     |
| Server Token              | Easy       | Internal server-to-server |

### Confluence Ingestion Implementation

```python
"""
confluence_ingestor.py - Ingest Atlassian Confluence pages into RAG
"""
import requests
from typing import List, Dict, Any, Optional


class ConfluenceIngestor:
    """Ingests Confluence wiki pages and attachments."""

    def __init__(self, api_url: str, api_token: str,
                 space_key: str = None):
        self.api_base = f"{api_url}/rest/api/v2"
        self.token = api_token
        self.space_key = space_key

    async def ingest_space(self, space_key: Optional[str] = None) -> int:
        """Ingest all pages from a Confluence space.

        Args:
            space_key: Space key (defaults to configured value)

        Returns:
            Total number of chunks created
        """
        headers = {
            "Authorization": f"Basic {base64.b64encode(
                f'':{self.token}'.encode()).decode()}"
        }

        params = {"limit": 50}

        total_chunks = 0

        # Fetch all pages in space
        while True:
            response = requests.get(
                f"{self.api_base}/space/{space_key or self.space_key}/pages",
                headers=headers,
                params=params
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            pages = response.json()

            for page in pages:
                await self._ingest_page(page["id"], headers)

            # Check if there are more pages
            total = response.headers.get("X-Total", "0")
            if int(total) <= len(pages):
                break

            params["start"] = params.get("start", 0) + 50

        return total_chunks

    async def _ingest_page(self, page_id: str, headers: Dict[str, str]) -> int:
        """Ingest a single Confluence page."""
        chunks_created = 0

        # Get page body in storage format (HTML)
        response = requests.get(
            f"{self.api_base}/page/{page_id}",
            headers=headers,
            params={"representation": "storage"}
        )

        html_content = response.json()["body"]["value"]

        # Convert HTML to Markdown
        markdown_content = self._html_to_markdown(html_content)

        # Chunk the content
        chunks = self._chunk_markdown(markdown_content, chunk_size=500)

        for i, chunk in enumerate(chunks):
            embedding = await self.embedding(chunk["text"])

            metadata = {
                "source": f"confluence::{page_id}",
                "content_type": "wiki",
                "chunk_index": i,
                "title": response.json().get("title", ""),
                **chunk.get("metadata", {})
            }

            # Store in vector DB (assume upsert method exists)
            await self.vector_db.upsert(
                id=f"confluence_{page_id}_chunk_{i}",
                embedding=embedding,
                metadata=metadata
            )

            chunks_created += 1

        return chunks_created

    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to Markdown for RAG compatibility."""
        # Use markdownify or similar library
        import markdownify

        md = markdownify.markdownify(html, heading_style="atx")

        return md.strip()

    def _chunk_markdown(
        self,
        content: str,
        chunk_size: int = 500,
        overlap: int = 100
    ) -> List[Dict[str, Any]]:
        """Split markdown into chunks."""
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\\n\\n", "\\n", ".", ",", ""]
        )

        return [
            {"text": chunk, "metadata": {}}
            for chunk in text_splitter.split_text(content)
        ]
```

## 5. Database Integration

### SQL-to-Text Extraction for Structured Data

| Database Type | Recommended Approach          | Example Use Case       |
| ------------- | ----------------------------- | ---------------------- |
| PostgreSQL    | `to_json()` + semantic search | Database documentation |
| MySQL         | JSON columns extraction       | API response schemas   |
| MongoDB       | Native document retrieval     | NoSQL data patterns    |
| Elasticsearch | Direct vector integration     | Log analysis systems   |

### SQL Database Integration Implementation

```python
"""
sql_ingestor.py - Extract text from SQL databases for RAG
"""
from sqlalchemy import create_engine, text
from typing import List, Dict, Any


class SQLDatasetIngestor:
    """Extracts structured data and converts to searchable text."""

    def __init__(self, vector_db_client, connection_url: str):
        self.vector_db = vector_db_client
        self.engine = create_engine(connection_url)

    async def ingest_database_schema(
        self,
        database_name: str = None
    ) -> int:
        """Ingest database schema documentation.

        Args:
            database_name: Specific database (or all for PostgreSQL)

        Returns:
            Number of chunks created
        """
        chunks_created = 0

        with self.engine.connect() as conn:
            # Get table information
            result = conn.execute(
                text("""
                    SELECT
                        table_schema,
                        table_name,
                        column_name,
                        data_type,
                        is_nullable,
                        column_comment
                    FROM information_schema.columns
                    WHERE table_catalog = :database_name
                """),
                {"database_name": database_name} if database_name else {}
            )

            # Format schema as documentation
            schema_docs = []
            for row in result:
                doc_block = f"""
## Table: {row.table_schema}.{row.table_name}

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| {row.column_name} | {row.data_type} | {'Yes' if row.is_nullable else 'No'} | {row.column_comment or 'N/A'} |

"""
                schema_docs.append(doc_block.strip())

            # Split into chunks
            full_schema = "\\n".join(schema_docs)
            chunks = self._split_into_chunks(full_schema, 500)

            for i, chunk in enumerate(chunks):
                embedding = await self.embedding(chunk["text"])

                await self.vector_db.upsert(
                    id=f"schema::{i}",
                    embedding=embedding,
                    metadata={
                        "source": "database_schema",
                        "chunk_index": i
                    }
                )

                chunks_created += 1

        return chunks_created

    def _split_into_chunks(self, content: str,
                          chunk_size: int = 500) -> List[str]:
        """Simple text splitting by characters."""
        # For database schemas, simpler splitting is often better
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
```

## Integration Configuration Templates

### YAML Configuration Example

```yaml
# integration_config.yaml
integrations:
  markdown_files:
    enabled: true
    source_paths:
      - "./core-component-00/engineering/harness-engineering"
      - "./core-component-00/engineering/prompt-engineering"
    polling_interval_seconds: 30

  pdf_documents:
    enabled: false
    source_paths:
      - "./documentation/architecture.pdf"
      - "./documentation/specifications/*.pdf"

  git_repositories:
    enabled: true
    repositories:
      - path: "./core-component-00"
        commit_hash: "HEAD~3" # Last 3 commits
        exclude_patterns:
          - ".git/**"
          - "*.pyc"
          - "__pycache__/**"

  confluence:
    enabled: false
    api_url: "https://company.atlassian.net"
    api_token: "${CONFLUENCE_API_TOKEN}"
    space_keys: ["DEV", "PROD"]

  databases:
    enabled: true
    connections:
      - name: "tech_docs_db"
        connection_string: "postgresql://user:pass@localhost:5432/tech_docs"
        extract_schema_only: true
```

## Best Practices Summary

| Aspect              | Recommendation                                   | Rationale                               |
| ------------------- | ------------------------------------------------ | --------------------------------------- |
| **Chunk Size**      | 500-800 tokens for text, smaller for code        | Balances context vs retrieval precision |
| **Overlap**         | 100-200 tokens preserves continuity              | Prevents information fragmentation      |
| **Metadata**        | Always include source path and chunk index       | Enables provenance tracking             |
| **Exclusions**      | Filter PII, secrets, binary files                | Security and accuracy requirements      |
| **Update Strategy** | Incremental updates preferred over full re-index | Performance and consistency             |
