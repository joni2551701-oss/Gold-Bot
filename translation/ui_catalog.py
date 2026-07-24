"""
Translation Layer — Telegram UI String Catalog (V1 Language Foundation,
Phase 1.3 Translation Engine).

This is a static localization catalog, not the dynamic-content
translation contract `translation.translation_manager.TranslationManager`
already owns (that module's `translate()` stays a clean Rule-4 rejection
-- no Google/DeepL/Gemini/OpenAI call anywhere in this package). A UI
catalog is a different concern: every string a handler can show a user
is hand-written once per supported language and looked up by a stable
key, the same "message catalog" pattern any localized product uses --
no live translation call happens here either.

`t(key, language, **kwargs)` is the single entry point every handler in
telegram/handlers.py calls instead of returning a literal string.
Lookup order per key: the caller's language -> EN -> whatever entry
exists -- so a language with an incomplete translation still degrades
to readable text instead of a KeyError, while UZ and RU are fully
covered here (the two languages `database.models`'s own schema default
and `/language`'s picker both treat as first-class, EN entries exist
for completeness and as the fallback rung).
"""

from typing import Optional

_DEFAULT_LANGUAGE = "EN"

_CATALOG: dict = {
    "start.created": {
        "EN": "Profile created.",
        "UZ": "Profil yaratildi.",
        "RU": "Профиль создан.",
    },
    "start.already_exists": {
        "EN": "User already exists.",
        "UZ": "Foydalanuvchi allaqachon mavjud.",
        "RU": "Пользователь уже существует.",
    },
    "start.error": {
        "EN": "Could not start: {error}",
        "UZ": "Ishga tushirib bo'lmadi: {error}",
        "RU": "Не удалось запустить: {error}",
    },
    "start.banned": {
        "EN": "Your account has been suspended.",
        "UZ": "Sizning hisobingiz bloklangan.",
        "RU": "Ваш аккаунт заблокирован.",
    },
    "help.text": {
        "EN": (
            "GoldBot Commands\n"
            "📊 Trading\n/signal\n/history\n/status\n"
            "👤 Profile\n/profile\n/settings\n/language\n/risk\n/strategy\n/timeframe\n/notifications\n"
            "💳 Plan\n/plan\n/subscription\n/upgrade\n"
            "ℹ️ Info\n/help\n/about"
        ),
        "UZ": (
            "GoldBot Buyruqlari\n"
            "📊 Savdo\n/signal\n/history\n/status\n"
            "👤 Profil\n/profile\n/settings\n/language\n/risk\n/strategy\n/timeframe\n/notifications\n"
            "💳 Tarif\n/plan\n/subscription\n/upgrade\n"
            "ℹ️ Ma'lumot\n/help\n/about"
        ),
        "RU": (
            "Команды GoldBot\n"
            "📊 Торговля\n/signal\n/history\n/status\n"
            "👤 Профиль\n/profile\n/settings\n/language\n/risk\n/strategy\n/timeframe\n/notifications\n"
            "💳 Тариф\n/plan\n/subscription\n/upgrade\n"
            "ℹ️ Информация\n/help\n/about"
        ),
    },
    "profile.error": {
        "EN": "Could not load profile: {error}",
        "UZ": "Profilni yuklab bo'lmadi: {error}",
        "RU": "Не удалось загрузить профиль: {error}",
    },
    "profile.not_found": {
        "EN": "No profile found.\nUse /start first.",
        "UZ": "Profil topilmadi.\nAvval /start buyrug'ini bosing.",
        "RU": "Профиль не найден.\nСначала используйте /start.",
    },
    "profile.display": {
        "EN": (
            "GoldBot Profile\n\nID:\n{telegram_id}\n\nUsername:\n{username}\n\nLanguage:\n{profile_language}\n\n"
            "Trading Style:\n{trading_style}\n\nStrategy:\n{strategy}\n\nRisk:\n{risk_percent}%\n\n"
            "Timeframe:\n{timeframe}\n\nPlan:\n{plan}\n\nNotifications:\n{notifications}\n\n"
            "Status:\n{status}\n\nCreated:\n{created_at}"
        ),
        "UZ": (
            "GoldBot Profili\n\nID:\n{telegram_id}\n\nFoydalanuvchi nomi:\n{username}\n\nTil:\n{profile_language}\n\n"
            "Savdo uslubi:\n{trading_style}\n\nStrategiya:\n{strategy}\n\nRisk:\n{risk_percent}%\n\n"
            "Vaqt oralig'i:\n{timeframe}\n\nTarif:\n{plan}\n\nBildirishnomalar:\n{notifications}\n\n"
            "Holat:\n{status}\n\nYaratilgan:\n{created_at}"
        ),
        "RU": (
            "Профиль GoldBot\n\nID:\n{telegram_id}\n\nИмя пользователя:\n{username}\n\nЯзык:\n{profile_language}\n\n"
            "Стиль торговли:\n{trading_style}\n\nСтратегия:\n{strategy}\n\nРиск:\n{risk_percent}%\n\n"
            "Таймфрейм:\n{timeframe}\n\nТариф:\n{plan}\n\nУведомления:\n{notifications}\n\n"
            "Статус:\n{status}\n\nСоздан:\n{created_at}"
        ),
    },
    "settings.menu": {
        "EN": (
            "Settings\n\n"
            "Language: {language_value}\nRisk: {risk_value}\nStrategy: {strategy_value}\n"
            "Timeframe: {timeframe_value}\nNotifications: {notifications_value}\n\n"
            "Use /language, /risk, /strategy, or /timeframe to change a setting."
        ),
        "UZ": (
            "Sozlamalar\n\n"
            "Til: {language_value}\nRisk: {risk_value}\nStrategiya: {strategy_value}\n"
            "Vaqt oralig'i: {timeframe_value}\nBildirishnomalar: {notifications_value}\n\n"
            "Sozlamani o'zgartirish uchun /language, /risk, /strategy yoki /timeframe dan foydalaning."
        ),
        "RU": (
            "Настройки\n\n"
            "Язык: {language_value}\nРиск: {risk_value}\nСтратегия: {strategy_value}\n"
            "Таймфрейм: {timeframe_value}\nУведомления: {notifications_value}\n\n"
            "Используйте /language, /risk, /strategy или /timeframe, чтобы изменить настройку."
        ),
    },
    "settings.saved": {
        "EN": "✅ Saved",
        "UZ": "✅ Saqlandi",
        "RU": "✅ Сохранено",
    },
    "risk.prompt": {
        "EN": "Choose risk percent:\n1%\n2%\n3%\n5%\n\nUse /risk 1, /risk 2, /risk 3, or /risk 5.",
        "UZ": "Risk foizini tanlang:\n1%\n2%\n3%\n5%\n\n/risk 1, /risk 2, /risk 3 yoki /risk 5 dan foydalaning.",
        "RU": "Выберите процент риска:\n1%\n2%\n3%\n5%\n\nИспользуйте /risk 1, /risk 2, /risk 3 или /risk 5.",
    },
    "risk.invalid": {
        "EN": "Invalid risk percent. Choose one of: 1, 2, 3, 5.",
        "UZ": "Noto'g'ri risk foizi. Quyidagilardan birini tanlang: 1, 2, 3, 5.",
        "RU": "Неверный процент риска. Выберите один из: 1, 2, 3, 5.",
    },
    "risk.error": {
        "EN": "Could not update risk: {error}",
        "UZ": "Riskni yangilab bo'lmadi: {error}",
        "RU": "Не удалось обновить риск: {error}",
    },
    "risk.updated": {
        "EN": "Risk updated to {percent}%.",
        "UZ": "Risk {percent}% ga o'zgartirildi.",
        "RU": "Риск обновлён до {percent}%.",
    },
    "strategy.prompt": {
        "EN": (
            "Choose strategy:\nLiquidity Sweep\nFVG\nAMD\nOrder Block\n\n"
            "Use /strategy Liquidity Sweep, /strategy FVG, /strategy AMD, or /strategy Order Block."
        ),
        "UZ": (
            "Strategiyani tanlang:\nLiquidity Sweep\nFVG\nAMD\nOrder Block\n\n"
            "/strategy Liquidity Sweep, /strategy FVG, /strategy AMD yoki /strategy Order Block dan foydalaning."
        ),
        "RU": (
            "Выберите стратегию:\nLiquidity Sweep\nFVG\nAMD\nOrder Block\n\n"
            "Используйте /strategy Liquidity Sweep, /strategy FVG, /strategy AMD или /strategy Order Block."
        ),
    },
    "strategy.invalid": {
        "EN": "Invalid strategy. Choose one of: Liquidity Sweep, FVG, AMD, Order Block.",
        "UZ": "Noto'g'ri strategiya. Quyidagilardan birini tanlang: Liquidity Sweep, FVG, AMD, Order Block.",
        "RU": "Неверная стратегия. Выберите одну из: Liquidity Sweep, FVG, AMD, Order Block.",
    },
    "strategy.error": {
        "EN": "Could not update strategy: {error}",
        "UZ": "Strategiyani yangilab bo'lmadi: {error}",
        "RU": "Не удалось обновить стратегию: {error}",
    },
    "strategy.updated": {
        "EN": "Strategy updated to {strategy}.",
        "UZ": "Strategiya {strategy} ga o'zgartirildi.",
        "RU": "Стратегия обновлена на {strategy}.",
    },
    "timeframe.prompt": {
        "EN": "Choose timeframe:\nM15\nH1\nH4\n\nUse /timeframe M15, /timeframe H1, or /timeframe H4.",
        "UZ": "Vaqt oralig'ini tanlang:\nM15\nH1\nH4\n\n/timeframe M15, /timeframe H1 yoki /timeframe H4 dan foydalaning.",
        "RU": "Выберите таймфрейм:\nM15\nH1\nH4\n\nИспользуйте /timeframe M15, /timeframe H1 или /timeframe H4.",
    },
    "timeframe.invalid": {
        "EN": "Invalid timeframe. Choose one of: M15, H1, H4.",
        "UZ": "Noto'g'ri vaqt oralig'i. Quyidagilardan birini tanlang: M15, H1, H4.",
        "RU": "Неверный таймфрейм. Выберите один из: M15, H1, H4.",
    },
    "timeframe.error": {
        "EN": "Could not update timeframe: {error}",
        "UZ": "Vaqt oralig'ini yangilab bo'lmadi: {error}",
        "RU": "Не удалось обновить таймфрейм: {error}",
    },
    "timeframe.updated": {
        "EN": "Timeframe updated to {timeframe}.",
        "UZ": "Vaqt oralig'i {timeframe} ga o'zgartirildi.",
        "RU": "Таймфрейм обновлён до {timeframe}.",
    },
    "notifications.status": {
        "EN": (
            "Notifications\n\nCurrent status:\n\nNotifications:\n{status}\n\n"
            "Options:\n\nEnable\nDisable\n\nUse /notifications on or /notifications off."
        ),
        "UZ": (
            "Bildirishnomalar\n\nJoriy holat:\n\nBildirishnomalar:\n{status}\n\n"
            "Tanlovlar:\n\nYoqish\nO'chirish\n\n/notifications on yoki /notifications off dan foydalaning."
        ),
        "RU": (
            "Уведомления\n\nТекущий статус:\n\nУведомления:\n{status}\n\n"
            "Опции:\n\nВключить\nВыключить\n\nИспользуйте /notifications on или /notifications off."
        ),
    },
    "notifications.status_on": {"EN": "ON ✅", "UZ": "YOQILGAN ✅", "RU": "ВКЛ ✅"},
    "notifications.status_off": {"EN": "OFF ❌", "UZ": "O'CHIRILGAN ❌", "RU": "ВЫКЛ ❌"},
    "notifications.invalid": {
        "EN": "Invalid option. Use /notifications on or /notifications off.",
        "UZ": "Noto'g'ri tanlov. /notifications on yoki /notifications off dan foydalaning.",
        "RU": "Неверный вариант. Используйте /notifications on или /notifications off.",
    },
    "notifications.error": {
        "EN": "Could not update notifications: {error}",
        "UZ": "Bildirishnomalarni yangilab bo'lmadi: {error}",
        "RU": "Не удалось обновить уведомления: {error}",
    },
    "notifications.enabled": {
        "EN": "Notifications enabled.",
        "UZ": "Bildirishnomalar yoqildi.",
        "RU": "Уведомления включены.",
    },
    "notifications.disabled": {
        "EN": "Notifications disabled.",
        "UZ": "Bildirishnomalar o'chirildi.",
        "RU": "Уведомления выключены.",
    },
    "signal.access_error": {
        "EN": "Could not check signal access: {error}",
        "UZ": "Signal huquqini tekshirib bo'lmadi: {error}",
        "RU": "Не удалось проверить доступ к сигналу: {error}",
    },
    "signal.load_error": {
        "EN": "Could not load signal: {error}",
        "UZ": "Signalni yuklab bo'lmadi: {error}",
        "RU": "Не удалось загрузить сигнал: {error}",
    },
    "signal.none": {
        "EN": "No active signal available.",
        "UZ": "Faol signal mavjud emas.",
        "RU": "Активный сигнал недоступен.",
    },
    "history.error": {
        "EN": "Could not load history: {error}",
        "UZ": "Tarixni yuklab bo'lmadi: {error}",
        "RU": "Не удалось загрузить историю: {error}",
    },
    "history.none": {
        "EN": "No signal history available.",
        "UZ": "Signal tarixi mavjud emas.",
        "RU": "История сигналов недоступна.",
    },
    "status.running": {
        "EN": "GoldBot is running.",
        "UZ": "GoldBot ishlamoqda.",
        "RU": "GoldBot работает.",
    },
    "about.text": {
        "EN": (
            "GoldBot is a semi-automatic XAUUSD (Gold) trading signal assistant.\n"
            "It analyzes market structure and delivers signals via Telegram."
        ),
        "UZ": (
            "GoldBot — yarim avtomatik XAUUSD (Oltin) savdo signali yordamchisi.\n"
            "U bozor tuzilishini tahlil qiladi va signallarni Telegram orqali yetkazadi."
        ),
        "RU": (
            "GoldBot — полуавтоматический торговый сигнальный ассистент по XAUUSD (Золото).\n"
            "Он анализирует структуру рынка и доставляет сигналы через Telegram."
        ),
    },
    "plan.error": {
        "EN": "Could not load plan: {detail}",
        "UZ": "Tarifni yuklab bo'lmadi: {detail}",
        "RU": "Не удалось загрузить тариф: {detail}",
    },
    "plan.display": {
        "EN": (
            "GoldBot Plan\n\nCurrent Plan:\n{plan}\n\nFeatures:\n✓ Basic signals\n✓ Signal history\n\n"
            "Upgrade:\nUse /upgrade"
        ),
        "UZ": (
            "GoldBot Tarifi\n\nJoriy tarif:\n{plan}\n\nImkoniyatlar:\n✓ Asosiy signallar\n✓ Signal tarixi\n\n"
            "Yangilash:\n/upgrade dan foydalaning"
        ),
        "RU": (
            "Тариф GoldBot\n\nТекущий тариф:\n{plan}\n\nВозможности:\n✓ Базовые сигналы\n✓ История сигналов\n\n"
            "Обновление:\nИспользуйте /upgrade"
        ),
    },
    "subscription.error": {
        "EN": "Could not load subscription: {detail}",
        "UZ": "Obunani yuklab bo'lmadi: {detail}",
        "RU": "Не удалось загрузить подписку: {detail}",
    },
    "subscription.display": {
        "EN": "Subscription Status\n\nPlan:\n{plan}\n\nStatus:\n{status}\n\nExpires:\n{expires}",
        "UZ": "Obuna Holati\n\nTarif:\n{plan}\n\nHolat:\n{status}\n\nMuddati:\n{expires}",
        "RU": "Статус Подписки\n\nТариф:\n{plan}\n\nСтатус:\n{status}\n\nИстекает:\n{expires}",
    },
    "upgrade.confirmation": {
        "EN": "Upgrade request received.\n\nPremium plans will be available soon.",
        "UZ": "Yangilash so'rovi qabul qilindi.\n\nPremium tariflar tez orada mavjud bo'ladi.",
        "RU": "Запрос на обновление получен.\n\nPremium тарифы скоро будут доступны.",
    },
    "feedback.prompt": {
        "EN": "Send your feedback:\n\nUse /feedback <your message>.",
        "UZ": "Fikr-mulohazangizni yuboring:\n\n/feedback <xabaringiz> dan foydalaning.",
        "RU": "Отправьте свой отзыв:\n\nИспользуйте /feedback <ваше сообщение>.",
    },
    "feedback.error": {
        "EN": "Could not send feedback: {error}",
        "UZ": "Fikr-mulohazani yuborib bo'lmadi: {error}",
        "RU": "Не удалось отправить отзыв: {error}",
    },
    "feedback.received": {
        "EN": "✅ Feedback received.\nID: #{id}\nStatus: {status}",
        "UZ": "✅ Fikr-mulohaza qabul qilindi.\nID: #{id}\nHolat: {status}",
        "RU": "✅ Отзыв получен.\nID: #{id}\nСтатус: {status}",
    },
    "contact.error": {
        "EN": "Could not process your phone number.",
        "UZ": "Telefon raqamingizni qayta ishlab bo'lmadi.",
        "RU": "Не удалось обработать ваш номер телефона.",
    },
    "contact.trial_active": {
        "EN": "✅ Phone verified. Your FREE trial is active.\nTrial expires: {expires}",
        "UZ": "✅ Telefon tasdiqlandi. Bepul sinov muddatingiz faol.\nSinov muddati tugaydi: {expires}",
        "RU": "✅ Телефон подтверждён. Ваш бесплатный пробный период активен.\nПробный период истекает: {expires}",
    },
    "contact.trial_ended": {
        "EN": "✅ Phone verified. Your FREE trial has ended.",
        "UZ": "✅ Telefon tasdiqlandi. Bepul sinov muddatingiz tugadi.",
        "RU": "✅ Телефон подтверждён. Ваш бесплатный пробный период закончился.",
    },
    "contact.not_registered": {
        "EN": "User not found -- send /start first.",
        "UZ": "Foydalanuvchi topilmadi -- avval /start yuboring.",
        "RU": "Пользователь не найден -- сначала отправьте /start.",
    },
    "contact.phone_reused": {
        "EN": "This phone number is already registered on another account.",
        "UZ": "Bu telefon raqami boshqa hisobda allaqachon ro'yxatdan o'tgan.",
        "RU": "Этот номер телефона уже зарегистрирован на другом аккаунте.",
    },
    "contact.wrong_owner": {
        "EN": "Please share your own phone number using the button.",
        "UZ": "Iltimos, tugma orqali o'zingizning telefon raqamingizni yuboring.",
        "RU": "Пожалуйста, поделитесь своим номером телефона с помощью кнопки.",
    },
    "registration.phone_prompt": {
        "EN": "One last step -- share your phone number to complete registration.",
        "UZ": "Oxirgi qadam -- ro'yxatdan o'tishni yakunlash uchun telefon raqamingizni yuboring.",
        "RU": "Последний шаг -- поделитесь номером телефона, чтобы завершить регистрацию.",
    },
    # Phase 1.6 -- /language's own reply text (language_status()/
    # language_handler()). _language_name() (telegram/handlers.py) stays
    # invariant across languages by design -- same "a language picker
    # shows each language's own name" rule as keyboard.language.*.
    "language.prompt": {
        "EN": "🌐 Language\nCurrent:\n{name}\n\nChoose a language",
        "UZ": "🌐 Til\nJoriy:\n{name}\n\nTilni tanlang",
        "RU": "🌐 Язык\nТекущий:\n{name}\n\nВыберите язык",
    },
    "language.invalid": {
        "EN": "⚠️ Invalid language. Choose one of: UZ, RU, EN.",
        "UZ": "⚠️ Noto'g'ri til. Quyidagilardan birini tanlang: UZ, RU, EN.",
        "RU": "⚠️ Неверный язык. Выберите один из: UZ, RU, EN.",
    },
    "language.already_selected": {
        "EN": "Already selected\n{name}",
        "UZ": "Allaqachon tanlangan\n{name}",
        "RU": "Уже выбрано\n{name}",
    },
    "language.update_error": {
        "EN": "Unable to update language.\nPlease try again.",
        "UZ": "Tilni yangilab bo'lmadi.\nQaytadan urinib ko'ring.",
        "RU": "Не удалось обновить язык.\nПопробуйте ещё раз.",
    },
    "language.updated": {
        "EN": "✅ Language updated\nCurrent language:\n{name}",
        "UZ": "✅ Til yangilandi\nJoriy til:\n{name}",
        "RU": "✅ Язык обновлён\nТекущий язык:\n{name}",
    },
    "common.na": {"EN": "N/A", "UZ": "N/A", "RU": "N/A"},
    "common.on": {"EN": "ON", "UZ": "YOQILGAN", "RU": "ВКЛ"},
    "common.off": {"EN": "OFF", "UZ": "O'CHIRILGAN", "RU": "ВЫКЛ"},
    # Phase 1.5 Localized Keyboards -- telegram/keyboards.py button labels
    # (USER-tier only; admin_panel_keyboard() stays English, Director
    # decision). Language-name and value buttons (lang_*, risk_*,
    # timeframe_*, strategy_*) are identical across all three languages
    # on purpose -- a language picker shows each language's own name,
    # and percentages/timeframes/strategy names are the same literal
    # value regardless of display language -- routed through t() anyway
    # so every button label has one single source, per Director's
    # instruction that ALL keyboard labels go through t().
    "keyboard.language.uz": {"EN": "🇺🇿 Uzbek", "UZ": "🇺🇿 Uzbek", "RU": "🇺🇿 Uzbek"},
    "keyboard.language.ru": {"EN": "🇷🇺 Русский", "UZ": "🇷🇺 Русский", "RU": "🇷🇺 Русский"},
    "keyboard.language.en": {"EN": "🇬🇧 English", "UZ": "🇬🇧 English", "RU": "🇬🇧 English"},
    "keyboard.risk.1": {"EN": "1%", "UZ": "1%", "RU": "1%"},
    "keyboard.risk.2": {"EN": "2%", "UZ": "2%", "RU": "2%"},
    "keyboard.risk.3": {"EN": "3%", "UZ": "3%", "RU": "3%"},
    "keyboard.risk.5": {"EN": "5%", "UZ": "5%", "RU": "5%"},
    "keyboard.timeframe.m15": {"EN": "M15", "UZ": "M15", "RU": "M15"},
    "keyboard.timeframe.h1": {"EN": "H1", "UZ": "H1", "RU": "H1"},
    "keyboard.timeframe.h4": {"EN": "H4", "UZ": "H4", "RU": "H4"},
    "keyboard.strategy.liquidity_sweep": {
        "EN": "Liquidity Sweep", "UZ": "Liquidity Sweep", "RU": "Liquidity Sweep",
    },
    "keyboard.strategy.fvg": {"EN": "FVG", "UZ": "FVG", "RU": "FVG"},
    "keyboard.strategy.amd": {"EN": "AMD", "UZ": "AMD", "RU": "AMD"},
    "keyboard.strategy.order_block": {
        "EN": "Order Block", "UZ": "Order Block", "RU": "Order Block",
    },
    "keyboard.settings.language": {"EN": "Language", "UZ": "Til", "RU": "Язык"},
    "keyboard.settings.risk": {"EN": "Risk", "UZ": "Risk", "RU": "Риск"},
    "keyboard.settings.strategy": {"EN": "Strategy", "UZ": "Strategiya", "RU": "Стратегия"},
    "keyboard.settings.timeframe": {
        "EN": "Timeframe", "UZ": "Vaqt oralig'i", "RU": "Таймфрейм",
    },
    "keyboard.settings.notifications": {
        "EN": "Notifications", "UZ": "Bildirishnomalar", "RU": "Уведомления",
    },
    "keyboard.notifications.enable": {
        "EN": "Enable Notifications", "UZ": "Bildirishnomalarni yoqish", "RU": "Включить уведомления",
    },
    "keyboard.notifications.disable": {
        "EN": "Disable Notifications", "UZ": "Bildirishnomalarni o'chirish", "RU": "Отключить уведомления",
    },
    "keyboard.phone_share": {
        "EN": "📱 Share Phone Number", "UZ": "📱 Telefon raqamini yuborish", "RU": "📱 Отправить номер телефона",
    },
    # V2 Phase 4 -- Persistent Menu (Telegram Menu Button) labels. USER
    # tier only; the ADMIN/OWNER menu's one extra entry each stays
    # language-invariant, same precedent telegram.keyboards.
    # admin_panel_keyboard() already established (Phase 1.5 Localized
    # Keyboards: OWNER/ADMIN UI is Director decision, out of scope for
    # USER-facing localization).
    "menu.home": {"EN": "🏠 Home", "UZ": "🏠 Bosh sahifa", "RU": "🏠 Главная"},
    "menu.profile": {"EN": "👤 Profile", "UZ": "👤 Profil", "RU": "👤 Профиль"},
    "menu.signals": {"EN": "📊 Signals", "UZ": "📊 Signallar", "RU": "📊 Сигналы"},
    "menu.subscription": {"EN": "💳 Subscription", "UZ": "💳 Obuna", "RU": "💳 Подписка"},
    "menu.settings": {"EN": "⚙️ Settings", "UZ": "⚙️ Sozlamalar", "RU": "⚙️ Настройки"},
    "menu.help": {"EN": "❓ Help", "UZ": "❓ Yordam", "RU": "❓ Помощь"},
    # V2 Phase 5.1 -- Reply Keyboard Navigation Mapping's ADMIN/OWNER
    # extra buttons. Language-invariant, matching the literal labels
    # telegram.menu_commands' _ADMIN_EXTRA/_OWNER_EXTRA already use for
    # the Persistent Menu (Phase 4) -- routed through t() here too so
    # every navigation button, including these, has one single source.
    "menu.admin": {"EN": "🛠 Admin", "UZ": "🛠 Admin", "RU": "🛠 Admin"},
    "menu.owner": {"EN": "👑 Owner", "UZ": "👑 Owner", "RU": "👑 Owner"},
    # V2 Phase 6.1 Director Decision 7 -- the short follow-up message
    # that carries the persistent Reply Keyboard right after
    # ReplyKeyboardRemove() on registration completion.
    "navigation.menu_ready": {
        "EN": "Menu ready.",
        "UZ": "Menyu tayyor.",
        "RU": "Меню готово.",
    },
    # V2 Phase 6.3 (Director Approved) -- Dynamic Reply Keyboard
    # Navigation: labels for the five submenu Reply Keyboards
    # (telegram/reply_keyboard_manager.py). "rkm." prefix distinguishes
    # these from the pre-existing "keyboard.settings.*"/"menu.*" keys,
    # which stay attached to the untouched inline value-picker
    # keyboards (settings_keyboard(), admin_panel_keyboard()) and the
    # Main-tier Reply Keyboard respectively -- deliberately not reused
    # here since several of those lack the emoji this phase's UX spec
    # requires. "◀️ Ortga" (rkm.back) is intentionally a different
    # glyph/label from Phase 6.1's retired "nav.back" ("⬅️ Orqaga") --
    # not the same button, a new one.
    #
    # Phase 6.3 Addendum (Director Review correction 3): Admin/Owner
    # action labels are localized in all three languages, same as
    # every other submenu -- the first pass's English-only precedent
    # (borrowed from the retired inline admin_panel_keyboard()) was
    # overridden by the Director: "GoldBot uch tilda ishlaydi. Demak
    # Reply Keyboard ham uch tilda bo'lishi kerak." "Runtime"/"Pipeline"
    # (rkm.owner.runtime/pipeline) stay as loanwords in UZ -- no
    # natural one-word Uzbek equivalent, same as their own RU rows.
    "rkm.back": {"EN": "◀️ Back", "UZ": "◀️ Ortga", "RU": "◀️ Назад"},
    "rkm.settings.language": {"EN": "🌐 Language", "UZ": "🌐 Til", "RU": "🌐 Язык"},
    "rkm.settings.risk": {"EN": "💰 Risk", "UZ": "💰 Risk", "RU": "💰 Риск"},
    "rkm.settings.strategy": {"EN": "📈 Strategy", "UZ": "📈 Strategiya", "RU": "📈 Стратегия"},
    "rkm.settings.timeframe": {"EN": "⏰ Timeframe", "UZ": "⏰ Vaqt oralig'i", "RU": "⏰ Таймфрейм"},
    "rkm.settings.notifications": {"EN": "🔔 Notifications", "UZ": "🔔 Bildirishnomalar", "RU": "🔔 Уведомления"},
    "rkm.admin.users": {"EN": "👥 Users", "UZ": "👥 Foydalanuvchilar", "RU": "👥 Пользователи"},
    "rkm.admin.statistics": {"EN": "📊 Statistics", "UZ": "📊 Statistika", "RU": "📊 Статистика"},
    "rkm.admin.system": {"EN": "🛠 System", "UZ": "🛠 Tizim", "RU": "🛠 Система"},
    "rkm.admin.broadcast": {"EN": "📢 Broadcast", "UZ": "📢 Xabar yuborish", "RU": "📢 Рассылка"},
    # Re-opens the Admin Panel (/admin) -- Director Review correction 1:
    # /addadmin is an action, not a menu destination (see
    # telegram/reply_keyboard_manager.py's module docstring).
    "rkm.admin.admins": {
        "EN": "👑 Admin Management", "UZ": "👑 Admin boshqaruvi", "RU": "👑 Управление администраторами",
    },
    "rkm.owner.runtime": {"EN": "⚙️ Runtime", "UZ": "⚙️ Runtime", "RU": "⚙️ Runtime"},
    "rkm.owner.health": {"EN": "❤️ Health", "UZ": "❤️ Salomatlik", "RU": "❤️ Здоровье"},
    "rkm.owner.performance": {"EN": "📈 Performance", "UZ": "📈 Unumdorlik", "RU": "📈 Производительность"},
    "rkm.owner.errors": {"EN": "🚨 Errors", "UZ": "🚨 Xatoliklar", "RU": "🚨 Ошибки"},
    "rkm.owner.pipeline": {"EN": "📦 Pipeline", "UZ": "📦 Pipeline", "RU": "📦 Пайплайн"},
    "rkm.owner.reports": {"EN": "📋 Reports", "UZ": "📋 Hisobotlar", "RU": "📋 Отчёты"},
    "rkm.profile.profile": {"EN": "📄 Profile", "UZ": "📄 Profile", "RU": "📄 Профиль"},
    "rkm.signals.live": {"EN": "📈 Live Signals", "UZ": "📈 Live Signals", "RU": "📈 Живые сигналы"},
    "rkm.signals.history": {"EN": "📜 History", "UZ": "📜 History", "RU": "📜 История"},
    "rkm.signals.premium": {"EN": "⭐ Premium", "UZ": "⭐ Premium", "RU": "⭐ Премиум"},
}


def t(key: str, language: Optional[str] = None, **kwargs) -> str:
    """
    Looks up `key` in the caller's language, falling back to EN and
    then to any entry the key has at all -- a missing key returns the
    key itself (loudly visible in a chat transcript, never a crash).
    Never raises: a bad format() placeholder falls back to the
    unformatted template rather than propagating.
    """
    entry = _CATALOG.get(key)
    if entry is None:
        return key

    code = (language or _DEFAULT_LANGUAGE).upper()
    template = entry.get(code) or entry.get(_DEFAULT_LANGUAGE) or next(iter(entry.values()))

    if not kwargs:
        return template
    try:
        return template.format(**kwargs)
    except Exception:
        return template
