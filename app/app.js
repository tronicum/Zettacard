// drivenow MVP — question browser (Sprint 1)
// Scope: click through all questions, switch language, reveal answer + explanation.
// Explicitly OUT of scope: exam simulation, scoring, pass/fail, timers.

const UI_STRINGS = {
  de: {
    title: "drivenow — Lernkarten",
    subtitle: (n) => `${n} Fragen · Lernkarten & Prüfungssimulation`,
    filterAll: "Alle",
    back: "← Liste",
    reveal: "Antwort anzeigen",
    revealed: "Antwort angezeigt",
    prev: "← Vorherige",
    next: "Nächste →",
    progress: (i, n) => `Frage ${i} von ${n}`,
    points: (p) => `${p} Punkte`,
    highStakes: "Sicherheitsrelevante Frage",
    imageNote: "🖼️ Bild ausstehend — Referenz: ",
    explanationLabel: "Erklärung",
    legalBasis: "Rechtsgrundlage",
    installHint: "Zum Startbildschirm hinzufügen für Offline-Nutzung.",
    empty: "Keine Fragen in dieser Kategorie.",
    correctMark: "Richtig",
  },
  en: {
    title: "drivenow — Flashcards",
    subtitle: (n) => `${n} questions · flashcards & exam simulation`,
    filterAll: "All",
    back: "← List",
    reveal: "Show answer",
    revealed: "Answer shown",
    prev: "← Previous",
    next: "Next →",
    progress: (i, n) => `Question ${i} of ${n}`,
    points: (p) => `${p} points`,
    highStakes: "Safety-critical question",
    imageNote: "🖼️ Image pending — ref: ",
    explanationLabel: "Explanation",
    legalBasis: "Legal basis",
    installHint: "Add to your home screen to use offline.",
    empty: "No questions in this category.",
    correctMark: "Correct",
  },
  uk: {
    title: "drivenow — Картки для навчання",
    subtitle: (n) => `${n} питань · картки та симуляція іспиту`,
    filterAll: "Усі",
    back: "← Список",
    reveal: "Показати відповідь",
    revealed: "Відповідь показано",
    prev: "← Попереднє",
    next: "Наступне →",
    progress: (i, n) => `Питання ${i} з ${n}`,
    points: (p) => `${p} балів`,
    highStakes: "Питання, важливе для безпеки",
    imageNote: "🖼️ Зображення відсутнє — посилання: ",
    explanationLabel: "Пояснення",
    legalBasis: "Правова основа",
    installHint: "Додайте на головний екран для використання офлайн.",
    empty: "У цій категорії немає питань.",
    correctMark: "Правильно",
  },
  pl: {
    title: "drivenow — Fiszki",
    subtitle: (n) => `${n} pytań · fiszki i symulacja egzaminu`,
    filterAll: "Wszystkie",
    back: "← Lista",
    reveal: "Pokaż odpowiedź",
    revealed: "Odpowiedź pokazana",
    prev: "← Poprzednie",
    next: "Następne →",
    progress: (i, n) => `Pytanie ${i} z ${n}`,
    points: (p) => `${p} punktów`,
    highStakes: "Pytanie istotne dla bezpieczeństwa",
    imageNote: "🖼️ Brak obrazu — odniesienie: ",
    explanationLabel: "Wyjaśnienie",
    legalBasis: "Podstawa prawna",
    installHint: "Dodaj do ekranu głównego, aby korzystać offline.",
    empty: "Brak pytań w tej kategorii.",
    correctMark: "Poprawnie",
  },
  ar: {
    title: "drivenow — بطاقات تعليمية",
    subtitle: (n) => `${n} سؤال · بطاقات تعليمية ومحاكاة امتحان`,
    filterAll: "الكل",
    back: "→ القائمة",
    reveal: "إظهار الإجابة",
    revealed: "تم إظهار الإجابة",
    prev: "→ السابق",
    next: "← التالي",
    progress: (i, n) => `السؤال ${i} من ${n}`,
    points: (p) => `${p} نقاط`,
    highStakes: "سؤال حرج للسلامة",
    imageNote: "🖼️ الصورة غير متوفرة — المرجع: ",
    explanationLabel: "الشرح",
    legalBasis: "الأساس القانوني",
    installHint: "أضف إلى الشاشة الرئيسية للاستخدام دون اتصال بالإنترنت.",
    empty: "لا توجد أسئلة في هذه الفئة.",
    correctMark: "صحيح",
  },
  zh: {
    title: "drivenow — 学习卡片",
    subtitle: (n) => `${n} 道题 · 学习卡片与模拟考试`,
    filterAll: "全部",
    back: "← 列表",
    reveal: "显示答案",
    revealed: "答案已显示",
    prev: "← 上一题",
    next: "下一题 →",
    progress: (i, n) => `第 ${i} 题，共 ${n} 题`,
    points: (p) => `${p} 分`,
    highStakes: "安全关键问题",
    imageNote: "🖼️ 图片暂缺 — 参考：",
    explanationLabel: "解释",
    legalBasis: "法律依据",
    installHint: "添加到主屏幕即可离线使用。",
    empty: "该类别下没有题目。",
    correctMark: "正确",
  },
  hi: {
    title: "drivenow — अभ्यास कार्ड",
    subtitle: (n) => `${n} प्रश्न · अभ्यास कार्ड और परीक्षा सिमुलेशन`,
    filterAll: "सभी",
    back: "← सूची",
    reveal: "उत्तर दिखाएं",
    revealed: "उत्तर दिखाया गया",
    prev: "← पिछला",
    next: "अगला →",
    progress: (i, n) => `प्रश्न ${i} / ${n}`,
    points: (p) => `${p} अंक`,
    highStakes: "सुरक्षा-महत्वपूर्ण प्रश्न",
    imageNote: "🖼️ चित्र उपलब्ध नहीं — संदर्भ: ",
    explanationLabel: "स्पष्टीकरण",
    legalBasis: "कानूनी आधार",
    installHint: "ऑफ़लाइन उपयोग के लिए होम स्क्रीन पर जोड़ें।",
    empty: "इस श्रेणी में कोई प्रश्न नहीं है।",
    correctMark: "सही",
  },
  tr: {
    title: "drivenow — Çalışma Kartları",
    subtitle: (n) => `${n} soru · çalışma kartları ve sınav simülasyonu`,
    filterAll: "Tümü",
    back: "← Liste",
    reveal: "Cevabı göster",
    revealed: "Cevap gösterildi",
    prev: "← Önceki",
    next: "Sonraki →",
    progress: (i, n) => `${n} sorudan ${i}.`,
    points: (p) => `${p} puan`,
    highStakes: "Güvenlik açısından kritik soru",
    imageNote: "🖼️ Görsel eksik — referans: ",
    explanationLabel: "Açıklama",
    legalBasis: "Yasal dayanak",
    installHint: "Çevrimdışı kullanım için ana ekrana ekleyin.",
    empty: "Bu kategoride soru yok.",
    correctMark: "Doğru",
  },
  fr: {
    title: "drivenow — Fiches d'apprentissage",
    subtitle: (n) => `${n} questions · fiches et simulation d'examen`,
    filterAll: "Toutes",
    back: "← Liste",
    reveal: "Afficher la réponse",
    revealed: "Réponse affichée",
    prev: "← Précédente",
    next: "Suivante →",
    progress: (i, n) => `Question ${i} sur ${n}`,
    points: (p) => `${p} points`,
    highStakes: "Question critique pour la sécurité",
    imageNote: "🖼️ Image manquante — référence : ",
    explanationLabel: "Explication",
    legalBasis: "Base légale",
    installHint: "Ajoutez à l'écran d'accueil pour une utilisation hors ligne.",
    empty: "Aucune question dans cette catégorie.",
    correctMark: "Correct",
  },
  ru: {
    title: "drivenow — Карточки для изучения",
    subtitle: (n) => `${n} вопросов · карточки и симуляция экзамена`,
    filterAll: "Все",
    back: "← Список",
    reveal: "Показать ответ",
    revealed: "Ответ показан",
    prev: "← Предыдущий",
    next: "Следующий →",
    progress: (i, n) => `Вопрос ${i} из ${n}`,
    points: (p) => `${p} баллов`,
    highStakes: "Вопрос, критичный для безопасности",
    imageNote: "🖼️ Изображение отсутствует — ссылка: ",
    explanationLabel: "Объяснение",
    legalBasis: "Правовая основа",
    installHint: "Добавьте на главный экран для использования офлайн.",
    empty: "В этой категории нет вопросов.",
    correctMark: "Правильно",
  },
  es: {
    title: "drivenow — Tarjetas de estudio",
    subtitle: (n) => `${n} preguntas · tarjetas y simulación de examen`,
    filterAll: "Todas",
    back: "← Lista",
    reveal: "Mostrar respuesta",
    revealed: "Respuesta mostrada",
    prev: "← Anterior",
    next: "Siguiente →",
    progress: (i, n) => `Pregunta ${i} de ${n}`,
    points: (p) => `${p} puntos`,
    highStakes: "Pregunta crítica para la seguridad",
    imageNote: "🖼️ Imagen pendiente — referencia: ",
    explanationLabel: "Explicación",
    legalBasis: "Base legal",
    installHint: "Añade a la pantalla de inicio para usarlo sin conexión.",
    empty: "No hay preguntas en esta categoría.",
    correctMark: "Correcto",
  },
  it: {
    title: "drivenow — Schede di studio",
    subtitle: (n) => `${n} domande · schede e simulazione d'esame`,
    filterAll: "Tutte",
    back: "← Elenco",
    reveal: "Mostra risposta",
    revealed: "Risposta mostrata",
    prev: "← Precedente",
    next: "Successiva →",
    progress: (i, n) => `Domanda ${i} di ${n}`,
    points: (p) => `${p} punti`,
    highStakes: "Domanda critica per la sicurezza",
    imageNote: "🖼️ Immagine mancante — riferimento: ",
    explanationLabel: "Spiegazione",
    legalBasis: "Base giuridica",
    installHint: "Aggiungi alla schermata Home per l'uso offline.",
    empty: "Nessuna domanda in questa categoria.",
    correctMark: "Corretto",
  },
};

