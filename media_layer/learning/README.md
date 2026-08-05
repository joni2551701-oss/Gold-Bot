# Learning Layer

## Overview

Learning Layer — GoldBot AI Ecosystem tarkibidagi professional AI-assisted Trading Academy hisoblanadi.

Uning asosiy maqsadi foydalanuvchini boshlang'ich darajadan professional trader darajasigacha bosqichma-bosqich o'qitish, bilimini baholash, amaliyot o'tkazish va rivojlanishini kuzatishdir.

Learning Layer oddiy video kurslar platformasi emas.

Bu AI yordamida ishlaydigan interaktiv ta'lim tizimi bo'lib, foydalanuvchi:

- o'rganadi;
- mashq qiladi;
- replay orqali takrorlaydi;
- AI Coach'dan feedback oladi;
- bilimini sinovdan o'tkazadi;
- sertifikat oladi;
- keyingi bosqichga o'tadi.

Learning Layer GoldBot Platform'ning ajralmas qismi hisoblanadi.

---

# Mission

Professional AI Trading Academy yaratish.

Maqsad:

- Trading bilimini tizimli o'rgatish.
- Amaliy mashg'ulotlarni tashkil qilish.
- AI yordamida foydalanuvchini rivojlantirish.
- Har bir foydalanuvchiga individual Learning Path yaratish.
- Professional sertifikatlash tizimini yaratish.

---

# Principles

Learning Layer quyidagi tamoyillar asosida quriladi.

## Learn First

Nazariya → Amaliyot → Tahlil → Baholash → Rivojlanish.

---

## AI Assisted

AI qaror qabul qilmaydi.

AI:

- tushuntiradi;
- baholaydi;
- tavsiya beradi;
- mentor vazifasini bajaradi.

---

## Practice Driven

Har bir dars amaliy mashq bilan yakunlanadi.

---

## Progressive Learning

Foydalanuvchi o'z bilim darajasiga mos yo'ldan boshlaydi.

---

## Reuse First (GEL-001)

Learning hech qachon Platform funksiyalarini takrorlamaydi.

Masalan:

- Language
- Theme
- User Profile
- Notification
- Authentication

Platform tomonidan boshqariladi.

Learning faqat o'quv logikasini boshqaradi.

---

## Layer Separation

Learning boshqa Layer'larning ichki logikasiga bevosita murojaat qilmaydi.

Barcha aloqa Learning API orqali amalga oshiriladi.

---

# Learning Workflow

```
User
    │
    ▼
Learning Path
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
    ▼
Practice
    │
    ▼
Replay / Simulator
    │
    ▼
AI Coach
    │
    ▼
Progress
    │
    ▼
Certification
    │
    ▼
Next Level
```

---

# Learning Structure

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

# Modules

## academy

Asosiy o'quv platformasi.

Ichida:

- Courses
- Modules
- Lessons
- Chapters
- Practice
- Quiz

---

## curriculum

Butun o'quv dasturini boshqaradi.

Misol:

```
Gold Trading

Beginner

Intermediate

Advanced

Professional
```

---

## learning_path

Har bir foydalanuvchi uchun individual o'quv yo'lini yaratadi.

Misol:

```
Beginner

↓

Lesson 1

↓

Lesson 2

↓

Assessment

↓

Intermediate
```

---

## ai_coach

Shaxsiy AI mentor.

Vazifalari:

- Savollarga javob beradi.
- Xatolarni tushuntiradi.
- Tavsiyalar beradi.
- Mashqlar yaratadi.
- Progressni tahlil qiladi.

AI hech qachon foydalanuvchi o'rniga javob bermaydi.

---

## simulator

Virtual Trading muhiti.

Maqsad:

Risksiz amaliyot.

---

## replay

Tarixiy bozorni qayta o'ynaydi.

Foydalanuvchi real sharoitda mashq qiladi.

---

## market_lab

Chart asosidagi laboratoriya.

Misollar:

