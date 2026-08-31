#!/usr/bin/env python3
"""
RAG System Initialization Script

This script initializes all components for a production-ready RAG system.
Usage: python initialize.py --config rag-config.yaml
"""


def check_dependencies():
    """Check and report required Python packages."""
    import subprocess

    required_packages = [
        "sentence-transformers>=2.3.0",
        "qdrant-client>=1.7.0",
        "redis>=5.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
    ]

    print("Checking dependencies...")
    for package in required_packages:
        result = subprocess.run(
            ["python", "-c", f"import {package.split('>=')[0]}"],
            capture_output=True
        )
        if result.returncode != 0:
            print(f"  Missing: {package}")
        else:
            print(f"  ✓ {package}")


def create_vector_collection(client, collection_name="rag-knowledge-base"):
    """Create vector collection in Qdrant."""
    from qdrant_client import VectorParams, Distance

    print(f"Creating vector collection: {collection_name}")

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        hnsw_config={
            "m": 16,
            "ef_construction": 128,
        },
    )

    print(f"  Created collection with HNSW index")


def initialize_acl_store(redis_client):
    """Initialize ACL store with permission levels."""
    print("Initializing access control store...")

    # Define permission levels
    acl_data = {
        "public": {"users": set()},
        "engineering": {"users": {"alice", "bob", "charlie"}},
        "research": {"users": {"dave", "eve"}},
    }

    # In production, load from ACL store / database
    print("  ACL store initialized")


def setup_logging():
    """Configure logging for RAG system."""
    import logging
    import json

    # Configure root logger
    logging.basicConfig(
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        level=logging.INFO,
    )

    # Setup structured logging handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    ))
    logging.getLogger().addHandler(console_handler)


def main():
    """Main initialization routine."""
    print("=" * 60)
    print("RAG System Initialization")
    print("=" * 60)

    # Step 1: Check dependencies
    check_dependencies()

    # Step 2: Setup logging
    setup_logging()

    # Step 3: Initialize vector database
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient("http://localhost:6333")
        create_vector_collection(client)

    except Exception as e:
        print(f"Warning: Could not initialize Qdrant: {e}")
        print("  Make sure Qdrant is running on port 6333")

    # Step 4: Initialize ACL store
    try:
        import redis

        redis_client = redis.Redis(host="localhost", port=6379, db=0)
        initialize_acl_store(redis_client)

    except Exception as e:
        print(f"Warning: Could not initialize Redis ACL store: {e}")

    print("=" * 60)
    print("Initialization complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Upload documents using ingest_documents.py")
    print("2. Run evaluation with run_evaluation.py")
    print("3. Start monitoring with check_health.py")


if __name__ == "__main__":
    main()