// Exam mode strings (DN-29). Kept as a separate dict from UI_STRINGS so the
// large existing per-locale blocks above didn't need touching individually -
// exam mode is a newer, additive feature layered on top of the flashcard UI.
const EXAM_STRINGS = {
  de: { startBtn: "Prüfung", pickerTitle: "Prüfungsmodus wählen", pickerDesc: "Wählen Sie, wie Sie üben möchten. Beide Modi ziehen 30 Fragen nach realer Gewichtung und werten nach der echten Bestehensregel aus.",
    trainingTitle: "Übungsprüfung", trainingDesc: "Ohne Zeitlimit. Ideal zum ruhigen Üben.",
    simTitle: "Prüfungssimulation", simDesc: "45 Minuten Zeitlimit, wie bei der echten Prüfung.",
    cancel: "Abbrechen", progress: (i, n) => `Frage ${i} von ${n}`, next: "Weiter", finish: "Prüfung abschließen",
    exit: "Abbrechen", timeUp: "Die Zeit ist abgelaufen — die Prüfung wurde automatisch abgegeben.",
    resultsPass: "Bestanden", resultsFail: "Nicht bestanden",
    summary: (err, wrong) => `Fehlerpunkte: ${err} von max. 10 zulässig. Falsch beantwortete sicherheitsrelevante Fragen: ${wrong} (bei 2 oder mehr: automatisches Nichtbestehen).`,
    reviewLabel: "Überprüfung der falschen Antworten", yourAnswer: "Ihre Antwort", rightAnswer: "Richtige Antwort",
    close: "Schließen", noMistakes: "Alle Fragen richtig beantwortet — sehr gut!", confirmExit: "Prüfung wirklich abbrechen? Der Fortschritt geht verloren." },
  en: { startBtn: "Exam", pickerTitle: "Choose exam mode", pickerDesc: "Choose how you want to practice. Both modes draw 30 questions with realistic weighting and score using the real pass rule.",
    trainingTitle: "Training exam", trainingDesc: "No time limit. Good for calm practice.",
    simTitle: "Simulated real exam", simDesc: "45-minute time limit, like the real exam.",
    cancel: "Cancel", progress: (i, n) => `Question ${i} of ${n}`, next: "Next", finish: "Finish exam",
    exit: "Cancel", timeUp: "Time is up — the exam was submitted automatically.",
    resultsPass: "Passed", resultsFail: "Not passed",
    summary: (err, wrong) => `Error points: ${err} of max. 10 allowed. Wrong safety-critical questions: ${wrong} (2 or more means automatic fail).`,
    reviewLabel: "Review of wrong answers", yourAnswer: "Your answer", rightAnswer: "Correct answer",
    close: "Close", noMistakes: "All questions answered correctly — well done!", confirmExit: "Really cancel the exam? Progress will be lost." },
  uk: { startBtn: "Іспит", pickerTitle: "Виберіть режим іспиту", pickerDesc: "Оберіть, як тренуватися. В обох режимах 30 питань з реальним розподілом і оцінюванням за справжнім правилом складання.",
    trainingTitle: "Тренувальний іспит", trainingDesc: "Без обмеження часу. Підходить для спокійного тренування.",
    simTitle: "Симуляція реального іспиту", simDesc: "Обмеження 45 хвилин, як на справжньому іспиті.",
    cancel: "Скасувати", progress: (i, n) => `Питання ${i} з ${n}`, next: "Далі", finish: "Завершити іспит",
    exit: "Скасувати", timeUp: "Час вийшов — іспит подано автоматично.",
    resultsPass: "Складено", resultsFail: "Не складено",
    summary: (err, wrong) => `Штрафні бали: ${err} з макс. 10 допустимих. Неправильні відповіді на питання, важливі для безпеки: ${wrong} (2 і більше — автоматичний провал).`,
    reviewLabel: "Перегляд неправильних відповідей", yourAnswer: "Ваша відповідь", rightAnswer: "Правильна відповідь",
    close: "Закрити", noMistakes: "Усі питання дано правильно — чудово!", confirmExit: "Дійсно скасувати іспит? Прогрес буде втрачено." },
  pl: { startBtn: "Egzamin", pickerTitle: "Wybierz tryb egzaminu", pickerDesc: "Wybierz sposób ćwiczenia. Oba tryby losują 30 pytań z realnym rozkładem i oceniają wg prawdziwej zasady zaliczenia.",
    trainingTitle: "Egzamin ćwiczeniowy", trainingDesc: "Bez limitu czasu. Do spokojnego ćwiczenia.",
    simTitle: "Symulacja prawdziwego egzaminu", simDesc: "Limit czasu 45 minut, jak na prawdziwym egzaminie.",
    cancel: "Anuluj", progress: (i, n) => `Pytanie ${i} z ${n}`, next: "Dalej", finish: "Zakończ egzamin",
    exit: "Anuluj", timeUp: "Czas minął — egzamin został przesłany automatycznie.",
    resultsPass: "Zdany", resultsFail: "Niezdany",
    summary: (err, wrong) => `Punkty karne: ${err} z maks. 10 dozwolonych. Błędne odpowiedzi na pytania istotne dla bezpieczeństwa: ${wrong} (2 lub więcej oznacza automatyczne niezaliczenie).`,
    reviewLabel: "Przegląd błędnych odpowiedzi", yourAnswer: "Twoja odpowiedź", rightAnswer: "Poprawna odpowiedź",
    close: "Zamknij", noMistakes: "Wszystkie pytania poprawne — świetnie!", confirmExit: "Na pewno przerwać egzamin? Postęp zostanie utracony." },
  ar: { startBtn: "الامتحان", pickerTitle: "اختر وضع الامتحان", pickerDesc: "اختر طريقة التدريب. يسحب كلا الوضعين 30 سؤالاً بتوزيع واقعي ويُقيَّمان وفق قاعدة النجاح الحقيقية.",
    trainingTitle: "امتحان تدريبي", trainingDesc: "بدون حد زمني. مناسب للتدريب الهادئ.",
    simTitle: "محاكاة الامتحان الحقيقي", simDesc: "حد زمني 45 دقيقة، كما في الامتحان الحقيقي.",
    cancel: "إلغاء", progress: (i, n) => `السؤال ${i} من ${n}`, next: "التالي", finish: "إنهاء الامتحان",
    exit: "إلغاء", timeUp: "انتهى الوقت — تم تسليم الامتحان تلقائيًا.",
    resultsPass: "ناجح", resultsFail: "غير ناجح",
    summary: (err, wrong) => `نقاط الخطأ: ${err} من 10 كحد أقصى مسموح. الأسئلة الحرجة للسلامة الخاطئة: ${wrong} (سؤالان أو أكثر يعني رسوبًا تلقائيًا).`,
    reviewLabel: "مراجعة الإجابات الخاطئة", yourAnswer: "إجابتك", rightAnswer: "الإجابة الصحيحة",
    close: "إغلاق", noMistakes: "تمت الإجابة عن جميع الأسئلة بشكل صحيح — أحسنت!", confirmExit: "هل تريد حقًا إلغاء الامتحان؟ سيُفقد التقدم." },
  zh: { startBtn: "考试", pickerTitle: "选择考试模式", pickerDesc: "选择练习方式。两种模式都会按真实比例抽取30道题,并按真实及格规则评分。",
    trainingTitle: "练习考试", trainingDesc: "无时间限制,适合从容练习。",
    simTitle: "模拟真实考试", simDesc: "45分钟时间限制,与真实考试一致。",
    cancel: "取消", progress: (i, n) => `第 ${i} 题，共 ${n} 题`, next: "下一题", finish: "完成考试",
    exit: "取消", timeUp: "时间到 — 考试已自动提交。",
    resultsPass: "通过", resultsFail: "未通过",
    summary: (err, wrong) => `错误分数：${err}分，最多允许10分。安全关键问题答错数：${wrong}题（2题或以上将自动判定不及格）。`,
    reviewLabel: "错误答案回顾", yourAnswer: "您的答案", rightAnswer: "正确答案",
    close: "关闭", noMistakes: "所有题目均答对 — 非常好!", confirmExit: "确定要取消考试吗?进度将丢失。" },
  hi: { startBtn: "परीक्षा", pickerTitle: "परीक्षा मोड चुनें", pickerDesc: "अभ्यास करने का तरीका चुनें। दोनों मोड वास्तविक भारांक के साथ 30 प्रश्न चुनते हैं और असली उत्तीर्ण नियम से स्कोर करते हैं।",
    trainingTitle: "अभ्यास परीक्षा", trainingDesc: "समय सीमा नहीं। शांति से अभ्यास के लिए अच्छा।",
    simTitle: "वास्तविक परीक्षा सिमुलेशन", simDesc: "45 मिनट की समय सीमा, असली परीक्षा जैसी।",
    cancel: "रद्द करें", progress: (i, n) => `प्रश्न ${i} / ${n}`, next: "अगला", finish: "परीक्षा समाप्त करें",
    exit: "रद्द करें", timeUp: "समय समाप्त — परीक्षा स्वतः जमा कर दी गई।",
    resultsPass: "उत्तीर्ण", resultsFail: "अनुत्तीर्ण",
    summary: (err, wrong) => `त्रुटि अंक: ${err}, अधिकतम 10 स्वीकार्य। गलत सुरक्षा-महत्वपूर्ण प्रश्न: ${wrong} (2 या अधिक होने पर स्वतः अनुत्तीर्ण)।`,
    reviewLabel: "गलत उत्तरों की समीक्षा", yourAnswer: "आपका उत्तर", rightAnswer: "सही उत्तर",
    close: "बंद करें", noMistakes: "सभी प्रश्नों के सही उत्तर — बहुत बढ़िया!", confirmExit: "क्या आप वाकई परीक्षा रद्द करना चाहते हैं? प्रगति खो जाएगी।" },
  tr: { startBtn: "Sınav", pickerTitle: "Sınav modunu seçin", pickerDesc: "Nasıl çalışmak istediğinizi seçin. Her iki mod da gerçekçi ağırlıkla 30 soru seçer ve gerçek geçme kuralına göre puanlar.",
    trainingTitle: "Alıştırma sınavı", trainingDesc: "Süre sınırı yok. Sakin çalışma için uygundur.",
    simTitle: "Gerçek sınav simülasyonu", simDesc: "Gerçek sınavdaki gibi 45 dakika süre sınırı.",
    cancel: "İptal", progress: (i, n) => `${n} sorudan ${i}.`, next: "İleri", finish: "Sınavı bitir",
    exit: "İptal", timeUp: "Süre doldu — sınav otomatik olarak gönderildi.",
    resultsPass: "Geçti", resultsFail: "Geçemedi",
    summary: (err, wrong) => `Hata puanı: ${err}, izin verilen maksimum 10. Yanlış güvenlik açısından kritik soru: ${wrong} (2 veya daha fazlası otomatik başarısızlık demektir).`,
    reviewLabel: "Yanlış cevapların incelenmesi", yourAnswer: "Cevabınız", rightAnswer: "Doğru cevap",
    close: "Kapat", noMistakes: "Tüm sorular doğru cevaplandı — harika!", confirmExit: "Sınavı gerçekten iptal etmek istiyor musunuz? İlerleme kaybolacak." },
  fr: { startBtn: "Examen", pickerTitle: "Choisir le mode d'examen", pickerDesc: "Choisissez votre façon de vous entraîner. Les deux modes tirent 30 questions avec une pondération réaliste et notent selon la règle de réussite réelle.",
    trainingTitle: "Examen d'entraînement", trainingDesc: "Sans limite de temps. Idéal pour s'entraîner calmement.",
    simTitle: "Simulation d'examen réel", simDesc: "Limite de 45 minutes, comme le véritable examen.",
    cancel: "Annuler", progress: (i, n) => `Question ${i} sur ${n}`, next: "Suivant", finish: "Terminer l'examen",
    exit: "Annuler", timeUp: "Le temps est écoulé — l'examen a été soumis automatiquement.",
    resultsPass: "Réussi", resultsFail: "Échoué",
    summary: (err, wrong) => `Points d'erreur : ${err} sur 10 maximum autorisés. Questions critiques pour la sécurité incorrectes : ${wrong} (2 ou plus entraîne un échec automatique).`,
    reviewLabel: "Révision des réponses incorrectes", yourAnswer: "Votre réponse", rightAnswer: "Bonne réponse",
    close: "Fermer", noMistakes: "Toutes les questions ont une réponse correcte — bravo !", confirmExit: "Voulez-vous vraiment annuler l'examen ? La progression sera perdue." },
  ru: { startBtn: "Экзамен", pickerTitle: "Выберите режим экзамена", pickerDesc: "Выберите способ тренировки. Оба режима выбирают 30 вопросов с реалистичным распределением и оцениваются по настоящему правилу сдачи.",
    trainingTitle: "Тренировочный экзамен", trainingDesc: "Без ограничения времени. Подходит для спокойной тренировки.",
    simTitle: "Симуляция настоящего экзамена", simDesc: "Ограничение 45 минут, как на настоящем экзамене.",
    cancel: "Отмена", progress: (i, n) => `Вопрос ${i} из ${n}`, next: "Далее", finish: "Завершить экзамен",
    exit: "Отмена", timeUp: "Время истекло — экзамен отправлен автоматически.",
    resultsPass: "Сдано", resultsFail: "Не сдано",
    summary: (err, wrong) => `Штрафные баллы: ${err} из макс. 10 допустимых. Неверные ответы на вопросы, критичные для безопасности: ${wrong} (2 и более означает автоматический провал).`,
    reviewLabel: "Разбор неверных ответов", yourAnswer: "Ваш ответ", rightAnswer: "Правильный ответ",
    close: "Закрыть", noMistakes: "Все вопросы даны верно — отлично!", confirmExit: "Действительно отменить экзамен? Прогресс будет потерян." },
  es: { startBtn: "Examen", pickerTitle: "Elegir modo de examen", pickerDesc: "Elige cómo quieres practicar. Ambos modos seleccionan 30 preguntas con ponderación realista y puntúan según la regla real de aprobación.",
    trainingTitle: "Examen de entrenamiento", trainingDesc: "Sin límite de tiempo. Ideal para practicar con calma.",
    simTitle: "Simulación de examen real", simDesc: "Límite de 45 minutos, como el examen real.",
    cancel: "Cancelar", progress: (i, n) => `Pregunta ${i} de ${n}`, next: "Siguiente", finish: "Finalizar examen",
    exit: "Cancelar", timeUp: "Se acabó el tiempo — el examen se envió automáticamente.",
    resultsPass: "Aprobado", resultsFail: "No aprobado",
    summary: (err, wrong) => `Puntos de error: ${err} de máx. 10 permitidos. Preguntas críticas para la seguridad incorrectas: ${wrong} (2 o más significa suspenso automático).`,
    reviewLabel: "Revisión de respuestas incorrectas", yourAnswer: "Tu respuesta", rightAnswer: "Respuesta correcta",
    close: "Cerrar", noMistakes: "Todas las preguntas respondidas correctamente — ¡muy bien!", confirmExit: "¿Seguro que quieres cancelar el examen? Se perderá el progreso." },
  it: { startBtn: "Esame", pickerTitle: "Scegli la modalità d'esame", pickerDesc: "Scegli come vuoi esercitarti. Entrambe le modalità estraggono 30 domande con una ponderazione realistica e valutano secondo la regola reale di superamento.",
    trainingTitle: "Esame di allenamento", trainingDesc: "Senza limite di tempo. Ideale per esercitarsi con calma.",
    simTitle: "Simulazione d'esame reale", simDesc: "Limite di 45 minuti, come l'esame reale.",
    cancel: "Annulla", progress: (i, n) => `Domanda ${i} di ${n}`, next: "Avanti", finish: "Termina esame",
    exit: "Annulla", timeUp: "Il tempo è scaduto — l'esame è stato inviato automaticamente.",
    resultsPass: "Superato", resultsFail: "Non superato",
    summary: (err, wrong) => `Punti di errore: ${err} su un massimo di 10 consentiti. Domande critiche per la sicurezza sbagliate: ${wrong} (2 o più significa bocciatura automatica).`,
    reviewLabel: "Revisione delle risposte sbagliate", yourAnswer: "La tua risposta", rightAnswer: "Risposta corretta",
    close: "Chiudi", noMistakes: "Tutte le domande risposte correttamente — ottimo lavoro!", confirmExit: "Vuoi davvero annullare l'esame? I progressi andranno persi." },
};

