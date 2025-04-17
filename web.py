from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from classes.FileFormat import JSON
from utils.parsers import parse_dict

app = FastAPI()


def f() -> str:
    return f"""\
<!DOCTYPE html>
<html>
    <head>
        <title>SN P String Computations</title>
    </head>
    <body>
        <h1>SN P String Computations</h1>
        <div style="display: flex; gap: 2em;">
            <div>
                <input type="text" id="systemName" placeholder="Type a system name"/>
                <button onclick="sendSystem()">Send</button>
                <pre id="system"></pre>
            </div>
            <div>
                <textarea id="inputs" placeholder="Type some inputs" rows=10></textarea>
                <button onclick="sendInputs()">Send</button>
                <pre id="results"></pre>
            </div>
        </div>
        <script>
            let ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {{
                let [a, b] = event.data.split("|");
                if (a === "system") {{
                    let preEl = document.getElementById('system');
                    preEl.innerText = b;
                }} else {{ 
                    let resultsEl = document.getElementById('results');
                    resultsEl.innerText = b;
                }}
            }};
            function sendSystem() {{
                let input = document.getElementById("systemName");
                ws.send(`systemName|${{input.value}}`);
            }}
            function sendInputs() {{
                let textarea = document.getElementById("inputs");
                ws.send(`inputs|${{textarea.value}}`);
            }}
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(f())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        path = ""
        s = ""

        while True:
            data = await websocket.receive_text()
            kind, val = data.split("|")
            if kind == "systemName":
                path = f"./data/json/{val}.json"
                try:
                    with open(path, "r") as f:
                        s = f.read()
                except:
                    s = "?"
                    path = ""
                await websocket.send_text(f"system|{s}")
            elif kind == "inputs":
                if len(path) > 0:
                    lines = val.splitlines()
                    w = max(len(line) for line in lines)
                    xs = [*map(int, lines)]
                    results = []

                    d = JSON().str_to_dict(s)
                    sys = parse_dict(d)

                    def g(n: int) -> bool:
                        for ans in sys.get_configs(n + 1, det=False, lazy=True):
                            if ans.get_spike_distance() == n:
                                return True
                        return False

                    for x in xs:
                        results.append(
                            f"{x:<{w+1}} is {'ACCEPTED' if g(x) else 'REJECTED'}"
                        )

                    await websocket.send_text(f"inputs|{'\n'.join(results)}")
                else:
                    await websocket.send_text(f"inputs|no system found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # This runs when the connection closes
        print("WebSocket connection closed")

