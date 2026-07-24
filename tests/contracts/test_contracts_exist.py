"""
Phase A17 -- Module Contracts foundation tests.

Pure filesystem/text checks -- this phase adds no production code, so
these tests import nothing from context/, strategies/, signals/, ai/,
decision/, risk/, execution/, telegram/, or database/. They verify
the documentation deliverable itself: every contract file exists, is
well-formed markdown, follows the required section format, and
actually states its forbidden dependencies -- not that the real code
still matches the contract (see contracts/README.md's "What this is
NOT" section for why that's a human/agent documentation-update step,
not a CI-enforceable check).
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = REPO_ROOT / "contracts"

# The nine layer contracts sharing the identical 8-section format
# (# Module Name / ## Responsibility / ## Input / ## Output /
# ## Allowed Dependencies / ## Forbidden Dependencies /
# ## Error Contract / ## Future Extension).
MODULE_CONTRACT_FILES = (
    "context_contract.md",
    "strategy_contract.md",
    "signal_contract.md",
    "ai_contract.md",
    "decision_contract.md",
    "risk_contract.md",
    "execution_contract.md",
    "telegram_contract.md",
    "database_contract.md",
)

# error_contract.md is cross-cutting (no per-module Input/Output) --
# checked separately for its own required sections.
ERROR_CONTRACT_FILE = "error_contract.md"

REQUIRED_MODULE_SECTIONS = (
    "## Responsibility",
    "## Input",
    "## Output",
    "## Allowed Dependencies",
    "## Forbidden Dependencies",
    "## Error Contract",
    "## Future Extension",
)

REQUIRED_ERROR_CONTRACT_SECTIONS = (
    "## Responsibility",
    "## Allowed Dependencies",
    "## Forbidden Dependencies",
    "## Error Contract",
    "## Future Extension",
)


def _read(filename: str) -> str:
    return (CONTRACTS_DIR / filename).read_text(encoding="utf-8")


def test_contracts_directory_exists():
    assert CONTRACTS_DIR.is_dir()


def test_contracts_readme_exists():
    assert (CONTRACTS_DIR / "README.md").is_file()


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES)
def test_module_contract_file_exists(filename):
    assert (CONTRACTS_DIR / filename).is_file(), f"{filename} is missing from contracts/"


def test_error_contract_file_exists():
    assert (CONTRACTS_DIR / ERROR_CONTRACT_FILE).is_file()


def test_docs_module_contracts_exists():
    assert (REPO_ROOT / "docs" / "MODULE_CONTRACTS.md").is_file()


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES)
def test_module_contract_has_all_required_sections(filename):
    content = _read(filename)
    for section in REQUIRED_MODULE_SECTIONS:
        assert section in content, f"{filename} is missing the '{section}' section"


def test_error_contract_has_all_required_sections():
    content = _read(ERROR_CONTRACT_FILE)
    for section in REQUIRED_ERROR_CONTRACT_SECTIONS:
        assert section in content, f"{ERROR_CONTRACT_FILE} is missing the '{section}' section"


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES)
def test_module_contract_starts_with_h1_title(filename):
    content = _read(filename)
    first_line = content.strip().splitlines()[0]
    assert first_line.startswith("# "), f"{filename} must start with a '# Module Name' H1 heading"
    assert not first_line.startswith("## "), f"{filename}'s first line must be an H1, not H2"


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES + (ERROR_CONTRACT_FILE, "README.md"))
def test_markdown_code_fences_are_balanced(filename):
    content = _read(filename)
    fence_count = len(re.findall(r"^```", content, flags=re.MULTILINE))
    assert fence_count % 2 == 0, f"{filename} has an unbalanced code fence (``` count={fence_count})"


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES)
def test_forbidden_dependencies_are_actually_documented(filename):
    """Every module contract's Forbidden Dependencies section must name at least one real forbidden module, not be empty."""
    content = _read(filename)
    section_match = re.search(
        r"## Forbidden Dependencies\n(.*?)(?=\n## |\Z)", content, flags=re.DOTALL
    )
    assert section_match is not None, f"{filename}'s Forbidden Dependencies section could not be parsed"
    section_body = section_match.group(1).strip()
    assert section_body, f"{filename}'s Forbidden Dependencies section is empty"
    assert "❌" in section_body, f"{filename}'s Forbidden Dependencies section has no ❌ bullet"


@pytest.mark.parametrize("filename", MODULE_CONTRACT_FILES)
def test_allowed_dependencies_are_documented(filename):
    content = _read(filename)
    section_match = re.search(
        r"## Allowed Dependencies\n(.*?)(?=\n## |\Z)", content, flags=re.DOTALL
    )
    assert section_match is not None, f"{filename}'s Allowed Dependencies section could not be parsed"
    section_body = section_match.group(1).strip()
    assert section_body, f"{filename}'s Allowed Dependencies section is empty"


def test_module_contracts_doc_has_architecture_map_and_dependency_table():
    content = (REPO_ROOT / "docs" / "MODULE_CONTRACTS.md").read_text(encoding="utf-8")
    assert "## Architecture map" in content
    assert "## Dependency rules" in content
    assert "```" in content  # the architecture-map diagram
    assert "|---|---|---|" in content or "| Module | May depend on" in content  # the dependency table


def test_every_module_contract_is_referenced_from_readme():
    readme = (CONTRACTS_DIR / "README.md").read_text(encoding="utf-8")
    for filename in MODULE_CONTRACT_FILES + (ERROR_CONTRACT_FILE,):
        assert filename in readme, f"contracts/README.md does not reference {filename}"