// Languages that read right-to-left - toggled via dir="rtl"/"ltr" on <html>.
const RTL_LANGS = new Set(["ar"]);

// Per-locale word for "Language," used as the select's aria-label - a UX
// review flagged the previous approach (concatenating all 7 translations
// into one aria-label, e.g. "Language / Sprache / Мова / ...") as verbose,
// since a screen reader announces the whole string every time regardless
// of which language is active. One word in the CURRENT language is enough.
const LANG_PICKER_LABEL = { de: "Sprache", en: "Language", uk: "Мова", pl: "Język", ar: "اللغة", zh: "语言", hi: "भाषा", tr: "Dil", fr: "Langue", ru: "Язык", es: "Idioma", it: "Lingua" };

// Maps a browser's navigator.language (e.g. "uk-UA", "zh-CN", "pt-BR") to
// the closest locale this app actually supports, so a first-time visitor
// doesn't always land on German regardless of their device's language -
// a UX review flagged the previous default (always "de" unless a saved
// preference exists) as a real gap for the very languages just added.
function detectBrowserLang() {
  try {
    const candidates = (navigator.languages && navigator.languages.length) ? navigator.languages : [navigator.language];
    for (const raw of candidates) {
      if (!raw) continue;
      const base = raw.toLowerCase().split("-")[0];
      if (UI_STRINGS[base]) return base;
    }
  } catch (e) { /* navigator.language unavailable - fall through to default */ }
  return null;
}

// Questions with an original birds-eye scenario diagram instead of (or on
// top of) a sign image - see assets/diagrams/*.svg (card DN-3).
const DIAGRAM_IDS = new Set([
  "vorfahrt-01", "vorfahrt-07", "vorfahrt-09", "vorfahrt-13",
  "vorfahrt-17", "vorfahrt-19", "vorfahrt-21",
]);

