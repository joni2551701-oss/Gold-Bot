# Learning Layer Module Map

## Overview

Learning Layer GoldBot AI Ecosystem tarkibidagi Professional Trading Academy hisoblanadi.

Ushbu hujjat Learning Layer tarkibidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishini tavsiflaydi.

Learning Layer faqat Learning API orqali tashqi Layer'lar bilan aloqa qiladi.

---

# Learning Layer Architecture

```
learning/
│
├── academy/
├── curriculum/
├── learning_path/
├── ai_coach/
├── simulator/
├── replay/
├── market_lab/
├── assessment/
├── certification/
├── progress/
├── roadmap/
├── achievements/
├── leaderboard/
├── analytics/
├── journal/
├── library/
├── career_mode/
├── challenge/
├── tournament/
├── pvp/
├── ai_vs_player/
└── learning_api/
```

---

# Module Relationships

```
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
Assessment
        │
        ▼
Progress
        │
        ▼
Certification
```

---

# Practice Pipeline

```
Academy

↓

Simulator

↓

Replay

↓

Market Lab

↓

AI Coach

↓

Assessment

↓

Progress
```

---

# Community Pipeline

```
Challenge

↓

PvP

↓

Tournament

↓

Leaderboard

↓

Achievements
```

---

# Personal Development Pipeline

```
Learning Path

↓

Academy

↓

Career Mode

↓

Progress

↓

Roadmap
```

---

# AI Pipeline

```
AI Coach

↓

Lesson Support

↓

Practice Evaluation

↓

Journal Feedback

↓

Learning Recommendation

↓

Roadmap Recommendation
```

---

# Module Responsibilities

## academy

Mas'uliyat:

- Courses
- Modules
- Lessons
- Chapters
- Practice

Bog'lanadi:

- Curriculum
- Assessment
- Progress
- AI Coach

---

## curriculum

Mas'uliyat:

- O'quv dasturi
- Kurs ketma-ketligi
- Learning Structure

Bog'lanadi:

- Academy
- Learning Path

---

## learning_path

Mas'uliyat:

- User Level
- Personalized Learning
- Next Lesson

Bog'lanadi:

- Curriculum
- Progress
- Roadmap

---

## ai_coach

Mas'uliyat:

- AI Mentor
- AI Evaluation
- AI Recommendation

Bog'lanadi:

- Academy
- Simulator
- Replay
- Journal
- Assessment

---

## simulator

Mas'uliyat:

- Virtual Trading
- Practice

Bog'lanadi:

- Replay
- Market Lab
- AI Coach

---

## replay

Mas'uliyat:

- Historical Replay
- Trade Replay

Bog'lanadi:

- Simulator
- Market Lab

---

## market_lab

Mas'uliyat:

- BOS
- CHoCH
- OB
- FVG
- Liquidity

Bog'lanadi:

- Replay
- Assessment
- AI Coach

---

## assessment

Mas'uliyat:

- Quiz
- Test
- Practical Task
- Final Exam

Bog'lanadi:

- Progress
- Certification

---

## certification

Mas'uliyat:

- Certificate
- Graduation

Bog'lanadi:

- Progress

---

## progress

Mas'uliyat:

- XP
- Level
- Statistics
- Learning History

Bog'lanadi:

- Roadmap
- Achievements

---

## roadmap

Mas'uliyat:

- Current Position
- Next Goal
- Remaining Lessons

Bog'lanadi:

- Progress
- Learning Path

---

## achievements

Mas'uliyat:

- Badge
- Achievement
- Rewards

Bog'lanadi:

- Leaderboard

---

## leaderboard

Mas'uliyat:

- Weekly Ranking
- Monthly Ranking
- Global Ranking

Bog'lanadi:

- Challenge
- Tournament
- PvP

---

## analytics

Mas'uliyat:

- Learning Statistics
- Success Rate
- Weak Topics
- Strong Topics

Bog'lanadi:

- Progress
- Journal

---

## journal

Mas'uliyat:

- Personal Notes
- AI Feedback
- Reflection

Bog'lanadi:

- AI Coach
- Analytics

---

## library

Mas'uliyat:

- PDF
- Cheat Sheet
- Strategy Guide
- Glossary
- Documentation

Bog'lanadi:

- Academy

---

## career_mode

Mas'uliyat:

- Trading Career
- Level Progression

Bog'lanadi:

- Progress
- Roadmap

---

## challenge

Mas'uliyat:

- Individual Challenges

Bog'lanadi:

- Leaderboard

---

## tournament

Mas'uliyat:

- Competition

Bog'lanadi:

- Leaderboard

---

## pvp

Mas'uliyat:

- Player vs Player

Bog'lanadi:

- Tournament

---

## ai_vs_player

Mas'uliyat:

- User Analysis
- AI Analysis
- Comparison

Bog'lanadi:

- AI Coach
- Assessment

---

## learning_api

Mas'uliyat:

- Public Learning API
- Platform Integration

Bog'lanadi:

- Telegram
- Web
- Desktop
- Mobile

---

# External Dependencies

Learning Layer quyidagi Layer'lar bilan ishlaydi.

```
GoldBot Core

↓

Chart Service

↓

AI Layer

↓

Business Layer

↓

Platform Layer
```

Learning Layer ushbu Layer'larning ichki logikasiga bevosita murojaat qilmaydi.

Barcha integratsiyalar API orqali amalga oshiriladi.

---

# Reuse Policy

Learning Layer:

Reuse qiladi:

- User Profile
- Authentication
- Authorization
- Language
- Notification
- Platform Settings

Learning Layer yaratmaydi:

- Trading Logic
- Market Data
- Decision Engine
- Risk Engine
- Execution Engine

---

# Module Dependency Order

```
Learning API

↓

Learning Path

↓

Curriculum

↓

Academy

↓

Assessment

↓

Progress

↓

Certification
```

Community modullari:

```
Challenge

↓

PvP

↓

Tournament

↓

Leaderboard
```

Practice modullari:

```
Simulator

↓

Replay

↓

Market Lab

↓

AI Coach
```

---

# Module Status

| Module | Status |
|----------|--------|
| Academy | Blueprint |
| Curriculum | Blueprint |
| Learning Path | Blueprint |
| AI Coach | Blueprint |
| Simulator | Blueprint |
| Replay | Blueprint |
| Market Lab | Blueprint |
| Assessment | Blueprint |
| Certification | Blueprint |
| Progress | Blueprint |
| Roadmap | Blueprint |
| Achievements | Blueprint |
| Leaderboard | Blueprint |
| Analytics | Blueprint |
| Journal | Blueprint |
| Library | Blueprint |
| Career Mode | Blueprint |
| Challenge | Blueprint |
| Tournament | Blueprint |
| PvP | Blueprint |
| AI vs Player | Blueprint |
| Learning API | Blueprint |

---

Version: v1.0

Status: Blueprint

Architecture: GoldBot V3

Lifecycle: GDL-001

Flow Standard: GFL-001

Module Standard: GEL-001

Language Standard: GLS-001