"""
Мультиязычная поддержка для Answers Platform.
Поддерживает 12 основных языков мира.
"""

# Доступные языки
SUPPORTED_LANGUAGES = {
    "en": {
        "name": "English",
        "native_name": "English",
        "flag": "🇬🇧",
        "direction": "ltr"
    },
    "es": {
        "name": "Spanish",
        "native_name": "Español",
        "flag": "🇪🇸",
        "direction": "ltr"
    },
    "de": {
        "name": "German",
        "native_name": "Deutsch",
        "flag": "🇩🇪",
        "direction": "ltr"
    },
    "ar": {
        "name": "Arabic",
        "native_name": "العربية",
        "flag": "🇸🇦",
        "direction": "rtl"
    },
    "tr": {
        "name": "Turkish",
        "native_name": "Türkçe",
        "flag": "🇹🇷",
        "direction": "ltr"
    },
    "ru": {
        "name": "Russian",
        "native_name": "Русский",
        "flag": "🇷🇺",
        "direction": "ltr"
    },
    "pt": {
        "name": "Portuguese",
        "native_name": "Português",
        "flag": "🇧🇷",
        "direction": "ltr"
    },
    "zh": {
        "name": "Chinese",
        "native_name": "中文",
        "flag": "🇨🇳",
        "direction": "ltr"
    },
    "it": {
        "name": "Italian",
        "native_name": "Italiano",
        "flag": "🇮🇹",
        "direction": "ltr"
    },
    "fr": {
        "name": "French",
        "native_name": "Français",
        "flag": "🇫🇷",
        "direction": "ltr"
    },
    "hi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "flag": "🇮🇳",
        "direction": "ltr"
    },
    "ja": {
        "name": "Japanese",
        "native_name": "日本語",
        "flag": "🇯🇵",
        "direction": "ltr"
    }
}

