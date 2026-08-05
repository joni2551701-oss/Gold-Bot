# Learning Layer State Diagram

## Overview

Ushbu hujjat Learning Layer ichidagi asosiy state'larni va ularning transition'larini belgilaydi.

State Diagram savoliga javob beradi:

- User hozir qaysi holatda?
- Qaysi holatdan qaysi holatga o'tishi mumkin?
- Qaysi holat qayta urinishga olib keladi?
- Qaysi holat sertifikat yoki keyingi bosqichga olib boradi?

Learning Layer foydalanuvchini Beginner'dan Professional darajagacha bosqichma-bosqich rivojlantiradi.

---

# Core User States

## 1. New User

Foydalanuvchi Learning tizimiga birinchi marta kirgan holat.

### Possible transitions
- Placement Test
- Manual Level Selection
- Onboarding Complete

---

## 2. Onboarding

Foydalanuvchi Learning tizimi bilan tanishish bosqichi.

### Possible transitions
- Learning Path Selection
- Continue to First Lesson
- Skip to Assessment

---

## 3. Beginner

Boshlang'ich daraja.

Foydalanuvchi trading asoslarini o'rganadi.

### Possible transitions
- Next Lesson
- Replay
- Practice
- Assessment
- AI Coach Help

---

## 4. Intermediate

O'rta daraja.

Foydalanuvchi market structure, liquidity, BOS, CHoCH kabi mavzularni o'rganadi.

### Possible transitions
- Next Lesson
- Simulator
- Replay
- Market Lab
- Assessment
- AI Coach Help

---

## 5. Advanced

Yuqori daraja.

Foydalanuvchi SMC, Wyckoff, AMD, Order Block, FVG va multi-timeframe analysis bilan ishlaydi.

### Possible transitions
- Replay
- Market Lab
- Simulator
- Challenge
- Assessment
- AI Coach Review

---

## 6. Professional

Professional daraja.

Foydalanuvchi amaliy, tizimli va advanced o'quv bosqichiga o'tadi.

### Possible transitions
- Certification Exam
- Tournament
- PvP
- AI vs Player
- Career Mode
- Certification Complete

---

## 7. Learning In Progress

Foydalanuvchi faol o'rganayotgan holat.

Bu state har bir lesson yoki module vaqtida ishlaydi.

### Possible transitions
- Lesson Complete
- Practice Complete
- Assessment Start
- Replay Start
- Simulator Start

---

## 8. Practice Mode

Foydalanuvchi mashq qilayotgan holat.

### Possible transitions
- Practice Success
- Practice Fail
- AI Coach Feedback
- Retry Practice
- Assessment Start

---

## 9. Replay Mode

Foydalanuvchi historical chart yoki session replay ko'rayotgan holat.

### Possible transitions
- Replay Complete
- Replay Pause
- Market Lab
- Assessment
- AI Coach Feedback

---

## 10. Simulator Mode

Demo trading yoki virtual trading holati.

### Possible transitions
- Simulation Success
- Simulation Fail
- Review Result
- Retry Simulation
- Assessment

---

## 11. Assessment Pending

Foydalanuvchi quiz, test yoki practical task topshirishga tayyor.

### Possible transitions
- Assessment Pass
- Assessment Fail
- Retry
- AI Coach Help

---

## 12. Assessment Passed

Foydalanuvchi testni muvaffaqiyatli topshirgan holat.

### Possible transitions
- Progress Update
- Next Lesson
- Certification
- Next Level

---

## 13. Assessment Failed

Foydalanuvchi testdan o'ta olmagan holat.

### Possible transitions
- AI Coach Feedback
- Retry Lesson
- Replay
- Practice
- Simulator

---

## 14. Certification Pending

Foydalanuvchi sertifikat olish bosqichida.

### Possible transitions
- Certification Approved
- Certification Failed
- Retake Exam

---

## 15. Certified

Foydalanuvchi sertifikat olgan holat.

### Possible transitions
- Next Level
- Career Mode
- Tournament
- Challenge
- Progress Update

---

## 16. Career Mode

Foydalanuvchi bosqichma-bosqich professional yo'l bo'yicha harakat qilmoqda.

### Possible transitions
- Beginner Trader
- Junior Trader
- Intermediate Trader
- Professional Trader
- GoldBot Expert

---

## 17. AI Coach Active

AI Coach foydalanuvchiga feedback berayotgan holat.

### Possible transitions
- Lesson Recommendation
- Practice Recommendation
- Replay Recommendation
- Retry Lesson
- Progress Update

