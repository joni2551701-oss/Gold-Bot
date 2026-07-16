"""
AI Layer — Education Tool (Phase 61.0, TASK 8; real logic Phase 61.3,
TASK 4).

Queries `knowledge/registry.py` (Phase 61.3, TASK 3) by key or free-text
search -- `knowledge/` has zero dependencies of its own, so this is the
only tool in this package with no cross-layer boundary to reason about.
"""

from typing import Optional

from ai.tools.tool_registry import BaseAITool, ToolResult
from knowledge.registry import get_entry, search


class EducationTool(BaseAITool):
    @property
    def name(self) -> str:
        return "education_tool"

    @property
    def description(self) -> str:
        return "Answers educational/how-it-works questions by looking up knowledge/ entries."

    def run(self, key: Optional[str] = None, query: Optional[str] = None, **kwargs) -> ToolResult:
        if key:
            entry = get_entry(key)
            if entry is None:
                return ToolResult(
                    content=f"No knowledge entry found for key '{key}'.",
                    metadata={"tool": self.name, "match_count": 0},
                )
            return ToolResult(
                content=f"{entry.title}: {entry.summary}",
                metadata={"tool": self.name, "match_count": 1, "category": entry.category.value},
            )

        if query:
            results = search(query)
            if not results:
                return ToolResult(
                    content=f"No knowledge entries matched '{query}'.",
                    metadata={"tool": self.name, "match_count": 0},
                )
            content = "\n".join(f"{entry.title}: {entry.summary}" for entry in results)
            return ToolResult(
                content=content,
                metadata={"tool": self.name, "match_count": len(results)},
            )

        return ToolResult(
            content="No key or query was supplied to this tool call.",
            metadata={"tool": self.name, "match_count": 0},
        )
