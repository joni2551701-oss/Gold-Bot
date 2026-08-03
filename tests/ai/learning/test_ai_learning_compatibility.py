"""
Phase 66.3 TASK 8/9 — Future Compatibility check: the brief's own named
future concepts (Quiz/Lesson/Exercise/Homework/Video/Replay/Practice/
Progress/Certificate) must NOT exist as implementation in this phase
-- "Faqat architecture tayyor. Implementatsiya yo'q" (only the
architecture is ready, no implementation).
"""

import pathlib

import ai_layer.knowledge_ai.learning_engine.access
import ai_layer.knowledge_ai.learning_engine.journal_adapter
import ai_layer.knowledge_ai.learning_engine.learning_runtime
import ai_layer.knowledge_ai.learning_engine.memory_adapter
import ai_layer.knowledge_ai.learning_engine.models


def _learning_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "knowledge_ai" / "learning_engine"


def test_no_quiz_module_exists():
    assert not (_learning_dir() / "quiz.py").exists()


def test_no_lesson_module_exists():
    assert not (_learning_dir() / "lesson.py").exists()


def test_no_exercise_module_exists():
    assert not (_learning_dir() / "exercise.py").exists()


def test_no_homework_module_exists():
    assert not (_learning_dir() / "homework.py").exists()


def test_no_video_module_exists():
    assert not (_learning_dir() / "video.py").exists()


def test_no_replay_module_exists():
    assert not (_learning_dir() / "replay.py").exists()


def test_no_practice_module_exists():
    assert not (_learning_dir() / "practice.py").exists()


def test_no_progress_module_exists():
    assert not (_learning_dir() / "progress.py").exists()


def test_no_certificate_module_exists():
    assert not (_learning_dir() / "certificate.py").exists()


def test_models_module_has_no_quiz_or_lesson_class():
    names = dir(ai_layer.knowledge_ai.learning_engine.models)
    forbidden = {"Quiz", "Lesson", "Exercise", "Homework", "Video", "Replay", "Practice", "Progress", "Certificate"}
    assert forbidden.isdisjoint(set(names))


def test_learning_runtime_has_no_quiz_or_lesson_method():
    from ai_layer.knowledge_ai.learning_engine.learning_runtime import LearningRuntime
    public_methods = {name for name in dir(LearningRuntime) if not name.startswith("_")}
    forbidden = {"generate_quiz", "generate_lesson", "grade", "coach", "evaluate"}
    assert forbidden.isdisjoint(public_methods)


def test_package_only_has_the_six_expected_files():
    # .py only: module folders now also hold their canonical documents.
    expected = {"__init__.py", "models.py", "access.py", "learning_runtime.py", "journal_adapter.py", "memory_adapter.py"}
    actual = {p.name for p in _learning_dir().iterdir() if p.is_file() and p.suffix == ".py"}
    assert actual == expected