- BOS topish
- CHoCH topish
- FVG topish
- Order Block topish
- Liquidity Sweep topish

AI natijani tekshiradi.

---

## assessment

Bilimni baholaydi.

Ichida:

- Quiz
- Test
- Practical Task
- Final Exam

---

## certification

O'qishni yakunlagan foydalanuvchiga sertifikat beradi.

---

## progress

Rivojlanishni kuzatadi.

Masalan:

- XP
- Level
- Accuracy
- Study Time
- Completed Lessons

---

## roadmap

Keyingi rivojlanish yo'lini ko'rsatadi.

Misol:

```
Current

Intermediate

↓

Next

Advanced

↓

Remaining

24 Lessons
```

---

## achievements

Achievement va Badge tizimi.

Misollar:

- First Lesson
- 10 Lessons
- SMC Master
- Risk Master

---

## leaderboard

Challenge va Tournament reytingi.

Ko'rinishlar:

- Weekly
- Monthly
- All Time

---

## analytics

Learning statistikasi.

Masalan:

- Completion Rate
- Quiz Accuracy
- Weak Topics
- Strong Topics
- Study Time

---

## journal

Foydalanuvchining shaxsiy o'quv kundaligi.

Ichida:

- Bugun nimani o'rgandim
- Qayerda xato qildim
- AI Feedback
- Personal Notes

---

## library

Qo'shimcha o'quv materiallari.

Masalan:

- PDF
- Cheat Sheet
- Strategy Guide
- Glossary
- Formula
- Checklist

---

## career_mode

Bosqichma-bosqich rivojlanish tizimi.

Misol:

```
Student

↓

Junior Trader

↓

Intermediate Trader

↓

Professional Trader

↓

GoldBot Expert
```

---

## challenge

Individual topshiriqlar.

Har bir foydalanuvchi mustaqil bajaradi.

---

## tournament

Ko'p foydalanuvchili musobaqalar.

---

## pvp

Ikki real foydalanuvchi o'rtasidagi bellashuv.

---

## ai_vs_player

Foydalanuvchi va AI analizini solishtiradi.

```
Chart

↓

User Analysis

↓

AI Analysis

↓

Comparison

↓

Explanation
```

AI bu yerda raqib emas.

AI benchmark va mentor vazifasini bajaradi.

---

## learning_api

Learning Layer'ni quyidagi platformalarga ulaydi:

- Telegram
- Mobile
- Desktop
- Web

Learning Layer tashqi Layer'lar bilan faqat Learning API orqali ishlaydi.

---

# Development Roadmap

## Phase 1 — Foundation

- Academy
- Curriculum
- Learning Path
- AI Coach
- Assessment
- Progress
- Learning API

---

## Phase 2 — Professional

- Simulator
- Replay
- Market Lab
- Certification
- Achievements
- Journal
- Analytics
- Roadmap

---

## Phase 3 — Community

- Challenge
- Tournament
- PvP
- AI vs Player
- Leaderboard
- Career Mode

---

# Design Rules

Learning Layer:

- Platform funksiyalarini takrorlamaydi.
- AI qaror qabul qilmaydi.
- Trading Engine'ga aralashmaydi.
- Market Data'ni o'zgartirmaydi.
- GoldBot Core'dan mustaqil ishlaydi.
- Faqat Learning API orqali tashqi aloqaga chiqadi.

---

# Future Vision

Learning Layer kelajakda quyidagilarni qo'llab-quvvatlaydi:

- AI Personal Mentor
- Multi-language Academy
- Interactive Charts
- Voice Lessons
- Video Lessons
- Adaptive Learning
- Personalized Curriculum
- Community Challenges
- Global Tournament
- Professional Certification
- Trading Career Development

---

# Status

Status: Blueprint

Version: v1.0

Architecture: GoldBot V3

Lifecycle: GDL-001

Flow Standard: GFL-001

Module Standard: GEL-001

Language Standard: GLS-001