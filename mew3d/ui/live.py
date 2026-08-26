"""Live console UI: a Claude-Code-style view of what every agent is doing right now.

Falls back to plain timestamped lines when stdout is not a terminal (logs, CI, pipes).
"""

import time

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

AGENT_ORDER = [
    "Orchestrator", "Analyst", "PromptSmith", "ImageGen",
    "Preprocessor", "MeshGen", "Judge", "Exporter",
]
AGENT_ICONS = {
    "Orchestrator": "🧠", "Analyst": "🔎", "PromptSmith": "✍️", "ImageGen": "🎨",
    "Preprocessor": "🪄", "MeshGen": "🧊", "Judge": "⚖️", "Exporter": "📦",
    "vram": "💾", "llm": "🔌",
}
STATE_STYLE = {
    "pending": ("○", "dim"),
    "running": ("●", "bold yellow"),
    "done": ("✔", "green"),
    "failed": ("✘", "red"),
}


class LiveUI:
    def __init__(self, ctx, plain: bool = False) -> None:
        self.ctx = ctx
        self.console = Console()
        self.plain = plain or not self.console.is_terminal
        self.agents: dict[str, dict] = {
            name: {"state": "pending", "activity": "", "started": None, "elapsed": None}
            for name in AGENT_ORDER
        }
        self.recent: list[str] = []
        self._live: Live | None = None
        ctx.bus.subscribe(self._on_event)

    # -- event handling -------------------------------------------------------
    def _on_event(self, ev) -> None:
        stamp = time.strftime("%H:%M:%S", time.localtime(ev.ts))
        icon = AGENT_ICONS.get(ev.agent, "·")
        line = f"[{stamp}] {icon} {ev.agent:<12} {ev.message}"

        info = self.agents.setdefault(
            ev.agent, {"state": "pending", "activity": "", "started": None, "elapsed": None}
        )
        if ev.type == "status":
            state = ev.data.get("state", "running")
            info["state"] = state
            if state == "running":
                info["started"] = ev.ts
                info["activity"] = "working..."
            else:
                info["elapsed"] = ev.data.get("elapsed")
                info["activity"] = ev.message if state == "failed" else ""
        elif ev.type in ("progress", "log", "decision", "artifact"):
            if info["state"] == "running":
                info["activity"] = ev.message

        if self.plain:
            self.console.print(line, highlight=False)
        else:
            self.recent.append(line)
            self.recent = self.recent[-12:]
            if self._live:
                self._live.update(self._render())

    # -- rendering ------------------------------------------------------------
    def _render(self):
        table = Table.grid(padding=(0, 1))
        table.add_column(width=2)
        table.add_column(width=3)
        table.add_column(width=14)
        table.add_column(ratio=1, overflow="ellipsis")
        table.add_column(width=8, justify="right")
        for name in AGENT_ORDER:
            info = self.agents[name]
            mark, style = STATE_STYLE[info["state"]]
            if info["state"] == "running" and info["started"]:
                elapsed = f"{time.time() - info['started']:.0f}s"
            elif info["elapsed"] is not None:
                elapsed = f"{info['elapsed']}s"
            else:
                elapsed = ""
            table.add_row(
                Text(mark, style=style),
                AGENT_ICONS.get(name, ""),
                Text(name, style="bold" if info["state"] == "running" else ""),
                Text(info["activity"], style="yellow" if info["state"] == "running" else "dim"),
                Text(elapsed, style="dim"),
            )
        header = Text(f" Mew3D · {self.ctx.run_id}", style="bold cyan")
        events_panel = Panel(
            Text("\n".join(self.recent), no_wrap=True, overflow="ellipsis"),
            title="events", border_style="dim", height=14,
        )
        return Panel(Group(header, Text(), table, Text(), events_panel),
                     border_style="cyan")

    # -- lifecycle ------------------------------------------------------------
    def __enter__(self):
        if not self.plain:
            self._live = Live(
                self._render(), console=self.console, refresh_per_second=6,
                vertical_overflow="visible",
            )
            self._live.__enter__()
        return self

    def __exit__(self, *exc):
        if self._live:
            self._live.update(self._render())
            self._live.__exit__(*exc)
            self._live = None
        return False
