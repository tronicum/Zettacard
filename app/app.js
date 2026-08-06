// Zettacard MVP — question browser (Sprint 1)
// Scope: click through all questions, switch language, reveal answer + explanation.
// Explicitly OUT of scope: exam simulation, scoring, pass/fail, timers.

const UI_STRINGS = {
  de: {
    title: "Zettacard — Lernkarten",
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
    multiSelectHint: "Mehrere Antworten möglich",
    imageNote: "🖼️ Bild ausstehend — Referenz: ",
    explanationLabel: "Erklärung",
    legalBasis: "Rechtsgrundlage",
    installHint: "Zum Startbildschirm hinzufügen für Offline-Nutzung.",
    empty: "Keine Fragen in dieser Kategorie.",
    correctMark: "Richtig",
  },
  en: {
    title: "Zettacard — Flashcards",
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
    multiSelectHint: "Multiple answers possible",
    imageNote: "🖼️ Image pending — ref: ",
    explanationLabel: "Explanation",
    legalBasis: "Legal basis",
    installHint: "Add to your home screen to use offline.",
    empty: "No questions in this category.",
    correctMark: "Correct",
  },
  uk: {
    title: "Zettacard — Картки для навчання",
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
    multiSelectHint: "Можливо кілька правильних відповідей",
    imageNote: "🖼️ Зображення відсутнє — посилання: ",
    explanationLabel: "Пояснення",
    legalBasis: "Правова основа",
    installHint: "Додайте на головний екран для використання офлайн.",
    empty: "У цій категорії немає питань.",
    correctMark: "Правильно",
  },
  pl: {
    title: "Zettacard — Fiszki",
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
    multiSelectHint: "Możliwych kilka poprawnych odpowiedzi",
    imageNote: "🖼️ Brak obrazu — odniesienie: ",
    explanationLabel: "Wyjaśnienie",
    legalBasis: "Podstawa prawna",
    installHint: "Dodaj do ekranu głównego, aby korzystać offline.",
    empty: "Brak pytań w tej kategorii.",
    correctMark: "Poprawnie",
  },
  ar: {
    title: "Zettacard — بطاقات تعليمية",
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
    multiSelectHint: "قد تكون هناك عدة إجابات صحيحة",
    imageNote: "🖼️ الصورة غير متوفرة — المرجع: ",
    explanationLabel: "الشرح",
    legalBasis: "الأساس القانوني",
    installHint: "أضف إلى الشاشة الرئيسية للاستخدام دون اتصال بالإنترنت.",
    empty: "لا توجد أسئلة في هذه الفئة.",
    correctMark: "صحيح",
  },
  zh: {
    title: "Zettacard — 学习卡片",
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
    multiSelectHint: "可能有多个正确答案",
    imageNote: "🖼️ 图片暂缺 — 参考：",
    explanationLabel: "解释",
    legalBasis: "法律依据",
    installHint: "添加到主屏幕即可离线使用。",
    empty: "该类别下没有题目。",
    correctMark: "正确",
  },
  hi: {
    title: "Zettacard — अभ्यास कार्ड",
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
    multiSelectHint: "कई सही उत्तर संभव हैं",
    imageNote: "🖼️ चित्र उपलब्ध नहीं — संदर्भ: ",
    explanationLabel: "स्पष्टीकरण",
    legalBasis: "कानूनी आधार",
    installHint: "ऑफ़लाइन उपयोग के लिए होम स्क्रीन पर जोड़ें।",
    empty: "इस श्रेणी में कोई प्रश्न नहीं है।",
    correctMark: "सही",
  },
  tr: {
    title: "Zettacard — Çalışma Kartları",
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
    multiSelectHint: "Birden fazla doğru cevap olabilir",
    imageNote: "🖼️ Görsel eksik — referans: ",
    explanationLabel: "Açıklama",
    legalBasis: "Yasal dayanak",
    installHint: "Çevrimdışı kullanım için ana ekrana ekleyin.",
    empty: "Bu kategoride soru yok.",
    correctMark: "Doğru",
  },
  fr: {
    title: "Zettacard — Fiches d'apprentissage",
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
    multiSelectHint: "Plusieurs réponses correctes possibles",
    imageNote: "🖼️ Image manquante — référence : ",
    explanationLabel: "Explication",
    legalBasis: "Base légale",
    installHint: "Ajoutez à l'écran d'accueil pour une utilisation hors ligne.",
    empty: "Aucune question dans cette catégorie.",
    correctMark: "Correct",
  },
  ru: {
    title: "Zettacard — Карточки для изучения",
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
    multiSelectHint: "Возможно несколько правильных ответов",
    imageNote: "🖼️ Изображение отсутствует — ссылка: ",
    explanationLabel: "Объяснение",
    legalBasis: "Правовая основа",
    installHint: "Добавьте на главный экран для использования офлайн.",
    empty: "В этой категории нет вопросов.",
    correctMark: "Правильно",
  },
  es: {
    title: "Zettacard — Tarjetas de estudio",
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
    multiSelectHint: "Puede haber varias respuestas correctas",
    imageNote: "🖼️ Imagen pendiente — referencia: ",
    explanationLabel: "Explicación",
    legalBasis: "Base legal",
    installHint: "Añade a la pantalla de inicio para usarlo sin conexión.",
    empty: "No hay preguntas en esta categoría.",
    correctMark: "Correcto",
  },
  it: {
    title: "Zettacard — Schede di studio",
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
    multiSelectHint: "Sono possibili più risposte corrette",
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
  datenschutz: {
    grundprinzipien: { de: "Grundprinzipien und Rechtsgrundlagen", en: "Core principles & legal bases" },
    betroffenenrechte: { de: "Betroffenenrechte", en: "Data subject rights" },
    datensicherheit: { de: "Datensicherheit (TOMs)", en: "Data security (TOMs)" },
    meldepflichten: { de: "Meldepflichten bei Datenpannen", en: "Breach notification duties" },
    auftragsverarbeitung: { de: "Auftragsverarbeitung und Drittländer", en: "Processor agreements & transfers" },
  },
  arbeitssicherheit: {
    grundpflichten: { de: "Grundpflichten", en: "Basic duties" },
    unterweisung: { de: "Unterweisungspflicht", en: "Instruction obligation" },
    gefaehrdungsbeurteilung: { de: "Gefährdungsbeurteilung", en: "Risk assessment" },
    psa_notfall: { de: "PSA und Notfälle", en: "PPE & emergencies" },
    bildschirmarbeit: { de: "Bildschirmarbeit und Ergonomie", en: "Screen work & ergonomics" },
  },
  ki_act: {
    grundlagen: { de: "Grundlagen und Risikoklassen", en: "Basics & risk tiers" },
    ki_kompetenz: { de: "KI-Kompetenzpflicht", en: "AI-literacy obligation" },
    verbotene_praktiken: { de: "Verbotene Praktiken", en: "Prohibited practices" },
    transparenzpflichten: { de: "Transparenzpflichten", en: "Transparency obligations" },
    ki_am_arbeitsplatz: { de: "KI am Arbeitsplatz", en: "AI at work" },
  },
  it_sicherheit: {
    zugriffsschutz: { de: "Zugriffsschutz", en: "Access protection" },
    phishing: { de: "Phishing und Social Engineering", en: "Phishing & social engineering" },
    datensicherung: { de: "Datensicherung und Geräte", en: "Backups & devices" },
    mobil_homeoffice: { de: "Mobile Geräte und Home-Office", en: "Mobile devices & home office" },
    meldepflicht_it: { de: "Meldung von Sicherheitsvorfällen", en: "Incident reporting" },
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

// --- Role filter (DN-44) -------------------------------------------------
// The 4 workplace-compliance modules carry a per-question `roles` array
// (see data/build_modules.py's CORE_FIELDS) - e.g. ["all"] for a question
// relevant to everyone, or ["it"]/["hr"]/["management"]/["all_staff"] for a
// more role-specific one. This is a SECOND, additive filter row shown only
// for those 4 modules, layered on top of the existing topic filter (a
// learner can combine both) rather than replacing it.
const COMPLIANCE_MODULES = new Set(["datenschutz", "arbeitssicherheit", "ki_act", "it_sicherheit"]);

// Role codes in a fixed display order - "all" here means "no role filter
// applied" (show every question regardless of its own roles tag), NOT to be
// confused with a question's own "all" role tag (meaning "relevant to
// everyone"), which is folded into every other filter's results below.
const ROLE_FILTER_CODES = ["all", "all_staff", "hr", "it", "management"];

const ROLE_FILTER_STRINGS = {
  de: { label: "Rolle", all: "Alle Rollen", all_staff: "Alle Mitarbeitenden", hr: "Personalabteilung", it: "IT", management: "Führungskraft" },
  en: { label: "Role", all: "All roles", all_staff: "All staff", hr: "HR", it: "IT", management: "Management" },
  uk: { label: "Роль", all: "Усі ролі", all_staff: "Весь персонал", hr: "Відділ кадрів", it: "ІТ", management: "Керівництво" },
  pl: { label: "Rola", all: "Wszystkie role", all_staff: "Wszyscy pracownicy", hr: "Dział HR", it: "IT", management: "Kierownictwo" },
  ar: { label: "الدور", all: "كل الأدوار", all_staff: "جميع الموظفين", hr: "الموارد البشرية", it: "تقنية المعلومات", management: "الإدارة" },
  zh: { label: "角色", all: "所有角色", all_staff: "全体员工", hr: "人力资源部", it: "IT部门", management: "管理层" },
  hi: { label: "भूमिका", all: "सभी भूमिकाएँ", all_staff: "सभी कर्मचारी", hr: "मानव संसाधन", it: "आईटी", management: "प्रबंधन" },
  tr: { label: "Rol", all: "Tüm roller", all_staff: "Tüm çalışanlar", hr: "İK", it: "BT", management: "Yönetim" },
  fr: { label: "Rôle", all: "Tous les rôles", all_staff: "Tout le personnel", hr: "RH", it: "Informatique", management: "Direction" },
  ru: { label: "Роль", all: "Все роли", all_staff: "Весь персонал", hr: "Отдел кадров", it: "ИТ", management: "Руководство" },
  es: { label: "Rol", all: "Todos los roles", all_staff: "Todo el personal", hr: "RR. HH.", it: "TI", management: "Dirección" },
  it: { label: "Ruolo", all: "Tutti i ruoli", all_staff: "Tutto il personale", hr: "Risorse umane", it: "IT", management: "Direzione" },
};
function roleFilterStrings(lang) {
  return ROLE_FILTER_STRINGS[lang] || ROLE_FILTER_STRINGS.en;
}

// A question matches a role filter if either the filter is "all" (no
// filtering), the question itself is tagged "all" (relevant to everyone,
// regardless of which specific role is selected), or the question's own
// roles array actually contains the selected code.
function questionMatchesRole(q, roleCode) {
  if (roleCode === "all") return true;
  const roles = q.roles || ["all"];
  return roles.includes("all") || roles.includes(roleCode);
}

const state = {
  lang: "de",
  topicFilter: "all",
  roleFilter: "all",
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
  // Local profile switcher: which per-device profile is active, and the
  // full registry of profiles on this device (see migrateOrInitProfiles()).
  profiles: [],
  activeProfileId: null,
  // Spaced-repetition "Review due" mode (DN-16, see openReviewSession()):
  // while true, filteredQuestions() sources #detail-view from reviewQueue
  // (the due-question list) instead of the topic-filtered browsing list.
  reviewMode: false,
  reviewQueue: [],
};

// --- Local profile switcher --------------------------------------------
// Lets several people share one device (e.g. a family) without their
// progress/settings colliding. Deliberately NOT a real account/recovery
// system - everything still lives in this browser's localStorage only,
// same zero-backend architecture as the rest of the app; a profile is just
// a namespace prefix, not an identity. Per-profile data: language,
// active module+scope, topic filter, module-intro-seen flags, and
// completions/certificates. Shared across all profiles: theme ("dn-theme",
// intentionally left flat/un-namespaced).
const PROFILE_REGISTRY_KEY = "dn-profiles";
const PROFILE_ACTIVE_KEY = "dn-active-profile";
// The old flat per-profile keys this app used before profiles existed -
// migrated (moved, not copied) into the auto-created "Default" profile's
// namespace the first time this code runs on a device that already has
// data under them. `dn-intro-seen-<examType>` isn't listed here since its
// suffix is dynamic - it's discovered separately via a startsWith scan.
const OLD_FLAT_KEYS = ["dn-lang", "dn-filter", "dn-exam-type", "dn-scope-code", "dn-completions"];

function genProfileId() {
  return `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;
}

// Every per-profile localStorage key goes through here rather than being
// hardcoded inline, so the active profile's namespace is always applied
// consistently. `base` is the key's old flat name with the "dn-" prefix
// stripped (e.g. "lang", "completions", "intro-seen-fuehrerschein").
function profileKey(base) {
  return `dn-p-${state.activeProfileId}-${base}`;
}

function loadProfileRegistry() {
  try {
    const raw = JSON.parse(localStorage.getItem(PROFILE_REGISTRY_KEY) || "null");
    return Array.isArray(raw) ? raw : null;
  } catch (e) {
    return null;
  }
}

function saveProfileRegistry(list) {
  try { localStorage.setItem(PROFILE_REGISTRY_KEY, JSON.stringify(list)); } catch (e) { /* non-fatal */ }
}

function setActiveProfileId(id) {
  try { localStorage.setItem(PROFILE_ACTIVE_KEY, id); } catch (e) { /* non-fatal */ }
}

// Runs once, before anything else touches localStorage. If a profile
// registry already exists, just loads it. Otherwise creates a single
// "Default" profile - MOVING (not copying) any pre-existing flat keys from
// before this feature existed into that profile's namespace, so an
// existing user's saved language/module/filter/completions survive
// untouched. A genuinely brand-new visitor (no registry, no old flat keys)
// just gets an empty Default profile and the normal first-visit flow
// (mandatory module picker, etc.) proceeds unchanged.
function migrateOrInitProfiles() {
  const existing = loadProfileRegistry();
  if (existing && existing.length > 0) {
    state.profiles = existing;
    let activeId = null;
    try { activeId = localStorage.getItem(PROFILE_ACTIVE_KEY); } catch (e) { /* non-fatal */ }
    state.activeProfileId = (activeId && existing.some((p) => p.id === activeId)) ? activeId : existing[0].id;
    return;
  }

  const id = genProfileId();
  let introSeenKeys = [];
  try {
    introSeenKeys = Object.keys(localStorage).filter((k) => k.startsWith("dn-intro-seen-"));
  } catch (e) { /* non-fatal */ }

  const hasOldData = OLD_FLAT_KEYS.some((k) => {
    try { return localStorage.getItem(k) !== null; } catch (e) { return false; }
  }) || introSeenKeys.length > 0;

  if (hasOldData) {
    OLD_FLAT_KEYS.forEach((k) => {
      try {
        const v = localStorage.getItem(k);
        if (v !== null) {
          localStorage.setItem(`dn-p-${id}-${k.slice(3)}`, v);
          localStorage.removeItem(k);
        }
      } catch (e) { /* non-fatal */ }
    });
    introSeenKeys.forEach((k) => {
      try {
        const v = localStorage.getItem(k);
        localStorage.setItem(`dn-p-${id}-${k.slice(3)}`, v);
        localStorage.removeItem(k);
      } catch (e) { /* non-fatal */ }
    });
  }

  const profiles = [{ id, name: "Default", createdAt: new Date().toISOString() }];
  saveProfileRegistry(profiles);
  setActiveProfileId(id);
  state.profiles = profiles;
  state.activeProfileId = id;
}

function currentProfileName() {
  const p = (state.profiles || []).find((prof) => prof.id === state.activeProfileId);
  return p ? p.name : "Default";
}

// Minimal standalone strings, same convention as MODULE_PICKER_STRINGS.
const PROFILE_STRINGS = {
  de: { switchAria: "Profil wechseln", title: "Profile auf diesem Gerät", close: "← Zurück", addPlaceholder: "Profilname", addConfirm: "+ Profil hinzufügen" },
  en: { switchAria: "Switch profile", title: "Profiles on this device", close: "← Back", addPlaceholder: "Profile name", addConfirm: "+ Add profile" },
  uk: { switchAria: "Змінити профіль", title: "Профілі на цьому пристрої", close: "← Назад", addPlaceholder: "Назва профілю", addConfirm: "+ Додати профіль" },
  pl: { switchAria: "Zmień profil", title: "Profile na tym urządzeniu", close: "← Wstecz", addPlaceholder: "Nazwa profilu", addConfirm: "+ Dodaj profil" },
  ar: { switchAria: "تبديل الملف الشخصي", title: "الملفات الشخصية على هذا الجهاز", close: "→ رجوع", addPlaceholder: "اسم الملف الشخصي", addConfirm: "+ إضافة ملف شخصي" },
  zh: { switchAria: "切换个人资料", title: "此设备上的个人资料", close: "← 返回", addPlaceholder: "个人资料名称", addConfirm: "+ 添加个人资料" },
  hi: { switchAria: "प्रोफ़ाइल बदलें", title: "इस डिवाइस पर प्रोफ़ाइल", close: "← वापस", addPlaceholder: "प्रोफ़ाइल का नाम", addConfirm: "+ प्रोफ़ाइल जोड़ें" },
  tr: { switchAria: "Profili değiştir", title: "Bu cihazdaki profiller", close: "← Geri", addPlaceholder: "Profil adı", addConfirm: "+ Profil ekle" },
  fr: { switchAria: "Changer de profil", title: "Profils sur cet appareil", close: "← Retour", addPlaceholder: "Nom du profil", addConfirm: "+ Ajouter un profil" },
  ru: { switchAria: "Сменить профиль", title: "Профили на этом устройстве", close: "← Назад", addPlaceholder: "Название профиля", addConfirm: "+ Добавить профиль" },
  es: { switchAria: "Cambiar de perfil", title: "Perfiles en este dispositivo", close: "← Atrás", addPlaceholder: "Nombre del perfil", addConfirm: "+ Añadir perfil" },
  it: { switchAria: "Cambia profilo", title: "Profili su questo dispositivo", close: "← Indietro", addPlaceholder: "Nome del profilo", addConfirm: "+ Aggiungi profilo" },
};
function profileStrings(lang) {
  return PROFILE_STRINGS[lang] || PROFILE_STRINGS.en;
}

function openProfileSwitcher() {
  el("#profile-view").hidden = false;
  history.pushState({ view: "profile-view" }, "");
  renderProfileSwitcher();
  setInertBehindDialog(true);
  el("#profile-title").focus();
}

function closeProfileSwitcher() {
  el("#profile-view").hidden = true;
  setInertBehindDialog(false);
}

function renderProfileSwitcher() {
  const P = profileStrings(state.lang);
  el("#profile-title").textContent = P.title;
  el("#profile-close-btn").textContent = P.close;
  el("#profile-add-input").placeholder = P.addPlaceholder;
  el("#profile-add-btn").textContent = P.addConfirm;

  const list = el("#profile-list");
  list.innerHTML = "";
  (state.profiles || []).forEach((p) => {
    const btn = document.createElement("button");
    btn.className = "exam-mode-btn profile-row" + (p.id === state.activeProfileId ? " active" : "");
    btn.textContent = p.name + (p.id === state.activeProfileId ? " ✓" : "");
    btn.addEventListener("click", () => switchProfile(p.id));
    list.appendChild(btn);
  });
}

// Switching profiles re-loads every piece of per-profile state from the
// newly-active profile's own localStorage namespace and re-renders
// everything - the same "full state reload" a language or module switch
// already does, just for a different profile's saved language/module/
// filter instead of the same profile's.
function switchProfile(id) {
  if (id === state.activeProfileId) {
    closeProfileSwitcher();
    return;
  }
  state.activeProfileId = id;
  setActiveProfileId(id);
  closeProfileSwitcher();
  loadActiveProfileState();
}

// Creates a brand-new, empty profile (no module/language selected yet -
// same starting point as a genuine first-time visitor, mandatory module
// picker included) and switches to it immediately.
function createProfile(name) {
  const trimmed = (name || "").trim();
  if (!trimmed) return;
  const id = genProfileId();
  const profile = { id, name: trimmed, createdAt: new Date().toISOString() };
  state.profiles = [...(state.profiles || []), profile];
  saveProfileRegistry(state.profiles);
  state.activeProfileId = id;
  setActiveProfileId(id);
  el("#profile-add-input").value = "";
  closeProfileSwitcher();
  loadActiveProfileState();
}

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

// DN-42: a "region" scope (Angelschein: state fisheries law) is additive -
// picking a specific state should still include nationwide (ALL) content,
// since a regional student needs the national baseline PLUS their state's
// extra rules, not instead of it. Most "class" scopes (Motorrad's A1/A2/A,
// LKW's C1/C/CE) stay exact-match: those are independent sibling classes,
// and content there already lists every class a question applies to
// directly in its own class_scope array (e.g. ["A1","A2","A"] for a fact
// common to all three) - there's no separate "general" code to fold in.
//
// DN-45: some classes genuinely ARE an add-on to another, not a sibling -
// Fuehrerschein's BE (car+trailer) requires everything B requires, plus
// BE-specific facts, the same "baseline + extra" relationship ALL/region
// has. Rather than duplicate the region-only special case, a class option
// can declare `extends: "<baseCode>"` in modules_manifest.json (see BE's
// entry) and the same additive logic applies - a class WITHOUT `extends`
// (every option so far except BE) behaves exactly as before.
function questionMatchesScope(q, scopeField, scopeKind, scopeCode, extendsCode) {
  const scopes = q[scopeField] || [];
  if (scopes.includes(scopeCode)) return true;
  if (scopeKind === "region") return scopeCode !== "ALL" && scopes.includes("ALL");
  return Boolean(extendsCode) && scopes.includes(extendsCode);
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
  const manifest = moduleManifestFor(examType);
  const scopeKind = manifest?.scopeKind;
  const scopeOpt = manifest?.options.find((o) => o.code === scopeCode);
  const extendsCode = scopeOpt?.extends || null;

  const merged = core.questions
    .filter((q) => questionMatchesScope(q, scopeField, scopeKind, scopeCode, extendsCode))
    .map((q) => {
      const t = localeText[q.id];
      return {
        ...q,
        // Reassembled into the same {text:{lang:{...}}, explanation:{lang:...}}
        // shape the existing render/exam code already expects, so those
        // functions didn't need to change for the module split - only ONE
        // locale is ever populated at a time now (whichever just loaded).
        // IMPORTANT: keyed under state.lang (the UI language actually
        // selected), NOT resolvedLang (the locale file that was actually
        // fetched) - every render/exam function indexes with
        // q.text[state.lang], so when a fallback occurs (e.g. a module
        // without Russian content falls back to English), keying under
        // resolvedLang left q.text[state.lang] undefined and crashed the
        // whole view (real bug: e.g. LKW - DE/EN only - failed to load at
        // all under Russian). Keying under state.lang instead means the
        // fallback TEXT still renders correctly under whatever language is
        // actually selected; state.contentLangFallback (set below) is what
        // a future "showing English because X isn't translated yet" UI
        // notice should read, not the text object's own keys.
        text: t ? { [state.lang]: { question: t.question, options: t.options } } : {},
        explanation: t ? { [state.lang]: t.explanation } : {},
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
    localStorage.setItem(profileKey("exam-type"), examType);
    localStorage.setItem(profileKey("scope-code"), scopeCode);
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

  // Fix for a real bug found in the 2026-08-05 UX review: this button had
  // NO text set anywhere, ever - it rendered as a blank, unreadable pill at
  // the bottom of the picker on every visit (not a contrast problem, an
  // actually-empty-label problem, which is worse - also invisible to
  // screen readers). On a mandatory first-ever visit (no module chosen
  // yet) cancelling would just immediately reopen the picker via the
  // popstate handler, so hide it there instead of showing a button that
  // does nothing.
  const cancelBtn = el("#module-picker-cancel");
  const MPC = MODULE_PICKER_STRINGS[state.lang] || MODULE_PICKER_STRINGS.en;
  cancelBtn.textContent = MPC.cancel;
  cancelBtn.hidden = !state.examType;

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
  state.roleFilter = "all";
  state.detailIndex = null;
  closeModulePicker();
  history.replaceState({ view: "list" }, "");
  render();

  // DN-43: if this module has an intro wizard and this device hasn't seen
  // it yet for this exam_type, show it now (first real study session in
  // the module) rather than dropping the user straight into a raw question
  // list with no orientation.
  const mod = state.pendingModule;
  if (mod && mod.intro && !hasSeenIntro(examType)) {
    openModuleIntro(mod);
  }
}

// Minimal standalone strings (not folded into UI_STRINGS/EXAM_STRINGS since
// this picker is shown before any module - and therefore any module's
// content locale - has loaded; only needs a couple of short labels).
const MODULE_PICKER_STRINGS = {
  de: { chooseModule: "Welche Prüfung lernst du?", back: "← Zurück", changeExam: "Prüfung wechseln", cancel: "Abbrechen" },
  en: { chooseModule: "Which exam are you studying for?", back: "← Back", changeExam: "Change exam", cancel: "Cancel" },
  uk: { chooseModule: "До якого іспиту ви готуєтесь?", back: "← Назад", changeExam: "Змінити іспит", cancel: "Скасувати" },
  pl: { chooseModule: "Do jakiego egzaminu się przygotowujesz?", back: "← Wstecz", changeExam: "Zmień egzamin", cancel: "Anuluj" },
  ar: { chooseModule: "لأي امتحان تستعد؟", back: "→ رجوع", changeExam: "تغيير الامتحان", cancel: "إلغاء" },
  zh: { chooseModule: "你在准备哪个考试？", back: "← 返回", changeExam: "更换考试", cancel: "取消" },
  hi: { chooseModule: "आप किस परीक्षा की तैयारी कर रहे हैं?", back: "← वापस", changeExam: "परीक्षा बदलें", cancel: "रद्द करें" },
  tr: { chooseModule: "Hangi sınava çalışıyorsun?", back: "← Geri", changeExam: "Sınavı değiştir", cancel: "İptal" },
  fr: { chooseModule: "Pour quel examen étudiez-vous ?", back: "← Retour", changeExam: "Changer d'examen", cancel: "Annuler" },
  ru: { chooseModule: "К какому экзамену вы готовитесь?", back: "← Назад", changeExam: "Сменить экзамен", cancel: "Отмена" },
  es: { chooseModule: "¿Para qué examen estás estudiando?", back: "← Atrás", changeExam: "Cambiar de examen", cancel: "Cancelar" },
  it: { chooseModule: "Per quale esame stai studiando?", back: "← Indietro", changeExam: "Cambia esame", cancel: "Annulla" },
};

// --- Module intro wizard (DN-43) ----------------------------------------
// A short, skippable walkthrough of what a module actually covers, shown
// once per device before a user's first study session in a module that
// has one (see modules_manifest.json's optional "intro" block), and
// reopenable any time via the header "About this module" button. DE/EN
// only for now, same scope decision as sign alt text (DN-28) - falls back
// to English for every other UI language rather than showing nothing.
const MODULE_INTRO_STRINGS = {
  de: { next: "Weiter", back: "← Zurück", skip: "Überspringen", start: "Los geht's", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Über dieses Modul" },
  en: { next: "Next", back: "← Back", skip: "Skip", start: "Let's start", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "About this module" },
};
function introStrings(lang) {
  return MODULE_INTRO_STRINGS[lang] || MODULE_INTRO_STRINGS.en;
}

function hasSeenIntro(examType) {
  try {
    return localStorage.getItem(profileKey(`intro-seen-${examType}`)) === "1";
  } catch (e) {
    return false;
  }
}

function markIntroSeen(examType) {
  try {
    localStorage.setItem(profileKey(`intro-seen-${examType}`), "1");
  } catch (e) { /* non-fatal */ }
}

function openModuleIntro(mod) {
  state.introModule = mod;
  state.introStepIndex = 0;
  el("#module-intro").hidden = false;
  history.pushState({ view: "module-intro" }, "");
  renderModuleIntro();
  setInertBehindDialog(true);
  el("#module-intro-title").focus();
}

function closeModuleIntro() {
  markIntroSeen(state.introModule.exam_type);
  el("#module-intro").hidden = true;
  setInertBehindDialog(false);
}

function renderModuleIntro() {
  const mod = state.introModule;
  const steps = mod.intro.steps;
  const i = state.introStepIndex;
  const step = steps[i];
  const lang = state.lang;
  const content = step[lang] || step.en || step.de;
  const S = introStrings(lang);

  el("#module-intro-title").textContent = content.title;
  el("#module-intro-body").textContent = content.body;

  const dots = el("#module-intro-dots");
  dots.innerHTML = "";
  steps.forEach((_, idx) => {
    const dot = document.createElement("span");
    dot.className = "dot" + (idx === i ? " active" : "");
    dots.appendChild(dot);
  });

  const backBtn = el("#module-intro-back");
  backBtn.textContent = S.back;
  backBtn.disabled = i === 0;

  el("#module-intro-skip").textContent = S.skip;
  el("#module-intro-skip").hidden = i === steps.length - 1;

  const nextBtn = el("#module-intro-next");
  nextBtn.innerHTML = `<strong>${i === steps.length - 1 ? S.start : S.next}</strong>`;
}

function wireModuleIntroControls() {
  el("#module-intro-back").addEventListener("click", () => {
    if (state.introStepIndex > 0) {
      state.introStepIndex -= 1;
      renderModuleIntro();
    }
  });
  el("#module-intro-next").addEventListener("click", () => {
    const steps = state.introModule.intro.steps;
    if (state.introStepIndex < steps.length - 1) {
      state.introStepIndex += 1;
      renderModuleIntro();
    } else {
      history.back();
    }
  });
  el("#module-intro-skip").addEventListener("click", () => history.back());
  el("#module-info-btn").addEventListener("click", () => {
    const mod = moduleManifestFor(state.examType);
    if (mod && mod.intro) openModuleIntro(mod);
  });
}

// --- Completion tracking & certificates (DN-14 / DN-44 prep) -----------
// A passed Simulation-mode exam (not Training - that's low-stakes
// practice, not a real attempt) is recorded on this device as a
// "completion." This is deliberately NOT a step toward exam mode's
// original no-scoring boundary being reopened again - it reuses exam
// mode's own existing pass/fail logic as the single source of truth for
// what counts as "completed," rather than inventing a second notion of
// passing.
//
// Portability is achieved by making the DOWNLOADED FILE the portable
// artifact, not the app's local state - localStorage here never leaves
// the device on its own; only an explicit "download certificate" /
// "download credential" action produces something the user can keep,
// print, or hand to someone else. This keeps the app's zero-backend,
// fully-static-PWA architecture intact.
//
// The JSON credential is shaped like an Open Badges 3.0 / W3C Verifiable
// Credential (the real, employer-independent standard for portable
// digital credentials - see docs/KANBAN.md retro log for why this
// standard was chosen over inventing a proprietary format) but is
// SELF-ISSUED and UNSIGNED: there is no backend keypair/issuer identity
// in this static-PWA architecture to produce a real cryptographic
// signature a third party could verify. It is honestly labeled as such
// in both the UI and the credential's own `unverified: true` field -
// making it cryptographically verifiable would need a real signing
// backend, a genuine architecture change, not something to fake.
const CERT_STRINGS = {
  de: {
    btn: "Meine Zertifikate", title: "Meine Zertifikate", close: "← Zurück",
    intro: "Bestandene Prüfungssimulationen werden hier als Nachweis gespeichert (nur auf diesem Gerät). Lade eine Zertifikatsdatei herunter, um sie zu behalten oder weiterzugeben - das ist die eigentlich portable Datei, nicht der App-Zustand.",
    empty: "Noch keine bestandene Prüfungssimulation. Bestehe eine Prüfungssimulation (nicht den Übungsmodus), um hier ein Zertifikat zu erhalten.",
    passedOn: (d) => `Bestanden am ${d}`,
    downloadCert: "Zertifikat herunterladen (HTML)", downloadCred: "Berechtigungsnachweis herunterladen (JSON)",
    disclaimer: "Selbst erstellter Nachweis, nicht kryptographisch signiert oder extern verifiziert.",
    // DN-44: simple renewal-due note for compliance modules that carry a
    // renewal_months value in their meta - only shown once the due date has
    // passed or is within 30 days (see renewalStatusForRecord()), not a
    // countdown for every completion.
    renewalOverdue: (d) => `Auffrischung überfällig seit ${d}`,
    renewalDueSoon: (d) => `Auffrischung fällig bis ${d}`,
  },
  en: {
    btn: "My certificates", title: "My certificates", close: "← Back",
    intro: "Passed exam simulations are recorded here as proof of completion (this device only). Download a certificate file to keep or share it - that file is the actual portable artifact, not the app's internal state.",
    empty: "No passed exam simulation yet. Pass an Exam Simulation (not Training mode) to get a certificate here.",
    passedOn: (d) => `Passed on ${d}`,
    downloadCert: "Download certificate (HTML)", downloadCred: "Download credential (JSON)",
    disclaimer: "Self-generated record, not cryptographically signed or independently verified.",
    renewalOverdue: (d) => `Refresher overdue since ${d}`,
    renewalDueSoon: (d) => `Refresher due by ${d}`,
  },
};
function certStrings(lang) {
  return CERT_STRINGS[lang] || CERT_STRINGS.en;
}

function getCompletions() {
  try {
    return JSON.parse(localStorage.getItem(profileKey("completions")) || "[]");
  } catch (e) {
    return [];
  }
}

// --- Real cryptographic signing (docs/open-badges-signing-scoping.md,
// section 4 "smallest viable version") ----------------------------------
// Netlify Function endpoint that signs a completion record as a JWT
// against the issuer keypair whose public half is published at
// /.well-known/jwks.json. This is genuinely optional at every call site:
// this app is an offline-capable PWA, so a passed exam simulation must
// keep producing a usable (if unverified) certificate even when the
// device is offline or the function isn't deployed/reachable yet - see
// trySignCompletion()'s catch path and credentialJsonDoc()'s fallback
// below. Nothing here ever blocks or fails the existing local-only flow.
const SIGN_CREDENTIAL_ENDPOINT = "/.netlify/functions/sign-credential";
const SIGN_CREDENTIAL_TIMEOUT_MS = 8000;

function persistCompletionUpdate(record) {
  try {
    const all = getCompletions();
    const idx = all.findIndex((r) => r.id === record.id);
    if (idx === -1) return;
    all[idx] = { ...all[idx], signedJwt: record.signedJwt, verified: record.verified, signedKid: record.signedKid, signedAlg: record.signedAlg };
    localStorage.setItem(profileKey("completions"), JSON.stringify(all));
  } catch (e) { /* non-fatal - storage may be full/unavailable */ }
}

// Best-effort: asks the signing function for a real signature over this
// completion record, mutates the record in place (so any already-rendered
// UI holding the same object reference picks it up), and persists the
// signed fields back into localStorage. Never throws - a failure here
// (offline, function not deployed, misconfigured env var, timeout) simply
// leaves the record as a self-issued/unverified one, exactly as it was
// before this feature existed.
async function trySignCompletion(record) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SIGN_CREDENTIAL_TIMEOUT_MS);
  try {
    const res = await fetch(SIGN_CREDENTIAL_ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        id: record.id,
        examType: record.examType,
        scopeCode: record.scopeCode,
        moduleLabel: record.moduleLabel,
        scopeLabel: record.scopeLabel,
        passedAt: record.passedAt,
        errorPoints: record.errorPoints,
        wrongHighStakes: record.wrongHighStakes,
        totalQuestions: record.totalQuestions,
      }),
      signal: controller.signal,
    });
    if (!res.ok) return; // server rejected it or isn't configured - stay unverified
    const body = await res.json();
    if (!body || !body.jwt || body.verified !== true) return;
    record.signedJwt = body.jwt;
    record.verified = true;
    record.signedKid = body.kid;
    record.signedAlg = body.alg;
    persistCompletionUpdate(record);
  } catch (e) {
    // Offline, function unreachable, timed out, or non-JSON response -
    // this is an expected, normal state for a static PWA and must not
    // surface as an error to the user; the unverified fallback stands.
  } finally {
    clearTimeout(timer);
  }
}

// Ensures a record has a signature attempt done at least once "fresh"
// before it's actually downloaded (in addition to the best-effort
// background attempt fired right after recordCompletion()) - covers the
// case where the background attempt hasn't resolved yet, was offline at
// the time but is online now, or the user is downloading an older
// already-recorded completion for the first time. Still falls back
// silently to the unverified shape on any failure.
async function ensureSignedCredential(record) {
  if (record.verified && record.signedJwt) return record;
  await trySignCompletion(record);
  return record;
}

function recordCompletion(examType, scopeCode, results) {
  const mod = moduleManifestFor(examType);
  const scopeOpt = mod?.options.find((o) => o.code === scopeCode);
  const record = {
    id: `${examType}-${scopeCode}-${Date.now()}`,
    examType,
    scopeCode,
    moduleLabel: mod ? (mod.label[state.lang] || mod.label.en) : examType,
    scopeLabel: scopeOpt ? (scopeOpt.label[state.lang] || scopeOpt.label.en) : scopeCode,
    passedAt: new Date().toISOString(),
    errorPoints: results.errorPoints,
    wrongHighStakes: results.wrongHighStakes,
    totalQuestions: state.exam.questions.length,
  };
  const all = getCompletions();
  all.push(record);
  try {
    localStorage.setItem(profileKey("completions"), JSON.stringify(all));
  } catch (e) { /* non-fatal - storage may be full/unavailable */ }
  // Best-effort, non-blocking: try to get a real signature right away so
  // it's likely already available by the time the user opens the
  // certificate screen and clicks download. Deliberately not awaited -
  // recordCompletion() must stay synchronous and must never make passing
  // an exam simulation depend on network access.
  trySignCompletion(record);
  return record;
}

function certificateHtmlDoc(record) {
  const C = certStrings(state.lang);
  const dateStr = new Date(record.passedAt).toLocaleDateString(state.lang);
  const escape = (s) => String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  return `<!doctype html>
<html lang="${state.lang}"><head><meta charset="utf-8"><title>${escape(record.moduleLabel)} - Certificate</title>
<style>
  body { font-family: Georgia, serif; max-width: 700px; margin: 60px auto; padding: 40px; border: 3px double #444; text-align: center; color: #222; }
  h1 { font-size: 1.6rem; margin-bottom: 4px; }
  .sub { color: #666; margin-bottom: 32px; }
  .module { font-size: 1.3rem; margin: 24px 0 4px; font-weight: bold; }
  .scope { color: #555; margin-bottom: 24px; }
  .meta { margin: 24px 0; font-size: 0.95rem; }
  .disclaimer { margin-top: 40px; font-size: 0.75rem; color: #888; font-family: Arial, sans-serif; }
</style></head>
<body>
  <h1>Zettacard</h1>
  <div class="sub">Certificate of Completion</div>
  <div class="module">${escape(record.moduleLabel)}</div>
  <div class="scope">${escape(record.scopeLabel)}</div>
  <div class="meta">${escape(C.passedOn(dateStr))}<br>${record.totalQuestions} question exam simulation &middot; ${record.errorPoints} error point(s) &middot; ${record.wrongHighStakes} safety-critical miss(es)</div>
  <div class="disclaimer">${escape(C.disclaimer)}</div>
</body></html>`;
}

function credentialJsonDoc(record) {
  const base = {
    "@context": ["https://www.w3.org/ns/credentials/v2", "https://purl.imsglobal.org/spec/ob/v3p0/context.json"],
    type: ["VerifiableCredential", "OpenBadgeCredential"],
    validFrom: record.passedAt,
    credentialSubject: {
      type: "AchievementSubject",
      achievement: {
        type: "Achievement",
        name: `${record.moduleLabel} - ${record.scopeLabel}`,
        description: `Passed an Exam Simulation for ${record.moduleLabel} (${record.scopeLabel}) in the Zettacard app.`,
        criteria: { narrative: `${record.totalQuestions}-question simulated exam, ${record.errorPoints} error points, ${record.wrongHighStakes} wrong safety-critical answer(s).` },
      },
    },
  };

  // Real signature available (netlify/functions/sign-credential.js
  // succeeded at some point for this record - see trySignCompletion()):
  // ship the actual signed JWT as the verifiable proof, drop the
  // unverified/unverifiedReason fields since they'd be actively false.
  // See docs/open-badges-signing-verification.md for how a third party
  // checks this signature themselves.
  if (record.verified && record.signedJwt) {
    return {
      ...base,
      issuer: { type: "Profile", id: (location.origin || ""), name: "Zettacard" },
      verified: true,
      proof: {
        type: "JsonWebSignature",
        jwt: record.signedJwt,
        alg: record.signedAlg || "ES256",
        kid: record.signedKid,
        jwksUrl: `${location.origin || ""}/.well-known/jwks.json`,
      },
    };
  }

  // Fallback: no signature yet (offline, function not deployed, signing
  // still in flight, or this is an older completion recorded before this
  // feature existed) - keep the original, honest self-issued shape rather
  // than blocking certificate/credential download on network access.
  return {
    ...base,
    unverified: true,
    unverifiedReason: "Self-issued by a zero-backend static PWA with no signing authority - not cryptographically signed, not independently verifiable by a third party.",
    issuer: { type: "Profile", name: "Zettacard (self-issued, unverified)" },
  };
}

function downloadTextFile(filename, content, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function openCertificates() {
  el("#certificates-view").hidden = false;
  history.pushState({ view: "certificates" }, "");
  renderCertificates();
  setInertBehindDialog(true);
  el("#certificates-title").focus();
}

function closeCertificates() {
  el("#certificates-view").hidden = true;
  setInertBehindDialog(false);
}

// DN-44: renewal-due indicator. A completion record only knows its own
// examType/scopeCode/passedAt - the renewal_months/renewal_basis policy
// lives in that module's core.json meta block (see data/build_modules.py),
// which may not be the CURRENTLY loaded module (e.g. viewing certificates
// for Datenschutz while Arbeitssicherheit is the active module). Fetched
// lazily and cached per exam_type rather than upfront for every module.
const moduleMetaCache = {};
async function getModuleMetaCached(examType) {
  if (moduleMetaCache[examType]) return moduleMetaCache[examType];
  try {
    const core = await fetchJson(`data/${examType}/core.json`);
    moduleMetaCache[examType] = core.meta || null;
  } catch (e) {
    moduleMetaCache[examType] = null;
  }
  return moduleMetaCache[examType];
}

function addMonths(date, months) {
  const d = new Date(date.getTime());
  d.setMonth(d.getMonth() + months);
  return d;
}

const RENEWAL_DUE_SOON_MS = 30 * 24 * 60 * 60 * 1000; // 30 days

// Returns null if this module has no fixed renewal_months (e.g. KI-Act) or
// the due date is more than 30 days away - the badge is only worth showing
// once it's actually actionable, not as a permanent countdown.
async function renewalStatusForRecord(record) {
  const meta = await getModuleMetaCached(record.examType);
  const months = meta && meta.renewal_months;
  if (!months) return null;
  const dueDate = addMonths(new Date(record.passedAt), months);
  const now = Date.now();
  if (dueDate.getTime() <= now) return { status: "overdue", dueDate };
  if (dueDate.getTime() - now <= RENEWAL_DUE_SOON_MS) return { status: "dueSoon", dueDate };
  return null;
}

async function renderCertificates() {
  const C = certStrings(state.lang);
  el("#certificates-title").textContent = C.title;
  el("#certificates-intro").textContent = C.intro;
  el("#certificates-close-btn").textContent = C.close;

  const list = el("#certificates-list");
  list.innerHTML = "";
  const records = getCompletions().slice().reverse();
  if (records.length === 0) {
    list.innerHTML = `<p class="empty">${C.empty}</p>`;
    return;
  }
  records.forEach(async (record) => {
    const dateStr = new Date(record.passedAt).toLocaleDateString(state.lang);
    const card = document.createElement("div");
    card.className = "cert-card";
    card.innerHTML = `
      <div class="cert-card-title">${record.moduleLabel} · ${record.scopeLabel}</div>
      <div class="cert-card-date">${C.passedOn(dateStr)}</div>
      <div class="cert-card-renewal"></div>
      <div class="cert-card-actions">
        <button class="back-btn cert-dl-cert">${C.downloadCert}</button>
        <button class="back-btn cert-dl-cred">${C.downloadCred}</button>
      </div>
    `;
    card.querySelector(".cert-dl-cert").addEventListener("click", () => {
      downloadTextFile(`${record.examType}-${record.scopeCode}-certificate.html`, certificateHtmlDoc(record), "text/html");
    });
    card.querySelector(".cert-dl-cred").addEventListener("click", async () => {
      // Give an unsigned/already-attempted record one more chance to get a
      // real signature (e.g. the device just came back online) before
      // building the download - falls back silently if it can't.
      await ensureSignedCredential(record);
      downloadTextFile(`${record.examType}-${record.scopeCode}-credential.json`, JSON.stringify(credentialJsonDoc(record), null, 2), "application/json");
    });
    list.appendChild(card);

    // Fetched/rendered after the card is already in the list (only the 4
    // compliance modules ever resolve to a non-null status) so a slow or
    // failed fetch never blocks showing the certificate itself.
    if (COMPLIANCE_MODULES.has(record.examType)) {
      const renewal = await renewalStatusForRecord(record);
      if (renewal) {
        const dueDateStr = renewal.dueDate.toLocaleDateString(state.lang);
        const text = renewal.status === "overdue" ? C.renewalOverdue(dueDateStr) : C.renewalDueSoon(dueDateStr);
        const slot = card.querySelector(".cert-card-renewal");
        if (slot) slot.innerHTML = `<span class="badge renewal-due">${text}</span>`;
      }
    }
  });
}

// --- Spaced repetition / Leitner system (DN-16) -------------------------
// A lightweight Leitner box scheme: every question a user has ever answered
// (in exam mode) or self-assessed (in the flashcard "Review due" mode) sits
// in one of 5 boxes (0-4). A correct/"knew it" answer promotes it one box
// up (reviewed less often going forward); a wrong/"didn't know it" answer
// resets it straight to box 0 (reviewed again soon) - the whole point of
// Leitner is that a single miss should undo several correct streaks' worth
// of spacing, not just step back one box, since a wrong answer on a
// recently-"mastered" question is a strong signal it wasn't mastered.
// Interval choice (deliberately simple, not a full SM-2/Anki-style
// algorithm - this is a lightweight add-on, not the app's whole model of
// learning):
//   box 0 -> due immediately (dueAt = now) - "next session" in practice,
//            since a review session already in progress keeps working
//            through the same due list rather than re-showing this
//            question a second later.
//   box 1 -> 1 day
//   box 2 -> 3 days
//   box 3 -> 7 days
//   box 4 -> 21 days (the ceiling - a question that keeps getting answered
//            correctly stays here rather than escaping review forever).
const SRS_BOX_INTERVAL_MS = [
  0,
  24 * 60 * 60 * 1000,
  3 * 24 * 60 * 60 * 1000,
  7 * 24 * 60 * 60 * 1000,
  21 * 24 * 60 * 60 * 1000,
];

// Data shape (per profile, via the same profileKey() namespace every other
// per-profile piece of state uses - see PROFILE_STRINGS block above):
//   { [questionId]: { box: 0-4, dueAt: <epoch ms> } }
// A question with no entry here has simply never been answered/assessed
// yet - it's not "due", it's just untracked, and stays that way until the
// first exam attempt or flashcard self-assessment touches it.
function loadSrsData() {
  try {
    const raw = JSON.parse(localStorage.getItem(profileKey("srs")) || "{}");
    return raw && typeof raw === "object" ? raw : {};
  } catch (e) {
    return {};
  }
}

function saveSrsData(data) {
  try { localStorage.setItem(profileKey("srs"), JSON.stringify(data)); } catch (e) { /* non-fatal */ }
}

// Single entry point for both feed paths (exam mode's real right/wrong and
// the flashcard review mode's self-assessment) so the box math only lives
// in one place.
function updateSrsBox(questionId, wasCorrect) {
  const srs = loadSrsData();
  const prevBox = srs[questionId]?.box ?? 0;
  const newBox = wasCorrect ? Math.min(SRS_BOX_INTERVAL_MS.length - 1, prevBox + 1) : 0;
  srs[questionId] = { box: newBox, dueAt: Date.now() + SRS_BOX_INTERVAL_MS[newBox] };
  saveSrsData(srs);
}

// Questions due right now for the CURRENTLY loaded module+scope (state.
// questions is already scoped to that - see loadModuleData). Deliberately
// ignores the topic filter: "due for review" is a study-priority queue
// across the whole module, not a subset of whatever topic happens to be
// selected in the regular browsing list.
function dueQuestionsForActiveScope() {
  const now = Date.now();
  const srs = loadSrsData();
  return state.questions.filter((q) => {
    const entry = srs[q.id];
    return entry && entry.dueAt <= now;
  });
}

// Same locale-object-per-language convention as PROFILE_STRINGS/CERT_STRINGS
// above, kept standalone rather than folded into UI_STRINGS since it's a
// self-contained additive feature (same reasoning EXAM_STRINGS documents).
const SRS_STRINGS = {
  de: { reviewBtn: (n) => `📅 Wiederholen (${n})`, reviewAria: "Fällige Wiederholungen", know: "Ich wusste es", dontKnow: "Ich wusste es nicht" },
  en: { reviewBtn: (n) => `📅 Review (${n})`, reviewAria: "Questions due for review", know: "I knew it", dontKnow: "I didn't know it" },
  uk: { reviewBtn: (n) => `📅 Повторення (${n})`, reviewAria: "Питання для повторення", know: "Я знав(ла) це", dontKnow: "Я не знав(ла) цього" },
  pl: { reviewBtn: (n) => `📅 Powtórka (${n})`, reviewAria: "Pytania do powtórki", know: "Wiedziałem/am to", dontKnow: "Nie wiedziałem/am tego" },
  ar: { reviewBtn: (n) => `📅 مراجعة (${n})`, reviewAria: "أسئلة مستحقة للمراجعة", know: "كنت أعرف ذلك", dontKnow: "لم أكن أعرف ذلك" },
  zh: { reviewBtn: (n) => `📅 复习 (${n})`, reviewAria: "待复习的问题", know: "我知道", dontKnow: "我不知道" },
  hi: { reviewBtn: (n) => `📅 पुनरावृत्ति (${n})`, reviewAria: "समीक्षा हेतु प्रश्न", know: "मुझे पता था", dontKnow: "मुझे नहीं पता था" },
  tr: { reviewBtn: (n) => `📅 Tekrar (${n})`, reviewAria: "Tekrar edilecek sorular", know: "Biliyordum", dontKnow: "Bilmiyordum" },
  fr: { reviewBtn: (n) => `📅 Révision (${n})`, reviewAria: "Questions à réviser", know: "Je le savais", dontKnow: "Je ne le savais pas" },
  ru: { reviewBtn: (n) => `📅 Повтор (${n})`, reviewAria: "Вопросы для повторения", know: "Я знал(а) это", dontKnow: "Я не знал(а) этого" },
  es: { reviewBtn: (n) => `📅 Repaso (${n})`, reviewAria: "Preguntas para repasar", know: "Lo sabía", dontKnow: "No lo sabía" },
  it: { reviewBtn: (n) => `📅 Ripasso (${n})`, reviewAria: "Domande da ripassare", know: "Lo sapevo", dontKnow: "Non lo sapevo" },
};
function srsStrings(lang) {
  return SRS_STRINGS[lang] || SRS_STRINGS.en;
}

// Opens the same #detail-view flashcard UI the regular question list uses,
// but sourced from the due queue instead of filteredQuestions()'s topic-
// filtered list (see the reviewMode branch in filteredQuestions() below) -
// deliberately reusing the existing single-question dialog rather than
// building a whole parallel view, since the only real difference is which
// list feeds it and what happens after reveal.
function openReviewSession() {
  const due = dueQuestionsForActiveScope();
  if (due.length === 0) return; // nothing to review right now - button stays visible showing "(0)"
  const srs = loadSrsData();
  state.reviewMode = true;
  // Most-overdue-first, so the questions that have been due longest (or
  // dropped straight back to box 0 most recently) surface before ones that
  // only just became due.
  state.reviewQueue = due.slice().sort((a, b) => srs[a.id].dueAt - srs[b.id].dueAt);
  state.detailIndex = 0;
  state.revealed = false;
  state.listScrollY = window.scrollY;
  state.lastOpenedIndex = null; // review mode isn't opened from a specific list card
  history.pushState({ view: "detail" }, "");
  render();
  setInertBehindDialog(true);
  el("#detail-question").focus();
}

// Records the self-assessment, feeds it into the Leitner box, and advances
// to the next due question (or exits review mode once the queue is empty).
function reviewAssess(wasCorrect) {
  const q = state.reviewQueue[state.detailIndex];
  if (!q) return;
  updateSrsBox(q.id, wasCorrect);
  state.reviewQueue.splice(state.detailIndex, 1);
  state.revealed = false;
  if (state.reviewQueue.length === 0) {
    history.back(); // triggers the popstate handler's closeDetail(), same exit path as the back button
    return;
  }
  if (state.detailIndex >= state.reviewQueue.length) state.detailIndex = state.reviewQueue.length - 1;
  render();
  el("#detail-question").focus();
}

// --- Sign Reference (Fuehrerschein-only) --------------------------------
// A browsable study reference of every StVO sign actually cited by a
// Fuehrerschein question's image_ref (see app/data/fuehrerschein/
// sign_reference.json, generated by assets/build_sign_reference.py). Every
// name/description in that JSON is lifted verbatim from an already-verified
// question's correct-option text / explanation rather than asserting any
// new fact about a sign's meaning - see that script's own header comment
// and BACKLOG.md's DN-32 entry for why this project treats traffic-sign
// facts with that discipline. DE/EN only for now, both for the reference
// content itself and (per the MODULE_PICKER_STRINGS/CERT_STRINGS
// convention already used elsewhere) the surrounding UI chrome, which
// falls back to English for the other 10 UI languages.
const SIGN_REF_STRINGS = {
  de: {
    btn: "📚 Schilder", ariaLabel: "Schilderreferenz", title: "Schilderreferenz",
    intro: "Alle Verkehrszeichen, die in den Fuehrerschein-Fragen vorkommen, mit Bedeutung - nach Zeichenart gruppiert.",
    close: "← Zurück", empty: "Keine Schilderreferenz verfügbar.",
  },
  en: {
    btn: "📚 Signs", ariaLabel: "Sign reference", title: "Sign reference",
    intro: "Every traffic sign referenced by a Fuehrerschein question, with its meaning - grouped by sign category.",
    close: "← Back", empty: "No sign reference available.",
  },
};

function signRefStrings(lang) {
  return SIGN_REF_STRINGS[lang] || SIGN_REF_STRINGS.en;
}

// StVO category headings, in the fixed study-reference order used by
// renderSignReferenceView() below (matches the order the categories are
// introduced in most driving-school material: danger, then the three
// regulatory families, then informational/other).
const SIGN_CATEGORY_ORDER = ["gefahrzeichen", "verbotszeichen", "gebotszeichen", "richtzeichen", "sonstige"];
const SIGN_CATEGORY_LABELS = {
  gefahrzeichen: { de: "Gefahrzeichen", en: "Warning signs" },
  verbotszeichen: { de: "Verbotszeichen", en: "Prohibition signs" },
  gebotszeichen: { de: "Gebotszeichen", en: "Mandatory signs" },
  richtzeichen: { de: "Richtzeichen", en: "Informational signs" },
  sonstige: { de: "Sonstige", en: "Other" },
};

function signCategoryLabel(cat, lang) {
  const entry = SIGN_CATEGORY_LABELS[cat];
  if (!entry) return cat;
  return entry[lang] || entry.en;
}

// Fetched once and cached - the reference data is static per module (not
// per-language: it already carries its own de/en keys per entry), so there
// is no reason to refetch it on every open or language switch.
let signReferenceCache = null;

async function loadSignReference() {
  if (signReferenceCache) return signReferenceCache;
  signReferenceCache = await fetchJson(`data/fuehrerschein/sign_reference.json`);
  return signReferenceCache;
}

function openSignReferenceView() {
  el("#sign-reference-view").hidden = false;
  history.pushState({ view: "sign-reference" }, "");
  setInertBehindDialog(true);
  renderSignReferenceView();
}

function closeSignReferenceView() {
  el("#sign-reference-view").hidden = true;
  setInertBehindDialog(false);
}

async function renderSignReferenceView() {
  const R = signRefStrings(state.lang);
  el("#sign-reference-title").textContent = R.title;
  el("#sign-reference-intro").textContent = R.intro;
  el("#sign-reference-close-btn").textContent = R.close;

  const list = el("#sign-reference-list");
  list.innerHTML = "";

  let data;
  try {
    data = await loadSignReference();
  } catch (e) {
    list.innerHTML = `<p class="empty">${R.empty}</p>`;
    el("#sign-reference-title").focus();
    return;
  }

  // Language for the reference CONTENT itself (name/desc) is DE/EN only -
  // fall back to English for the other 10 UI languages, same convention as
  // the surrounding chrome strings above.
  const contentLang = state.lang === "de" ? "de" : "en";

  let any = false;
  SIGN_CATEGORY_ORDER.forEach((cat) => {
    const entries = data[cat] || [];
    if (entries.length === 0) return;
    any = true;
    const heading = document.createElement("h3");
    heading.className = "sign-ref-category";
    heading.textContent = signCategoryLabel(cat, state.lang);
    list.appendChild(heading);

    entries.forEach((entry) => {
      const item = document.createElement("div");
      item.className = "sign-ref-item";
      const localized = entry[contentLang] || entry.en || entry.de;
      const img = document.createElement("img");
      img.className = "sign-ref-icon";
      img.src = `assets/signs/${entry.ref}.svg`;
      img.alt = localized.name;
      img.loading = "lazy";
      const text = document.createElement("div");
      text.className = "sign-ref-text";
      text.innerHTML = `<div class="sign-ref-name">${entry.ref} · ${localized.name}</div><div class="sign-ref-desc">${localized.desc}</div>`;
      item.appendChild(img);
      item.appendChild(text);
      list.appendChild(item);
    });
  });

  if (!any) {
    list.innerHTML = `<p class="empty">${R.empty}</p>`;
  }

  el("#sign-reference-title").focus();
}

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

  const isMultiSelect = q.question_type === "multi_choice";
  el("#exam-progress").textContent = X.progress(ex.index + 1, ex.questions.length);
  el("#exam-meta").innerHTML = `
    <span class="badge topic">${topicLabel}</span>
    <span class="badge points">${S.points(q.points)}</span>
    ${q.high_stakes ? `<span class="badge high-stakes">${S.highStakes}</span>` : ""}
    ${isMultiSelect ? `<span class="badge multi-select">${S.multiSelectHint}</span>` : ""}
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
  // Multi-select questions (DN-4, question_type "multi_choice") let more
  // than one option be selected at once, toggling independently - a real
  // checkbox rather than the radio-style single overwrite used for
  // single_choice. ex.answers[q.id] is a plain string key for single_choice
  // (unchanged from before) and an array of key strings for multi_choice, so
  // computeExamResults() below has to branch on question_type too.
  const applySelection = () => {
    const selected = ex.answers[q.id];
    const isSelected = (key) => isMultiSelect
      ? Array.isArray(selected) && selected.includes(key)
      : selected === key;
    optionsEl.querySelectorAll(".option").forEach((div) => {
      const isSel = isSelected(div.dataset.key);
      div.classList.toggle("exam-selected", isSel);
      if (isMultiSelect) div.setAttribute("aria-checked", String(isSel));
      else div.setAttribute("aria-pressed", String(isSel));
      const mark = div.querySelector(".selected-mark");
      if (mark) mark.textContent = isSel ? "✓" : "";
    });
  };
  Object.entries(t.options).forEach(([key, text]) => {
    const div = document.createElement("div");
    div.className = "option" + (isMultiSelect ? " option-checkbox" : "");
    div.dataset.key = key;
    if (isMultiSelect) {
      div.setAttribute("role", "checkbox");
      div.setAttribute("aria-checked", "false");
    } else {
      div.setAttribute("role", "button");
      div.setAttribute("aria-pressed", "false");
    }
    div.tabIndex = 0;
    // The "your selected answer" state previously relied ENTIRELY on a
    // border-color/background tint shift (2026-08-05 UX review) - a real
    // color-only signal, same class of issue this project already fixed
    // for the correct-answer mark. The checkmark span makes selection a
    // shape change too, not just a color change, for colorblind users.
    div.innerHTML = `<span class="key">${key.toUpperCase()}</span><span>${text}</span><span class="selected-mark" aria-hidden="true"></span>`;
    const pick = () => {
      if (isMultiSelect) {
        const current = Array.isArray(ex.answers[q.id]) ? ex.answers[q.id] : [];
        ex.answers[q.id] = current.includes(key)
          ? current.filter((k) => k !== key)
          : [...current, key];
      } else {
        ex.answers[q.id] = key;
      }
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

// A multi_choice question is only correct if the given set of picks is
// EXACTLY the correct set - matching the real exam's all-or-nothing scoring
// (no partial credit for picking some but not all of the right options, and
// picking an extra wrong option alongside right ones is still a full miss).
function isExamAnswerCorrect(q, given) {
  if (q.question_type === "multi_choice") {
    if (!Array.isArray(given) || given.length === 0) return false;
    if (given.length !== q.correct.length) return false;
    return given.every((k) => q.correct.includes(k));
  }
  return given != null && q.correct.includes(given);
}

function computeExamResults() {
  const ex = state.exam;
  let errorPoints = 0;
  let wrongHighStakes = 0;
  const wrongList = [];
  ex.questions.forEach((q) => {
    const given = ex.answers[q.id];
    const isCorrect = isExamAnswerCorrect(q, given);
    if (!isCorrect) {
      errorPoints += q.points;
      if (q.high_stakes) wrongHighStakes += 1;
      wrongList.push({ q, given });
    }
  });
  const passed = errorPoints <= 10 && wrongHighStakes < 2;
  return { errorPoints, wrongHighStakes, wrongList, passed };
}

// DN-16: exam mode already has a real, unambiguous right/wrong signal per
// question (isExamAnswerCorrect), unlike the flashcard view - so exam
// attempts feed the Leitner schedule automatically, with no extra UI, right
// alongside completion recording below. Only questions the user actually
// answered are touched; an unanswered question in Training mode (no time
// pressure, so this mostly matters for a timed-out Simulation run) isn't
// assumed to be a "miss" for scheduling purposes, since the user never
// engaged with it at all.
function feedExamResultsIntoSrs(ex) {
  ex.questions.forEach((q) => {
    const given = ex.answers[q.id];
    const wasAnswered = Array.isArray(given) ? given.length > 0 : given != null;
    if (!wasAnswered) return;
    updateSrsBox(q.id, isExamAnswerCorrect(q, given));
  });
}

function finishExam(timedOut) {
  stopExamTimer();
  state.exam.finished = true;
  state.exam.timedOut = !!timedOut;
  el("#exam-view").hidden = true;
  el("#exam-results").hidden = false;
  history.replaceState({ view: "exam-results" }, "");
  const results = computeExamResults();
  feedExamResultsIntoSrs(state.exam);
  if (results.passed && state.exam.mode === "simulation") {
    state.exam.certRecord = recordCompletion(state.examType, state.scopeCode, results);
  }
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
      // Multi-select questions can have 2+ correct keys and a given answer
      // that's an array (or unanswered) - join them into one readable list
      // rather than assuming a single string like the original single_choice
      // code did (which would have shown "undefined" for an array).
      const givenText = Array.isArray(given)
        ? (given.length ? given.map((k) => t.options[k]).join(", ") : "—")
        : (given && t.options[given]) || "—";
      const correctText = q.correct.map((k) => t.options[k]).join(", ");
      const item = document.createElement("div");
      item.className = "exam-review-item";
      item.innerHTML = `
        <div class="q-card-text">${t.question}</div>
        <div class="your-answer">${X.yourAnswer}: ${givenText}</div>
        <div class="right-answer">${X.rightAnswer}: ${correctText}</div>
      `;
      reviewEl.appendChild(item);
    });
  }
  el("#exam-results-close-btn").textContent = X.close;

  const certEl = el("#exam-results-certificate");
  const C = certStrings(state.lang);
  if (state.exam.certRecord) {
    certEl.innerHTML = `
      <div class="cert-card">
        <div class="cert-card-title">🎓 ${C.title}</div>
        <div class="cert-card-actions">
          <button class="back-btn" id="exam-results-cert-html">${C.downloadCert}</button>
          <button class="back-btn" id="exam-results-cert-json">${C.downloadCred}</button>
        </div>
      </div>
    `;
    const record = state.exam.certRecord;
    el("#exam-results-cert-html").addEventListener("click", () => {
      downloadTextFile(`zettacard-zertifikat-${record.id}.html`, certificateHtmlDoc(record), "text/html");
    });
    el("#exam-results-cert-json").addEventListener("click", async () => {
      await ensureSignedCredential(record);
      downloadTextFile(`zettacard-credential-${record.id}.json`, JSON.stringify(credentialJsonDoc(record), null, 2), "application/json");
    });
  } else {
    certEl.innerHTML = "";
  }
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
  // Review mode (DN-16) swaps the list source entirely - the topic filter
  // doesn't apply while cycling through the due queue, see openReviewSession().
  if (state.reviewMode) return state.reviewQueue;
  let qs = state.questions;
  if (state.topicFilter !== "all") qs = qs.filter((q) => q.topic_code === state.topicFilter);
  // Role filter (DN-44) is additive to the topic filter above, and only
  // ever meaningfully narrows anything for the 4 compliance modules (every
  // other module's questions have no "roles" field, so questionMatchesRole
  // treats them as ["all"] and they always pass).
  if (state.roleFilter !== "all") qs = qs.filter((q) => questionMatchesRole(q, state.roleFilter));
  return qs;
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

  // DN-43: the "About this module" info button only makes sense once a
  // module is active and that module actually has an intro wizard defined.
  const infoBtn = el("#module-info-btn");
  infoBtn.hidden = !(moduleMod && moduleMod.intro);
  infoBtn.title = introStrings(state.lang).aboutBtn;
  infoBtn.setAttribute("aria-label", introStrings(state.lang).aboutBtn);

  // Sign Reference only makes sense for Fuehrerschein (that's the only
  // module whose questions carry StVO sign image_refs so far) - hidden for
  // every other module, same pattern as the info button above.
  const signRefBtn = el("#sign-reference-btn");
  signRefBtn.hidden = state.examType !== "fuehrerschein";
  const R = signRefStrings(state.lang);
  signRefBtn.textContent = R.btn;
  signRefBtn.title = R.title;
  signRefBtn.setAttribute("aria-label", R.ariaLabel);

  ["lang-select", "detail-lang-select"].forEach((id) => {
    el("#" + id).value = state.lang;
    el("#" + id).setAttribute("aria-label", LANG_PICKER_LABEL[state.lang] || "Language");
  });

  const PR = profileStrings(state.lang);
  const profileBtn = el("#profile-switch-btn");
  profileBtn.textContent = `👤 ${currentProfileName()} ▾`;
  profileBtn.setAttribute("aria-label", PR.switchAria);
  profileBtn.title = PR.switchAria;

  // DN-16: shown even at 0 due (never hidden) - a learner should be able to
  // see "nothing due right now" rather than wonder if review mode exists.
  const SR = srsStrings(state.lang);
  const dueCount = dueQuestionsForActiveScope().length;
  const reviewBtn = el("#review-btn");
  reviewBtn.textContent = SR.reviewBtn(dueCount);
  reviewBtn.setAttribute("aria-label", SR.reviewAria);
  reviewBtn.title = SR.reviewAria;
  reviewBtn.classList.toggle("has-due", dueCount > 0);

  renderFilters();
  renderRoleFilter();

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
      try { localStorage.setItem(profileKey("filter"), code); } catch (e) { /* non-fatal */ }
      render();
    });
    container.appendChild(btn);
  });
}

// DN-44: second, additive filter row - only shown for the 4 workplace-
// compliance modules, since that's the only content that carries a `roles`
// tag. Hidden entirely (not just empty) for every other module, same
// pattern the Sign Reference button already uses to hide itself outside
// Fuehrerschein.
function renderRoleFilter() {
  const container = el("#role-filters");
  if (!container) return;
  const isCompliance = COMPLIANCE_MODULES.has(state.examType);
  container.hidden = !isCompliance;
  if (!isCompliance) return;

  const R = roleFilterStrings(state.lang);
  container.setAttribute("aria-label", R.label);
  container.innerHTML = "";
  ROLE_FILTER_CODES.forEach((code) => {
    const btn = document.createElement("button");
    btn.textContent = R[code];
    btn.className = state.roleFilter === code ? "active" : "";
    btn.setAttribute("aria-pressed", String(state.roleFilter === code));
    btn.addEventListener("click", () => {
      state.roleFilter = code;
      state.detailIndex = null;
      try { localStorage.setItem(profileKey("role-filter"), code); } catch (e) { /* non-fatal */ }
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
        ${q.question_type === "multi_choice" ? `<span class="badge multi-select">${S.multiSelectHint}</span>` : ""}
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
      // Focus the question itself first (tabindex="-1", see app.html) so a
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
    ${q.question_type === "multi_choice" ? `<span class="badge multi-select">${S.multiSelectHint}</span>` : ""}
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

  // DN-16: review mode replaces the usual prev/next browsing controls with
  // self-assessment buttons once the answer is revealed - this view has no
  // other explicit right/wrong signal the way exam mode does (real answer
  // capture), so the Leitner box update needs the user's own honest
  // judgment of whether they actually knew it.
  const SR = srsStrings(state.lang);
  el("#detail-nav-row").hidden = state.reviewMode;
  const reviewActions = el("#review-actions");
  reviewActions.hidden = !(state.reviewMode && state.revealed);
  if (state.reviewMode) {
    el("#review-know-btn").textContent = SR.know;
    el("#review-dontknow-btn").textContent = SR.dontKnow;
  }

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
  try { localStorage.setItem(profileKey("lang"), lang); } catch (e) { /* storage unavailable, non-fatal */ }
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
  // Leaving the detail dialog always exits review mode too (whether via the
  // back button, browser back gesture, or the queue running out in
  // reviewAssess()) - there's no "paused" review session to resume, a new
  // one is just built fresh from whatever's due next time.
  state.reviewMode = false;
  state.reviewQueue = [];
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
  wireModuleIntroControls();
  el("#certificates-btn").addEventListener("click", openCertificates);
  el("#certificates-close-btn").addEventListener("click", () => history.back());
  el("#review-btn").addEventListener("click", openReviewSession);
  el("#review-know-btn").addEventListener("click", () => reviewAssess(true));
  el("#review-dontknow-btn").addEventListener("click", () => reviewAssess(false));
  el("#sign-reference-btn").addEventListener("click", openSignReferenceView);
  el("#sign-reference-close-btn").addEventListener("click", () => history.back());

  el("#profile-switch-btn").addEventListener("click", openProfileSwitcher);
  el("#profile-close-btn").addEventListener("click", () => history.back());
  el("#profile-add-btn").addEventListener("click", () => createProfile(el("#profile-add-input").value));
  el("#profile-add-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); createProfile(el("#profile-add-input").value); }
  });

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
    if (!el("#module-intro").hidden) closeModuleIntro();
    if (!el("#certificates-view").hidden) closeCertificates();
    if (!el("#sign-reference-view").hidden) closeSignReferenceView();
    if (!el("#profile-view").hidden) closeProfileSwitcher();
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

// Loads every piece of per-profile state (language, topic filter, active
// module+scope) from the CURRENTLY active profile's localStorage namespace
// and re-renders everything - used both by init() on first load and by
// switchProfile()/createProfile() so switching profiles is a full state
// reload, exactly like a language or module switch already is.
async function loadActiveProfileState() {
  state.detailIndex = null;
  state.exam = null;
  state.topicFilter = "all";
  state.roleFilter = "all";
  state.examType = null;
  state.scopeCode = null;

  try {
    const savedLang = localStorage.getItem(profileKey("lang"));
    if (savedLang && UI_STRINGS[savedLang]) {
      state.lang = savedLang;
    } else {
      // No explicit preference saved yet for this profile - try the
      // browser/device language before falling back to German, so a
      // first-time visitor in one of the supported languages doesn't
      // always land on German chrome.
      const detected = detectBrowserLang();
      state.lang = detected || "de";
    }
    const savedFilter = localStorage.getItem(profileKey("filter"));
    state.topicFilter = savedFilter || "all";
    // DN-44: role filter is per-profile too (same key convention as the
    // topic filter above) - only ever visibly applied for the 4 compliance
    // modules, but harmless to restore unconditionally since
    // questionMatchesRole() treats every other module's untagged questions
    // as always matching.
    const savedRoleFilter = localStorage.getItem(profileKey("role-filter"));
    state.roleFilter = ROLE_FILTER_CODES.includes(savedRoleFilter) ? savedRoleFilter : "all";
  } catch (e) { /* storage unavailable, defaults are fine */ }

  document.documentElement.setAttribute("lang", state.lang);
  document.documentElement.setAttribute("dir", RTL_LANGS.has(state.lang) ? "rtl" : "ltr");

  let savedExamType = null, savedScopeCode = null;
  try {
    savedExamType = localStorage.getItem(profileKey("exam-type"));
    savedScopeCode = localStorage.getItem(profileKey("scope-code"));
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
    // First-ever visit for this profile, or no saved selection yet - block
    // on choosing a module before showing any content, same pattern as the
    // exam-mode picker (a full-screen dialog, not a silent default).
    render();
    openModulePicker();
  }
}

async function init() {
  migrateOrInitProfiles();

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

  await loadActiveProfileState();

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("service-worker.js").catch(() => {
      /* offline caching is a nice-to-have; app still works without it */
    });
  }
}

init();
