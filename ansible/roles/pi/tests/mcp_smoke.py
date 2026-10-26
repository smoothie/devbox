import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import threading


class McpClient:
    def __init__(self, command):
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        self.messages = queue.Queue()
        self.counter = 0
        threading.Thread(target=self.receive, daemon=True).start()
        self.request("initialize", {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "devbox-smoke", "version": "1.0.0"},
        })
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def receive(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except json.JSONDecodeError:
                continue

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params):
        self.counter += 1
        self.send({"jsonrpc": "2.0", "id": self.counter, "method": method, "params": params})
        while True:
            message = self.messages.get(timeout=90)
            if message.get("id") == self.counter:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message["result"]

    def call(self, name, arguments):
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()


def verify_packages(agent_dir):
    settings = json.loads((agent_dir / "settings.json").read_text())
    sources = [item if isinstance(item, str) else item["source"] for item in settings["packages"]]
    for name in ["npm:@tintinweb/pi-tasks", "npm:@tintinweb/pi-subagents"]:
        assert sum(source == name or source.startswith(name + "@") for source in sources) == 1, sources
    print("PASS Pi packages: task and subagent configured exactly once")


def verify_sqlite(bin_dir, agent_dir):
    client = McpClient([str(bin_dir / "dbhub"), "--transport", "stdio", "--config",
                        str(agent_dir / "databases/sqlite.toml")])
    try:
        tools = client.request("tools/list", {})["tools"]
        names = {tool["name"] for tool in tools}
        assert "execute_sql" in names
        assert "search_objects" in names
        result = client.call("execute_sql", {"sql": "SELECT 42 AS answer"})
        assert not result.get("isError"), result
        assert "42" in json.dumps(result), result
        rejected = client.call("execute_sql", {"sql": "CREATE TABLE pi_smoke_forbidden (id INTEGER)"})
        assert rejected.get("isError"), rejected
        print("PASS SQLite: SELECT and read-only rejection")
    finally:
        client.close()


def verify_browser(bin_dir):
    client = McpClient([str(bin_dir / "agent-browser"), "mcp"])
    try:
        result = client.call("agent_browser_open", {"url": "https://example.com", "session": "pi-mcp-smoke"})
        assert not result.get("isError"), result
        result = client.call("agent_browser_get_title", {"session": "pi-mcp-smoke"})
        assert not result.get("isError"), result
        assert "Example Domain" in json.dumps(result), result
        print("PASS agent-browser MCP: navigate and get title")
    finally:
        try:
            client.call("agent_browser_close", {"session": "pi-mcp-smoke"})
        finally:
            client.close()


def verify_context7(bin_dir):
    client = McpClient([str(bin_dir / "context7-mcp")])
    try:
        tools = client.request("tools/list", {})["tools"]
        names = {tool["name"] for tool in tools}
        assert {"resolve-library-id", "query-docs"} <= names
        print("PASS Context7: initialize and discover documentation tools")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin-dir", type=Path, default=Path.home() / ".local/bin")
    parser.add_argument("--agent-dir", type=Path, default=Path.home() / ".pi/agent")
    args = parser.parse_args()
    os.environ["AGENT_BROWSER_CONTENT_BOUNDARIES"] = "1"
    verify_packages(args.agent_dir)
    verify_sqlite(args.bin_dir, args.agent_dir)
    verify_browser(args.bin_dir)
    verify_context7(args.bin_dir)