# Переводы интерфейса
TRANSLATIONS = {
    "en": {
        # Header & Navigation
        "app_title": "Answers Platform",
        "app_subtitle": "Wisdom from 8 philosophical and religious traditions",
        
        # Main Page
        "select_tradition": "Select a Tradition",
        "enter_question": "Enter your question",
        "question_placeholder": "For example: How to overcome fear of the future?",
        "get_answer": "Get Answer",
        "ask_question": "Ask a Question",
        
        # Results
        "answer": "Answer",
        "sources": "Sources",
        "compare_traditions": "See what other traditions say",
        "comparing": "Comparing approaches...",
        "other_traditions": "Other Traditions",
        
        # Traditions
        "tradition_stoicism": "Stoicism",
        "tradition_christianity": "Christianity",
        "tradition_islam": "Islam",
        "tradition_buddhism": "Buddhism",
        "tradition_judaism": "Judaism",
        "tradition_hinduism": "Hinduism",
        "tradition_taoism": "Taoism",
        "tradition_humanism": "Secular Humanism",
        
        # Errors & Status
        "error": "Error",
        "loading": "Loading...",
        "generating_answer": "Generating answer...",
        "no_sources": "Not enough sources to answer this question",
        "try_again": "Try Again",
        
        # Metadata
        "provider": "Provider",
        "model": "Model",
        "response_time": "Response Time",
        "fallback_used": "Fallback Used",
        
        # Footer
        "powered_by": "Powered by AI with authentic sources",
        "privacy": "Privacy-focused: No tracking without consent"
    },
    
    "ru": {
        # Header & Navigation
        "app_title": "Платформа Ответов",
        "app_subtitle": "Мудрость 8 философских и религиозных традиций",
        
        # Main Page
        "select_tradition": "Выберите традицию",
        "enter_question": "Введите ваш вопрос",
        "question_placeholder": "Например: Как преодолеть страх перед будущим?",
        "get_answer": "Получить ответ",
        "ask_question": "Задать вопрос",
        
        # Results
        "answer": "Ответ",
        "sources": "Источники",
        "compare_traditions": "Посмотреть, что говорят другие традиции",
        "comparing": "Сравниваем подходы...",
        "other_traditions": "Другие традиции",
        
        # Traditions
        "tradition_stoicism": "Стоицизм",
        "tradition_christianity": "Христианство",
        "tradition_islam": "Ислам",
        "tradition_buddhism": "Буддизм",
        "tradition_judaism": "Иудаизм",
        "tradition_hinduism": "Индуизм",
        "tradition_taoism": "Даосизм",
        "tradition_humanism": "Светский гуманизм",
        
        # Errors & Status
        "error": "Ошибка",
        "loading": "Загрузка...",
        "generating_answer": "Генерируем ответ...",
        "no_sources": "Недостаточно источников для ответа",
        "try_again": "Попробовать снова",
        
        # Metadata
        "provider": "Провайдер",
        "model": "Модель",
        "response_time": "Время ответа",
        "fallback_used": "Использован fallback",
        
        # Footer
        "powered_by": "Работает на ИИ с аутентичными источниками",
        "privacy": "Конфиденциальность: без отслеживания без согласия"
    },
    
    "es": {
        "app_title": "Plataforma de Respuestas",
        "app_subtitle": "Sabiduría de 8 tradiciones filosóficas y religiosas",
        "select_tradition": "Selecciona una tradición",
        "enter_question": "Ingresa tu pregunta",
        "question_placeholder": "Por ejemplo: ¿Cómo superar el miedo al futuro?",
        "get_answer": "Obtener Respuesta",
        "ask_question": "Hacer una Pregunta",
        "answer": "Respuesta",
        "sources": "Fuentes",
        "compare_traditions": "Ver qué dicen otras tradiciones",
        "comparing": "Comparando enfoques...",
        "other_traditions": "Otras Tradiciones",
        "tradition_stoicism": "Estoicismo",
        "tradition_christianity": "Cristianismo",
        "tradition_islam": "Islam",
        "tradition_buddhism": "Budismo",
        "tradition_judaism": "Judaísmo",
        "tradition_hinduism": "Hinduismo",
        "tradition_taoism": "Taoísmo",
        "tradition_humanism": "Humanismo Secular",
        "error": "Error",
        "loading": "Cargando...",
        "generating_answer": "Generando respuesta...",
        "no_sources": "No hay suficientes fuentes para responder",
        "try_again": "Intentar de nuevo",
        "provider": "Proveedor",
        "model": "Modelo",
        "response_time": "Tiempo de Respuesta",
        "fallback_used": "Fallback Usado",
        "powered_by": "Impulsado por IA con fuentes auténticas",
        "privacy": "Privacidad: Sin rastreo sin consentimiento"
    },
    
    "fr": {
        "app_title": "Plateforme de Réponses",
        "app_subtitle": "Sagesse de 8 traditions philosophiques et religieuses",
        "select_tradition": "Sélectionnez une tradition",
        "enter_question": "Entrez votre question",
        "question_placeholder": "Par exemple: Comment surmonter la peur de l'avenir?",
        "get_answer": "Obtenir la Réponse",
        "ask_question": "Poser une Question",
        "answer": "Réponse",
        "sources": "Sources",
        "compare_traditions": "Voir ce que disent les autres traditions",
        "comparing": "Comparaison des approches...",
        "other_traditions": "Autres Traditions",
        "tradition_stoicism": "Stoïcisme",
        "tradition_christianity": "Christianisme",
        "tradition_islam": "Islam",
        "tradition_buddhism": "Bouddhisme",
        "tradition_judaism": "Judaïsme",
        "tradition_hinduism": "Hindouisme",
        "tradition_taoism": "Taoïsme",
        "tradition_humanism": "Humanisme Laïque",
        "error": "Erreur",
        "loading": "Chargement...",
        "generating_answer": "Génération de la réponse...",
        "no_sources": "Pas assez de sources pour répondre",
        "try_again": "Réessayer",
        "provider": "Fournisseur",
        "model": "Modèle",
        "response_time": "Temps de Réponse",
        "fallback_used": "Fallback Utilisé",
        "powered_by": "Propulsé par l'IA avec des sources authentiques",
        "privacy": "Confidentialité: Pas de suivi sans consentement"
    },
    
    "de": {
        "app_title": "Antworten Plattform",
        "app_subtitle": "Weisheit aus 8 philosophischen und religiösen Traditionen",
        "select_tradition": "Wähle eine Tradition",
        "enter_question": "Gib deine Frage ein",
        "question_placeholder": "Zum Beispiel: Wie überwinde ich Angst vor der Zukunft?",
        "get_answer": "Antwort Erhalten",
        "ask_question": "Frage Stellen",
        "answer": "Antwort",
        "sources": "Quellen",
        "compare_traditions": "Sehen, was andere Traditionen sagen",
        "comparing": "Vergleiche Ansätze...",
        "other_traditions": "Andere Traditionen",
        "tradition_stoicism": "Stoizismus",
        "tradition_christianity": "Christentum",
        "tradition_islam": "Islam",
        "tradition_buddhism": "Buddhismus",
        "tradition_judaism": "Judentum",
        "tradition_hinduism": "Hinduismus",
        "tradition_taoism": "Taoismus",
        "tradition_humanism": "Säkularer Humanismus",
        "error": "Fehler",
        "loading": "Laden...",
        "generating_answer": "Antwort wird generiert...",
        "no_sources": "Nicht genug Quellen für eine Antwort",
        "try_again": "Erneut versuchen",
        "provider": "Anbieter",
        "model": "Modell",
        "response_time": "Antwortzeit",
        "fallback_used": "Fallback Verwendet",
        "powered_by": "Betrieben durch KI mit authentischen Quellen",
        "privacy": "Datenschutz: Kein Tracking ohne Zustimmung"
    },
    
    "zh": {
        "app_title": "答案平台",
        "app_subtitle": "来自8个哲学和宗教传统的智慧",
        "select_tradition": "选择一个传统",
        "enter_question": "输入你的问题",
        "question_placeholder": "例如：如何克服对未来的恐惧？",
        "get_answer": "获取答案",
        "ask_question": "提问",
        "answer": "答案",
        "sources": "来源",
        "compare_traditions": "查看其他传统的观点",
        "comparing": "比较不同方法...",
        "other_traditions": "其他传统",
        "tradition_stoicism": "斯多葛主义",
        "tradition_christianity": "基督教",
        "tradition_islam": "伊斯兰教",
        "tradition_buddhism": "佛教",
        "tradition_judaism": "犹太教",
        "tradition_hinduism": "印度教",
        "tradition_taoism": "道教",
        "tradition_humanism": "世俗人文主义",
        "error": "错误",
        "loading": "加载中...",
        "generating_answer": "生成答案中...",
        "no_sources": "没有足够的来源来回答",
        "try_again": "重试",
        "provider": "提供商",
        "model": "模型",
        "response_time": "响应时间",
        "fallback_used": "已使用备用",
        "powered_by": "由AI驱动，提供真实来源",
        "privacy": "隐私保护：未经同意不跟踪"
    },
    
    "ar": {
        "app_title": "منصة الإجابات",
        "app_subtitle": "حكمة من 8 تقاليد فلسفية ودينية",
        "select_tradition": "اختر تقليدًا",
        "enter_question": "أدخل سؤالك",
        "question_placeholder": "على سبيل المثال: كيف تتغلب على الخوف من المستقبل؟",
        "get_answer": "احصل على إجابة",
        "ask_question": "اطرح سؤالاً",
        "answer": "إجابة",
        "sources": "مصادر",
        "compare_traditions": "انظر ماذا تقول التقاليد الأخرى",
        "comparing": "مقارنة النهج...",
        "other_traditions": "تقاليد أخرى",
        "tradition_stoicism": "الرواقية",
        "tradition_christianity": "المسيحية",
        "tradition_islam": "الإسلام",
        "tradition_buddhism": "البوذية",
        "tradition_judaism": "اليهودية",
        "tradition_hinduism": "الهندوسية",
        "tradition_taoism": "الطاوية",
        "tradition_humanism": "الإنسانية العلمانية",
        "error": "خطأ",
        "loading": "جارٍ التحميل...",
        "generating_answer": "جارٍ إنشاء الإجابة...",
        "no_sources": "لا توجد مصادر كافية للإجابة",
        "try_again": "حاول مرة أخرى",
        "provider": "مزود",
        "model": "نموذج",
        "response_time": "وقت الاستجابة",
        "fallback_used": "تم استخدام الاحتياطي",
        "powered_by": "مدعوم بالذكاء الاصطناعي مع مصادر موثوقة",
        "privacy": "الخصوصية: لا تتبع بدون موافقة"
    },
    
    "pt": {
        "app_title": "Plataforma de Respostas",
        "app_subtitle": "Sabedoria de 8 tradições filosóficas e religiosas",
        "select_tradition": "Selecione uma tradição",
        "enter_question": "Digite sua pergunta",
        "question_placeholder": "Por exemplo: Como superar o medo do futuro?",
        "get_answer": "Obter Resposta",
        "ask_question": "Fazer Pergunta",
        "answer": "Resposta",
        "sources": "Fontes",
        "compare_traditions": "Ver o que outras tradições dizem",
        "comparing": "Comparando abordagens...",
        "other_traditions": "Outras Tradições",
        "tradition_stoicism": "Estoicismo",
        "tradition_christianity": "Cristianismo",
        "tradition_islam": "Islã",
        "tradition_buddhism": "Budismo",
        "tradition_judaism": "Judaísmo",
        "tradition_hinduism": "Hinduísmo",
        "tradition_taoism": "Taoísmo",
        "tradition_humanism": "Humanismo Secular",
        "error": "Erro",
        "loading": "Carregando...",
        "generating_answer": "Gerando resposta...",
        "no_sources": "Fontes insuficientes para responder",
        "try_again": "Tentar Novamente",
        "provider": "Provedor",
        "model": "Modelo",
        "response_time": "Tempo de Resposta",
        "fallback_used": "Fallback Usado",
        "powered_by": "Impulsionado por IA com fontes autênticas",
        "privacy": "Privacidade: Sem rastreamento sem consentimento"
    },
    
    "it": {
        "app_title": "Piattaforma di Risposte",
        "app_subtitle": "Saggezza da 8 tradizioni filosofiche e religiose",
        "select_tradition": "Seleziona una tradizione",
        "enter_question": "Inserisci la tua domanda",
        "question_placeholder": "Per esempio: Come superare la paura del futuro?",
        "get_answer": "Ottieni Risposta",
        "ask_question": "Fai una Domanda",
        "answer": "Risposta",
        "sources": "Fonti",
        "compare_traditions": "Vedi cosa dicono altre tradizioni",
        "comparing": "Confrontando approcci...",
        "other_traditions": "Altre Tradizioni",
        "tradition_stoicism": "Stoicismo",
        "tradition_christianity": "Cristianesimo",
        "tradition_islam": "Islam",
        "tradition_buddhism": "Buddhismo",
        "tradition_judaism": "Ebraismo",
        "tradition_hinduism": "Induismo",
        "tradition_taoism": "Taoismo",
        "tradition_humanism": "Umanesimo Secolare",
        "error": "Errore",
        "loading": "Caricamento...",
        "generating_answer": "Generazione risposta...",
        "no_sources": "Fonti insufficienti per rispondere",
        "try_again": "Riprova",
        "provider": "Provider",
        "model": "Modello",
        "response_time": "Tempo di Risposta",
        "fallback_used": "Fallback Usato",
        "powered_by": "Guidato dall'IA con fonti autentiche",
        "privacy": "Privacy: Nessun tracciamento senza consenso"
    },
    
    "tr": {
        "app_title": "Cevaplar Platformu",
        "app_subtitle": "8 felsefi ve dini gelenekten bilgelik",
        "select_tradition": "Bir gelenek seçin",
        "enter_question": "Sorunuzu girin",
        "question_placeholder": "Örneğin: Gelecek korkusunun üstesinden nasıl gelinir?",
        "get_answer": "Cevap Al",
        "ask_question": "Soru Sor",
        "answer": "Cevap",
        "sources": "Kaynaklar",
        "compare_traditions": "Diğer geleneklerin ne dediğini görün",
        "comparing": "Yaklaşımlar karşılaştırılıyor...",
        "other_traditions": "Diğer Gelenekler",
        "tradition_stoicism": "Stoacılık",
        "tradition_christianity": "Hıristiyanlık",
        "tradition_islam": "İslam",
        "tradition_buddhism": "Budizm",
        "tradition_judaism": "Yahudilik",
        "tradition_hinduism": "Hinduizm",
        "tradition_taoism": "Taoculuk",
        "tradition_humanism": "Seküler Hümanizm",
        "error": "Hata",
        "loading": "Yükleniyor...",
        "generating_answer": "Cevap oluşturuluyor...",
        "no_sources": "Cevap vermek için yeterli kaynak yok",
        "try_again": "Tekrar Dene",
        "provider": "Sağlayıcı",
        "model": "Model",
        "response_time": "Yanıt Süresi",
        "fallback_used": "Fallback Kullanıldı",
        "powered_by": "Otantik kaynaklarla AI destekli",
        "privacy": "Gizlilik: İzinsiz takip yok"
    },
    
    "hi": {
        "app_title": "उत्तर प्लेटफॉर्म",
        "app_subtitle": "8 दार्शनिक और धार्मिक परंपराओं से ज्ञान",
        "select_tradition": "एक परंपरा चुनें",
        "enter_question": "अपना प्रश्न दर्ज करें",
        "question_placeholder": "उदाहरण के लिए: भविष्य के डर को कैसे दूर करें?",
        "get_answer": "उत्तर प्राप्त करें",
        "ask_question": "प्रश्न पूछें",
        "answer": "उत्तर",
        "sources": "स्रोत",
        "compare_traditions": "देखें अन्य परंपराएं क्या कहती हैं",
        "comparing": "दृष्टिकोणों की तुलना...",
        "other_traditions": "अन्य परंपराएं",
        "tradition_stoicism": "स्टोइसिज़्म",
        "tradition_christianity": "ईसाई धर्म",
        "tradition_islam": "इस्लाम",
        "tradition_buddhism": "बौद्ध धर्म",
        "tradition_judaism": "यहूदी धर्म",
        "tradition_hinduism": "हिंदू धर्म",
        "tradition_taoism": "ताओ धर्म",
        "tradition_humanism": "धर्मनिरपेक्ष मानवतावाद",
        "error": "त्रुटि",
        "loading": "लोड हो रहा है...",
        "generating_answer": "उत्तर उत्पन्न हो रहा है...",
        "no_sources": "उत्तर देने के लिए पर्याप्त स्रोत नहीं",
        "try_again": "पुनः प्रयास करें",
        "provider": "प्रदाता",
        "model": "मॉडल",
        "response_time": "प्रतिक्रिया समय",
        "fallback_used": "फ़ॉलबैक उपयोग किया गया",
        "powered_by": "प्रामाणिक स्रोतों के साथ AI द्वारा संचालित",
        "privacy": "गोपनीयता: सहमति के बिना कोई ट्रैकिंग नहीं"
    },
    
    "ja": {
        "app_title": "アンサープラットフォーム",
        "app_subtitle": "8つの哲学的・宗教的伝統からの知恵",
        "select_tradition": "伝統を選択",
        "enter_question": "質問を入力",
        "question_placeholder": "例：将来への恐怖を克服するには？",
        "get_answer": "回答を取得",
        "ask_question": "質問する",
        "answer": "回答",
        "sources": "情報源",
        "compare_traditions": "他の伝統の見解を見る",
        "comparing": "アプローチを比較中...",
        "other_traditions": "他の伝統",
        "tradition_stoicism": "ストア派",
        "tradition_christianity": "キリスト教",
        "tradition_islam": "イスラム教",
        "tradition_buddhism": "仏教",
        "tradition_judaism": "ユダヤ教",
        "tradition_hinduism": "ヒンドゥー教",
        "tradition_taoism": "道教",
        "tradition_humanism": "世俗的人間主義",
        "error": "エラー",
        "loading": "読み込み中...",
        "generating_answer": "回答を生成中...",
        "no_sources": "回答するための情報源が不足しています",
        "try_again": "再試行",
        "provider": "プロバイダー",
        "model": "モデル",
        "response_time": "応答時間",
        "fallback_used": "フォールバック使用済み",
        "powered_by": "信頼できる情報源によるAI搭載",
        "privacy": "プライバシー：同意なしに追跡しません"
    }
}


def get_translation(lang_code: str, key: str, default: str = None) -> str:
    """
    Получить перевод для указанного языка и ключа.
    
    Args:
        lang_code: Код языка (например, 'en', 'ru', 'es')
        key: Ключ перевода
        default: Значение по умолчанию если перевод не найден
    
    Returns:
        Переведенная строка или значение по умолчанию
    """
    if lang_code not in TRANSLATIONS:
        lang_code = "en"  # Fallback to English
    
    translation = TRANSLATIONS[lang_code].get(key)
    if translation is None and default:
        return default
    return translation or key


def get_language_info(lang_code: str) -> dict:
    """
    Получить информацию о языке.
    
    Args:
        lang_code: Код языка
    
    Returns:
        Словарь с информацией о языке
    """
    return SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES["en"])


def detect_language_from_headers(headers: dict) -> str:
    """
    Определить язык из HTTP заголовков (Accept-Language).
    
    Args:
        headers: HTTP заголовки запроса
    
    Returns:
        Код языка
    """
    accept_language = headers.get("accept-language", "en")
    
    # Простая логика определения языка
    for lang_code in SUPPORTED_LANGUAGES.keys():
        if lang_code in accept_language.lower():
            return lang_code
    
    return "en"  # Default to English
