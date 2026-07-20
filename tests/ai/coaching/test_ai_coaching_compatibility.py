"""
Phase 66.4 TASK 7/9 — Future Compatibility check: the brief's own named
future concepts (AI Coach/Lesson/Exercise/Homework/Daily Plan/Weekly
Plan/Monthly Goal/Certification/Academy/Voice Coach) must NOT exist as
implementation in this phase -- only the Foundation (models + CRUD
Runtime + adapters) is built. Mirrors
`tests/ai/learning/test_ai_learning_compatibility.py`'s own pattern
exactly.
"""

import pathlib

import ai.coaching.access
import ai.coaching.coaching_runtime
import ai.coaching.journal_adapter
import ai.coaching.learning_adapter
import ai.coaching.models


def _coaching_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "coaching"


def test_no_lesson_module_exists():
    assert not (_coaching_dir() / "lesson.py").exists()


def test_no_exercise_module_exists():
    assert not (_coaching_dir() / "exercise.py").exists()


def test_no_homework_module_exists():
    assert not (_coaching_dir() / "homework.py").exists()


def test_no_daily_plan_module_exists():
    assert not (_coaching_dir() / "daily_plan.py").exists()


def test_no_weekly_plan_module_exists():
    assert not (_coaching_dir() / "weekly_plan.py").exists()


def test_no_monthly_goal_module_exists():
    assert not (_coaching_dir() / "monthly_goal.py").exists()


def test_no_certification_module_exists():
    assert not (_coaching_dir() / "certification.py").exists()


def test_no_academy_module_exists():
    assert not (_coaching_dir() / "academy.py").exists()


def test_no_voice_coach_module_exists():
    assert not (_coaching_dir() / "voice_coach.py").exists()


def test_models_module_has_no_future_concept_classes():
    names = dir(ai.coaching.models)
    forbidden = {
        "Lesson", "Exercise", "Homework", "DailyPlan", "WeeklyPlan",
        "MonthlyGoal", "Certification", "Academy", "VoiceCoach", "AICoach",
    }
    assert forbidden.isdisjoint(set(names))


def test_coaching_runtime_has_no_generation_or_evaluation_method():
    from ai.coaching.coaching_runtime import CoachingRuntime
    public_methods = {name for name in dir(CoachingRuntime) if not name.startswith("_")}
    forbidden = {
        "generate_lesson", "generate_exercise", "generate_homework",
        "generate_daily_plan", "generate_weekly_plan", "generate_monthly_goal",
        "certify", "coach", "evaluate", "decide", "grade",
    }
    assert forbidden.isdisjoint(public_methods)


def test_package_only_has_the_seven_expected_files():
    expected = {
        "__init__.py", "models.py", "access.py", "coaching_runtime.py",
        "learning_adapter.py", "journal_adapter.py", "README.md",
    }
    actual = {p.name for p in _coaching_dir().iterdir() if p.is_file()}
    assert actual == expected
