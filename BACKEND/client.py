import requests

SERVER_URL = "https://mcp-server-r967.onrender.com"

def list_tools():
    url = f"{SERVER_URL}/listTools"
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json={}, headers=headers)
    resp.raise_for_status()
    return resp.json()

def call_tool(name, arguments):
    url = f"{SERVER_URL}/callTool"
    payload = {"name": name, "arguments": arguments}
    print("DEBUG payload:", {"name": name, "arguments": arguments})
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
