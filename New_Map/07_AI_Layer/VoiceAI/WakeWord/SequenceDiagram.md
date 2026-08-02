# Wake Word Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat WakeWord Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
User Voice
↓
WakeWord
↓
Listen Audio
↓
Detect Wake Word
↓
Validate Trigger
↓
Generate Wake Event
↓
SpeechToText
```
---
# Runtime Rules
1. Audio Stream doimiy tinglanishi mumkin.
2. Wake Word aniqlanishi shart.
3. Trigger tasdiqlanishi shart.
4. SpeechToText faqat Activation'dan keyin boshlanadi.
---
# State Flow
```text
Idle
↓
Listening
↓
Wake Word Detected
↓
Validating
↓
Activated
↓
Speech Recognition
```
---
# Summary
User Voice
↓
WakeWord
↓
SpeechToText