// Alt text describes what's VISUALLY on the sign (shape/color/symbol) -
// deliberately NOT its legal meaning, since for most sign questions
// identifying that meaning IS the question. A screen-reader user should
// have to reason it out from the same visual facts a sighted user gets,
// not be handed the answer through the alt text.
const SIGN_ALT = {
  "101": { de: "Rot umrandetes weißes Dreieck mit schwarzem Ausrufezeichen", en: "Red-bordered white triangle with a black exclamation mark" },
  "102": { de: "Rot umrandetes weißes Dreieck mit schwarzem Kreuzsymbol", en: "Red-bordered white triangle with a black crossroads symbol" },
  "120": { de: "Rot umrandetes weißes Dreieck mit zwei aufeinander zulaufenden schwarzen Linien", en: "Red-bordered white triangle with two converging black lines" },
  "123": { de: "Rot umrandetes weißes Dreieck mit einer schwarzen Figur mit Schaufel", en: "Red-bordered white triangle with a black figure holding a shovel" },
  "133": { de: "Rot umrandetes weißes Dreieck mit einer schwarzen erwachsenen Figur", en: "Red-bordered white triangle with a single black adult figure" },
  "136": { de: "Rot umrandetes weißes Dreieck mit zwei kleinen schwarzen Figuren", en: "Red-bordered white triangle with two small black figures" },
  "151": { de: "Rot umrandetes weißes Dreieck mit schwarzem Zugsymbol", en: "Red-bordered white triangle with a black train symbol" },
  "201": { de: "Rotes X (Andreaskreuz) auf weißem Grund", en: "Red X (St. Andrew's cross) on a white background" },
  "205": { de: "Nach unten zeigendes, rot umrandetes weißes Dreieck ohne Symbol", en: "Downward-pointing, red-bordered white triangle with no symbol" },
  "206": { de: "Rotes Achteck mit weißer Aufschrift STOP", en: "Red octagon with white STOP lettering" },
  "209": { de: "Blauer Kreis mit weißem, nach rechts zeigendem Pfeil", en: "Blue circle with a white arrow pointing right" },
  "215": { de: "Blauer Kreis mit weißem Kreispfeil", en: "Blue circle with a white circular arrow" },
  "220": { de: "Blaues Quadrat mit weißem, nach oben zeigendem Pfeil", en: "Blue square with a white upward-pointing arrow" },
  "237": { de: "Blauer Kreis mit weißem Fahrradsymbol", en: "Blue circle with a white bicycle symbol" },
  "240": { de: "Blauer Kreis mit weißem Fußgänger- und Fahrradsymbol übereinander", en: "Blue circle with white pedestrian and bicycle symbols stacked" },
  "250": { de: "Weißer Kreis mit dickem rotem Rand, kein Symbol", en: "White circle with a thick red border, no symbol" },
  "260": { de: "Weißer Kreis mit rotem Rand und schwarzer Autosilhouette", en: "White circle with a red border and a black car silhouette" },
  "267": { de: "Roter Kreis mit weißem waagerechtem Balken", en: "Red circle with a white horizontal bar" },
  "274": { de: "Weißer Kreis mit rotem Rand und einer schwarzen Zahl", en: "White circle with a red border and a black number" },
  "276": { de: "Weißer Kreis mit rotem Rand und zwei Autosilhouetten (schwarz und rot)", en: "White circle with a red border and two car silhouettes (black and red)" },
  "278": { de: "Weißer Kreis mit grauem Rand, Zahl von grauer Diagonale durchgestrichen", en: "White circle with a grey border, a number crossed out by a grey diagonal line" },
  "282": { de: "Weißer Kreis mit fünf grauen Diagonalstreifen", en: "White circle with five grey diagonal stripes" },
  "283": { de: "Blauer Kreis mit rotem X", en: "Blue circle with a red X" },
  "286": { de: "Blauer Kreis mit einem roten Diagonalstrich", en: "Blue circle with a single red diagonal stripe" },
  "293": { de: "Blaues Quadrat mit weißem Dreieck und schwarzer Fußgängerfigur", en: "Blue square with a white triangle and a black pedestrian figure" },
  "301": { de: "Gelbe Raute mit weißem Rand, kein Symbol", en: "Yellow diamond with a white border, no symbol" },
  "306": { de: "Gelbes Quadrat mit schwarz-weißem Rand, kein Symbol", en: "Yellow square with a black-and-white border, no symbol" },
  "307": { de: "Gelbes Quadrat mit schwarz-weißem Rand, von grauen Diagonalen durchgestrichen", en: "Yellow square with a black-and-white border, crossed out by grey diagonal lines" },
  "314": { de: "Blaues Quadrat mit weißem Buchstaben P", en: "Blue square with a white letter P" },
  "315": { de: "Blaues Quadrat mit weißem Buchstaben P über einem Auto-auf-Linie-Symbol", en: "Blue square with a white letter P above a car-on-a-line symbol" },
  "330-1": { de: "Blaues Quadrat mit weißem Brücken-/Straßensymbol", en: "Blue square with a white bridge/road symbol" },
  "330-2": { de: "Blaues Quadrat mit weißem Brücken-/Straßensymbol, von rotem Diagonalstrich durchgestrichen", en: "Blue square with a white bridge/road symbol, crossed out by a red diagonal line" },
  "350": { de: "Blaues Quadrat mit weißem Dreieck und schwarzer Fußgängerfigur", en: "Blue square with a white triangle and a black pedestrian figure" },
  "720": { de: "Schwarze quadratische Tafel mit grünem, nach rechts zeigendem Pfeil", en: "Black square plate with a green arrow pointing right" },
  "zusatz": { de: "Weißes Rechteck mit schwarzem Rand und zwei waagerechten Linien (Zusatztafel)", en: "White rectangle with a black border and two horizontal lines (a supplementary plate)" },
};

// Diagram alt text: "plain" describes only the neutral scene (matches what's
// shown before the answer is revealed); "answer" adds who has priority
// (matches what's shown after reveal) - kept in sync with the visual so a
// screen-reader user gets exactly as much information as a sighted one, no
// more, no less, at each stage.
const DIAGRAM_ALT = {
  "vorfahrt-01": {
    plain: { de: "Kreuzung ohne Ampel und ohne Schilder. Ihr Auto kommt von unten, ein anderes Fahrzeug kommt von rechts.", en: "Intersection with no traffic light and no signs. Your car approaches from the bottom, another vehicle from the right." },
    answer: { de: "Das Fahrzeug von rechts hat Vorfahrt, Sie müssen warten.", en: "The vehicle from the right has priority, you must yield." },
  },
  "vorfahrt-07": {
    plain: { de: "Kreuzung: Ihr Auto will links abbiegen, ein entgegenkommendes Fahrzeug fährt geradeaus.", en: "Intersection: your car wants to turn left, an oncoming vehicle is going straight." },
    answer: { de: "Der entgegenkommende Verkehr hat Vorfahrt, Sie müssen warten.", en: "The oncoming traffic has priority, you must yield." },
  },
  "vorfahrt-09": {
    plain: { de: "Kreuzung: Ihr Auto kommt von unten, eine Straßenbahn kommt von rechts aus einer Nebenstraße.", en: "Intersection: your car approaches from the bottom, a tram approaches from a side street on the right." },
    answer: { de: "Die Straßenbahn hat Vorfahrt, Sie müssen warten.", en: "The tram has priority, you must yield." },
  },
  "vorfahrt-13": {
    plain: { de: "Kreuzung mit Ampel. Ein Polizist steht in der Mitte und hebt den Arm.", en: "Intersection with a traffic light. A police officer stands in the middle with a raised arm." },
    answer: { de: "Die Zeichen des Polizisten gelten, die Ampel wird in diesem Fall ignoriert.", en: "The officer's signals apply; the traffic light is overridden in this case." },
  },
  "vorfahrt-17": {
    plain: { de: "Straße mit Radweg. Ihr Auto biegt rechts ab, ein Radfahrer fährt auf dem Radweg geradeaus.", en: "Road with a cycle lane. Your car is turning right, a cyclist is going straight in the cycle lane." },
    answer: { de: "Der Radfahrer hat Vorfahrt, Sie müssen warten.", en: "The cyclist has priority, you must yield." },
  },
  "vorfahrt-19": {
    plain: { de: "Straße mit zwei Fahrspuren. Ein Einsatzfahrzeug mit Blaulicht nähert sich von hinten.", en: "Road with two lanes. An emergency vehicle with blue lights approaches from behind." },
    answer: { de: "Das Einsatzfahrzeug hat immer Vorrang, unabhängig von der sonstigen Vorfahrt.", en: "The emergency vehicle always has priority, regardless of the usual right of way." },
  },
  "vorfahrt-21": {
    plain: { de: "Straße kreuzt Bahngleise ohne Schranke. Ein Zug nähert sich.", en: "Road crossing railway tracks with no barrier. A train is approaching." },
    answer: { de: "Der Zug hat immer Vorrang, auch wenn Ihre Straße sonst eine Vorfahrtstraße ist.", en: "The train always has priority, even though your road is otherwise a priority road." },
  },
};

// Alt text for signs/diagrams is only translated into de/en so far (DN-28 -
// tracked as a follow-up, not yet done for uk/pl/ar/zh/hi). Falls back to
// English, then German, rather than showing nothing or the raw code, so a
// screen-reader user in an untranslated-alt-text language still gets a real
// description instead of silence.
function pickAlt(entry, lang) {
  if (!entry) return null;
  return entry[lang] || entry.en || entry.de;
}

function resolveImage(q, revealed) {
  const lang = state.lang;
  if (q.image_ref) {
    const key = q.image_ref.split("/")[1];
    const altEntry = SIGN_ALT[key];
    return { src: `assets/signs/${key}.svg`, alt: altEntry ? pickAlt(altEntry, lang) : q.image_ref };
  }
  if (DIAGRAM_IDS.has(q.id)) {
    const variant = revealed ? "answer" : "plain";
    const suffix = revealed ? "-answer" : "";
    const altEntry = DIAGRAM_ALT[q.id];
    return { src: `assets/diagrams/${q.id}${suffix}.svg`, alt: altEntry ? pickAlt(altEntry[variant], lang) : q.id };
  }
  return null;
}

