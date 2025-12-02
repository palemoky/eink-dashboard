"""Tests for TODO providers and markdown parsing.

Tests cover:
- Markdown parsing with various formats
- Config-based TODO retrieval
- Gist-based TODO retrieval (mocked)
- Error handling and fallback behavior
"""

import pytest

from src.providers.todo import (
    get_todo_from_config,
    get_todo_lists,
    parse_markdown_todo,
)


class TestMarkdownParsing:
    """Test markdown TODO parsing with various formats."""

    def test_simple_list_format(self):
        """Test parsing simple list format."""
        content = """
## Goals
- English Practice
- Gym Workout

## Must
- Fix bug #123
- Review PR

## Optional
- Read docs
"""
        goals, must, optional = parse_markdown_todo(content)
        assert goals == ["English Practice", "Gym Workout"]
        assert must == ["Fix bug #123", "Review PR"]
        assert optional == ["Read docs"]

    def test_github_task_list_format(self):
        """Test parsing GitHub task list format with checkboxes."""
        content = """
# Goals
- [ ] Python
- [x] Rust

# Must
- [ ] Fix bug
- [ ] Review code

# Optional
- [ ] Refactor
"""
        goals, must, optional = parse_markdown_todo(content)

        # Verify parsing - completed items should have ✓ marker
        assert goals == ["Python", "✓Rust"]
        assert must == ["Fix bug", "Review code"]
        assert optional == ["Refactor"]

    def test_mixed_format(self):
        """Test parsing mixed format (simple + task list)."""
        content = """
## Goals
- [ ] Task with checkbox
- Regular item
* Item with asterisk

## Must
- [x] Completed task
- Pending task

## Optional
- [ ] Optional task
"""
        goals, must, optional = parse_markdown_todo(content)
        assert len(goals) == 3
        assert "Task with checkbox" in goals
        assert "Regular item" in goals
        assert "Item with asterisk" in goals
        assert len(must) == 2
        assert "✓Completed task" in must
        assert "Pending task" in must
        assert len(optional) == 1
        assert "Optional task" in optional

    def test_case_insensitive_headers(self):
        """Test case insensitive section headers."""
        content = """
# GOALS
- Item 1

## must
- Item 2

# optional
- Item 3
"""
        goals, must, optional = parse_markdown_todo(content)
        assert goals == ["Item 1"]
        assert must == ["Item 2"]
        assert optional == ["Item 3"]

    def test_typo_tolerant_headers(self):
        """Test typo-tolerant section headers (e.g., 'Optinal' instead of 'Optional')."""
        content = """
# Goals
- Goal item

# Must
- Must item

# Optinal
- Optional item
"""
        goals, must, optional = parse_markdown_todo(content)
        assert goals == ["Goal item"]
        assert must == ["Must item"]
        assert optional == ["Optional item"]

    def test_single_and_double_hash(self):
        """Test both single (#) and double (##) hash headers."""
        content = """
# Goals
- Goal 1

## Must
- Must 1

# Optional
- Optional 1
"""
        goals, must, optional = parse_markdown_todo(content)
        assert len(goals) == 1
        assert len(must) == 1
        assert len(optional) == 1

    def test_empty_sections(self):
        """Test parsing with empty sections."""
        content = """
## Goals

## Must
- Must item

## Optional
"""
        goals, must, optional = parse_markdown_todo(content)
        assert goals == []
        assert must == ["Must item"]
        assert optional == []

    def test_no_sections(self):
        """Test parsing content with no valid sections."""
        content = """
Some random text
- Item without section
* Another item
"""
        goals, must, optional = parse_markdown_todo(content)
        assert goals == []
        assert must == []
        assert optional == []

    def test_uppercase_checkbox(self):
        """Test parsing with uppercase [X] checkbox."""
        content = """
# Goals
- [X] Completed with uppercase
- [ ] Not completed
"""
        goals, must, optional = parse_markdown_todo(content)

        # Both [x] and [X] should be recognized as completed (with ✓ marker)
        assert goals == ["✓Completed with uppercase", "Not completed"]

    def test_real_world_example(self):
        """Test parsing a real-world example."""
        content = """
# Goals
- [ ] English Practice (Daily)
- [x] Gym Workout

# Must
- [ ] Fix authentication bug
- [ ] Review PR #456
- Deploy to production

## Optional
- Read Rust documentation
- [ ] Refactor legacy code
"""
        goals, must, optional = parse_markdown_todo(content)

        # Verify all sections parsed correctly
        # Completed items should have ✓ marker
        assert len(goals) == 2
        assert "English Practice (Daily)" in goals
        assert "✓Gym Workout" in goals
        assert len(must) == 3
        assert "Fix authentication bug" in must
        assert "Review PR #456" in must
        assert "Deploy to production" in must
        assert len(optional) == 2
        assert "Read Rust documentation" in optional
        assert "Refactor legacy code" in optional


class TestConfigTODO:
    """Test config-based TODO retrieval."""

    def test_get_todo_from_config(self, monkeypatch):
        """Test getting TODO from config."""
        from src.config import Config

        # Mock the todo config group with correct field names
        monkeypatch.setattr(Config.todo, "list_goals", ["Goal 1", "Goal 2"])
        monkeypatch.setattr(Config.todo, "list_must", ["Must 1"])
        monkeypatch.setattr(Config.todo, "list_optional", ["Optional 1", "Optional 2"])

        goals, must, optional = get_todo_from_config()

        assert goals == ["Goal 1", "Goal 2"]
        assert must == ["Must 1"]
        assert optional == ["Optional 1", "Optional 2"]


class TestTODOIntegration:
    """Test TODO provider integration and fallback behavior."""

    @pytest.mark.asyncio
    async def test_get_todo_lists_config_source(self, monkeypatch):
        """Test get_todo_lists with config source."""
        from src.config import Config

        monkeypatch.setattr(Config.todo, "source", "config")
        monkeypatch.setattr(Config.todo, "list_goals", ["Config Goal"])
        monkeypatch.setattr(Config.todo, "list_must", ["Config Must"])
        monkeypatch.setattr(Config.todo, "list_optional", ["Config Optional"])

        goals, must, optional = await get_todo_lists()

        assert goals == ["Config Goal"]
        assert must == ["Config Must"]
        assert optional == ["Config Optional"]

    @pytest.mark.asyncio
    async def test_get_todo_lists_invalid_source_fallback(self, monkeypatch):
        """Test fallback to config when invalid source is specified."""
        from src.config import Config

        monkeypatch.setattr(Config.todo, "source", "invalid_source")
        monkeypatch.setattr(Config.todo, "list_goals", ["Fallback Goal"])
        monkeypatch.setattr(Config.todo, "list_must", ["Fallback Must"])
        monkeypatch.setattr(Config.todo, "list_optional", ["Fallback Optional"])

        goals, must, optional = await get_todo_lists()

        # Should fall back to config
        assert goals == ["Fallback Goal"]
        assert must == ["Fallback Must"]
        assert optional == ["Fallback Optional"]