---

## 18. Progress Updated

Foydalanuvchi progress ma'lumotlari yangilangan holat.

### Possible transitions
- Next Lesson
- Next Module
- Roadmap Update
- Achievement Unlock
- Certification

---

## 19. Achievement Unlocked

Foydalanuvchi badge yoki achievement olgan holat.

### Possible transitions
- Continue Learning
- Leaderboard Update
- Certification
- Career Mode

---

## 20. Leaderboard Updated

Foydalanuvchi ranking tizimiga qo'shilgan holat.

### Possible transitions
- Continue Challenge
- Tournament
- PvP
- Achievement Unlock

---

# Global Learning State Flow

```text
New User
    │
    ▼
Onboarding
    │
    ├── Placement Test ───────────────► Beginner / Intermediate / Advanced / Professional
    │
    └── Manual Level Selection ───────► Beginner / Intermediate / Advanced / Professional
```

---

```text
Beginner
    │
    ▼
Learning In Progress
    │
    ├── Practice Mode
    ├── Replay Mode
    ├── Simulator Mode
    ├── AI Coach Active
    └── Assessment Pending
```

---

```text
Assessment Pending
    │
    ├── Pass ───────────────► Assessment Passed
    │                         │
    │                         ▼
    │                    Progress Updated
    │                         │
    │                         ▼
    │                    Next Lesson / Next Module
    │
    └── Fail ───────────────► Assessment Failed
                              │
                              ▼
                        AI Coach Active
                              │
                              ▼
                        Retry Lesson / Practice / Replay
```

---

```text
Assessment Passed
    │
    ├── Progress Updated
    ├── Achievement Unlocked
    ├── Certification Pending
    └── Next Level
```

---

```text
Certification Pending
    │
    ├── Approved ───────────► Certified
    │                         │
    │                         ▼
    │                    Career Mode
    │
    └── Failed ─────────────► Assessment Failed
```

---

```text
Certified
    │
    ├── Challenge
    ├── Tournament
    ├── PvP
    ├── AI vs Player
    └── Career Mode
```

---

# State Transition Rules

## Rule 1

Foydalanuvchi bir bosqichdan keyingi bosqichga faqat:

- lesson complete
- assessment pass
- progress update

dan keyin o'tishi mumkin.

---

## Rule 2

Foydalanuvchi Assessment'dan o'tmasa, keyingi level ochilmaydi.

---

## Rule 3

AI Coach state doim yordamchi hisoblanadi.

AI Coach hech qachon yakuniy decision bermaydi.

---

## Rule 4

Simulator va Replay foydalanuvchini o'qitish va mashq qilish uchun ishlatiladi.

Ular progress va assessment bilan bog'lanadi.

---

## Rule 5

Certification faqat verification qilingan progress asosida beriladi.

---

## Rule 6

Career Mode faqat barqaror learning progress mavjud bo'lganda ochiladi.

---

## Rule 7

Challenge, Tournament, PvP va AI vs Player faqat maxsus competition state sifatida ishlaydi.

Ular Academy va Practice'dan alohida, lekin Learning Layer tarkibida bo'ladi.

---

# State Categories

## User Identity States

- New User
- Onboarding
- Learning Path Selected

## Learning States

- Beginner
- Intermediate
- Advanced
- Professional

## Activity States

- Learning In Progress
- Practice Mode
- Replay Mode
- Simulator Mode
- AI Coach Active

## Result States

- Assessment Pending
- Assessment Passed
- Assessment Failed
- Certification Pending
- Certified

## Growth States

- Progress Updated
- Achievement Unlocked
- Leaderboard Updated
- Career Mode

---

# External Dependencies

Learning Layer quyidagi tashqi komponentlar bilan ishlaydi:

- Platform Layer
- GoldBot Core API
- AI Layer
- Chart Service
- Business Layer

Lekin ular bilan faqat rasmiy API yoki contract orqali aloqa qiladi.

Learning Layer hech qachon tashqi layer ichki logikasiga bevosita kirib bormaydi.

---

# Forbidden Transitions

Quyidagi o'tishlar taqiqlanadi:

- Assessment Failed → Certified
- New User → Professional
- Beginner → Tournament without progress
- Certification Pending → Career Mode without pass
- AI Coach Active → Final Decision
- Learning Layer → Trading Decision Engine direct access

---

# Status

Status: Blueprint

Version: v1.0

Architecture: GoldBot V3

Lifecycle: GDL-001

Flow Standard: GFL-001

Module Standard: GEL-001

Language Standard: GLS-001