// Nested by exam_type (DN-39) - each module can have its own topic set with
// no risk of a topic_code collision between modules (e.g. a future
// Angelschein "technik" topic wouldn't clash with Fuehrerschein's "umwelt").
// A locale missing for a given module (Angelschein only ships de/en so far)
// simply isn't looked up - callers always fall back through pickLocaleText-
// style chains rather than indexing this directly with an unchecked locale.
const TOPIC_LABELS = {
  fuehrerschein: {
    vorfahrt: { de: "Vorfahrt und Kreuzungen", en: "Right of way & intersections", uk: "Проїзд перехресть", pl: "Pierwszeństwo i skrzyżowania", ar: "الأولوية والتقاطعات", zh: "路权与交叉路口", hi: "प्राथमिकता और चौराहे", tr: "Geçiş hakkı ve kavşaklar", fr: "Priorité et intersections", ru: "Приоритет проезда и перекрёстки", es: "Prioridad de paso e intersecciones", it: "Precedenza e incroci" },
    verkehrszeichen: { de: "Verkehrszeichen", en: "Traffic signs", uk: "Дорожні знаки", pl: "Znaki drogowe", ar: "إشارات المرور", zh: "交通标志", hi: "यातायात संकेत", tr: "Trafik işaretleri", fr: "Panneaux de signalisation", ru: "Дорожные знаки", es: "Señales de tráfico", it: "Segnaletica stradale" },
    gefahr: { de: "Gefahrenlehre", en: "Hazard perception", uk: "Розпізнавання небезпек", pl: "Nauka o zagrożeniach", ar: "إدراك المخاطر", zh: "危险识别", hi: "खतरा पहचान", tr: "Tehlike algısı", fr: "Perception des dangers", ru: "Распознавание опасностей", es: "Percepción de riesgos", it: "Percezione del pericolo" },
    umwelt: { de: "Umwelt und Technik", en: "Environment & technology", uk: "Довкілля та техніка", pl: "Środowisko i technika", ar: "البيئة والتقنية", zh: "环境与技术", hi: "पर्यावरण और तकनीक", tr: "Çevre ve teknik", fr: "Environnement et technique", ru: "Экология и техника", es: "Medio ambiente y técnica", it: "Ambiente e tecnica" },
    verhalten: { de: "Allgemeines Verhalten", en: "General road behavior", uk: "Загальна поведінка на дорозі", pl: "Ogólne zachowanie na drodze", ar: "السلوك العام على الطريق", zh: "一般道路行为", hi: "सामान्य सड़क व्यवहार", tr: "Genel trafik davranışı", fr: "Comportement général", ru: "Общее поведение на дороге", es: "Comportamiento general", it: "Comportamento generale" },
    autobahn: { de: "Autobahn und Überholen", en: "Motorway & overtaking", uk: "Автомагістраль і обгін", pl: "Autostrada i wyprzedzanie", ar: "الطريق السريع والتجاوز", zh: "高速公路与超车", hi: "मोटरवे और ओवरटेकिंग", tr: "Otoyol ve sollama", fr: "Autoroute et dépassement", ru: "Автомагистраль и обгон", es: "Autopista y adelantamiento", it: "Autostrada e sorpasso" },
    parken: { de: "Parken und Halten", en: "Parking & stopping", uk: "Паркування і зупинка", pl: "Parkowanie i zatrzymywanie", ar: "الوقوف والتوقف", zh: "停车与停靠", hi: "पार्किंग और रुकना", tr: "Park etme ve durma", fr: "Stationnement et arrêt", ru: "Парковка и остановка", es: "Estacionamiento y parada", it: "Parcheggio e sosta" },
    ladung: { de: "Ladungssicherung und Mitfahrende", en: "Cargo & passenger safety", uk: "Кріплення вантажу та пасажири", pl: "Mocowanie ładunku i pasażerowie", ar: "تثبيت الحمولة والركاب", zh: "货物固定与乘客安全", hi: "भार सुरक्षा और सह-यात्री", tr: "Yük sabitleme ve yolcular", fr: "Arrimage du chargement et passagers", ru: "Крепление груза и пассажиры", es: "Sujeción de la carga y pasajeros", it: "Fissaggio del carico e passeggeri" },
    erstehilfe: { de: "Unfaelle und Erste Hilfe", en: "Accidents & first aid", uk: "ДТП та перша допомога", pl: "Wypadki i pierwsza pomoc", ar: "الحوادث والإسعافات الأولية", zh: "事故与急救", hi: "दुर्घटना और प्राथमिक चिकित्सा", tr: "Kazalar ve ilk yardım", fr: "Accidents et premiers secours", ru: "ДТП и первая помощь", es: "Accidentes y primeros auxilios", it: "Incidenti e primo soccorso" },
    fahrtuechtigkeit: { de: "Alkohol, Drogen und Fahrtuechtigkeit", en: "Alcohol, drugs & fitness to drive", uk: "Алкоголь, наркотики і придатність до керування", pl: "Alkohol, narkotyki i zdolność do jazdy", ar: "الكحول والمخدرات واللياقة للقيادة", zh: "酒精、毒品与驾驶适宜性", hi: "शराब, नशा और ड्राइविंग योग्यता", tr: "Alkol, uyuşturucu ve sürüşe uygunluk", fr: "Alcool, drogues et aptitude à conduire", ru: "Алкоголь, наркотики и годность к вождению", es: "Alcohol, drogas y aptitud para conducir", it: "Alcol, droghe e idoneità alla guida" },
  },
  angelschein: {
    tierschutz: { de: "Tierschutz und Waidgerechtigkeit", en: "Animal welfare & ethical practice" },
    schonzeit: { de: "Schonzeiten und Mindestmaße", en: "Closed seasons & minimum sizes" },
    geraete: { de: "Geräte und Methoden", en: "Tackle & methods" },
    gewaesser: { de: "Gewässerordnung und Angelschein", en: "Water rules & the licence itself" },
  },
};

// Looks up a topic label for the CURRENT module/locale, falling back to EN
// then the raw topic name - same fallback shape as pickAlt() below, applied
// here because Angelschein's seed topics only have de/en so far.
function getTopicLabel(topicCode, fallbackTopic) {
  const forModule = TOPIC_LABELS[state.examType] || {};
  const entry = forModule[topicCode];
  if (!entry) return fallbackTopic;
  return entry[state.lang] || entry.en || entry.de || fallbackTopic;
}

const state = {
  lang: "de",
  topicFilter: "all",
  questions: [],
  detailIndex: null, // index into filtered list, or null when showing the list
  revealed: false,
  exam: null, // set while an exam run (training or simulation) is active - see below
  // Module system (DN-39): examType is "fuehrerschein" | "angelschein" | null
  // (null = no selection yet, module picker is shown). scopeCode is the
  // active class code (Fuehrerschein, e.g. "B") or region code (Angelschein,
  // e.g. "NRW") within that module - see MODULES_MANIFEST / openModulePicker.
  examType: null,
  scopeCode: null,
  modulesManifest: null,
};

// --- Module system (DN-39) ----------------------------------------------
// Splits content by exam module (Fuehrerschein vs. Angelschein, and future
// modules) AND by locale (folding in the DN-36 architecture recommendation,
// since both restructurings touch the same loading code). Runtime data now
// lives under data/modules.json (manifest) + data/<exam_type>/core.json
// (locale-independent fields) + data/<exam_type>/locales/<lang>.json - see
// data/build_modules.py for how these are generated from the flat editable
// master files content actually gets authored in.

function moduleManifestFor(examType) {
  return (state.modulesManifest?.modules || []).find((m) => m.exam_type === examType);
}

// A module's "scope" is whichever dimension it partitions content by - a
// class (Fuehrerschein: B, and eventually A/C/CE) or a region (Angelschein:
// state fisheries law varies, unlike the federally-uniform StVO). Kept
// generic here so a future module can introduce a third kind without
// touching this function.
function scopeFieldFor(examType) {
  const manifest = moduleManifestFor(examType);
  return manifest && manifest.scopeKind === "region" ? "region_scope" : "class_scope";
}

async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();
}

// Not every module ships every locale yet (Angelschein's seed is de/en
// only) - try the active UI language, then English, then German, so a
// French-language user picking Angelschein still gets real text instead of
// an empty question. Mirrors pickAlt()'s fallback philosophy below.
async function fetchLocaleTextWithFallback(examType, lang) {
  const candidates = [...new Set([lang, "en", "de"])];
  let lastErr;
  for (const candidate of candidates) {
    try {
      return { lang: candidate, text: await fetchJson(`data/${examType}/locales/${candidate}.json`) };
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr;
}

async function loadModuleData(examType, scopeCode) {
  const core = await fetchJson(`data/${examType}/core.json`);
  const { lang: resolvedLang, text: localeText } = await fetchLocaleTextWithFallback(examType, state.lang);
  const scopeField = scopeFieldFor(examType);

  const merged = core.questions
    .filter((q) => (q[scopeField] || []).includes(scopeCode))
    .map((q) => {
      const t = localeText[q.id];
      return {
        ...q,
        // Reassembled into the same {text:{lang:{...}}, explanation:{lang:...}}
        // shape the existing render/exam code already expects, so those
        // functions didn't need to change for the module split - only ONE
        // locale is ever populated at a time now (whichever just loaded),
        // which is fine since nothing reads any locale but state.lang.
        text: t ? { [resolvedLang]: { question: t.question, options: t.options } } : {},
        explanation: t ? { [resolvedLang]: t.explanation } : {},
      };
    });

  state.examType = examType;
  state.scopeCode = scopeCode;
  state.questions = merged;
  state.moduleMeta = core.meta;
  // A locale fallback means state.lang itself doesn't change (the picker
  // stays showing the user's chosen UI language) - only the CONTENT text
  // fell back. render() below still reads q.text[state.lang], so keep the
  // merged objects keyed under the language actually resolved.
  if (resolvedLang !== state.lang) {
    state.contentLangFallback = resolvedLang;
  } else {
    state.contentLangFallback = null;
  }

  try {
    localStorage.setItem("dn-exam-type", examType);
    localStorage.setItem("dn-scope-code", scopeCode);
  } catch (e) { /* non-fatal */ }
}

function openModulePicker() {
  state.modulePickerStep = "module";
  el("#module-picker").hidden = false;
  history.pushState({ view: "module-picker" }, "");
  renderModulePicker();
  setInertBehindDialog(true);
  // Move focus into the dialog so a screen-reader user lands on its content
  // immediately rather than the still-focused (now inert-behind) control
  // that opened it - title isn't natively focusable, tabindex="-1" makes it
  // a valid one-time focus target without adding it to the tab order.
  el("#module-picker-title").focus();
}

function closeModulePicker() {
  el("#module-picker").hidden = true;
  setInertBehindDialog(false);
}

function renderModulePicker() {
  const M = state.modulesManifest.modules;
  const container = el("#module-picker-body");
  container.innerHTML = "";

  if (state.modulePickerStep === "module") {
    el("#module-picker-title").textContent = MODULE_PICKER_STRINGS[state.lang]?.chooseModule
      || MODULE_PICKER_STRINGS.en.chooseModule;
    M.forEach((mod) => {
      const btn = document.createElement("button");
      btn.className = "exam-mode-btn";
      const label = mod.label[state.lang] || mod.label.en;
      btn.innerHTML = `<strong>${label}</strong>`;
      btn.addEventListener("click", () => {
        state.pendingModule = mod;
        if (mod.options.length === 1) {
          selectModuleAndScope(mod.exam_type, mod.options[0].code);
        } else {
          state.modulePickerStep = "scope";
          renderModulePicker();
        }
      });
      container.appendChild(btn);
    });
  } else {
    const mod = state.pendingModule;
    el("#module-picker-title").textContent = mod.label[state.lang] || mod.label.en;
    mod.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className = "exam-mode-btn";
      btn.innerHTML = `<strong>${opt.label[state.lang] || opt.label.en}</strong>`;
      btn.addEventListener("click", () => selectModuleAndScope(mod.exam_type, opt.code));
      container.appendChild(btn);
    });
    const back = document.createElement("button");
    back.className = "back-btn";
    back.textContent = MODULE_PICKER_STRINGS[state.lang]?.back || MODULE_PICKER_STRINGS.en.back;
    back.addEventListener("click", () => {
      state.modulePickerStep = "module";
      renderModulePicker();
    });
    container.appendChild(back);
  }
}

