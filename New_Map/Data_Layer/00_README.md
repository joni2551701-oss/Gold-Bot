00_README.md — Data Layer uchun kirish hujjati.

Bu hujjat Data Layer’ni tushuntiradi, lekin implementatsiya tafsilotlarini bermaydi. Batafsil ma’lumot keyingi .md fayllarda joylashadi.

⸻

Document Information

Document Name
00_README.md
Layer
02_Data_Layer
Status
Canonical
Priority
Critical

⸻

Purpose

Data Layer — GoldBot ekotizimining eng quyi qatlami bo’lib, barcha market ma’lumotlarini yig’ish, tekshirish, saqlash va GoldBot Core’ga uzatish uchun javobgar.

Data Layer hech qanday savdo qarori qabul qilmaydi.

⸻

Responsibilities

Data Layer quyidagilar uchun javobgar:

* Historical ma’lumotlarni yuklash.
* Live market oqimini qabul qilish.
* Tick va Candle validatsiyasi.
* Market Memory boshqaruvi.
* Event tarqatish.
* Providerlar bilan ishlash.
* GoldBot Core’ni ishonchli ma’lumot bilan ta’minlash.

⸻

Not Responsible

Data Layer quyidagilarni bajarmaydi:

* Market Analysis
* Context Calculation
* Strategy
* Confluence
* Decision
* Risk Management
* Signal Generation
* Telegram
* Mobile
* Web
* Desktop
* AI
* Execution

⸻

Internal Structure

02_Data_Layer/
01_Historical_Data/
02_Live_Data/
03_Market_Memory/
04_Event_System/
05_Data_Validation/
06_Providers/
07_Module_Map.md
08_Sequence_Diagrams.md

⸻

Data Layer Modules

01_Historical_Data

Tarixiy ma’lumotlarni boshqaradi.

⸻

02_Live_Data

Real vaqt narx oqimini boshqaradi.

⸻

03_Market_Memory

Market holatining yagona manbai (Single Source of Truth).

⸻

04_Event_System

Ichki modullar orasidagi event almashinuvi.

⸻

05_Data_Validation

Barcha kiruvchi ma’lumotlarni tekshiradi.

⸻

06_Providers

Tashqi market providerlari bilan ishlaydi.

⸻

Layer Position

Providers
↓
Data Layer
↓
GoldBot Core
↓
Application Services
↓
Platform Layer
↓
User

⸻

Golden Rules

1. Data Layer faqat market ma’lumotlari bilan ishlaydi.
2. Market Memory — yagona ma’lumot manbai.
3. Live Tick faqat PriceStreamService orqali kiradi.
4. Historical ma’lumot faqat HistoricalDataService orqali kiradi.
5. Har bir ma’lumot validatsiyadan o’tishi shart.
6. Data Layer yuqori qatlamlarga bog’liq bo’lmaydi.
7. Core faqat Data Layer orqali market ma’lumot oladi.

⸻

Documentation Map

00_README.md
        │
        ├── 01_Historical_Data/
        ├── 02_Live_Data/
        ├── 03_Market_Memory/
        ├── 04_Event_System/
        ├── 05_Data_Validation/
        ├── 06_Providers/
        ├── 07_Module_Map.md
        └── 08_Sequence_Diagrams.md

⸻

Reading Order

Data Layer hujjatlari quyidagi tartibda o’qiladi:

1. 00_README.md
2. 01_Historical_Data/
3. 02_Live_Data/
4. 03_Market_Memory/
5. 04_Event_System/
6. 05_Data_Validation/
7. 06_Providers/
8. 07_Module_Map.md
9. 08_Sequence_Diagrams.md

⸻

Summary

Data Layer GoldBot uchun barcha market ma’lumotlarini yig’ish, tekshirish va boshqarish vazifasini bajaradi. U GoldBot Core uchun yagona va ishonchli ma’lumot manbai hisoblanadi hamda hech qanday tahlil yoki savdo logikasini bajarmaydi.

