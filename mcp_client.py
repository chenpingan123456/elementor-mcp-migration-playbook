"""Generic MCP discovery client. Credentials stay in local configuration."""
from pathlib import Path
import json
import os
import tomllib
import requests


def connection():
    config_path=Path(os.getenv('MCP_CONFIG') or str(Path.home()/'.codex/config.toml'))
    name=os.getenv('MCP_SERVER','elementor')
    server={}
    if config_path.exists():
        config=tomllib.loads(config_path.read_text('utf-8-sig'))
        server=dict(config.get('mcp_servers',{}).get(name,{}))
    url=os.getenv('MCP_URL') or server.get('url')
    headers=dict(server.get('headers',{}))
    headers.update(server.get('http_headers',{}))
    if os.getenv('MCP_AUTHORIZATION'):
        headers['Authorization']=os.environ['MCP_AUTHORIZATION']
    if not url:
        raise RuntimeError('Set MCP_URL or configure the local server selected by MCP_SERVER.')
    return url,headers


class MCP:
    def __init__(self):
        self.url,headers=connection()
        self.session=requests.Session()
        self.session.headers.update(headers)
        self.session.headers.update({'Accept':'application/json, text/event-stream','Content-Type':'application/json'})
        self.counter=0
        self.rpc('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'elementor-mcp-playbook','version':'1.0.0'}})
        self.session.post(self.url,json={'jsonrpc':'2.0','method':'notifications/initialized'},timeout=60).raise_for_status()

    def rpc(self,method,params):
        self.counter+=1
        response=self.session.post(self.url,json={'jsonrpc':'2.0','id':self.counter,'method':method,'params':params},timeout=60)
        response.raise_for_status()
        if response.headers.get('Mcp-Session-Id'):
            self.session.headers['Mcp-Session-Id']=response.headers['Mcp-Session-Id']
        if method=='initialize':
            self.session.headers['MCP-Protocol-Version']='2025-11-25'
        if response.text.lstrip().startswith('{'):
            data=response.json()
        else:
            events=[json.loads(line[5:].strip()) for line in response.text.splitlines() if line.startswith('data:')]
            data=next(event for event in events if event.get('id')==self.counter)
        if 'error' in data:
            raise RuntimeError('MCP error code: '+str(data['error'].get('code')))
        return data['result']


def main():
    client=MCP()
    tools=client.rpc('tools/list',{}).get('tools',[])
    print(json.dumps({'tools':[tool['name'] for tool in tools]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