async function selectModuleAndScope(examType, scopeCode) {
  try {
    await loadModuleData(examType, scopeCode);
  } catch (err) {
    el("#module-picker-body").innerHTML = `<div class="empty">Could not load content: ${err}</div>`;
    return;
  }
  state.topicFilter = "all";
  state.detailIndex = null;
  closeModulePicker();
  history.replaceState({ view: "list" }, "");
  render();
}

// Minimal standalone strings (not folded into UI_STRINGS/EXAM_STRINGS since
// this picker is shown before any module - and therefore any module's
// content locale - has loaded; only needs a couple of short labels).
const MODULE_PICKER_STRINGS = {
  de: { chooseModule: "Welche Prüfung lernst du?", back: "← Zurück", changeExam: "Prüfung wechseln" },
  en: { chooseModule: "Which exam are you studying for?", back: "← Back", changeExam: "Change exam" },
  uk: { chooseModule: "До якого іспиту ви готуєтесь?", back: "← Назад", changeExam: "Змінити іспит" },
  pl: { chooseModule: "Do jakiego egzaminu się przygotowujesz?", back: "← Wstecz", changeExam: "Zmień egzamin" },
  ar: { chooseModule: "لأي امتحان تستعد؟", back: "→ رجوع", changeExam: "تغيير الامتحان" },
  zh: { chooseModule: "你在准备哪个考试？", back: "← 返回", changeExam: "更换考试" },
  hi: { chooseModule: "आप किस परीक्षा की तैयारी कर रहे हैं?", back: "← वापस", changeExam: "परीक्षा बदलें" },
  tr: { chooseModule: "Hangi sınava çalışıyorsun?", back: "← Geri", changeExam: "Sınavı değiştir" },
  fr: { chooseModule: "Pour quel examen étudiez-vous ?", back: "← Retour", changeExam: "Changer d'examen" },
  ru: { chooseModule: "К какому экзамену вы готовитесь?", back: "← Назад", changeExam: "Сменить экзамен" },
  es: { chooseModule: "¿Para qué examen estás estudiando?", back: "← Atrás", changeExam: "Cambiar de examen" },
  it: { chooseModule: "Per quale esame stai studiando?", back: "← Indietro", changeExam: "Cambia esame" },
};

// --- Exam mode (DN-29) --------------------------------------------------
// Reverses the original Sprint-1 "no exam mode" boundary, with explicit PO
// sign-off (see docs/KANBAN.md retro log). Two modes share the same draw
// and scoring logic, matching the real Klasse-B exam structure recorded in
// data.meta.pass_rule_note: 30 questions, 2-5 points each, fail if error
// points > 10 OR 2+ wrong high_stakes questions (high_stakes = safety-
// critical, and spans 6 topics in the real data, not just Vorfahrt - see
// the DN-29/DN-21 correction in BACKLOG.md). "Training" drops the time
// limit for calm practice; "simulation" adds the real 45-minute limit and
// auto-submits when it expires.
const EXAM_QUESTION_COUNT = 30;
const EXAM_TIME_LIMIT_MS = 45 * 60 * 1000;

// Target draw distribution across the 10 topics, summing to 30. Roughly
// proportional to each topic's real share of the question pool, with a
// floor high enough on Verkehrszeichen and Vorfahrt to keep both realistic
// and to guarantee at least one Vorfahrt question (the topic with the
// densest concentration of high_stakes items) is always drawn.
// Namespaced by exam_type (DN-39) since the weighting is specific to each
// module's real topic distribution. A module with no entry here (a future
// module, or Angelschein before it has enough content to weight sensibly)
// just falls through to drawExamQuestions()'s uniform-random top-up below -
// and the exam-mode entry point is disabled entirely under EXAM_QUESTION_COUNT
// questions anyway, so this only matters once a module has real depth.
const EXAM_TOPIC_DRAW = {
  fuehrerschein: {
    verkehrszeichen: 8,
    vorfahrt: 4,
    gefahr: 3,
    verhalten: 3,
    autobahn: 3,
    umwelt: 2,
    parken: 2,
    ladung: 2,
    fahrtuechtigkeit: 2,
    erstehilfe: 1,
  },
};

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function drawExamQuestions() {
  const byTopic = {};
  state.questions.forEach((q) => {
    (byTopic[q.topic_code] = byTopic[q.topic_code] || []).push(q);
  });
  let draw = [];
  const topicDraw = EXAM_TOPIC_DRAW[state.examType] || {};
  Object.entries(topicDraw).forEach(([topic, n]) => {
    const pool = shuffle(byTopic[topic] || []);
    draw = draw.concat(pool.slice(0, n));
  });
  // If a topic's pool were ever smaller than its target (not the case at
  // 500 questions, but defensive for future smaller content packs), top up
  // from the overall pool so an exam run is always exactly 30 questions.
  if (draw.length < EXAM_QUESTION_COUNT) {
    const usedIds = new Set(draw.map((q) => q.id));
    const rest = shuffle(state.questions.filter((q) => !usedIds.has(q.id)));
    draw = draw.concat(rest.slice(0, EXAM_QUESTION_COUNT - draw.length));
  }
  return shuffle(draw).slice(0, EXAM_QUESTION_COUNT);
}

function openExamPicker() {
  el("#exam-picker").hidden = false;
  history.pushState({ view: "exam-picker" }, "");
  renderExamPicker();
  setInertBehindDialog(true);
}

function closeExamPicker() {
  el("#exam-picker").hidden = true;
  setInertBehindDialog(false);
}

function renderExamPicker() {
  const X = EXAM_STRINGS[state.lang];
  el("#exam-picker-title").textContent = X.pickerTitle;
  el("#exam-picker-desc").textContent = X.pickerDesc;
  el("#exam-pick-training").innerHTML = `<strong>${X.trainingTitle}</strong>${X.trainingDesc}`;
  el("#exam-pick-simulation").innerHTML = `<strong>${X.simTitle}</strong>${X.simDesc}`;
  el("#exam-picker-cancel").textContent = X.cancel;
}

function startExam(mode) {
  el("#exam-picker").hidden = true;
  state.exam = {
    mode, // "training" | "simulation"
    questions: drawExamQuestions(),
    answers: {}, // questionId -> selected option key
    index: 0,
    startedAt: Date.now(),
    finished: false,
  };
  history.replaceState({ view: "exam" }, "");
  el("#exam-view").hidden = false;
  setInertBehindDialog(true);
  if (mode === "simulation") startExamTimer();
  renderExamQuestion();
  el("#exam-question").focus();
}

function startExamTimer() {
  const tick = () => {
    if (!state.exam || state.exam.finished) return;
    const elapsed = Date.now() - state.exam.startedAt;
    const remaining = EXAM_TIME_LIMIT_MS - elapsed;
    const timerEl = el("#exam-timer");
    timerEl.hidden = false;
    if (remaining <= 0) {
      timerEl.textContent = "0:00";
      finishExam(true);
      return;
    }
    const mins = Math.floor(remaining / 60000);
    const secs = Math.floor((remaining % 60000) / 1000);
    timerEl.textContent = `${mins}:${String(secs).padStart(2, "0")}`;
    timerEl.classList.toggle("low-time", remaining < 5 * 60 * 1000);
    state.exam.timerHandle = setTimeout(tick, 1000);
  };
  tick();
}

function stopExamTimer() {
  if (state.exam && state.exam.timerHandle) {
    clearTimeout(state.exam.timerHandle);
    state.exam.timerHandle = null;
  }
}

