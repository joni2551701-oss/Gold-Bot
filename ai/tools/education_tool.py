"""AI Layer — Education Tool (Phase 61.0, TASK 8). Interface only -- does not call database/ or any content store."""

from ai.tools.tool_registry import BaseAITool, ToolResult


class EducationTool(BaseAITool):
    @property
    def name(self) -> str:
        return "education_tool"

    @property
    def description(self) -> str:
        return "Would answer educational/how-it-works questions for the AI layer. Placeholder -- no real content source yet."

    def run(self, **kwargs) -> ToolResult:
        return ToolResult(content="[education_tool] placeholder -- no real content source yet.", metadata={"tool": self.name})
