"""Offline self-check: syntax and local environment-based connection parsing."""
from pathlib import Path
import ast
import os
from unittest.mock import patch
import mcp_client

root=Path(__file__).resolve().parent
for file in root.glob('*.py'):
    ast.parse(file.read_text('utf-8'),filename=str(file))
with patch.dict(os.environ,{'MCP_URL':'http://127.0.0.1:9999/mcp/','MCP_AUTHORIZATION':'local-fixture','MCP_CONFIG':str(root/'nonexistent.local.json')},clear=True):
    url,headers=mcp_client.connection()
    assert url=='http://127.0.0.1:9999/mcp/'
    assert headers['Authorization']=='local-fixture'
print('Offline checks passed. No network request or CMS write performed.')