function renderExamQuestion() {
  const S = UI_STRINGS[state.lang];
  const X = EXAM_STRINGS[state.lang];
  const ex = state.exam;
  const q = ex.questions[ex.index];
  const t = q.text[state.lang];
  const topicLabel = getTopicLabel(q.topic_code, q.topic);

  el("#exam-progress").textContent = X.progress(ex.index + 1, ex.questions.length);
  el("#exam-meta").innerHTML = `
    <span class="badge topic">${topicLabel}</span>
    <span class="badge points">${S.points(q.points)}</span>
    ${q.high_stakes ? `<span class="badge high-stakes">${S.highStakes}</span>` : ""}
  `;
  el("#exam-question").textContent = t.question;

  const img = resolveImage(q, false); // never reveal the answer-variant image mid-exam
  const imgEl = el("#exam-image-note");
  if (img) {
    imgEl.innerHTML = `<img src="${img.src}" alt="${img.alt}" class="q-illustration" />`;
    imgEl.className = "image-illustration";
    imgEl.hidden = false;
  } else {
    imgEl.innerHTML = "";
    imgEl.hidden = true;
  }

  const optionsEl = el("#exam-options");
  optionsEl.innerHTML = "";
  // Selecting an option updates classes/aria on the existing divs in place
  // rather than re-rendering the whole question (which would destroy and
  // recreate every option element, dropping keyboard focus back to <body>
  // on every single answer - the same class of focus-loss bug DN-17 fixed
  // for the flashcard reveal flow, now avoided here from the start).
  const applySelection = () => {
    const selected = ex.answers[q.id];
    optionsEl.querySelectorAll(".option").forEach((div) => {
      const isSel = div.dataset.key === selected;
      div.classList.toggle("exam-selected", isSel);
      div.setAttribute("aria-pressed", String(isSel));
    });
  };
  Object.entries(t.options).forEach(([key, text]) => {
    const div = document.createElement("div");
    div.className = "option";
    div.dataset.key = key;
    div.setAttribute("role", "button");
    div.setAttribute("aria-pressed", "false");
    div.tabIndex = 0;
    div.innerHTML = `<span class="key">${key.toUpperCase()}</span><span>${text}</span>`;
    const pick = () => {
      ex.answers[q.id] = key;
      applySelection();
    };
    div.addEventListener("click", pick);
    div.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); }
    });
    optionsEl.appendChild(div);
  });
  applySelection();

  const isLast = ex.index === ex.questions.length - 1;
  el("#exam-next-btn").textContent = isLast ? X.finish : X.next;
  el("#exam-exit-btn").textContent = X.exit;
}

function examNext() {
  const ex = state.exam;
  if (ex.index < ex.questions.length - 1) {
    ex.index += 1;
    renderExamQuestion();
    el("#exam-view").scrollTop = 0;
  } else {
    finishExam(false);
  }
}

function computeExamResults() {
  const ex = state.exam;
  let errorPoints = 0;
  let wrongHighStakes = 0;
  const wrongList = [];
  ex.questions.forEach((q) => {
    const given = ex.answers[q.id];
    const isCorrect = given != null && q.correct.includes(given);
    if (!isCorrect) {
      errorPoints += q.points;
      if (q.high_stakes) wrongHighStakes += 1;
      wrongList.push({ q, given });
    }
  });
  const passed = errorPoints <= 10 && wrongHighStakes < 2;
  return { errorPoints, wrongHighStakes, wrongList, passed };
}

function finishExam(timedOut) {
  stopExamTimer();
  state.exam.finished = true;
  state.exam.timedOut = !!timedOut;
  el("#exam-view").hidden = true;
  el("#exam-results").hidden = false;
  history.replaceState({ view: "exam-results" }, "");
  renderExamResults();
  el("#exam-results-title").focus ? null : null; // no-op, kept for symmetry with detail focus pattern
}

function renderExamResults() {
  const S = UI_STRINGS[state.lang];
  const X = EXAM_STRINGS[state.lang];
  const results = computeExamResults();
  const titleEl = el("#exam-results-title");
  titleEl.textContent = results.passed ? X.resultsPass : X.resultsFail;
  titleEl.className = results.passed ? "exam-results-pass" : "exam-results-fail";

  const summaryEl = el("#exam-results-summary");
  let summaryHtml = `<div class="exam-results-summary-box">${X.summary(results.errorPoints, results.wrongHighStakes)}</div>`;
  if (state.exam.timedOut) {
    summaryHtml = `<div class="exam-results-summary-box">${X.timeUp}</div>` + summaryHtml;
  }
  summaryEl.innerHTML = summaryHtml;

  const reviewEl = el("#exam-results-review");
  if (results.wrongList.length === 0) {
    reviewEl.innerHTML = `<p>${X.noMistakes}</p>`;
  } else {
    reviewEl.innerHTML = `<h3>${X.reviewLabel}</h3>`;
    results.wrongList.forEach(({ q, given }) => {
      const t = q.text[state.lang];
      const correctKey = q.correct[0];
      const item = document.createElement("div");
      item.className = "exam-review-item";
      item.innerHTML = `
        <div class="q-card-text">${t.question}</div>
        <div class="your-answer">${X.yourAnswer}: ${(given && t.options[given]) || "—"}</div>
        <div class="right-answer">${X.rightAnswer}: ${t.options[correctKey]}</div>
      `;
      reviewEl.appendChild(item);
    });
  }
  el("#exam-results-close-btn").textContent = X.close;
}

function exitExam() {
  const X = EXAM_STRINGS[state.lang];
  if (state.exam && !state.exam.finished) {
    if (!confirm(X.confirmExit)) return;
  }
  stopExamTimer();
  state.exam = null;
  el("#exam-view").hidden = true;
  el("#exam-results").hidden = true;
  setInertBehindDialog(false);
  history.replaceState({ view: "list" }, "");
}

const el = (sel) => document.querySelector(sel);

function filteredQuestions() {
  if (state.topicFilter === "all") return state.questions;
  return state.questions.filter((q) => q.topic_code === state.topicFilter);
}

function render() {
  const S = UI_STRINGS[state.lang];
  const MP = MODULE_PICKER_STRINGS[state.lang] || MODULE_PICKER_STRINGS.en;
  document.title = S.title;
  el("#app-title").textContent = S.title;
  el("#app-subtitle").textContent = S.subtitle(state.questions.length);
  el("#install-hint").textContent = S.installHint;
  el("#exam-start-btn").textContent = EXAM_STRINGS[state.lang].startBtn;
  // No real exam is meaningful with only a handful of seed questions (see
  // Angelschein's placeholder content) - disable rather than let someone
  // start a "30-question exam" that silently draws far fewer.
  el("#exam-start-btn").disabled = state.questions.length < EXAM_QUESTION_COUNT;

  const moduleMod = moduleManifestFor(state.examType);
  const moduleBtn = el("#module-switch-btn");
  if (moduleMod) {
    const scopeOpt = moduleMod.options.find((o) => o.code === state.scopeCode);
    const moduleLabel = moduleMod.label[state.lang] || moduleMod.label.en;
    const scopeLabel = scopeOpt ? (scopeOpt.label[state.lang] || scopeOpt.label.en) : "";
    moduleBtn.textContent = `${moduleLabel} · ${scopeLabel}`;
    moduleBtn.title = MP.changeExam;
  } else {
    moduleBtn.textContent = MP.changeExam;
  }

  ["lang-select", "detail-lang-select"].forEach((id) => {
    el("#" + id).value = state.lang;
    el("#" + id).setAttribute("aria-label", LANG_PICKER_LABEL[state.lang] || "Language");
  });

  renderFilters();

  if (state.detailIndex === null) {
    el("#detail-view").hidden = true;
    renderList();
  } else {
    el("#detail-view").hidden = false;
    renderDetail();
  }
}

function renderFilters() {
  const S = UI_STRINGS[state.lang];
  const topics = ["all", ...Object.keys(TOPIC_LABELS[state.examType] || {})];
  const container = el("#filters");
  container.innerHTML = "";
  topics.forEach((code) => {
    const btn = document.createElement("button");
    btn.textContent = code === "all" ? S.filterAll : getTopicLabel(code, code);
    btn.className = state.topicFilter === code ? "active" : "";
    btn.setAttribute("aria-pressed", String(state.topicFilter === code));
    btn.addEventListener("click", () => {
      state.topicFilter = code;
      state.detailIndex = null;
      try { localStorage.setItem("dn-filter", code); } catch (e) { /* non-fatal */ }
      render();
    });
    container.appendChild(btn);
  });
}

function renderList() {
  const S = UI_STRINGS[state.lang];
  const list = el("#list");
  const qs = filteredQuestions();
  list.innerHTML = "";

  if (qs.length === 0) {
    list.innerHTML = `<div class="empty">${S.empty}</div>`;
    return;
  }

  qs.forEach((q, i) => {
    const card = document.createElement("div");
    card.className = "q-card";
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    const topicLabel = getTopicLabel(q.topic_code, q.topic);
    card.innerHTML = `
      <div class="q-card-top">
        <span class="badge topic">${topicLabel}</span>
        <span class="badge points">${S.points(q.points)}</span>
        ${q.high_stakes ? `<span class="badge high-stakes">${S.highStakes}</span>` : ""}
        <span class="q-card-id">${q.id}</span>
      </div>
      <div class="q-card-text">${q.text[state.lang].question}</div>
    `;
    const open = () => {
      state.listScrollY = window.scrollY;
      state.lastOpenedIndex = i; // so focus can return to the same card on close
      state.detailIndex = i;
      state.revealed = false;
      history.pushState({ view: "detail" }, "");
      render();
      setInertBehindDialog(true);
      // Focus the question itself first (tabindex="-1", see index.html) so a
      // screen reader announces the dialog's content immediately, before any
      // control - this also fixes keyboard users otherwise landing 50 Tab
      // presses deep into the still-focusable list underneath (see KANBAN
      // retro: caught by the accessibility audit, not the earlier UX pass).
      el("#detail-question").focus();
    };
    card.addEventListener("click", open);
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); }
    });
    list.appendChild(card);
  });
}

