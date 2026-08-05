# Learning Layer Sequence Diagram

## Overview

Learning Layer foydalanuvchini boshlang'ich bilim darajasidan Professional Trader darajasigacha bosqichma-bosqich rivojlantirish uchun mo'ljallangan.

Ushbu hujjat Learning Layer ichidagi asosiy Sequence Diagramlarni tavsiflaydi.

---

# Main Learning Sequence

```
User
 │
 ▼
Learning API
 │
 ▼
Learning Path
 │
 ▼
Curriculum
 │
 ▼
Academy
 │
 ▼
Lesson
 │
 ▼
Assessment
 │
 ├────────────── PASS ──────────────┐
 │                                  │
 │                                  ▼
 │                           Progress Update
 │                                  │
 │                                  ▼
 │                            Next Lesson
 │
 └────────────── FAIL ──────────────┐
                                    │
                                    ▼
                              AI Coach
                                    │
                                    ▼
                               Recommendation
                                    │
                                    ▼
                              Retry Lesson
```

---

# AI Coach Sequence

```
Lesson Finished
        │
        ▼
Assessment
        │
        ▼
AI Coach
        │
        ├── Analyze Mistakes
        ├── Explain Errors
        ├── Give Feedback
        ├── Recommend Lesson
        └── Create Practice
        │
        ▼
User
```

---

# Simulator Sequence

```
User
 │
 ▼
Simulator
 │
 ▼
Virtual Trading
 │
 ▼
Trade Result
 │
 ▼
Assessment
 │
 ▼
AI Coach
 │
 ▼
Progress
```

---

# Replay Sequence

```
User
 │
 ▼
Replay
 │
 ▼
Historical Chart
 │
 ▼
Market Lab
 │
 ▼
AI Coach
 │
 ▼
Assessment
```

---

# Market Lab Sequence

```
Historical Chart
 │
 ▼
Market Lab
 │
 ▼
Exercise
 │
 ▼
User Analysis
 │
 ▼
AI Analysis
 │
 ▼
Comparison
 │
 ▼
Assessment
```

---

# Assessment Sequence

```
Lesson
 │
 ▼
Quiz
 │
 ▼
Practical Task
 │
 ▼
Exam
 │
 ▼
Score
 │
 ▼
Progress
```

---

# Certification Sequence

```
Assessment
 │
 ▼
Pass
 │
 ▼
Certification
 │
 ▼
Certificate
 │
 ▼
User
```

---

# Progress Sequence

```
Lesson Complete
 │
 ▼
XP Update
 │
 ▼
Statistics Update
 │
 ▼
Level Update
 │
 ▼
Roadmap Update
```

---

# Career Mode Sequence

```
Progress
 │
 ▼
Career Mode
 │
 ▼
Student
 │
 ▼
Junior Trader
 │
 ▼
Intermediate Trader
 │
 ▼
Professional Trader
 │
 ▼
GoldBot Expert
```

---

# Challenge Sequence

```
Challenge
 │
 ▼
User
 │
 ▼
Submission
 │
 ▼
Assessment
 │
 ▼
Score
 │
 ▼
Leaderboard
```

---

# PvP Sequence

```
Player A
      │
      ▼
   Challenge
      ▲
      │
Player B
      │
      ▼
Assessment
      │
      ▼
Winner
      │
      ▼
Leaderboard
```

---

# Tournament Sequence

```
Users
 │
 ▼
Tournament
 │
 ▼
Assessment
 │
 ▼
Ranking
 │
 ▼
Leaderboard
```

---

# AI vs Player Sequence

```
Chart
 │
 ▼
User Analysis
 │
 ▼
AI Analysis
 │
 ▼
Comparison
 │
 ▼
Explanation
 │
 ▼
Learning Result
```

AI bu yerda raqib emas.

AI:

- Benchmark
- Mentor
- Evaluator

vazifalarini bajaradi.

---

# Roadmap Sequence

```
Progress
 │
 ▼
Roadmap
 │
 ▼
Current Position
 │
 ▼
Next Goal
 │
 ▼
Remaining Lessons
```

---

# Learning Analytics Sequence

```
Progress
 │
 ▼
Analytics
 │
 ▼
Weak Topics
 │
 ▼
Strong Topics
 │
 ▼
Study Statistics
 │
 ▼
AI Recommendation
```

---

# Journal Sequence

```
Lesson Complete
 │
 ▼
Journal
 │
 ▼
User Notes
 │
 ▼
AI Feedback
 │
 ▼
Reflection
```

---

# Library Sequence

```
Lesson
 │
 ▼
Library
 │
 ├── PDF
 ├── Cheat Sheet
 ├── Strategy Guide
 ├── Glossary
 └── Checklist
 │
 ▼
User
```

---

# Complete Learning Lifecycle

```
User
 │
 ▼
Learning Path
 │
 ▼
Curriculum
 │
 ▼
Academy
 │
 ▼
Lesson
 │
 ▼
Practice
 │
 ▼
Simulator
 │
 ▼
Replay
 │
 ▼
Market Lab
 │
 ▼
Assessment
 │
 ▼
AI Coach
 │
 ▼
Progress
 │
 ▼
Achievements
 │
 ▼
Certification
 │
 ▼
Career Mode
 │
 ▼
Roadmap
 │
 ▼
Professional Trader
```

---

# Community Learning Lifecycle

```
Challenge
 │
 ▼
PvP
 │
 ▼
Tournament
 │
 ▼
Leaderboard
 │
 ▼
Achievements
```

---

# Layer Interaction

```
Platform Layer
        │
        ▼
Learning API
        │
        ▼
Learning Layer
        │
        ▼
AI Layer
        │
        ▼
Chart Service
        │
        ▼
Business Layer
```

Learning Layer hech qachon boshqa Layer ichki logikasiga bevosita murojaat qilmaydi.

Barcha integratsiyalar API yoki rasmiy Service Contract orqali amalga oshiriladi.

---

# Sequence Status

Status:
Blueprint

Version:
v1.0

Architecture:
GoldBot V3

Lifecycle:
GDL-001

Flow Standard:
GFL-001

Module Standard:
GEL-001

Language Standard:
GLS-001