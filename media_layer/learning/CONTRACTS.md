# Learning Layer Contracts

## Overview

Learning Layer GoldBot AI Ecosystem tarkibidagi Professional AI Trading Academy hisoblanadi.

Ushbu hujjat Learning Layer va uning modullari uchun rasmiy kontraktlarni (Contracts) belgilaydi.

Har bir modul ushbu kontraktlarga qat'iy amal qilishi shart.

---

# Contract Principles

Learning Layer quyidagi tamoyillarga amal qiladi:

- Single Responsibility
- Layer Separation
- Reuse First (GEL-001)
- API First
- Contract First
- AI Assisted
- Platform Independent

---

# Learning Layer Contract

## Input

Learning Layer quyidagi ma'lumotlarni qabul qiladi.

- User Request
- User Progress
- Learning Path
- Curriculum
- Assessment Result
- Replay Result
- Simulator Result
- AI Feedback

---

## Processing

Learning Layer quyidagi vazifalarni bajaradi.

- Learning Management
- Lesson Management
- Progress Tracking
- Assessment
- AI Coaching
- Certification
- Learning Analytics

---

## Output

Learning Layer quyidagilarni ishlab chiqaradi.

- Lessons
- Quiz
- Practice Tasks
- Progress
- Certificates
- Statistics
- Leaderboard
- Learning Report

---

## Consumer

Learning Layer natijalaridan foydalanadi.

- Telegram
- Mobile
- Desktop
- Web

---

# Public API

Learning Layer tashqi tizimlarga faqat Learning API orqali xizmat ko'rsatadi.

Public API:

- Get Courses
- Get Lesson
- Start Lesson
- Complete Lesson
- Get Progress
- Start Quiz
- Submit Quiz
- Start Simulator
- Start Replay
- Get Certificate
- Get Leaderboard

Learning Layer ichki modullarini tashqariga ochmaydi.

---

# Internal Contracts

## academy

### Input

- Curriculum
- Learning Path

### Output

- Lessons
- Courses
- Modules

### Consumer

- Assessment
- AI Coach
- Progress

---

## curriculum

### Input

Director tomonidan tasdiqlangan o'quv dasturi.

### Output

Course Structure

### Consumer

- Academy
- Learning Path

---

## learning_path

### Input

- User Level
- Progress

### Output

Next Lesson

### Consumer

- Academy
- Roadmap

---

## ai_coach

### Input

- Lesson
- Assessment
- Replay
- Simulator
- Journal

### Output

- AI Feedback
- Recommendation
- Hint
- Explanation

### Consumer

- User

---

## simulator

### Input

- Lesson
- Practice Task

### Output

- Trade Result
- Practice Result

### Consumer

- Assessment
- AI Coach

---

## replay

### Input

Historical Market Data

### Output

Replay Session

### Consumer

- Simulator
- Market Lab

---

## market_lab

### Input

Replay Data

### Output

Chart Exercise

### Consumer

- Assessment
- AI Coach

---

## assessment

### Input

- Quiz
- Practical Task

### Output

- Score
- Pass
- Fail

### Consumer

- Progress
- Certification

---

## certification

### Input

Assessment Result

### Output

Certificate

### Consumer

User

---

## progress

### Input

Learning Activities

### Output

- XP
- Level
- Statistics

### Consumer

- Roadmap
- Analytics

---

## roadmap

### Input

Progress

### Output

Learning Roadmap

### Consumer

User

---

## achievements

### Input

Progress

### Output

Badges

### Consumer

Leaderboard

---

## leaderboard

### Input

Challenge Result

### Output

Ranking

### Consumer

Tournament

---

## analytics

### Input

Progress Data

### Output

Learning Analytics

### Consumer

AI Coach

---

## journal

### Input

User Notes

### Output

Learning History

### Consumer

AI Coach

---

## library

### Input

Learning Content

### Output

Study Materials

### Consumer

Academy

---

## career_mode

### Input

Progress

### Output

Career Level

### Consumer

Roadmap

---

## challenge

### Input

Learning Task

### Output

Challenge Result

### Consumer

Leaderboard

---

## tournament

### Input

Challenge Result

### Output

Tournament Ranking

### Consumer

Leaderboard

---

## pvp

### Input

Player A

Player B

### Output

Match Result

### Consumer

Leaderboard

---

## ai_vs_player

### Input

- User Analysis
- AI Analysis

### Output

Comparison Report

### Consumer

User

---

## learning_api

### Input

Platform Request

### Output

Learning Response

### Consumer

- Telegram
- Mobile
- Desktop
- Web

---

# External Dependencies

Learning Layer quyidagi Layer'larni reuse qiladi.

Business Layer

- User
- Subscription
- Identity

Platform Layer

- Language
- Authentication
- Notification
- Theme

Chart Service

- Replay
- Charts

GoldBot Core

- Market Context

AI Layer

- AI Services

Learning Layer ushbu Layer'larning ichki logikasiga bevosita murojaat qilmaydi.

---

# Forbidden

Learning Layer:

❌ Trading qilmaydi.

❌ Signal yaratmaydi.

❌ Decision qabul qilmaydi.

❌ Risk hisoblamaydi.

❌ Execution qilmaydi.

❌ Market Memory'ni o'zgartirmaydi.

❌ Chart Service logikasini o'zgartirmaydi.

❌ Platform Settings yaratmaydi.

❌ User Profile yaratmaydi.

❌ Notification yaratmaydi.

❌ Language boshqarmaydi.

---

# Reuse Rules

Reuse qilinadi:

- Identity
- Authentication
- Authorization
- User Profile
- Language
- Notification
- Theme
- Chart Service
- AI Layer

Takrorlash taqiqlanadi.

---

# Contract Stability

Contract Status:

Stable

Breaking Changes:

Forbidden

Har qanday Contract o'zgarishi:

- RFC
- ADR
- Director Decision

orqali amalga oshiriladi.

---

Version: v1.0

Status: Blueprint

Architecture: GoldBot V3

Lifecycle: GDL-001

Flow Standard: GFL-001

Module Standard: GEL-001

Language Standard: GLS-001