function renderDetail() {
  const S = UI_STRINGS[state.lang];
  const qs = filteredQuestions();
  const q = qs[state.detailIndex];
  const topicLabel = getTopicLabel(q.topic_code, q.topic);
  const t = q.text[state.lang];
  const expl = q.explanation[state.lang];

  el("#detail-progress").textContent = S.progress(state.detailIndex + 1, qs.length);

  el("#detail-meta").innerHTML = `
    <span class="badge topic">${topicLabel}</span>
    <span class="badge points">${S.points(q.points)}</span>
    ${q.high_stakes ? `<span class="badge high-stakes">${S.highStakes}</span>` : ""}
  `;

  el("#detail-question").textContent = t.question;

  const img = resolveImage(q, state.revealed);
  const imageNoteEl = el("#image-note");
  if (img) {
    imageNoteEl.innerHTML = `<img src="${img.src}" alt="${img.alt}" class="q-illustration" />`;
    imageNoteEl.className = "image-illustration";
    imageNoteEl.hidden = false;
  } else if (q.image_ref) {
    // Shouldn't happen for the current 34 sign refs, kept as a safety net
    // for future content batches that reference art not yet produced.
    imageNoteEl.innerHTML = `${S.imageNote}<code>${q.image_ref}</code>`;
    imageNoteEl.className = "image-note";
    imageNoteEl.hidden = false;
  } else {
    imageNoteEl.innerHTML = "";
    imageNoteEl.className = "image-note"; // reset - a leftover "image-illustration"
    imageNoteEl.hidden = true;              // class has equal CSS specificity to [hidden]
  }

  const optionsEl = el("#options");
  optionsEl.innerHTML = "";
  Object.entries(t.options).forEach(([key, text]) => {
    const isCorrect = q.correct.includes(key);
    const showCorrect = state.revealed && isCorrect;
    const div = document.createElement("div");
    div.className = "option" + (showCorrect ? " correct" : "");
    // Correct answer is marked with text + a checkmark, not color alone -
    // color-only signalling is unreliable for colorblind users (amber/green
    // read as near-identical under some forms of color blindness).
    div.innerHTML = `<span class="key">${key.toUpperCase()}</span><span>${text}</span>${
      showCorrect ? `<span class="correct-mark">✓ ${S.correctMark}</span>` : ""
    }`;
    optionsEl.appendChild(div);
  });

  const revealBtn = el("#reveal-btn");
  revealBtn.textContent = state.revealed ? S.revealed : S.reveal;
  revealBtn.disabled = state.revealed;

  el("#explanation").hidden = !state.revealed;
  el("#explanation").innerHTML = state.revealed
    ? `<strong>${S.explanationLabel}:</strong> ${expl}<div class="legal-cite">${S.legalBasis}: ${q.legal_basis}</div>`
    : "";

  el("#prev-btn").textContent = S.prev;
  el("#next-btn").textContent = S.next;
  el("#prev-btn").disabled = state.detailIndex === 0;
  el("#next-btn").disabled = state.detailIndex === qs.length - 1;

  el("#back-btn").textContent = S.back;
}

async function setLang(lang) {
  state.lang = lang;
  document.documentElement.setAttribute("lang", lang); // keeps AT pronunciation correct (WCAG 3.1.1)
  // Arabic reads right-to-left - mirrors layout direction for correct reading
  // order (WCAG 1.3.2) rather than leaving RTL text inside an LTR container.
  document.documentElement.setAttribute("dir", RTL_LANGS.has(lang) ? "rtl" : "ltr");
  try { localStorage.setItem("dn-lang", lang); } catch (e) { /* storage unavailable, non-fatal */ }
  // Content is now loaded ONE locale at a time per module (DN-39) rather
  // than all 12 up front, so switching languages mid-session means
  // re-fetching that module's text file for the newly-selected language -
  // the (small) core.json with all the non-text fields doesn't need
  // re-fetching, only the locale file does.
  if (state.examType && state.scopeCode) {
    try {
      await loadModuleData(state.examType, state.scopeCode);
    } catch (err) {
      // Keep showing the previous locale's content rather than blanking
      // the app if the new locale's file fails to load.
    }
  }
  render();
}

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  try { localStorage.setItem("dn-theme", theme); } catch (e) { /* non-fatal */ }
  renderThemeToggle();
}

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

function renderThemeToggle() {
  const isLight = currentTheme() === "light";
  const icon = isLight ? "🌙" : "☀️";
  ["theme-toggle", "detail-theme-toggle"].forEach((id) => {
    el("#" + id).textContent = icon;
    el("#" + id).setAttribute("aria-pressed", String(isLight));
  });
}

function setInertBehindDialog(isInert) {
  // While the detail "dialog" is open, everything behind it (header controls,
  // the list) should be out of the tab order and hidden from AT - otherwise
  // a keyboard/screen-reader user can reach controls that are visually
  // covered by the full-screen overlay, or has to tab through the entire
  // list to escape it. `inert` also removes it from the accessibility tree;
  // aria-hidden is set alongside as a fallback for engines without `inert`.
  const header = document.querySelector("header");
  const main = document.querySelector("main");
  [header, main].forEach((elm) => {
    if (!elm) return;
    elm.inert = isInert;
    if (isInert) elm.setAttribute("aria-hidden", "true");
    else elm.removeAttribute("aria-hidden");
  });
}

function closeDetail() {
  const returnIndex = state.lastOpenedIndex;
  state.detailIndex = null;
  render();
  setInertBehindDialog(false);
  window.scrollTo(0, state.listScrollY || 0);
  // Return keyboard focus to the card that was originally activated, instead
  // of dropping it to <body> - otherwise a keyboard user has to restart
  // tabbing from the very top of the page every time they close a question.
  if (returnIndex != null) {
    const cards = document.querySelectorAll("#list .q-card");
    if (cards[returnIndex]) cards[returnIndex].focus();
  }
}

function wireStaticControls() {
  el("#lang-select").addEventListener("change", (e) => setLang(e.target.value));
  el("#detail-lang-select").addEventListener("change", (e) => setLang(e.target.value));
  el("#module-switch-btn").addEventListener("click", openModulePicker);
  el("#module-picker-cancel").addEventListener("click", () => history.back());

  const toggleTheme = () => setTheme(currentTheme() === "light" ? "dark" : "light");
  el("#theme-toggle").addEventListener("click", toggleTheme);
  el("#detail-theme-toggle").addEventListener("click", toggleTheme);

  // Closing via the in-app back button goes through history.back() so it's
  // symmetric with the phone/browser back gesture (see popstate handler below) -
  // otherwise the two paths diverge and leave a stray history entry.
  el("#back-btn").addEventListener("click", () => {
    history.back();
  });

  window.addEventListener("popstate", () => {
    if (state.detailIndex !== null) closeDetail();
    if (!el("#exam-picker").hidden) closeExamPicker();
    if (!el("#exam-view").hidden || !el("#exam-results").hidden) exitExam();
    if (!el("#module-picker").hidden) {
      // On first-ever visit the module picker is mandatory (no content is
      // loaded yet) - a back gesture there shouldn't leave the app in a
      // blank state, so only actually close it if a module was already
      // active before the picker was reopened via "change exam".
      if (state.examType) closeModulePicker();
      else openModulePicker();
    }
  });

  el("#exam-start-btn").addEventListener("click", openExamPicker);
  el("#exam-picker-cancel").addEventListener("click", () => history.back());
  el("#exam-pick-training").addEventListener("click", () => startExam("training"));
  el("#exam-pick-simulation").addEventListener("click", () => startExam("simulation"));
  el("#exam-exit-btn").addEventListener("click", exitExam);
  el("#exam-next-btn").addEventListener("click", examNext);
  el("#exam-results-close-btn").addEventListener("click", exitExam);

  el("#reveal-btn").addEventListener("click", () => {
    state.revealed = true;
    render();
    // Move focus to the newly-revealed explanation so keyboard/screen-reader
    // users land on the new content instead of losing focus entirely.
    el("#explanation").focus();
  });

  el("#prev-btn").addEventListener("click", () => {
    if (state.detailIndex > 0) {
      state.detailIndex -= 1;
      state.revealed = false;
      render();
      el("#detail-view").scrollTop = 0;
    }
  });

  el("#next-btn").addEventListener("click", () => {
    const qs = filteredQuestions();
    if (state.detailIndex < qs.length - 1) {
      state.detailIndex += 1;
      state.revealed = false;
      render();
      el("#detail-view").scrollTop = 0;
    }
  });
}

async function init() {
  try {
    const savedLang = localStorage.getItem("dn-lang");
    if (savedLang && UI_STRINGS[savedLang]) {
      state.lang = savedLang;
    } else {
      // No explicit preference saved yet - try the browser/device language
      // before falling back to German, so a first-time visitor in one of
      // the 7 supported languages doesn't always land on German chrome.
      const detected = detectBrowserLang();
      if (detected) state.lang = detected;
    }
    const savedFilter = localStorage.getItem("dn-filter");
    if (savedFilter) state.topicFilter = savedFilter;
  } catch (e) { /* storage unavailable, defaults are fine */ }

  document.documentElement.setAttribute("lang", state.lang);
  document.documentElement.setAttribute("dir", RTL_LANGS.has(state.lang) ? "rtl" : "ltr");
  wireStaticControls();
  renderThemeToggle();

  try {
    state.modulesManifest = await fetchJson("data/modules.json");
  } catch (err) {
    el("#list").innerHTML = `<div class="empty">Could not load data/modules.json: ${err}</div>`;
    return;
  }

  let savedExamType = null, savedScopeCode = null;
  try {
    savedExamType = localStorage.getItem("dn-exam-type");
    savedScopeCode = localStorage.getItem("dn-scope-code");
  } catch (e) { /* non-fatal */ }

  const savedModuleValid = savedExamType && savedScopeCode
    && moduleManifestFor(savedExamType)?.options.some((o) => o.code === savedScopeCode);

  if (savedModuleValid) {
    try {
      await loadModuleData(savedExamType, savedScopeCode);
      render();
    } catch (err) {
      // Saved selection no longer resolves (e.g. content files moved) -
      // fall through to the picker rather than showing a dead app.
      render();
      openModulePicker();
    }
  } else {
    // First-ever visit, or no saved selection yet - block on choosing a
    // module before showing any content, same pattern as the exam-mode
    // picker (a full-screen dialog, not a silent default).
    render();
    openModulePicker();
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("service-worker.js").catch(() => {
      /* offline caching is a nice-to-have; app still works without it */
    });
  }
}

init();
