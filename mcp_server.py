"""MCP Server for Tapestry DOLR Skill."""
import json
import sys
from client import TapestryRouter

def main():
    router = TapestryRouter("PRIMARY_ROUTER")
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "publish_object",
                                "description": "Publish object pointer into DOLR mesh",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "object_id": {"type": "string"},
                                        "server_id": {"type": "string"}
                                    },
                                    "required": ["object_id", "server_id"]
                                }
                            },
                            {
                                "name": "route_object",
                                "description": "Find closest server hosting object",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"object_id": {"type": "string"}},
                                    "required": ["object_id"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "publish_object":
                    router.publish_object(args["object_id"], args["server_id"])
                    out = {"status": "published"}
                else:
                    h = router.route_to_object(args["object_id"])
                    out = {"hosting_server": h}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
