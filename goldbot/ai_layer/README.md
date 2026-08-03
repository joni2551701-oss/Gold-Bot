# 07_AI_Layer

Status: SKELETON (Phase A) — implementatsiya Phase B-E davomida qo'shiladi.

Bu papka `New_Map/` dagi Canonical Architecture'ning importga yaroqli aksi.
Biznes mantiq hali ko'chirilmagan.

## Canonical hujjatlar

- [Layer README](../../New_Map/07_AI_Layer/README.md)
- [Layer Contracts](../../New_Map/07_AI_Layer/Layer_Contracts.md)
- [Layer ModuleMap](../../New_Map/07_AI_Layer/Layer_ModuleMap.md)
- [Layer DataFlow](../../New_Map/07_AI_Layer/Layer_DataFlow.md)
- [Layer SequenceDiagram](../../New_Map/07_AI_Layer/Layer_SequenceDiagram.md)

## Modullar (39)

| Python package | Canonical hujjat |
|---|---|
| `goldbot.ai_layer.ai_coordinator` | [AICoordinator](../../New_Map/07_AI_Layer/AICoordinator/README.md) |
| `goldbot.ai_layer.ai_engine` | [AIEngine](../../New_Map/07_AI_Layer/AIEngine/README.md) |
| `goldbot.ai_layer.ai_service` | [AIService](../../New_Map/07_AI_Layer/AIService/README.md) |
| `goldbot.ai_layer.confidence_ai` | [ConfidenceAI](../../New_Map/07_AI_Layer/ConfidenceAI/README.md) |
| `goldbot.ai_layer.explanation_ai` | [ExplanationAI](../../New_Map/07_AI_Layer/ExplanationAI/README.md) |
| `goldbot.ai_layer.fundamental_ai` | [FundamentalAI](../../New_Map/07_AI_Layer/FundamentalAI/README.md) |
| `goldbot.ai_layer.fundamental_ai.correlation_ai` | [FundamentalAI/CorrelationAI](../../New_Map/07_AI_Layer/FundamentalAI/CorrelationAI/README.md) |
| `goldbot.ai_layer.fundamental_ai.economic_calendar_ai` | [FundamentalAI/EconomicCalendarAI](../../New_Map/07_AI_Layer/FundamentalAI/EconomicCalendarAI/README.md) |
| `goldbot.ai_layer.fundamental_ai.news_ai` | [FundamentalAI/NewsAI](../../New_Map/07_AI_Layer/FundamentalAI/NewsAI/README.md) |
| `goldbot.ai_layer.fundamental_ai.sentiment_ai` | [FundamentalAI/SentimentAI](../../New_Map/07_AI_Layer/FundamentalAI/SentimentAI/README.md) |
| `goldbot.ai_layer.knowledge_ai` | [KnowledgeAI](../../New_Map/07_AI_Layer/KnowledgeAI/README.md) |
| `goldbot.ai_layer.knowledge_ai.knowledge_base` | [KnowledgeAI/KnowledgeBase](../../New_Map/07_AI_Layer/KnowledgeAI/KnowledgeBase/README.md) |
| `goldbot.ai_layer.knowledge_ai.knowledge_base.personal_knowledge` | [KnowledgeAI/KnowledgeBase/PersonalKnowledge](../../New_Map/07_AI_Layer/KnowledgeAI/KnowledgeBase/PersonalKnowledge/README.md) |
| `goldbot.ai_layer.knowledge_ai.knowledge_base.system_knowledge` | [KnowledgeAI/KnowledgeBase/SystemKnowledge](../../New_Map/07_AI_Layer/KnowledgeAI/KnowledgeBase/SystemKnowledge/README.md) |
| `goldbot.ai_layer.knowledge_ai.knowledge_manager` | [KnowledgeAI/KnowledgeManager](../../New_Map/07_AI_Layer/KnowledgeAI/KnowledgeManager/README.md) |
| `goldbot.ai_layer.knowledge_ai.learning_engine` | [KnowledgeAI/LearningEngine](../../New_Map/07_AI_Layer/KnowledgeAI/LearningEngine/README.md) |
| `goldbot.ai_layer.knowledge_ai.memory_manager` | [KnowledgeAI/MemoryManager](../../New_Map/07_AI_Layer/KnowledgeAI/MemoryManager/README.md) |
| `goldbot.ai_layer.knowledge_ai.memory_search` | [KnowledgeAI/MemorySearch](../../New_Map/07_AI_Layer/KnowledgeAI/MemorySearch/README.md) |
| `goldbot.ai_layer.knowledge_ai.provider_router` | [KnowledgeAI/ProviderRouter](../../New_Map/07_AI_Layer/KnowledgeAI/ProviderRouter/README.md) |
| `goldbot.ai_layer.knowledge_ai.rag` | [KnowledgeAI/RAG](../../New_Map/07_AI_Layer/KnowledgeAI/RAG/README.md) |
| `goldbot.ai_layer.knowledge_ai.validation_engine` | [KnowledgeAI/ValidationEngine](../../New_Map/07_AI_Layer/KnowledgeAI/ValidationEngine/README.md) |
| `goldbot.ai_layer.personal_ai` | [PersonalAI](../../New_Map/07_AI_Layer/PersonalAI/README.md) |
| `goldbot.ai_layer.personal_ai.interaction_manager` | [PersonalAI/InteractionManager](../../New_Map/07_AI_Layer/PersonalAI/InteractionManager/README.md) |
| `goldbot.ai_layer.personal_ai.persona_manager` | [PersonalAI/PersonaManager](../../New_Map/07_AI_Layer/PersonalAI/PersonaManager/README.md) |
| `goldbot.ai_layer.personal_ai.senior` | [PersonalAI/Senior](../../New_Map/07_AI_Layer/PersonalAI/Senior/README.md) |
| `goldbot.ai_layer.personal_ai.seniorita` | [PersonalAI/Seniorita](../../New_Map/07_AI_Layer/PersonalAI/Seniorita/README.md) |
| `goldbot.ai_layer.personal_ai.user_profile` | [PersonalAI/UserProfile](../../New_Map/07_AI_Layer/PersonalAI/UserProfile/README.md) |
| `goldbot.ai_layer.vision_ai` | [VisionAI](../../New_Map/07_AI_Layer/VisionAI/README.md) |
| `goldbot.ai_layer.vision_ai.chart_vision` | [VisionAI/ChartVision](../../New_Map/07_AI_Layer/VisionAI/ChartVision/README.md) |
| `goldbot.ai_layer.vision_ai.image_analysis` | [VisionAI/ImageAnalysis](../../New_Map/07_AI_Layer/VisionAI/ImageAnalysis/README.md) |
| `goldbot.ai_layer.vision_ai.ocr` | [VisionAI/OCR](../../New_Map/07_AI_Layer/VisionAI/OCR/README.md) |
| `goldbot.ai_layer.vision_ai.pattern_recognition` | [VisionAI/PatternRecognition](../../New_Map/07_AI_Layer/VisionAI/PatternRecognition/README.md) |
| `goldbot.ai_layer.voice_ai` | [VoiceAI](../../New_Map/07_AI_Layer/VoiceAI/README.md) |
| `goldbot.ai_layer.voice_ai.speech_to_text` | [VoiceAI/SpeechToText](../../New_Map/07_AI_Layer/VoiceAI/SpeechToText/README.md) |
| `goldbot.ai_layer.voice_ai.text_to_speech` | [VoiceAI/TextToSpeech](../../New_Map/07_AI_Layer/VoiceAI/TextToSpeech/README.md) |
| `goldbot.ai_layer.voice_ai.voice_commands` | [VoiceAI/VoiceCommands](../../New_Map/07_AI_Layer/VoiceAI/VoiceCommands/README.md) |
| `goldbot.ai_layer.voice_ai.voice_provider` | [VoiceAI/VoiceProvider](../../New_Map/07_AI_Layer/VoiceAI/VoiceProvider/README.md) |
| `goldbot.ai_layer.voice_ai.voice_session` | [VoiceAI/VoiceSession](../../New_Map/07_AI_Layer/VoiceAI/VoiceSession/README.md) |
| `goldbot.ai_layer.voice_ai.wake_word` | [VoiceAI/WakeWord](../../New_Map/07_AI_Layer/VoiceAI/WakeWord/README.md) |
