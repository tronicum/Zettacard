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
    tryItHint: "Zum Ausprobieren antippen",
    yourPickWrong: "Deine Antwort",
    imageNote: "🖼️ Bild ausstehend — Referenz: ",
    explanationLabel: "Erklärung",
    legalBasis: "Rechtsgrundlage",
    installHint: "Zum Startbildschirm hinzufügen für Offline-Nutzung.",
    empty: "Keine Fragen in dieser Kategorie.",
    correctMark: "Richtig",
    offlinePrepBtn: "📥 Für offline verfügbar machen",
    offlinePrepReady: "✅ Offline verfügbar",
    offlinePrepLoading: (i, n) => `Lade ${i}/${n}…`,
    offlinePrepError: "⚠️ Nicht alles konnte geladen werden — bitte erneut versuchen",
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
    tryItHint: "Tap to try answering",
    yourPickWrong: "Your answer",
    imageNote: "🖼️ Image pending — ref: ",
    explanationLabel: "Explanation",
    legalBasis: "Legal basis",
    installHint: "Add to your home screen to use offline.",
    empty: "No questions in this category.",
    correctMark: "Correct",
    offlinePrepBtn: "📥 Make available offline",
    offlinePrepReady: "✅ Available offline",
    offlinePrepLoading: (i, n) => `Loading ${i}/${n}…`,
    offlinePrepError: "⚠️ Some files failed — try again",
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
    tryItHint: "Торкніться, щоб спробувати відповісти",
    yourPickWrong: "Твоя відповідь",
    imageNote: "🖼️ Зображення відсутнє — посилання: ",
    explanationLabel: "Пояснення",
    legalBasis: "Правова основа",
    installHint: "Додайте на головний екран для використання офлайн.",
    empty: "У цій категорії немає питань.",
    correctMark: "Правильно",
    offlinePrepBtn: "📥 Зробити доступним офлайн",
    offlinePrepReady: "✅ Доступно офлайн",
    offlinePrepLoading: (i, n) => `Завантаження ${i}/${n}…`,
    offlinePrepError: "⚠️ Не все вдалося завантажити — спробуйте ще раз",
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
    tryItHint: "Dotknij, aby spróbować odpowiedzieć",
    yourPickWrong: "Twoja odpowiedź",
    imageNote: "🖼️ Brak obrazu — odniesienie: ",
    explanationLabel: "Wyjaśnienie",
    legalBasis: "Podstawa prawna",
    installHint: "Dodaj do ekranu głównego, aby korzystać offline.",
    empty: "Brak pytań w tej kategorii.",
    correctMark: "Poprawnie",
    offlinePrepBtn: "📥 Udostępnij offline",
    offlinePrepReady: "✅ Dostępne offline",
    offlinePrepLoading: (i, n) => `Wczytywanie ${i}/${n}…`,
    offlinePrepError: "⚠️ Nie wszystko się udało — spróbuj ponownie",
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
    tryItHint: "اضغط للمحاولة في الإجابة",
    yourPickWrong: "إجابتك",
    imageNote: "🖼️ الصورة غير متوفرة — المرجع: ",
    explanationLabel: "الشرح",
    legalBasis: "الأساس القانوني",
    installHint: "أضف إلى الشاشة الرئيسية للاستخدام دون اتصال بالإنترنت.",
    empty: "لا توجد أسئلة في هذه الفئة.",
    correctMark: "صحيح",
    offlinePrepBtn: "📥 إتاحة العمل دون اتصال",
    offlinePrepReady: "✅ متاح دون اتصال",
    offlinePrepLoading: (i, n) => `جارٍ التحميل ${i}/${n}…`,
    offlinePrepError: "⚠️ تعذّر تحميل بعض الملفات — حاول مرة أخرى",
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
    tryItHint: "点击尝试作答",
    yourPickWrong: "你的答案",
    imageNote: "🖼️ 图片暂缺 — 参考：",
    explanationLabel: "解释",
    legalBasis: "法律依据",
    installHint: "添加到主屏幕即可离线使用。",
    empty: "该类别下没有题目。",
    correctMark: "正确",
    offlinePrepBtn: "📥 设为离线可用",
    offlinePrepReady: "✅ 已可离线使用",
    offlinePrepLoading: (i, n) => `正在加载 ${i}/${n}…`,
    offlinePrepError: "⚠️ 部分文件加载失败 — 请重试",
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
    tryItHint: "उत्तर देने के लिए टैप करें",
    yourPickWrong: "आपका उत्तर",
    imageNote: "🖼️ चित्र उपलब्ध नहीं — संदर्भ: ",
    explanationLabel: "स्पष्टीकरण",
    legalBasis: "कानूनी आधार",
    installHint: "ऑफ़लाइन उपयोग के लिए होम स्क्रीन पर जोड़ें।",
    empty: "इस श्रेणी में कोई प्रश्न नहीं है।",
    correctMark: "सही",
    offlinePrepBtn: "📥 ऑफ़लाइन उपलब्ध कराएं",
    offlinePrepReady: "✅ ऑफ़लाइन उपलब्ध",
    offlinePrepLoading: (i, n) => `लोड हो रहा है ${i}/${n}…`,
    offlinePrepError: "⚠️ कुछ फ़ाइलें लोड नहीं हुईं — फिर कोशिश करें",
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
    tryItHint: "Cevaplamayı denemek için dokunun",
    yourPickWrong: "Cevabınız",
    imageNote: "🖼️ Görsel eksik — referans: ",
    explanationLabel: "Açıklama",
    legalBasis: "Yasal dayanak",
    installHint: "Çevrimdışı kullanım için ana ekrana ekleyin.",
    empty: "Bu kategoride soru yok.",
    correctMark: "Doğru",
    offlinePrepBtn: "📥 Çevrimdışı kullanıma hazırla",
    offlinePrepReady: "✅ Çevrimdışı kullanılabilir",
    offlinePrepLoading: (i, n) => `Yükleniyor ${i}/${n}…`,
    offlinePrepError: "⚠️ Bazı dosyalar yüklenemedi — tekrar deneyin",
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
    tryItHint: "Touchez pour essayer de répondre",
    yourPickWrong: "Votre réponse",
    imageNote: "🖼️ Image manquante — référence : ",
    explanationLabel: "Explication",
    legalBasis: "Base légale",
    installHint: "Ajoutez à l'écran d'accueil pour une utilisation hors ligne.",
    empty: "Aucune question dans cette catégorie.",
    correctMark: "Correct",
    offlinePrepBtn: "📥 Rendre disponible hors ligne",
    offlinePrepReady: "✅ Disponible hors ligne",
    offlinePrepLoading: (i, n) => `Chargement ${i}/${n}…`,
    offlinePrepError: "⚠️ Certains fichiers ont échoué — réessayez",
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
    tryItHint: "Нажмите, чтобы попробовать ответить",
    yourPickWrong: "Ваш ответ",
    imageNote: "🖼️ Изображение отсутствует — ссылка: ",
    explanationLabel: "Объяснение",
    legalBasis: "Правовая основа",
    installHint: "Добавьте на главный экран для использования офлайн.",
    empty: "В этой категории нет вопросов.",
    correctMark: "Правильно",
    offlinePrepBtn: "📥 Сделать доступным офлайн",
    offlinePrepReady: "✅ Доступно офлайн",
    offlinePrepLoading: (i, n) => `Загрузка ${i}/${n}…`,
    offlinePrepError: "⚠️ Не всё удалось загрузить — попробуйте снова",
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
    tryItHint: "Toca para intentar responder",
    yourPickWrong: "Tu respuesta",
    imageNote: "🖼️ Imagen pendiente — referencia: ",
    explanationLabel: "Explicación",
    legalBasis: "Base legal",
    installHint: "Añade a la pantalla de inicio para usarlo sin conexión.",
    empty: "No hay preguntas en esta categoría.",
    correctMark: "Correcto",
    offlinePrepBtn: "📥 Disponible sin conexión",
    offlinePrepReady: "✅ Disponible sin conexión",
    offlinePrepLoading: (i, n) => `Cargando ${i}/${n}…`,
    offlinePrepError: "⚠️ Algunos archivos fallaron — inténtalo de nuevo",
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
    tryItHint: "Tocca per provare a rispondere",
    yourPickWrong: "La tua risposta",
    imageNote: "🖼️ Immagine mancante — riferimento: ",
    explanationLabel: "Spiegazione",
    legalBasis: "Base giuridica",
    installHint: "Aggiungi alla schermata Home per l'uso offline.",
    empty: "Nessuna domanda in questa categoria.",
    correctMark: "Corretto",
    offlinePrepBtn: "📥 Rendi disponibile offline",
    offlinePrepReady: "✅ Disponibile offline",
    offlinePrepLoading: (i, n) => `Caricamento ${i}/${n}…`,
    offlinePrepError: "⚠️ Alcuni file non sono stati caricati — riprova",
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
    close: "Schließen", noMistakes: "Alle Fragen richtig beantwortet — sehr gut!", confirmExit: "Prüfung wirklich abbrechen? Der Fortschritt geht verloren.",
    skip: "Später beantworten", skipBanner: "Wiederholung übersprungener Fragen — diese Fragen müssen jetzt final beantwortet werden.", skipProgress: (i, n) => `Übersprungene Fragen: ${i} von ${n}` },
  en: { startBtn: "Exam", pickerTitle: "Choose exam mode", pickerDesc: "Choose how you want to practice. Both modes draw 30 questions with realistic weighting and score using the real pass rule.",
    trainingTitle: "Training exam", trainingDesc: "No time limit. Good for calm practice.",
    simTitle: "Simulated real exam", simDesc: "45-minute time limit, like the real exam.",
    cancel: "Cancel", progress: (i, n) => `Question ${i} of ${n}`, next: "Next", finish: "Finish exam",
    exit: "Cancel", timeUp: "Time is up — the exam was submitted automatically.",
    resultsPass: "Passed", resultsFail: "Not passed",
    summary: (err, wrong) => `Error points: ${err} of max. 10 allowed. Wrong safety-critical questions: ${wrong} (2 or more means automatic fail).`,
    reviewLabel: "Review of wrong answers", yourAnswer: "Your answer", rightAnswer: "Correct answer",
    close: "Close", noMistakes: "All questions answered correctly — well done!", confirmExit: "Really cancel the exam? Progress will be lost.",
    skip: "Answer later", skipBanner: "Reviewing skipped questions — these must be answered now.", skipProgress: (i, n) => `Skipped questions: ${i} of ${n}` },
  uk: { startBtn: "Іспит", pickerTitle: "Виберіть режим іспиту", pickerDesc: "Оберіть, як тренуватися. В обох режимах 30 питань з реальним розподілом і оцінюванням за справжнім правилом складання.",
    trainingTitle: "Тренувальний іспит", trainingDesc: "Без обмеження часу. Підходить для спокійного тренування.",
    simTitle: "Симуляція реального іспиту", simDesc: "Обмеження 45 хвилин, як на справжньому іспиті.",
    cancel: "Скасувати", progress: (i, n) => `Питання ${i} з ${n}`, next: "Далі", finish: "Завершити іспит",
    exit: "Скасувати", timeUp: "Час вийшов — іспит подано автоматично.",
    resultsPass: "Складено", resultsFail: "Не складено",
    summary: (err, wrong) => `Штрафні бали: ${err} з макс. 10 допустимих. Неправильні відповіді на питання, важливі для безпеки: ${wrong} (2 і більше — автоматичний провал).`,
    reviewLabel: "Перегляд неправильних відповідей", yourAnswer: "Ваша відповідь", rightAnswer: "Правильна відповідь",
    close: "Закрити", noMistakes: "Усі питання дано правильно — чудово!", confirmExit: "Дійсно скасувати іспит? Прогрес буде втрачено.",
    skip: "Відповісти пізніше", skipBanner: "Перегляд пропущених питань — на них потрібно відповісти зараз.", skipProgress: (i, n) => `Пропущені питання: ${i} з ${n}` },
  pl: { startBtn: "Egzamin", pickerTitle: "Wybierz tryb egzaminu", pickerDesc: "Wybierz sposób ćwiczenia. Oba tryby losują 30 pytań z realnym rozkładem i oceniają wg prawdziwej zasady zaliczenia.",
    trainingTitle: "Egzamin ćwiczeniowy", trainingDesc: "Bez limitu czasu. Do spokojnego ćwiczenia.",
    simTitle: "Symulacja prawdziwego egzaminu", simDesc: "Limit czasu 45 minut, jak na prawdziwym egzaminie.",
    cancel: "Anuluj", progress: (i, n) => `Pytanie ${i} z ${n}`, next: "Dalej", finish: "Zakończ egzamin",
    exit: "Anuluj", timeUp: "Czas minął — egzamin został przesłany automatycznie.",
    resultsPass: "Zdany", resultsFail: "Niezdany",
    summary: (err, wrong) => `Punkty karne: ${err} z maks. 10 dozwolonych. Błędne odpowiedzi na pytania istotne dla bezpieczeństwa: ${wrong} (2 lub więcej oznacza automatyczne niezaliczenie).`,
    reviewLabel: "Przegląd błędnych odpowiedzi", yourAnswer: "Twoja odpowiedź", rightAnswer: "Poprawna odpowiedź",
    close: "Zamknij", noMistakes: "Wszystkie pytania poprawne — świetnie!", confirmExit: "Na pewno przerwać egzamin? Postęp zostanie utracony.",
    skip: "Odpowiedz później", skipBanner: "Przegląd pominiętych pytań — teraz trzeba na nie odpowiedzieć.", skipProgress: (i, n) => `Pominięte pytania: ${i} z ${n}` },
  ar: { startBtn: "الامتحان", pickerTitle: "اختر وضع الامتحان", pickerDesc: "اختر طريقة التدريب. يسحب كلا الوضعين 30 سؤالاً بتوزيع واقعي ويُقيَّمان وفق قاعدة النجاح الحقيقية.",
    trainingTitle: "امتحان تدريبي", trainingDesc: "بدون حد زمني. مناسب للتدريب الهادئ.",
    simTitle: "محاكاة الامتحان الحقيقي", simDesc: "حد زمني 45 دقيقة، كما في الامتحان الحقيقي.",
    cancel: "إلغاء", progress: (i, n) => `السؤال ${i} من ${n}`, next: "التالي", finish: "إنهاء الامتحان",
    exit: "إلغاء", timeUp: "انتهى الوقت — تم تسليم الامتحان تلقائيًا.",
    resultsPass: "ناجح", resultsFail: "غير ناجح",
    summary: (err, wrong) => `نقاط الخطأ: ${err} من 10 كحد أقصى مسموح. الأسئلة الحرجة للسلامة الخاطئة: ${wrong} (سؤالان أو أكثر يعني رسوبًا تلقائيًا).`,
    reviewLabel: "مراجعة الإجابات الخاطئة", yourAnswer: "إجابتك", rightAnswer: "الإجابة الصحيحة",
    close: "إغلاق", noMistakes: "تمت الإجابة عن جميع الأسئلة بشكل صحيح — أحسنت!", confirmExit: "هل تريد حقًا إلغاء الامتحان؟ سيُفقد التقدم.",
    skip: "الإجابة لاحقًا", skipBanner: "مراجعة الأسئلة المتخطاة — يجب الإجابة عنها الآن.", skipProgress: (i, n) => `الأسئلة المتخطاة: ${i} من ${n}` },
  zh: { startBtn: "考试", pickerTitle: "选择考试模式", pickerDesc: "选择练习方式。两种模式都会按真实比例抽取30道题,并按真实及格规则评分。",
    trainingTitle: "练习考试", trainingDesc: "无时间限制,适合从容练习。",
    simTitle: "模拟真实考试", simDesc: "45分钟时间限制,与真实考试一致。",
    cancel: "取消", progress: (i, n) => `第 ${i} 题，共 ${n} 题`, next: "下一题", finish: "完成考试",
    exit: "取消", timeUp: "时间到 — 考试已自动提交。",
    resultsPass: "通过", resultsFail: "未通过",
    summary: (err, wrong) => `错误分数：${err}分，最多允许10分。安全关键问题答错数：${wrong}题（2题或以上将自动判定不及格）。`,
    reviewLabel: "错误答案回顾", yourAnswer: "您的答案", rightAnswer: "正确答案",
    close: "关闭", noMistakes: "所有题目均答对 — 非常好!", confirmExit: "确定要取消考试吗?进度将丢失。",
    skip: "稍后回答", skipBanner: "正在复查跳过的题目 — 现在必须作答。", skipProgress: (i, n) => `跳过的题目：第 ${i} 题，共 ${n} 题` },
  hi: { startBtn: "परीक्षा", pickerTitle: "परीक्षा मोड चुनें", pickerDesc: "अभ्यास करने का तरीका चुनें। दोनों मोड वास्तविक भारांक के साथ 30 प्रश्न चुनते हैं और असली उत्तीर्ण नियम से स्कोर करते हैं।",
    trainingTitle: "अभ्यास परीक्षा", trainingDesc: "समय सीमा नहीं। शांति से अभ्यास के लिए अच्छा।",
    simTitle: "वास्तविक परीक्षा सिमुलेशन", simDesc: "45 मिनट की समय सीमा, असली परीक्षा जैसी।",
    cancel: "रद्द करें", progress: (i, n) => `प्रश्न ${i} / ${n}`, next: "अगला", finish: "परीक्षा समाप्त करें",
    exit: "रद्द करें", timeUp: "समय समाप्त — परीक्षा स्वतः जमा कर दी गई।",
    resultsPass: "उत्तीर्ण", resultsFail: "अनुत्तीर्ण",
    summary: (err, wrong) => `त्रुटि अंक: ${err}, अधिकतम 10 स्वीकार्य। गलत सुरक्षा-महत्वपूर्ण प्रश्न: ${wrong} (2 या अधिक होने पर स्वतः अनुत्तीर्ण)।`,
    reviewLabel: "गलत उत्तरों की समीक्षा", yourAnswer: "आपका उत्तर", rightAnswer: "सही उत्तर",
    close: "बंद करें", noMistakes: "सभी प्रश्नों के सही उत्तर — बहुत बढ़िया!", confirmExit: "क्या आप वाकई परीक्षा रद्द करना चाहते हैं? प्रगति खो जाएगी।",
    skip: "बाद में उत्तर दें", skipBanner: "छोड़े गए प्रश्नों की समीक्षा — अब इनका उत्तर देना आवश्यक है।", skipProgress: (i, n) => `छोड़े गए प्रश्न: ${i} / ${n}` },
  tr: { startBtn: "Sınav", pickerTitle: "Sınav modunu seçin", pickerDesc: "Nasıl çalışmak istediğinizi seçin. Her iki mod da gerçekçi ağırlıkla 30 soru seçer ve gerçek geçme kuralına göre puanlar.",
    trainingTitle: "Alıştırma sınavı", trainingDesc: "Süre sınırı yok. Sakin çalışma için uygundur.",
    simTitle: "Gerçek sınav simülasyonu", simDesc: "Gerçek sınavdaki gibi 45 dakika süre sınırı.",
    cancel: "İptal", progress: (i, n) => `${n} sorudan ${i}.`, next: "İleri", finish: "Sınavı bitir",
    exit: "İptal", timeUp: "Süre doldu — sınav otomatik olarak gönderildi.",
    resultsPass: "Geçti", resultsFail: "Geçemedi",
    summary: (err, wrong) => `Hata puanı: ${err}, izin verilen maksimum 10. Yanlış güvenlik açısından kritik soru: ${wrong} (2 veya daha fazlası otomatik başarısızlık demektir).`,
    reviewLabel: "Yanlış cevapların incelenmesi", yourAnswer: "Cevabınız", rightAnswer: "Doğru cevap",
    close: "Kapat", noMistakes: "Tüm sorular doğru cevaplandı — harika!", confirmExit: "Sınavı gerçekten iptal etmek istiyor musunuz? İlerleme kaybolacak.",
    skip: "Sonra cevapla", skipBanner: "Atlanan soruların gözden geçirilmesi — bunlar şimdi cevaplanmalı.", skipProgress: (i, n) => `Atlanan sorular: ${n} sorudan ${i}.` },
  fr: { startBtn: "Examen", pickerTitle: "Choisir le mode d'examen", pickerDesc: "Choisissez votre façon de vous entraîner. Les deux modes tirent 30 questions avec une pondération réaliste et notent selon la règle de réussite réelle.",
    trainingTitle: "Examen d'entraînement", trainingDesc: "Sans limite de temps. Idéal pour s'entraîner calmement.",
    simTitle: "Simulation d'examen réel", simDesc: "Limite de 45 minutes, comme le véritable examen.",
    cancel: "Annuler", progress: (i, n) => `Question ${i} sur ${n}`, next: "Suivant", finish: "Terminer l'examen",
    exit: "Annuler", timeUp: "Le temps est écoulé — l'examen a été soumis automatiquement.",
    resultsPass: "Réussi", resultsFail: "Échoué",
    summary: (err, wrong) => `Points d'erreur : ${err} sur 10 maximum autorisés. Questions critiques pour la sécurité incorrectes : ${wrong} (2 ou plus entraîne un échec automatique).`,
    reviewLabel: "Révision des réponses incorrectes", yourAnswer: "Votre réponse", rightAnswer: "Bonne réponse",
    close: "Fermer", noMistakes: "Toutes les questions ont une réponse correcte — bravo !", confirmExit: "Voulez-vous vraiment annuler l'examen ? La progression sera perdue.",
    skip: "Répondre plus tard", skipBanner: "Révision des questions passées — elles doivent maintenant recevoir une réponse.", skipProgress: (i, n) => `Questions passées : ${i} sur ${n}` },
  ru: { startBtn: "Экзамен", pickerTitle: "Выберите режим экзамена", pickerDesc: "Выберите способ тренировки. Оба режима выбирают 30 вопросов с реалистичным распределением и оцениваются по настоящему правилу сдачи.",
    trainingTitle: "Тренировочный экзамен", trainingDesc: "Без ограничения времени. Подходит для спокойной тренировки.",
    simTitle: "Симуляция настоящего экзамена", simDesc: "Ограничение 45 минут, как на настоящем экзамене.",
    cancel: "Отмена", progress: (i, n) => `Вопрос ${i} из ${n}`, next: "Далее", finish: "Завершить экзамен",
    exit: "Отмена", timeUp: "Время истекло — экзамен отправлен автоматически.",
    resultsPass: "Сдано", resultsFail: "Не сдано",
    summary: (err, wrong) => `Штрафные баллы: ${err} из макс. 10 допустимых. Неверные ответы на вопросы, критичные для безопасности: ${wrong} (2 и более означает автоматический провал).`,
    reviewLabel: "Разбор неверных ответов", yourAnswer: "Ваш ответ", rightAnswer: "Правильный ответ",
    close: "Закрыть", noMistakes: "Все вопросы даны верно — отлично!", confirmExit: "Действительно отменить экзамен? Прогресс будет потерян.",
    skip: "Ответить позже", skipBanner: "Повторный просмотр пропущенных вопросов — на них нужно ответить сейчас.", skipProgress: (i, n) => `Пропущенные вопросы: ${i} из ${n}` },
  es: { startBtn: "Examen", pickerTitle: "Elegir modo de examen", pickerDesc: "Elige cómo quieres practicar. Ambos modos seleccionan 30 preguntas con ponderación realista y puntúan según la regla real de aprobación.",
    trainingTitle: "Examen de entrenamiento", trainingDesc: "Sin límite de tiempo. Ideal para practicar con calma.",
    simTitle: "Simulación de examen real", simDesc: "Límite de 45 minutos, como el examen real.",
    cancel: "Cancelar", progress: (i, n) => `Pregunta ${i} de ${n}`, next: "Siguiente", finish: "Finalizar examen",
    exit: "Cancelar", timeUp: "Se acabó el tiempo — el examen se envió automáticamente.",
    resultsPass: "Aprobado", resultsFail: "No aprobado",
    summary: (err, wrong) => `Puntos de error: ${err} de máx. 10 permitidos. Preguntas críticas para la seguridad incorrectas: ${wrong} (2 o más significa suspenso automático).`,
    reviewLabel: "Revisión de respuestas incorrectas", yourAnswer: "Tu respuesta", rightAnswer: "Respuesta correcta",
    close: "Cerrar", noMistakes: "Todas las preguntas respondidas correctamente — ¡muy bien!", confirmExit: "¿Seguro que quieres cancelar el examen? Se perderá el progreso.",
    skip: "Responder más tarde", skipBanner: "Revisión de preguntas omitidas — ahora deben responderse.", skipProgress: (i, n) => `Preguntas omitidas: ${i} de ${n}` },
  it: { startBtn: "Esame", pickerTitle: "Scegli la modalità d'esame", pickerDesc: "Scegli come vuoi esercitarti. Entrambe le modalità estraggono 30 domande con una ponderazione realistica e valutano secondo la regola reale di superamento.",
    trainingTitle: "Esame di allenamento", trainingDesc: "Senza limite di tempo. Ideale per esercitarsi con calma.",
    simTitle: "Simulazione d'esame reale", simDesc: "Limite di 45 minuti, come l'esame reale.",
    cancel: "Annulla", progress: (i, n) => `Domanda ${i} di ${n}`, next: "Avanti", finish: "Termina esame",
    exit: "Annulla", timeUp: "Il tempo è scaduto — l'esame è stato inviato automaticamente.",
    resultsPass: "Superato", resultsFail: "Non superato",
    summary: (err, wrong) => `Punti di errore: ${err} su un massimo di 10 consentiti. Domande critiche per la sicurezza sbagliate: ${wrong} (2 o più significa bocciatura automatica).`,
    reviewLabel: "Revisione delle risposte sbagliate", yourAnswer: "La tua risposta", rightAnswer: "Risposta corretta",
    close: "Chiudi", noMistakes: "Tutte le domande risposte correttamente — ottimo lavoro!", confirmExit: "Vuoi davvero annullare l'esame? I progressi andranno persi.",
    skip: "Rispondi più tardi", skipBanner: "Revisione delle domande saltate — ora devono essere risposte.", skipProgress: (i, n) => `Domande saltate: ${i} di ${n}` },
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
  // DN-27 pilot round (2026-08-07): 28 of the 40 "gefahr" (hazard/road-
  // condition) topic questions - the rest were deliberately skipped as
  // purely definitional/behavioural with nothing spatial to draw (see
  // BACKLOG.md for the full skip list and reasoning). New scene types
  // drawn by assets/generate_hazard_diagrams.py (sibling to
  // generate_diagrams.py, reuses its svg()/car()/badge()/arrow() helpers).
  "gefahr-01", "gefahr-02", "gefahr-04", "gefahr-05", "gefahr-06", "gefahr-07",
  "gefahr-08", "gefahr-09", "gefahr-10", "gefahr-16", "gefahr-18", "gefahr-19",
  "gefahr-20", "gefahr-22", "gefahr-23", "gefahr-24", "gefahr-25", "gefahr-26",
  "gefahr-27", "gefahr-29", "gefahr-32", "gefahr-33", "gefahr-34", "gefahr-35",
  "gefahr-36", "gefahr-37", "gefahr-38", "gefahr-40",
]);

// Alt text describes what's VISUALLY on the sign (shape/color/symbol) -
// deliberately NOT its legal meaning, since for most sign questions
// identifying that meaning IS the question. A screen-reader user should
// have to reason it out from the same visual facts a sighted user gets,
// not be handed the answer through the alt text.
const SIGN_ALT = {
  "101": { de: "Rot umrandetes weißes Dreieck mit schwarzem Ausrufezeichen", en: "Red-bordered white triangle with a black exclamation mark", uk: "Білий трикутник з червоною облямівкою та чорним знаком оклику", pl: "Biały trójkąt z czerwoną obwódką i czarnym wykrzyknikiem", ar: "مثلث أبيض بحافة حمراء وعلامة تعجب سوداء", zh: "红边白色三角形,内有黑色感叹号", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें काला विस्मयादिबोधक चिह्न है", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde siyah ünlem işareti", fr: "Triangle blanc bordé de rouge avec un point d'exclamation noir", ru: "Белый треугольник с красной каймой и чёрным восклицательным знаком", es: "Triángulo blanco con borde rojo y un signo de exclamación negro", it: "Triangolo bianco bordato di rosso con un punto esclamativo nero" },
  "102": { de: "Rot umrandetes weißes Dreieck mit schwarzem Kreuzsymbol", en: "Red-bordered white triangle with a black crossroads symbol", uk: "Білий трикутник з червоною облямівкою та чорним символом перехрестя", pl: "Biały trójkąt z czerwoną obwódką i czarnym symbolem skrzyżowania", ar: "مثلث أبيض بحافة حمراء ورمز تقاطع طرق أسود", zh: "红边白色三角形,内有黑色十字路口符号", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें काला चौराहा प्रतीक है", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde siyah dört yol ağzı simgesi", fr: "Triangle blanc bordé de rouge avec un symbole de croisement noir", ru: "Белый треугольник с красной каймой и чёрным символом перекрёстка", es: "Triángulo blanco con borde rojo y un símbolo de cruce negro", it: "Triangolo bianco bordato di rosso con un simbolo di incrocio nero" },
  "120": { de: "Rot umrandetes weißes Dreieck mit zwei aufeinander zulaufenden schwarzen Linien", en: "Red-bordered white triangle with two converging black lines", uk: "Білий трикутник з червоною облямівкою та двома лініями, що сходяться", pl: "Biały trójkąt z czerwoną obwódką i dwiema zbiegającymi się czarnymi liniami", ar: "مثلث أبيض بحافة حمراء وخطان أسودان يتقاربان", zh: "红边白色三角形,内有两条汇聚的黑线", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें दो अभिसरण होती काली रेखाएँ हैं", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde birbirine yaklaşan iki siyah çizgi", fr: "Triangle blanc bordé de rouge avec deux lignes noires convergentes", ru: "Белый треугольник с красной каймой и двумя сходящимися чёрными линиями", es: "Triángulo blanco con borde rojo y dos líneas negras convergentes", it: "Triangolo bianco bordato di rosso con due linee nere convergenti" },
  "123": { de: "Rot umrandetes weißes Dreieck mit einer schwarzen Figur mit Schaufel", en: "Red-bordered white triangle with a black figure holding a shovel", uk: "Білий трикутник з червоною облямівкою та чорною фігурою з лопатою", pl: "Biały trójkąt z czerwoną obwódką i czarną postacią z łopatą", ar: "مثلث أبيض بحافة حمراء وشكل أسود يحمل مجرفة", zh: "红边白色三角形,内有一个手持铁锹的黑色人形", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें फावड़ा पकड़े एक काली आकृति है", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde kürek tutan siyah bir figür", fr: "Triangle blanc bordé de rouge avec une silhouette noire tenant une pelle", ru: "Белый треугольник с красной каймой и чёрной фигурой с лопатой", es: "Triángulo blanco con borde rojo y una figura negra con una pala", it: "Triangolo bianco bordato di rosso con una figura nera con una pala" },
  "133": { de: "Rot umrandetes weißes Dreieck mit einer schwarzen erwachsenen Figur", en: "Red-bordered white triangle with a single black adult figure", uk: "Білий трикутник з червоною облямівкою та однією чорною фігурою дорослого", pl: "Biały trójkąt z czerwoną obwódką i pojedynczą czarną postacią dorosłego", ar: "مثلث أبيض بحافة حمراء وشكل بالغ أسود واحد", zh: "红边白色三角形,内有一个黑色成人人形", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें एक काली वयस्क आकृति है", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde tek bir siyah yetişkin figürü", fr: "Triangle blanc bordé de rouge avec une seule silhouette noire d'adulte", ru: "Белый треугольник с красной каймой и одной чёрной фигурой взрослого человека", es: "Triángulo blanco con borde rojo y una sola figura negra de un adulto", it: "Triangolo bianco bordato di rosso con una singola figura nera di un adulto" },
  "136": { de: "Rot umrandetes weißes Dreieck mit zwei kleinen schwarzen Figuren", en: "Red-bordered white triangle with two small black figures", uk: "Білий трикутник з червоною облямівкою та двома маленькими чорними фігурами", pl: "Biały trójkąt z czerwoną obwódką i dwiema małymi czarnymi postaciami", ar: "مثلث أبيض بحافة حمراء وشكلان صغيران أسودان", zh: "红边白色三角形,内有两个小黑色人形", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें दो छोटी काली आकृतियाँ हैं", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde iki küçük siyah figür", fr: "Triangle blanc bordé de rouge avec deux petites silhouettes noires", ru: "Белый треугольник с красной каймой и двумя маленькими чёрными фигурами", es: "Triángulo blanco con borde rojo y dos pequeñas figuras negras", it: "Triangolo bianco bordato di rosso con due piccole figure nere" },
  "151": { de: "Rot umrandetes weißes Dreieck mit schwarzem Zugsymbol", en: "Red-bordered white triangle with a black train symbol", uk: "Білий трикутник з червоною облямівкою та чорним символом потяга", pl: "Biały trójkąt z czerwoną obwódką i czarnym symbolem pociągu", ar: "مثلث أبيض بحافة حمراء ورمز قطار أسود", zh: "红边白色三角形,内有黑色火车符号", hi: "लाल किनारी वाला सफेद त्रिकोण जिसमें काला ट्रेन प्रतीक है", tr: "Kırmızı kenarlıklı beyaz üçgen, içinde siyah tren simgesi", fr: "Triangle blanc bordé de rouge avec un symbole de train noir", ru: "Белый треугольник с красной каймой и чёрным символом поезда", es: "Triángulo blanco con borde rojo y un símbolo de tren negro", it: "Triangolo bianco bordato di rosso con un simbolo di treno nero" },
  "201": { de: "Rotes X (Andreaskreuz) auf weißem Grund", en: "Red X (St. Andrew's cross) on a white background", uk: "Червоний хрест (Андріївський хрест) на білому тлі", pl: "Czerwony X (krzyż św. Andrzeja) na białym tle", ar: "علامة X حمراء (صليب القديس أندراوس) على خلفية بيضاء", zh: "白色背景上的红色X形(圣安德鲁十字)", hi: "सफेद पृष्ठभूमि पर लाल X (सेंट एंड्रयू क्रॉस)", tr: "Beyaz zemin üzerinde kırmızı X (Aziz Andreas çarpraz işareti)", fr: "Croix rouge (croix de Saint-André) sur fond blanc", ru: "Красный крест (Андреевский крест) на белом фоне", es: "X roja (cruz de San Andrés) sobre fondo blanco", it: "X rossa (croce di Sant'Andrea) su sfondo bianco" },
  "205": { de: "Nach unten zeigendes, rot umrandetes weißes Dreieck ohne Symbol", en: "Downward-pointing, red-bordered white triangle with no symbol", uk: "Спрямований вниз білий трикутник з червоною облямівкою без символу", pl: "Skierowany w dół biały trójkąt z czerwoną obwódką, bez symbolu", ar: "مثلث أبيض بحافة حمراء يشير إلى الأسفل بدون رمز", zh: "尖角朝下的红边白色三角形,无符号", hi: "नीचे की ओर इशारा करता, लाल किनारी वाला सफेद त्रिकोण, बिना किसी प्रतीक के", tr: "Aşağı bakan, kırmızı kenarlıklı beyaz üçgen, sembolsüz", fr: "Triangle blanc bordé de rouge pointant vers le bas, sans symbole", ru: "Белый треугольник с красной каймой, направленный вершиной вниз, без символа", es: "Triángulo blanco con borde rojo apuntando hacia abajo, sin símbolo", it: "Triangolo bianco bordato di rosso rivolto verso il basso, senza simbolo" },
  "206": { de: "Rotes Achteck mit weißer Aufschrift STOP", en: "Red octagon with white STOP lettering", uk: "Червоний восьмикутник з білим написом STOP", pl: "Czerwony ośmiokąt z białym napisem STOP", ar: "مثمن أحمر يحمل كلمة STOP بيضاء", zh: "红色八角形,白色STOP字样", hi: "लाल अष्टकोण जिस पर सफेद अक्षरों में STOP लिखा है", tr: "Beyaz STOP yazılı kırmızı sekizgen", fr: "Octogone rouge avec l'inscription blanche STOP", ru: "Красный восьмиугольник с белой надписью STOP", es: "Octógono rojo con la inscripción blanca STOP", it: "Ottagono rosso con la scritta bianca STOP" },
  "209": { de: "Blauer Kreis mit weißem, nach rechts zeigendem Pfeil", en: "Blue circle with a white arrow pointing right", uk: "Синє коло з білою стрілкою, що вказує праворуч", pl: "Niebieskie koło z białą strzałką skierowaną w prawo", ar: "دائرة زرقاء بسهم أبيض يشير إلى اليمين", zh: "蓝色圆形,内有指向右方的白色箭头", hi: "नीला वृत्त जिसमें दाईं ओर इशारा करता सफेद तीर है", tr: "Mavi daire, içinde sağa dönük beyaz ok", fr: "Cercle bleu avec une flèche blanche pointant vers la droite", ru: "Синий круг с белой стрелкой, указывающей направо", es: "Círculo azul con una flecha blanca apuntando hacia la derecha", it: "Cerchio blu con una freccia bianca rivolta verso destra" },
  "215": { de: "Blauer Kreis mit weißem Kreispfeil", en: "Blue circle with a white circular arrow", uk: "Синє коло з білою круговою стрілкою", pl: "Niebieskie koło z białą strzałką okrężną", ar: "دائرة زرقاء بسهم دائري أبيض", zh: "蓝色圆形,内有白色环形箭头", hi: "नीला वृत्त जिसमें सफेद गोलाकार तीर है", tr: "Mavi daire, içinde beyaz dairesel ok", fr: "Cercle bleu avec une flèche circulaire blanche", ru: "Синий круг с белой круговой стрелкой", es: "Círculo azul con una flecha circular blanca", it: "Cerchio blu con una freccia circolare bianca" },
  "220": { de: "Blaues Quadrat mit weißem, nach oben zeigendem Pfeil", en: "Blue square with a white upward-pointing arrow", uk: "Синій квадрат з білою стрілкою, що вказує вгору", pl: "Niebieski kwadrat z białą strzałką skierowaną w górę", ar: "مربع أزرق بسهم أبيض يشير إلى الأعلى", zh: "蓝色正方形,内有指向上方的白色箭头", hi: "नीला वर्ग जिसमें ऊपर की ओर इशारा करता सफेद तीर है", tr: "Mavi kare, içinde yukarı dönük beyaz ok", fr: "Carré bleu avec une flèche blanche pointant vers le haut", ru: "Синий квадрат с белой стрелкой, указывающей вверх", es: "Cuadrado azul con una flecha blanca apuntando hacia arriba", it: "Quadrato blu con una freccia bianca rivolta verso l'alto" },
  "237": { de: "Blauer Kreis mit weißem Fahrradsymbol", en: "Blue circle with a white bicycle symbol", uk: "Синє коло з білим символом велосипеда", pl: "Niebieskie koło z białym symbolem roweru", ar: "دائرة زرقاء برمز دراجة هوائية أبيض", zh: "蓝色圆形,内有白色自行车符号", hi: "नीला वृत्त जिसमें सफेद साइकिल प्रतीक है", tr: "Mavi daire, içinde beyaz bisiklet simgesi", fr: "Cercle bleu avec un symbole de vélo blanc", ru: "Синий круг с белым символом велосипеда", es: "Círculo azul con un símbolo de bicicleta blanco", it: "Cerchio blu con un simbolo di bicicletta bianco" },
  "240": { de: "Blauer Kreis mit weißem Fußgänger- und Fahrradsymbol übereinander", en: "Blue circle with white pedestrian and bicycle symbols stacked", uk: "Синє коло з білими символами пішохода та велосипеда один над одним", pl: "Niebieskie koło z białymi symbolami pieszego i roweru jeden nad drugim", ar: "دائرة زرقاء برمزي مشاة ودراجة هوائية أبيضين متراكبين", zh: "蓝色圆形,内有上下叠放的白色行人和自行车符号", hi: "नीला वृत्त जिसमें एक के ऊपर एक सफेद पैदल यात्री और साइकिल प्रतीक हैं", tr: "Mavi daire, içinde alt alta beyaz yaya ve bisiklet simgeleri", fr: "Cercle bleu avec les symboles blancs d'un piéton et d'un vélo superposés", ru: "Синий круг с белыми символами пешехода и велосипеда друг над другом", es: "Círculo azul con los símbolos blancos de un peatón y una bicicleta superpuestos", it: "Cerchio blu con i simboli bianchi di un pedone e di una bicicletta sovrapposti" },
  "250": { de: "Weißer Kreis mit dickem rotem Rand, kein Symbol", en: "White circle with a thick red border, no symbol", uk: "Біле коло з товстою червоною облямівкою, без символу", pl: "Białe koło z grubą czerwoną obwódką, bez symbolu", ar: "دائرة بيضاء بحافة حمراء سميكة، بدون رمز", zh: "白色圆形,粗红边,无符号", hi: "सफेद वृत्त जिसकी मोटी लाल किनारी है, बिना किसी प्रतीक के", tr: "Beyaz daire, kalın kırmızı kenarlıklı, sembolsüz", fr: "Cercle blanc avec un épais bord rouge, sans symbole", ru: "Белый круг с толстой красной каймой, без символа", es: "Círculo blanco con un borde rojo grueso, sin símbolo", it: "Cerchio bianco con un bordo rosso spesso, senza simbolo" },
  "260": { de: "Weißer Kreis mit rotem Rand und schwarzer Autosilhouette", en: "White circle with a red border and a black car silhouette", uk: "Біле коло з червоною облямівкою та чорним силуетом автомобіля", pl: "Białe koło z czerwoną obwódką i czarną sylwetką samochodu", ar: "دائرة بيضاء بحافة حمراء وصورة ظلية سوداء لسيارة", zh: "白色圆形,红边,内有黑色汽车剪影", hi: "सफेद वृत्त जिसकी लाल किनारी है और जिसमें काली कार की आकृति है", tr: "Kırmızı kenarlıklı beyaz daire, içinde siyah araba silüeti", fr: "Cercle blanc avec un bord rouge et une silhouette de voiture noire", ru: "Белый круг с красной каймой и чёрным силуэтом автомобиля", es: "Círculo blanco con un borde rojo y una silueta de coche negra", it: "Cerchio bianco con un bordo rosso e una sagoma di automobile nera" },
  "267": { de: "Roter Kreis mit weißem waagerechtem Balken", en: "Red circle with a white horizontal bar", uk: "Червоне коло з білою горизонтальною смугою", pl: "Czerwone koło z białym poziomym paskiem", ar: "دائرة حمراء بشريط أفقي أبيض", zh: "红色圆形,内有白色横杠", hi: "लाल वृत्त जिसमें सफेद क्षैतिज पट्टी है", tr: "Kırmızı daire, içinde beyaz yatay çubuk", fr: "Cercle rouge avec une barre horizontale blanche", ru: "Красный круг с белой горизонтальной полосой", es: "Círculo rojo con una barra horizontal blanca", it: "Cerchio rosso con una barra orizzontale bianca" },
  "274": { de: "Weißer Kreis mit rotem Rand und einer schwarzen Zahl", en: "White circle with a red border and a black number", uk: "Біле коло з червоною облямівкою та чорним числом", pl: "Białe koło z czerwoną obwódką i czarną liczbą", ar: "دائرة بيضاء بحافة حمراء ورقم أسود", zh: "白色圆形,红边,内有黑色数字", hi: "सफेद वृत्त जिसकी लाल किनारी है और जिसमें एक काला अंक है", tr: "Kırmızı kenarlıklı beyaz daire, içinde siyah bir sayı", fr: "Cercle blanc avec un bord rouge et un chiffre noir", ru: "Белый круг с красной каймой и чёрной цифрой", es: "Círculo blanco con un borde rojo y un número negro", it: "Cerchio bianco con un bordo rosso e un numero nero" },
  "276": { de: "Weißer Kreis mit rotem Rand und zwei Autosilhouetten (schwarz und rot)", en: "White circle with a red border and two car silhouettes (black and red)", uk: "Біле коло з червоною облямівкою та двома силуетами автомобілів (чорним і червоним)", pl: "Białe koło z czerwoną obwódką i dwiema sylwetkami samochodów (czarną i czerwoną)", ar: "دائرة بيضاء بحافة حمراء وصورتان ظليتان لسيارتين (سوداء وحمراء)", zh: "白色圆形,红边,内有两辆汽车剪影(黑色和红色)", hi: "सफेद वृत्त जिसकी लाल किनारी है और जिसमें दो कार की आकृतियाँ हैं (काली और लाल)", tr: "Kırmızı kenarlıklı beyaz daire, içinde iki araba silüeti (siyah ve kırmızı)", fr: "Cercle blanc avec un bord rouge et deux silhouettes de voiture (noire et rouge)", ru: "Белый круг с красной каймой и двумя силуэтами автомобилей (чёрным и красным)", es: "Círculo blanco con un borde rojo y dos siluetas de coche (negra y roja)", it: "Cerchio bianco con un bordo rosso e due sagome di automobile (nera e rossa)" },
  "278": { de: "Weißer Kreis mit grauem Rand, Zahl von grauer Diagonale durchgestrichen", en: "White circle with a grey border, a number crossed out by a grey diagonal line", uk: "Біле коло із сірою облямівкою, число перекреслене сірою діагональною лінією", pl: "Białe koło z szarą obwódką, liczba przekreślona szarą ukośną linią", ar: "دائرة بيضاء بحافة رمادية، رقم مشطوب بخط قطري رمادي", zh: "白色圆形,灰边,数字被一条灰色斜线划掉", hi: "सफेद वृत्त जिसकी धूसर किनारी है, एक अंक को धूसर विकर्ण रेखा से काटा गया है", tr: "Gri kenarlıklı beyaz daire, gri bir çapraz çizgiyle üzeri çizilmiş bir sayı", fr: "Cercle blanc avec un bord gris, un chiffre barré par une ligne diagonale grise", ru: "Белый круг с серой каймой, цифра перечёркнута серой диагональной линией", es: "Círculo blanco con un borde gris, un número tachado por una línea diagonal gris", it: "Cerchio bianco con un bordo grigio, un numero barrato da una linea diagonale grigia" },
  "282": { de: "Weißer Kreis mit fünf grauen Diagonalstreifen", en: "White circle with five grey diagonal stripes", uk: "Біле коло з п'ятьма сірими діагональними смугами", pl: "Białe koło z pięcioma szarymi ukośnymi paskami", ar: "دائرة بيضاء بخمسة خطوط قطرية رمادية", zh: "白色圆形,内有五条灰色斜条纹", hi: "सफेद वृत्त जिसमें पांच धूसर विकर्ण धारियाँ हैं", tr: "Beyaz daire, içinde beş gri çapraz çizgi", fr: "Cercle blanc avec cinq bandes diagonales grises", ru: "Белый круг с пятью серыми диагональными полосами", es: "Círculo blanco con cinco franjas diagonales grises", it: "Cerchio bianco con cinque strisce diagonali grigie" },
  "283": { de: "Blauer Kreis mit rotem X", en: "Blue circle with a red X", uk: "Синє коло з червоним хрестом X", pl: "Niebieskie koło z czerwonym X", ar: "دائرة زرقاء بعلامة X حمراء", zh: "蓝色圆形,内有红色X", hi: "नीला वृत्त जिसमें लाल X है", tr: "Mavi daire, içinde kırmızı X", fr: "Cercle bleu avec une croix rouge", ru: "Синий круг с красным крестом", es: "Círculo azul con una X roja", it: "Cerchio blu con una X rossa" },
  "286": { de: "Blauer Kreis mit einem roten Diagonalstrich", en: "Blue circle with a single red diagonal stripe", uk: "Синє коло з однією червоною діагональною смугою", pl: "Niebieskie koło z pojedynczym czerwonym ukośnym paskiem", ar: "دائرة زرقاء بخط قطري أحمر واحد", zh: "蓝色圆形,内有一条红色斜条纹", hi: "नीला वृत्त जिसमें एक लाल विकर्ण धारी है", tr: "Mavi daire, içinde tek bir kırmızı çapraz çizgi", fr: "Cercle bleu avec une seule bande diagonale rouge", ru: "Синий круг с одной красной диагональной полосой", es: "Círculo azul con una sola franja diagonal roja", it: "Cerchio blu con una singola striscia diagonale rossa" },
  "293": { de: "Blaues Quadrat mit weißem Dreieck und schwarzer Fußgängerfigur", en: "Blue square with a white triangle and a black pedestrian figure", uk: "Синій квадрат з білим трикутником та чорною фігурою пішохода", pl: "Niebieski kwadrat z białym trójkątem i czarną postacią pieszego", ar: "مربع أزرق بمثلث أبيض وشكل أسود لمشاة", zh: "蓝色正方形,内有白色三角形和黑色行人人形", hi: "नीला वर्ग जिसमें सफेद त्रिकोण और काली पैदल यात्री आकृति है", tr: "Mavi kare, içinde beyaz üçgen ve siyah yaya figürü", fr: "Carré bleu avec un triangle blanc et une silhouette noire de piéton", ru: "Синий квадрат с белым треугольником и чёрной фигурой пешехода", es: "Cuadrado azul con un triángulo blanco y una figura negra de peatón", it: "Quadrato blu con un triangolo bianco e una figura nera di pedone" },
  "301": { de: "Gelbe Raute mit weißem Rand, kein Symbol", en: "Yellow diamond with a white border, no symbol", uk: "Жовтий ромб з білою облямівкою, без символу", pl: "Żółty romb z białą obwódką, bez symbolu", ar: "معين أصفر بحافة بيضاء، بدون رمز", zh: "黄色菱形,白边,无符号", hi: "सफेद किनारी वाला पीला हीरा (डायमंड) आकार, बिना किसी प्रतीक के", tr: "Beyaz kenarlıklı sarı eşkenar dörtgen, sembolsüz", fr: "Losange jaune avec un bord blanc, sans symbole", ru: "Жёлтый ромб с белой каймой, без символа", es: "Rombo amarillo con un borde blanco, sin símbolo", it: "Rombo giallo con un bordo bianco, senza simbolo" },
  "306": { de: "Gelbes Quadrat mit schwarz-weißem Rand, kein Symbol", en: "Yellow square with a black-and-white border, no symbol", uk: "Жовтий квадрат з чорно-білою облямівкою, без символу", pl: "Żółty kwadrat z czarno-białą obwódką, bez symbolu", ar: "مربع أصفر بحافة سوداء وبيضاء، بدون رمز", zh: "黄色正方形,黑白相间边框,无符号", hi: "पीला वर्ग जिसकी काली-सफेद किनारी है, बिना किसी प्रतीक के", tr: "Siyah-beyaz kenarlıklı sarı kare, sembolsüz", fr: "Carré jaune avec un bord noir et blanc, sans symbole", ru: "Жёлтый квадрат с чёрно-белой каймой, без символа", es: "Cuadrado amarillo con un borde blanco y negro, sin símbolo", it: "Quadrato giallo con un bordo bianco e nero, senza simbolo" },
  "307": { de: "Gelbes Quadrat mit schwarz-weißem Rand, von grauen Diagonalen durchgestrichen", en: "Yellow square with a black-and-white border, crossed out by grey diagonal lines", uk: "Жовтий квадрат з чорно-білою облямівкою, перекреслений сірими діагональними лініями", pl: "Żółty kwadrat z czarno-białą obwódką, przekreślony szarymi ukośnymi liniami", ar: "مربع أصفر بحافة سوداء وبيضاء، مشطوب بخطوط قطرية رمادية", zh: "黄色正方形,黑白相间边框,被灰色斜线划掉", hi: "पीला वर्ग जिसकी काली-सफेद किनारी है, धूसर विकर्ण रेखाओं से काटा गया", tr: "Siyah-beyaz kenarlıklı sarı kare, gri çapraz çizgilerle üzeri çizilmiş", fr: "Carré jaune avec un bord noir et blanc, barré par des lignes diagonales grises", ru: "Жёлтый квадрат с чёрно-белой каймой, перечёркнутый серыми диагональными линиями", es: "Cuadrado amarillo con un borde blanco y negro, tachado por líneas diagonales grises", it: "Quadrato giallo con un bordo bianco e nero, barrato da linee diagonali grigie" },
  "314": { de: "Blaues Quadrat mit weißem Buchstaben P", en: "Blue square with a white letter P", uk: "Синій квадрат з білою літерою P", pl: "Niebieski kwadrat z białą literą P", ar: "مربع أزرق بحرف P أبيض", zh: "蓝色正方形,内有白色字母P", hi: "नीला वर्ग जिसमें सफेद अक्षर P है", tr: "Mavi kare, içinde beyaz P harfi", fr: "Carré bleu avec la lettre blanche P", ru: "Синий квадрат с белой буквой P", es: "Cuadrado azul con la letra blanca P", it: "Quadrato blu con la lettera bianca P" },
  "315": { de: "Blaues Quadrat mit weißem Buchstaben P über einem Auto-auf-Linie-Symbol", en: "Blue square with a white letter P above a car-on-a-line symbol", uk: "Синій квадрат з білою літерою P над символом автомобіля на лінії", pl: "Niebieski kwadrat z białą literą P nad symbolem samochodu na linii", ar: "مربع أزرق بحرف P أبيض فوق رمز سيارة على خط", zh: "蓝色正方形,白色字母P位于汽车压线符号上方", hi: "नीला वर्ग जिसमें सफेद अक्षर P एक रेखा पर खड़ी कार के प्रतीक के ऊपर है", tr: "Mavi kare, çizgi üzerindeki araba simgesinin üstünde beyaz P harfi", fr: "Carré bleu avec la lettre blanche P au-dessus d'un symbole de voiture sur une ligne", ru: "Синий квадрат с белой буквой P над символом автомобиля на линии", es: "Cuadrado azul con la letra blanca P sobre un símbolo de coche sobre una línea", it: "Quadrato blu con la lettera bianca P sopra un simbolo di automobile su una linea" },
  "330-1": { de: "Blaues Quadrat mit weißem Brücken-/Straßensymbol", en: "Blue square with a white bridge/road symbol", uk: "Синій квадрат з білим символом мосту/дороги", pl: "Niebieski kwadrat z białym symbolem mostu/drogi", ar: "مربع أزرق برمز جسر/طريق أبيض", zh: "蓝色正方形,内有白色桥梁/道路符号", hi: "नीला वर्ग जिसमें सफेद पुल/सड़क प्रतीक है", tr: "Mavi kare, içinde beyaz köprü/yol simgesi", fr: "Carré bleu avec un symbole blanc de pont/route", ru: "Синий квадрат с белым символом моста/дороги", es: "Cuadrado azul con un símbolo blanco de puente/carretera", it: "Quadrato blu con un simbolo bianco di ponte/strada" },
  "330-2": { de: "Blaues Quadrat mit weißem Brücken-/Straßensymbol, von rotem Diagonalstrich durchgestrichen", en: "Blue square with a white bridge/road symbol, crossed out by a red diagonal line", uk: "Синій квадрат з білим символом мосту/дороги, перекреслений червоною діагональною лінією", pl: "Niebieski kwadrat z białym symbolem mostu/drogi, przekreślony czerwoną ukośną linią", ar: "مربع أزرق برمز جسر/طريق أبيض، مشطوب بخط قطري أحمر", zh: "蓝色正方形,内有白色桥梁/道路符号,被红色斜线划掉", hi: "नीला वर्ग जिसमें सफेद पुल/सड़क प्रतीक है, लाल विकर्ण रेखा से काटा गया", tr: "Mavi kare, içinde beyaz köprü/yol simgesi, kırmızı çapraz çizgiyle üzeri çizilmiş", fr: "Carré bleu avec un symbole blanc de pont/route, barré par une ligne diagonale rouge", ru: "Синий квадрат с белым символом моста/дороги, перечёркнутый красной диагональной линией", es: "Cuadrado azul con un símbolo blanco de puente/carretera, tachado por una línea diagonal roja", it: "Quadrato blu con un simbolo bianco di ponte/strada, barrato da una linea diagonale rossa" },
  "350": { de: "Blaues Quadrat mit weißem Dreieck und schwarzer Fußgängerfigur", en: "Blue square with a white triangle and a black pedestrian figure", uk: "Синій квадрат з білим трикутником та чорною фігурою пішохода", pl: "Niebieski kwadrat z białym trójkątem i czarną postacią pieszego", ar: "مربع أزرق بمثلث أبيض وشكل أسود لمشاة", zh: "蓝色正方形,内有白色三角形和黑色行人人形", hi: "नीला वर्ग जिसमें सफेद त्रिकोण और काली पैदल यात्री आकृति है", tr: "Mavi kare, içinde beyaz üçgen ve siyah yaya figürü", fr: "Carré bleu avec un triangle blanc et une silhouette noire de piéton", ru: "Синий квадрат с белым треугольником и чёрной фигурой пешехода", es: "Cuadrado azul con un triángulo blanco y una figura negra de peatón", it: "Quadrato blu con un triangolo bianco e una figura nera di pedone" },
  "720": { de: "Schwarze quadratische Tafel mit grünem, nach rechts zeigendem Pfeil", en: "Black square plate with a green arrow pointing right", uk: "Чорна квадратна табличка із зеленою стрілкою, що вказує праворуч", pl: "Czarna kwadratowa tablica z zieloną strzałką skierowaną w prawo", ar: "لوحة مربعة سوداء بسهم أخضر يشير إلى اليمين", zh: "黑色方形牌,内有指向右方的绿色箭头", hi: "काली वर्गाकार पट्टिका जिसमें दाईं ओर इशारा करता हरा तीर है", tr: "Siyah kare levha, içinde sağa dönük yeşil ok", fr: "Plaque carrée noire avec une flèche verte pointant vers la droite", ru: "Чёрная квадратная табличка с зелёной стрелкой, указывающей направо", es: "Placa cuadrada negra con una flecha verde apuntando hacia la derecha", it: "Targa quadrata nera con una freccia verde rivolta verso destra" },
  "zusatz": { de: "Weißes Rechteck mit schwarzem Rand und zwei waagerechten Linien (Zusatztafel)", en: "White rectangle with a black border and two horizontal lines (a supplementary plate)", uk: "Білий прямокутник з чорною облямівкою та двома горизонтальними лініями (додаткова табличка)", pl: "Biały prostokąt z czarną obwódką i dwiema poziomymi liniami (tabliczka dodatkowa)", ar: "مستطيل أبيض بحافة سوداء وخطين أفقيين (لوحة إضافية)", zh: "白色矩形,黑边,内有两条横线(附加标志牌)", hi: "काली किनारी वाला सफेद आयत जिसमें दो क्षैतिज रेखाएँ हैं (एक अतिरिक्त पट्टिका)", tr: "Siyah kenarlıklı beyaz dikdörtgen, içinde iki yatay çizgi (ek levha)", fr: "Rectangle blanc avec un bord noir et deux lignes horizontales (panneau additionnel)", ru: "Белый прямоугольник с чёрной каймой и двумя горизонтальными линиями (дополнительная табличка)", es: "Rectángulo blanco con un borde negro y dos líneas horizontales (placa complementaria)", it: "Rettangolo bianco con un bordo nero e due linee orizzontali (pannello integrativo)" },
};

// Diagram alt text: "plain" describes only the neutral scene (matches what's
// shown before the answer is revealed); "answer" adds who has priority
// (matches what's shown after reveal) - kept in sync with the visual so a
// screen-reader user gets exactly as much information as a sighted one, no
// more, no less, at each stage.
const DIAGRAM_ALT = {
  "vorfahrt-01": {
    plain: { de: "Kreuzung ohne Ampel und ohne Schilder. Ihr Auto kommt von unten, ein anderes Fahrzeug kommt von rechts.", en: "Intersection with no traffic light and no signs. Your car approaches from the bottom, another vehicle from the right.", uk: "Перехрестя без світлофора і без знаків. Ваш автомобіль наближається знизу, інший транспортний засіб — справа.", pl: "Skrzyżowanie bez sygnalizacji świetlnej i bez znaków. Twój samochód nadjeżdża z dołu, inny pojazd z prawej strony.", ar: "تقاطع بدون إشارة ضوئية وبدون لافتات. سيارتك قادمة من الأسفل، ومركبة أخرى قادمة من اليمين.", zh: "没有红绿灯也没有标志的十字路口。您的车从下方驶来,另一辆车从右侧驶来。", hi: "बिना ट्रैफिक लाइट और बिना किसी संकेत चिह्न वाला चौराहा। आपकी कार नीचे से आ रही है, एक अन्य वाहन दाईं ओर से आ रहा है।", tr: "Trafik ışığı ve tabelası olmayan bir kavşak. Sizin aracınız aşağıdan, başka bir araç ise sağdan yaklaşıyor.", fr: "Intersection sans feu de signalisation ni panneaux. Votre voiture arrive du bas, un autre véhicule arrive de la droite.", ru: "Перекрёсток без светофора и без знаков. Ваш автомобиль приближается снизу, другой автомобиль — справа.", es: "Intersección sin semáforo y sin señales. Su coche se acerca desde abajo, otro vehículo desde la derecha.", it: "Incrocio senza semaforo e senza segnali. La vostra auto arriva dal basso, un altro veicolo arriva da destra." },
    answer: { de: "Das Fahrzeug von rechts hat Vorfahrt, Sie müssen warten.", en: "The vehicle from the right has priority, you must yield.", uk: "Транспортний засіб справа має перевагу, ви повинні пропустити.", pl: "Pojazd z prawej strony ma pierwszeństwo, musisz ustąpić.", ar: "المركبة القادمة من اليمين لها الأولوية، وعليك الانتظار.", zh: "从右侧驶来的车辆拥有优先权,您必须让行。", hi: "दाईं ओर से आ रहे वाहन को प्राथमिकता है, आपको रुकना होगा।", tr: "Sağdan gelen araç önceliklidir, siz yol vermelisiniz.", fr: "Le véhicule venant de droite est prioritaire, vous devez céder le passage.", ru: "Автомобиль справа имеет преимущество, вы должны уступить дорогу.", es: "El vehículo que viene de la derecha tiene prioridad, usted debe ceder el paso.", it: "Il veicolo proveniente da destra ha la precedenza, dovete dare la precedenza." },
  },
  "vorfahrt-07": {
    plain: { de: "Kreuzung: Ihr Auto will links abbiegen, ein entgegenkommendes Fahrzeug fährt geradeaus.", en: "Intersection: your car wants to turn left, an oncoming vehicle is going straight.", uk: "Перехрестя: ваш автомобіль хоче повернути ліворуч, зустрічний транспортний засіб їде прямо.", pl: "Skrzyżowanie: twój samochód chce skręcić w lewo, nadjeżdżający z naprzeciwka pojazd jedzie na wprost.", ar: "تقاطع: سيارتك تريد الانعطاف يسارًا، ومركبة قادمة من الاتجاه المعاكس تسير مباشرة.", zh: "十字路口:您的车想左转,对向来车直行。", hi: "चौराहा: आपकी कार बाएं मुड़ना चाहती है, सामने से आ रहा वाहन सीधा जा रहा है।", tr: "Kavşak: aracınız sola dönmek istiyor, karşıdan gelen araç düz gidiyor.", fr: "Intersection : votre voiture veut tourner à gauche, un véhicule venant en sens inverse roule tout droit.", ru: "Перекрёсток: ваш автомобиль хочет повернуть налево, встречный автомобиль едет прямо.", es: "Intersección: su coche quiere girar a la izquierda, un vehículo que viene de frente circula recto.", it: "Incrocio: la vostra auto vuole svoltare a sinistra, un veicolo che procede in senso opposto va dritto." },
    answer: { de: "Der entgegenkommende Verkehr hat Vorfahrt, Sie müssen warten.", en: "The oncoming traffic has priority, you must yield.", uk: "Зустрічний рух має перевагу, ви повинні пропустити.", pl: "Ruch nadjeżdżający z naprzeciwka ma pierwszeństwo, musisz ustąpić.", ar: "حركة المرور القادمة من الاتجاه المعاكس لها الأولوية، وعليك الانتظار.", zh: "对向来车拥有优先权,您必须让行。", hi: "सामने से आ रहे यातायात को प्राथमिकता है, आपको रुकना होगा।", tr: "Karşıdan gelen trafik önceliklidir, siz yol vermelisiniz.", fr: "La circulation venant en sens inverse est prioritaire, vous devez céder le passage.", ru: "Встречный транспорт имеет преимущество, вы должны уступить дорогу.", es: "El tráfico en sentido contrario tiene prioridad, usted debe ceder el paso.", it: "Il traffico proveniente in senso opposto ha la precedenza, dovete dare la precedenza." },
  },
  "vorfahrt-09": {
    plain: { de: "Kreuzung: Ihr Auto kommt von unten, eine Straßenbahn kommt von rechts aus einer Nebenstraße.", en: "Intersection: your car approaches from the bottom, a tram approaches from a side street on the right.", uk: "Перехрестя: ваш автомобіль наближається знизу, трамвай наближається з бічної вулиці справа.", pl: "Skrzyżowanie: twój samochód nadjeżdża z dołu, tramwaj nadjeżdża z bocznej ulicy z prawej strony.", ar: "تقاطع: سيارتك قادمة من الأسفل، وترام قادم من شارع جانبي على اليمين.", zh: "十字路口:您的车从下方驶来,一辆有轨电车从右侧的支路驶来。", hi: "चौराहा: आपकी कार नीचे से आ रही है, एक ट्राम दाईं ओर की एक सड़क से आ रही है।", tr: "Kavşak: aracınız aşağıdan yaklaşıyor, bir tramvay sağdaki yan sokaktan geliyor.", fr: "Intersection : votre voiture arrive du bas, un tramway arrive de la droite depuis une rue latérale.", ru: "Перекрёсток: ваш автомобиль приближается снизу, трамвай приближается справа с боковой улицы.", es: "Intersección: su coche se acerca desde abajo, un tranvía se acerca desde la derecha por una calle lateral.", it: "Incrocio: la vostra auto arriva dal basso, un tram arriva da destra da una strada laterale." },
    answer: { de: "Die Straßenbahn hat Vorfahrt, Sie müssen warten.", en: "The tram has priority, you must yield.", uk: "Трамвай має перевагу, ви повинні пропустити.", pl: "Tramwaj ma pierwszeństwo, musisz ustąpić.", ar: "الترام له الأولوية، وعليك الانتظار.", zh: "有轨电车拥有优先权,您必须让行。", hi: "ट्राम को प्राथमिकता है, आपको रुकना होगा।", tr: "Tramvay önceliklidir, siz yol vermelisiniz.", fr: "Le tramway est prioritaire, vous devez céder le passage.", ru: "Трамвай имеет преимущество, вы должны уступить дорогу.", es: "El tranvía tiene prioridad, usted debe ceder el paso.", it: "Il tram ha la precedenza, dovete dare la precedenza." },
  },
  "vorfahrt-13": {
    plain: { de: "Kreuzung mit Ampel. Ein Polizist steht in der Mitte und hebt den Arm.", en: "Intersection with a traffic light. A police officer stands in the middle with a raised arm.", uk: "Перехрестя зі світлофором. Посередині стоїть поліцейський із піднятою рукою.", pl: "Skrzyżowanie z sygnalizacją świetlną. Policjant stoi na środku z uniesioną ręką.", ar: "تقاطع بإشارة ضوئية. شرطي يقف في المنتصف ويرفع ذراعه.", zh: "有红绿灯的十字路口。一名警察站在中间,举起一只手臂。", hi: "ट्रैफिक लाइट वाला चौराहा। एक पुलिसकर्मी बीच में खड़ा है और अपनी बांह उठाए हुए है।", tr: "Trafik ışıklı bir kavşak. Bir polis memuru ortada durmuş, kolunu kaldırmış.", fr: "Intersection avec feu de signalisation. Un policier se tient au milieu, un bras levé.", ru: "Перекрёсток со светофором. Посреди перекрёстка стоит полицейский с поднятой рукой.", es: "Intersección con semáforo. Un policía está de pie en el medio con un brazo levantado.", it: "Incrocio con semaforo. Un agente di polizia si trova al centro con un braccio alzato." },
    answer: { de: "Die Zeichen des Polizisten gelten, die Ampel wird in diesem Fall ignoriert.", en: "The officer's signals apply; the traffic light is overridden in this case.", uk: "Діють сигнали поліцейського, світлофор у цьому випадку не враховується.", pl: "Obowiązują sygnały policjanta, sygnalizacja świetlna jest w tym przypadku pomijana.", ar: "تُطبَّق إشارات الشرطي، ويتم تجاهل الإشارة الضوئية في هذه الحالة.", zh: "警察的手势优先,此时红绿灯的指示被忽略。", hi: "पुलिसकर्मी के संकेत लागू होते हैं; इस स्थिति में ट्रैफिक लाइट को अनदेखा किया जाता है।", tr: "Polis memurunun işaretleri geçerlidir; bu durumda trafik ışığı devre dışı kalır.", fr: "Les signaux du policier priment, le feu de signalisation est ignoré dans ce cas.", ru: "Действуют сигналы полицейского, в этом случае сигналы светофора не учитываются.", es: "Las señales del policía prevalecen, el semáforo se ignora en este caso.", it: "I segnali dell'agente prevalgono, in questo caso il semaforo viene ignorato." },
  },
  "vorfahrt-17": {
    plain: { de: "Straße mit Radweg. Ihr Auto biegt rechts ab, ein Radfahrer fährt auf dem Radweg geradeaus.", en: "Road with a cycle lane. Your car is turning right, a cyclist is going straight in the cycle lane.", uk: "Дорога з велосипедною доріжкою. Ваш автомобіль повертає праворуч, велосипедист їде прямо велосипедною доріжкою.", pl: "Droga ze ścieżką rowerową. Twój samochód skręca w prawo, rowerzysta jedzie na wprost ścieżką rowerową.", ar: "طريق بمسار للدراجات الهوائية. سيارتك تنعطف يمينًا، ودراجة هوائية تسير مباشرة في مسار الدراجات.", zh: "有自行车道的道路。您的车正在右转,一名骑车人在自行车道上直行。", hi: "साइकिल लेन वाली सड़क। आपकी कार दाएं मुड़ रही है, एक साइकिल चालक साइकिल लेन में सीधा जा रहा है।", tr: "Bisiklet yolu olan bir yol. Aracınız sağa dönüyor, bir bisikletli bisiklet yolunda düz gidiyor.", fr: "Route avec piste cyclable. Votre voiture tourne à droite, un cycliste roule tout droit sur la piste cyclable.", ru: "Дорога с велодорожкой. Ваш автомобиль поворачивает направо, велосипедист едет прямо по велодорожке.", es: "Carretera con carril bici. Su coche gira a la derecha, un ciclista circula recto por el carril bici.", it: "Strada con pista ciclabile. La vostra auto svolta a destra, un ciclista procede dritto sulla pista ciclabile." },
    answer: { de: "Der Radfahrer hat Vorfahrt, Sie müssen warten.", en: "The cyclist has priority, you must yield.", uk: "Велосипедист має перевагу, ви повинні пропустити.", pl: "Rowerzysta ma pierwszeństwo, musisz ustąpić.", ar: "الدراجة الهوائية لها الأولوية، وعليك الانتظار.", zh: "骑车人拥有优先权,您必须让行。", hi: "साइकिल चालक को प्राथमिकता है, आपको रुकना होगा।", tr: "Bisikletli önceliklidir, siz yol vermelisiniz.", fr: "Le cycliste est prioritaire, vous devez céder le passage.", ru: "Велосипедист имеет преимущество, вы должны уступить дорогу.", es: "El ciclista tiene prioridad, usted debe ceder el paso.", it: "Il ciclista ha la precedenza, dovete dare la precedenza." },
  },
  "vorfahrt-19": {
    plain: { de: "Straße mit zwei Fahrspuren. Ein Einsatzfahrzeug mit Blaulicht nähert sich von hinten.", en: "Road with two lanes. An emergency vehicle with blue lights approaches from behind.", uk: "Дорога з двома смугами руху. Спецавтомобіль із синім проблисковим маячком наближається ззаду.", pl: "Droga z dwoma pasami ruchu. Pojazd uprzywilejowany z niebieskim światłem zbliża się od tyłu.", ar: "طريق بمسارين. مركبة طوارئ بأضواء زرقاء تقترب من الخلف.", zh: "有两条车道的道路。一辆闪着蓝灯的紧急车辆从后方驶来。", hi: "दो लेन वाली सड़क। नीली बत्ती वाला एक आपातकालीन वाहन पीछे से आ रहा है।", tr: "İki şeritli bir yol. Mavi ışıklı bir acil durum aracı arkadan yaklaşıyor.", fr: "Route à deux voies. Un véhicule d'intervention avec gyrophare bleu approche par l'arrière.", ru: "Дорога с двумя полосами. Сзади приближается автомобиль экстренной службы с синим проблесковым маячком.", es: "Carretera con dos carriles. Un vehículo de emergencia con luces azules se acerca por detrás.", it: "Strada a due corsie. Un veicolo di soccorso con lampeggianti blu si avvicina da dietro." },
    answer: { de: "Das Einsatzfahrzeug hat immer Vorrang, unabhängig von der sonstigen Vorfahrt.", en: "The emergency vehicle always has priority, regardless of the usual right of way.", uk: "Спецавтомобіль завжди має перевагу, незалежно від звичайних правил проїзду.", pl: "Pojazd uprzywilejowany zawsze ma pierwszeństwo, niezależnie od zwykłych zasad pierwszeństwa.", ar: "مركبة الطوارئ لها الأولوية دائمًا، بغض النظر عن قواعد الأولوية المعتادة.", zh: "紧急车辆始终拥有优先权,无论通常的路权规则如何。", hi: "सामान्य प्राथमिकता नियमों की परवाह किए बिना, आपातकालीन वाहन को हमेशा प्राथमिकता होती है।", tr: "Acil durum aracı, olağan geçiş hakkından bağımsız olarak her zaman önceliklidir.", fr: "Le véhicule d'intervention est toujours prioritaire, indépendamment des règles de priorité habituelles.", ru: "Автомобиль экстренной службы всегда имеет преимущество, независимо от обычных правил проезда.", es: "El vehículo de emergencia siempre tiene prioridad, independientemente de las reglas de prioridad habituales.", it: "Il veicolo di soccorso ha sempre la precedenza, indipendentemente dalle normali regole di precedenza." },
  },
  "vorfahrt-21": {
    plain: { de: "Straße kreuzt Bahngleise ohne Schranke. Ein Zug nähert sich.", en: "Road crossing railway tracks with no barrier. A train is approaching.", uk: "Дорога перетинає залізничні колії без шлагбаума. Наближається потяг.", pl: "Droga krzyżuje się z torami kolejowymi bez szlabanu. Zbliża się pociąg.", ar: "طريق يقطع سكة حديد بدون حاجز. قطار يقترب.", zh: "道路与铁轨交叉,没有栏杆。一列火车正在驶近。", hi: "बिना बैरियर वाला रेलवे ट्रैक पार करता एक सड़क मार्ग। एक ट्रेन आ रही है।", tr: "Bariyeri olmayan bir demiryolu geçidi. Bir tren yaklaşıyor.", fr: "La route croise des voies ferrées sans barrière. Un train approche.", ru: "Дорога пересекает железнодорожные пути без шлагбаума. Приближается поезд.", es: "La carretera cruza vías de tren sin barrera. Se acerca un tren.", it: "La strada attraversa i binari ferroviari senza barriera. Si avvicina un treno." },
    answer: { de: "Der Zug hat immer Vorrang, auch wenn Ihre Straße sonst eine Vorfahrtstraße ist.", en: "The train always has priority, even though your road is otherwise a priority road.", uk: "Потяг завжди має перевагу, навіть якщо ваша дорога зазвичай є дорогою з перевагою проїзду.", pl: "Pociąg zawsze ma pierwszeństwo, nawet jeśli twoja droga jest zwykle drogą z pierwszeństwem przejazdu.", ar: "القطار له الأولوية دائمًا، حتى لو كان طريقك عادة طريق أولوية.", zh: "即使您的道路通常是优先道路,火车也始终拥有优先权。", hi: "भले ही आपकी सड़क अन्यथा एक प्राथमिकता वाली सड़क हो, ट्रेन को हमेशा प्राथमिकता होती है।", tr: "Yolunuz normalde öncelikli bir yol olsa bile, tren her zaman önceliklidir.", fr: "Le train est toujours prioritaire, même si votre route est par ailleurs une route prioritaire.", ru: "Поезд всегда имеет преимущество, даже если ваша дорога в остальном является дорогой с преимущественным правом проезда.", es: "El tren siempre tiene prioridad, aunque su carretera sea normalmente una carretera prioritaria.", it: "Il treno ha sempre la precedenza, anche se la vostra strada è normalmente una strada con diritto di precedenza." },
  },
  // DN-27 pilot round (2026-08-07) - see DIAGRAM_IDS above.
  // Extended to all 12 locales 2026-08-08 (follow-up to DN-28: the
  // fixed-exam-material-alt-text precedent was revisited and this
  // block, plus SIGN_ALT above, now carry every locale the app's
  // question content already does.
  "gefahr-01": {
    plain: { de: "Zwei Fahrspuren nebeneinander, trocken und nass, mit einem Auto am Start jeder Spur.", en: "Two lanes side by side, one dry and one wet, with a car at the start of each.", uk: "Дві смуги руху поруч, одна суха, одна мокра, з автомобілем на початку кожної смуги.", pl: "Dwa pasy ruchu obok siebie, jeden suchy i jeden mokry, z samochodem na początku każdego pasa.", ar: "مساران متجاوران، أحدهما جاف والآخر مبلل، مع سيارة عند بداية كل مسار.", zh: "两条并排的车道,一条干燥、一条潮湿,每条车道起点各有一辆车。", hi: "एक साथ दो लेन, एक सूखी और एक गीली, हर एक की शुरुआत में एक कार।", tr: "Yan yana iki şerit, biri kuru biri ıslak, her birinin başında bir araba.", fr: "Deux voies côte à côte, une sèche et une mouillée, avec une voiture au départ de chaque voie.", ru: "Две полосы рядом друг с другом, сухая и мокрая, с автомобилем в начале каждой полосы.", es: "Dos carriles uno al lado del otro, uno seco y uno mojado, con un coche al inicio de cada carril.", it: "Due corsie affiancate, una asciutta e una bagnata, con un'auto all'inizio di ciascuna corsia." },
    answer: { de: "Trockene Spur mit kurzem Bremsweg (grün), nasse Spur mit deutlich längerem Bremsweg (gelb).", en: "Dry lane shows a short braking mark (green), wet lane shows a much longer one (amber).", uk: "Суха смуга показує короткий гальмівний слід (зелений), мокра смуга показує значно довший (жовтий).", pl: "Suchy pas pokazuje krótki ślad hamowania (zielony), mokry pas pokazuje wyraźnie dłuższy (żółty).", ar: "المسار الجاف يظهر أثر فرملة قصيرًا (أخضر)، والمسار المبلل يظهر أثرًا أطول بكثير (أصفر).", zh: "干燥车道显示较短的制动痕迹(绿色),潮湿车道显示明显更长的制动痕迹(琥珀色)。", hi: "सूखी लेन में छोटा ब्रेकिंग निशान (हरा) दिखता है, गीली लेन में कहीं ज्यादा लंबा निशान (अंबर) दिखता है।", tr: "Kuru şeritte kısa bir fren izi (yeşil), ıslak şeritte çok daha uzun bir fren izi (kehribar) gösteriliyor.", fr: "La voie sèche affiche une trace de freinage courte (vert), la voie mouillée une trace nettement plus longue (jaune/orange).", ru: "Сухая полоса показывает короткий тормозной след (зелёный), мокрая полоса — значительно более длинный (жёлтый).", es: "El carril seco muestra una marca de frenado corta (verde), el carril mojado una marca mucho más larga (ámbar).", it: "La corsia asciutta mostra una traccia di frenata corta (verde), quella bagnata una traccia molto più lunga (giallo/ambra)." },
  },
  "gefahr-02": {
    plain: { de: "Seitenansicht eines Autoreifens über einer Wasserschicht auf der Fahrbahn.", en: "Side view of a car tire above a layer of water on the road.", uk: "Вигляд збоку на автомобільну шину над шаром води на дорозі.", pl: "Widok z boku na oponę samochodową nad warstwą wody na jezdni.", ar: "منظر جانبي لإطار سيارة فوق طبقة من الماء على الطريق.", zh: "侧视图显示汽车轮胎悬浮在路面的一层水膜之上。", hi: "सड़क पर पानी की परत के ऊपर एक कार के टायर का साइड व्यू।", tr: "Yol üzerindeki bir su tabakasının üzerinde duran bir araba lastiğinin yandan görünümü.", fr: "Vue de côté d'un pneu de voiture au-dessus d'une couche d'eau sur la chaussée.", ru: "Вид сбоку на автомобильную шину над слоем воды на дороге.", es: "Vista lateral de un neumático de coche sobre una capa de agua en la carretera.", it: "Vista laterale di un pneumatico d'auto sopra uno strato d'acqua sulla strada." },
    answer: { de: "Der Reifen ist vom Wasserfilm angehoben und hat keinen Fahrbahnkontakt mehr.", en: "The tire is lifted by the water film and has lost contact with the road.", uk: "Шина піднята водяною плівкою і втратила контакт з дорогою.", pl: "Opona jest uniesiona przez warstwę wody i straciła kontakt z nawierzchnią.", ar: "الإطار مرفوع بواسطة طبقة الماء وفقد ملامسته للطريق.", zh: "轮胎被水膜托起,已与路面失去接触。", hi: "टायर पानी की परत से ऊपर उठा हुआ है और सड़क से उसका संपर्क टूट गया है।", tr: "Lastik su tabakası tarafından kaldırılmış ve yol ile teması kesilmiştir.", fr: "Le pneu est soulevé par le film d'eau et n'a plus de contact avec la chaussée.", ru: "Шина приподнята водяной плёнкой и больше не касается дороги.", es: "El neumático está levantado por la capa de agua y ha perdido el contacto con la carretera.", it: "Il pneumatico è sollevato dal velo d'acqua e ha perso il contatto con la strada." },
  },
  "gefahr-04": {
    plain: { de: "Straße mit einer Brücke links und einem schattenspendenden Baum rechts.", en: "Road with a bridge on the left and a shade-casting tree on the right.", uk: "Дорога з мостом ліворуч і деревом, що відкидає тінь, праворуч.", pl: "Droga z mostem po lewej stronie i drzewem rzucającym cień po prawej stronie.", ar: "طريق بجسر على اليسار وشجرة تُلقي ظلًا على اليمين.", zh: "道路左侧有一座桥,右侧有一棵投下阴影的树。", hi: "सड़क के बाईं ओर एक पुल है और दाईं ओर छाया देने वाला एक पेड़ है।", tr: "Solda bir köprü, sağda gölge veren bir ağaç bulunan bir yol.", fr: "Route avec un pont à gauche et un arbre projetant de l'ombre à droite.", ru: "Дорога с мостом слева и деревом, отбрасывающим тень, справа.", es: "Carretera con un puente a la izquierda y un árbol que proyecta sombra a la derecha.", it: "Strada con un ponte a sinistra e un albero che proietta ombra a destra." },
    answer: { de: "Eisflächen sind unter der Brücke und im Schatten des Baumes markiert.", en: "Icy patches are marked under the bridge and in the tree's shade.", uk: "Крижані ділянки позначені під мостом і в тіні дерева.", pl: "Oblodzone miejsca są zaznaczone pod mostem i w cieniu drzewa.", ar: "البقع الجليدية موضحة تحت الجسر وفي ظل الشجرة.", zh: "桥下和树荫处标出了结冰路面。", hi: "पुल के नीचे और पेड़ की छाया में बर्फीले हिस्सों को चिह्नित किया गया है।", tr: "Köprünün altında ve ağacın gölgesinde buzlu bölgeler işaretlenmiştir.", fr: "Des plaques de glace sont marquées sous le pont et dans l'ombre de l'arbre.", ru: "Обледенелые участки отмечены под мостом и в тени дерева.", es: "Se marcan placas de hielo bajo el puente y en la sombra del árbol.", it: "Sono segnalate lastre di ghiaccio sotto il ponte e nell'ombra dell'albero." },
  },
  "gefahr-05": {
    plain: { de: "Ein Auto auf der Straße, noch ohne markierten Reaktions- oder Bremsweg.", en: "A car on the road, with no reaction or braking distance marked yet.", uk: "Автомобіль на дорозі, ще без позначеної дистанції реакції чи гальмування.", pl: "Samochód na drodze, bez jeszcze zaznaczonej drogi reakcji lub hamowania.", ar: "سيارة على الطريق، دون تحديد مسافة رد الفعل أو الفرملة بعد.", zh: "道路上有一辆车,尚未标出反应距离或制动距离。", hi: "सड़क पर एक कार, अभी तक कोई प्रतिक्रिया या ब्रेकिंग दूरी चिह्नित नहीं है।", tr: "Yolda bir araba, henüz tepki veya fren mesafesi işaretlenmemiş.", fr: "Une voiture sur la route, sans distance de réaction ni de freinage encore marquée.", ru: "Автомобиль на дороге, без обозначенного пока пути реакции или торможения.", es: "Un coche en la carretera, sin distancia de reacción ni de frenado marcada todavía.", it: "Un'auto sulla strada, senza ancora alcuna distanza di reazione o di frenata segnata." },
    answer: { de: "Gestrichelter Reaktionsweg-Abschnitt gefolgt von einem markierten Bremsweg-Abschnitt.", en: "A dashed reaction-distance segment followed by a marked braking-distance segment.", uk: "Пунктирна ділянка дистанції реакції, за якою йде позначена ділянка гальмівного шляху.", pl: "Przerywany odcinek drogi reakcji, po którym następuje zaznaczony odcinek drogi hamowania.", ar: "قطعة متقطعة تمثل مسافة رد الفعل تليها قطعة محددة تمثل مسافة الفرملة.", zh: "一段虚线表示反应距离,随后是一段标出的制动距离。", hi: "एक धराशायी (डैश्ड) प्रतिक्रिया-दूरी खंड, उसके बाद एक चिह्नित ब्रेकिंग-दूरी खंड।", tr: "Kesikli çizgiyle gösterilen bir tepki mesafesi bölümünü, işaretli bir fren mesafesi bölümü izliyor.", fr: "Un segment en pointillés pour la distance de réaction suivi d'un segment marqué pour la distance de freinage.", ru: "Пунктирный участок пути реакции, за которым следует обозначенный участок тормозного пути.", es: "Un segmento discontinuo de distancia de reacción seguido de un segmento marcado de distancia de frenado.", it: "Un tratto tratteggiato per la distanza di reazione seguito da un tratto segnato per la distanza di frenata." },
  },
  "gefahr-06": {
    plain: { de: "Zwei Autos hintereinander auf einer Fahrspur mit Abstand dazwischen.", en: "Two cars one behind the other in a lane, with a gap between them.", uk: "Два автомобілі один за одним на одній смузі з проміжком між ними.", pl: "Dwa samochody jeden za drugim na jednym pasie, z odstępem między nimi.", ar: "سيارتان متتاليتان في نفس المسار مع مسافة بينهما.", zh: "同一车道上前后两辆车,之间有一段间距。", hi: "एक लेन में एक-दूसरे के पीछे दो कारें, उनके बीच एक गैप के साथ।", tr: "Bir şeritte art arda iki araba, aralarında bir boşluk var.", fr: "Deux voitures l'une derrière l'autre sur une voie, avec un espace entre elles.", ru: "Два автомобиля друг за другом на одной полосе, с промежутком между ними.", es: "Dos coches uno detrás del otro en un carril, con un espacio entre ellos.", it: "Due auto una dietro l'altra in una corsia, con uno spazio tra loro." },
    answer: { de: "Der Abstand zwischen beiden Autos ist als 'mindestens halbe Geschwindigkeit in Metern' markiert.", en: "The gap between the two cars is marked as 'at least half the speed in metres'.", uk: "Відстань між обома автомобілями позначена як 'щонайменше половина швидкості в метрах'.", pl: "Odstęp między obydwoma samochodami jest oznaczony jako 'co najmniej połowa prędkości w metrach'.", ar: "المسافة بين السيارتين موضحة على أنها 'نصف السرعة بالمتر على الأقل'.", zh: "两车之间的间距被标注为“至少为车速数值一半的米数”。", hi: "दोनों कारों के बीच के गैप को 'मीटर में कम से कम आधी गति' के रूप में चिह्नित किया गया है।", tr: "İki araba arasındaki boşluk 'metre cinsinden en az hızın yarısı' olarak işaretlenmiştir.", fr: "L'espace entre les deux voitures est indiqué comme 'au moins la moitié de la vitesse en mètres'.", ru: "Промежуток между двумя автомобилями обозначен как 'не менее половины скорости в метрах'.", es: "El espacio entre los dos coches está marcado como 'al menos la mitad de la velocidad en metros'.", it: "Lo spazio tra le due auto è indicato come 'almeno metà della velocità in metri'." },
  },
  "gefahr-07": {
    plain: { de: "Zwei Autos hintereinander mit einem markierten Fixpunkt auf der Fahrbahn.", en: "Two cars one behind the other with a marked fixed point on the road.", uk: "Два автомобілі один за одним з позначеною фіксованою точкою на дорозі.", pl: "Dwa samochody jeden za drugim z zaznaczonym stałym punktem na jezdni.", ar: "سيارتان متتاليتان مع نقطة ثابتة محددة على الطريق.", zh: "前后两辆车,道路上标出一个固定参照点。", hi: "एक-दूसरे के पीछे दो कारें, सड़क पर एक चिह्नित स्थिर बिंदु के साथ।", tr: "Art arda iki araba, yolda işaretlenmiş sabit bir nokta ile.", fr: "Deux voitures l'une derrière l'autre avec un point de repère marqué sur la chaussée.", ru: "Два автомобиля друг за другом с отмеченной на дороге неподвижной точкой отсчёта.", es: "Dos coches uno detrás del otro con un punto fijo marcado en la carretera.", it: "Due auto una dietro l'altra con un punto fisso segnato sulla strada." },
    answer: { de: "Hinweis, dass mindestens drei Sekunden bis zum Fixpunkt vergehen sollten.", en: "Note that at least three seconds should pass before reaching the fixed point.", uk: "Вказівка, що до фіксованої точки повинно пройти щонайменше три секунди.", pl: "Wskazówka, że do stałego punktu powinny upłynąć co najmniej trzy sekundy.", ar: "إشارة إلى ضرورة مرور ثلاث ثوانٍ على الأقل قبل الوصول إلى النقطة الثابتة.", zh: "提示:到达该固定点前应至少间隔三秒。", hi: "नोट: निश्चित बिंदु तक पहुंचने से पहले कम से कम तीन सेकंड बीतने चाहिए।", tr: "Not: sabit noktaya ulaşmadan önce en az üç saniye geçmelidir.", fr: "Indication qu'au moins trois secondes doivent s'écouler avant d'atteindre le point de repère.", ru: "Указание, что до достижения этой точки должно пройти не менее трёх секунд.", es: "Indicación de que deben transcurrir al menos tres segundos antes de llegar al punto fijo.", it: "Indicazione che devono trascorrere almeno tre secondi prima di raggiungere il punto fisso." },
  },
  "gefahr-08": {
    plain: { de: "Ein Ball rollt vom Straßenrand auf die Fahrbahn, ein Auto nähert sich.", en: "A ball rolls from the roadside onto the road as a car approaches.", uk: "М'яч котиться з узбіччя на проїжджу частину, наближається автомобіль.", pl: "Piłka toczy się z pobocza na jezdnię, zbliża się samochód.", ar: "كرة تتدحرج من جانب الطريق إلى الطريق بينما تقترب سيارة.", zh: "一个球从路边滚到路面上,一辆车正驶近。", hi: "एक कार के आते समय एक गेंद सड़क किनारे से लुढ़ककर सड़क पर आ जाती है।", tr: "Bir top yol kenarından yola doğru yuvarlanırken bir araba yaklaşıyor.", fr: "Un ballon roule du bord de la route vers la chaussée, une voiture approche.", ru: "Мяч катится с обочины на проезжую часть, приближается автомобиль.", es: "Una pelota rueda desde el borde de la carretera hacia la calzada, un coche se acerca.", it: "Una palla rotola dal bordo della strada verso la carreggiata, un'auto si avvicina." },
    answer: { de: "Ein Kind ist angedeutet, das dem Ball folgen könnte, mit Hinweis zum Tempo verringern.", en: "A child that might follow the ball is indicated, with a note to slow down.", uk: "Позначено дитину, яка може побігти за м'ячем, з вказівкою знизити швидкість.", pl: "Zaznaczone jest dziecko, które może pobiec za piłką, ze wskazówką o zmniejszeniu prędkości.", ar: "يُشار إلى طفل قد يتبع الكرة، مع ملاحظة لتقليل السرعة.", zh: "图中暗示可能有孩子追着球跑,并提示减速。", hi: "एक बच्चे का संकेत दिया गया है जो गेंद के पीछे आ सकता है, साथ में धीमा करने का नोट है।", tr: "Topun peşinden gelebilecek bir çocuğa işaret edilmiş, yavaşlama notu eklenmiş.", fr: "Un enfant susceptible de suivre le ballon est esquissé, avec une indication de ralentir.", ru: "Обозначен ребёнок, который может побежать за мячом, с указанием снизить скорость.", es: "Se indica un niño que podría seguir a la pelota, con una nota para reducir la velocidad.", it: "Viene indicato un bambino che potrebbe seguire la palla, con una nota per rallentare." },
  },
  "gefahr-09": {
    plain: { de: "Ein Bus steht an einer Haltestelle, ein Auto nähert sich auf der Fahrspur.", en: "A bus is stopped at a bus stop, with a car approaching in the lane.", uk: "Автобус стоїть на зупинці, автомобіль наближається на смузі руху.", pl: "Autobus stoi na przystanku, samochód zbliża się na pasie ruchu.", ar: "حافلة متوقفة عند محطة، وسيارة تقترب في المسار.", zh: "一辆公交车停在站台,车道上有一辆车驶近。", hi: "एक बस स्टॉप पर रुकी हुई है, लेन में एक कार आ रही है।", tr: "Bir otobüs durakta durmuş, şeritte bir araba yaklaşıyor.", fr: "Un bus est arrêté à un arrêt, une voiture approche sur la voie.", ru: "Автобус стоит на остановке, по полосе приближается автомобиль.", es: "Un autobús está parado en una parada, un coche se acerca por el carril.", it: "Un autobus è fermo a una fermata, un'auto si avvicina sulla corsia." },
    answer: { de: "Bereich vor dem Bus ist markiert, in den der Bus einfädeln darf.", en: "The area in front of the bus is marked as space the bus may pull into.", uk: "Позначена ділянка перед автобусом, куди автобус може виїхати.", pl: "Zaznaczony jest obszar przed autobusem, w który autobus może wjechać.", ar: "المنطقة أمام الحافلة موضحة كمساحة قد تدخل إليها الحافلة.", zh: "公交车前方区域被标为公交车可驶入的空间。", hi: "बस के सामने के क्षेत्र को उस स्थान के रूप में चिह्नित किया गया है जहां बस प्रवेश कर सकती है।", tr: "Otobüsün önündeki alan, otobüsün girebileceği bir boşluk olarak işaretlenmiştir.", fr: "La zone devant le bus est marquée comme l'espace dans lequel le bus peut s'insérer.", ru: "Зона перед автобусом обозначена как пространство, в которое автобус может выехать.", es: "El área frente al autobús está marcada como el espacio al que el autobús puede incorporarse.", it: "L'area davanti all'autobus è indicata come lo spazio in cui l'autobus può immettersi." },
  },
  "gefahr-10": {
    plain: { de: "Draufsicht auf eine Fahrspur mit einem Auto und einem schattierten Bereich seitlich daneben.", en: "Top-down view of a lane with a car and a shaded area beside it.", uk: "Вигляд згори на смугу руху з автомобілем і затіненою ділянкою поруч із ним.", pl: "Widok z góry na pas ruchu z samochodem i zacienionym obszarem obok niego.", ar: "منظر علوي لمسار به سيارة ومنطقة مظللة بجانبها.", zh: "俯视图显示一条车道,一辆车旁有一块阴影区域。", hi: "एक लेन का टॉप-डाउन दृश्य जिसमें एक कार और उसके बगल में एक छायांकित क्षेत्र है।", tr: "Bir arabanın ve yanındaki gölgeli bir alanın olduğu şeridin kuşbakışı görünümü.", fr: "Vue de dessus d'une voie avec une voiture et une zone ombrée à côté.", ru: "Вид сверху на полосу движения с автомобилем и затемнённой зоной рядом.", es: "Vista superior de un carril con un coche y una zona sombreada al lado.", it: "Vista dall'alto di una corsia con un'auto e una zona ombreggiata accanto." },
    answer: { de: "Ein zweites Fahrzeug ist im schattierten Bereich versteckt und für die Spiegel unsichtbar.", en: "A second vehicle is hidden in the shaded area, invisible to the mirrors.", uk: "Другий транспортний засіб схований у затіненій ділянці і невидимий у дзеркалах.", pl: "Drugi pojazd jest ukryty w zacienionym obszarze i niewidoczny w lusterkach.", ar: "مركبة ثانية مخفية في المنطقة المظللة وغير مرئية في المرايا.", zh: "阴影区域中隐藏着第二辆车,后视镜无法看到它。", hi: "छायांकित क्षेत्र में एक दूसरा वाहन छिपा है, जो मिररों (शीशों) से दिखाई नहीं देता।", tr: "Gölgeli alanda, aynalardan görünmeyen ikinci bir araç gizlenmiştir.", fr: "Un second véhicule est caché dans la zone ombrée et invisible dans les rétroviseurs.", ru: "Второй автомобиль скрыт в затемнённой зоне и невидим в зеркалах.", es: "Un segundo vehículo está oculto en la zona sombreada e invisible para los espejos.", it: "Un secondo veicolo è nascosto nella zona ombreggiata e invisibile agli specchietti." },
  },
  "gefahr-16": {
    plain: { de: "Draufsicht auf eine Reihe geparkter Autos am Straßenrand, ein Auto fährt vorbei.", en: "Top-down view of a row of parked cars at the roadside, with a car driving past.", uk: "Вигляд згори на ряд припаркованих автомобілів на узбіччі, повз проїжджає автомобіль.", pl: "Widok z góry na rząd zaparkowanych samochodów przy poboczu, samochód przejeżdża obok.", ar: "منظر علوي لصف من السيارات المتوقفة على جانب الطريق، وسيارة تمر بجانبها.", zh: "俯视图显示路边一排停放的车辆,一辆车正驶过。", hi: "सड़क किनारे खड़ी कारों की एक कतार का टॉप-डाउन दृश्य, जिसके पास से एक कार गुजर रही है।", tr: "Yol kenarında park etmiş bir sıra arabanın kuşbakışı görünümü, yanından bir araba geçiyor.", fr: "Vue de dessus d'une rangée de voitures garées au bord de la route, une voiture passe.", ru: "Вид сверху на ряд припаркованных у обочины автомобилей, мимо проезжает автомобиль.", es: "Vista superior de una fila de coches aparcados en el borde de la carretera, un coche pasa por delante.", it: "Vista dall'alto di una fila di auto parcheggiate sul bordo della strada, un'auto passa accanto." },
    answer: { de: "Eine Person ist zwischen zwei geparkten Autos verdeckt und könnte hervortreten.", en: "A person is hidden between two parked cars and could step out.", uk: "Людина схована між двома припаркованими автомобілями і може вийти на дорогу.", pl: "Osoba jest ukryta między dwoma zaparkowanymi samochodami i mogłaby wystąpić na jezdnię.", ar: "شخص مخفي بين سيارتين متوقفتين وقد يخرج فجأة.", zh: "两辆停放的车之间藏着一个人,可能会突然走出来。", hi: "दो पार्क की गई कारों के बीच एक व्यक्ति छिपा है और बाहर निकल सकता है।", tr: "Park halindeki iki araba arasında gizlenmiş bir kişi var ve dışarı çıkabilir.", fr: "Une personne est cachée entre deux voitures garées et pourrait surgir.", ru: "Между двумя припаркованными автомобилями скрыт человек, который может выйти на дорогу.", es: "Una persona está oculta entre dos coches aparcados y podría salir de repente.", it: "Una persona è nascosta tra due auto parcheggiate e potrebbe uscire improvvisamente." },
  },
  "gefahr-18": {
    plain: { de: "Zwei Fahrspuren mit unterschiedlicher Geschwindigkeit (v und doppelte Geschwindigkeit).", en: "Two lanes at different speeds (v and double v).", uk: "Дві смуги руху з різною швидкістю (v і подвійна швидкість).", pl: "Dwa pasy ruchu z różnymi prędkościami (v i podwójna prędkość).", ar: "مساران بسرعتين مختلفتين (v وضعف السرعة).", zh: "两条车道分别以不同速度行驶(v和2倍v)。", hi: "अलग-अलग गति (v और दोगुनी v) पर दो लेन।", tr: "Farklı hızlarda (v ve iki katı v) iki şerit.", fr: "Deux voies à des vitesses différentes (v et le double de v).", ru: "Две полосы с разной скоростью (v и удвоенная скорость).", es: "Dos carriles a diferentes velocidades (v y el doble de v).", it: "Due corsie a velocità diverse (v e il doppio di v)." },
    answer: { de: "Bremsweg bei doppelter Geschwindigkeit ist deutlich mehr als doppelt so lang markiert.", en: "The braking mark at double speed is shown far more than twice as long.", uk: "Гальмівний слід при подвійній швидкості позначений як значно більше ніж удвічі довший.", pl: "Ślad hamowania przy podwójnej prędkości jest zaznaczony jako wyraźnie ponad dwukrotnie dłuższy.", ar: "أثر الفرملة عند ضعف السرعة موضح بأنه أطول بكثير من الضعف.", zh: "双倍速度下的制动痕迹显示远远超过两倍长度。", hi: "दोगुनी गति पर ब्रेकिंग निशान दोगुने से कहीं अधिक लंबा दिखाया गया है।", tr: "İki kat hızdaki fren izi, iki katından çok daha uzun gösterilmiştir.", fr: "À vitesse double, la trace de freinage marquée est nettement plus que deux fois plus longue.", ru: "При удвоенной скорости обозначенный тормозной путь значительно более чем в два раза длиннее.", es: "A doble velocidad, la marca de frenado indicada es mucho más del doble de larga.", it: "Alla velocità doppia, la traccia di frenata segnata è molto più del doppio più lunga." },
  },
  "gefahr-19": {
    plain: { de: "Ein Auto fährt dicht hinter einem Lastwagen auf der Straße.", en: "A car driving close behind a truck on the road.", uk: "Автомобіль їде близько позаду вантажівки на дорозі.", pl: "Samochód jadący blisko za ciężarówką na drodze.", ar: "سيارة تسير قريبة خلف شاحنة على الطريق.", zh: "一辆车紧跟在一辆卡车后面行驶。", hi: "सड़क पर एक ट्रक के ठीक पीछे चल रही एक कार।", tr: "Yolda bir kamyonun hemen arkasından giden bir araba.", fr: "Une voiture roule de près derrière un camion sur la route.", ru: "Автомобиль едет вплотную позади грузовика на дороге.", es: "Un coche circulando muy cerca detrás de un camión en la carretera.", it: "Un'auto viaggia a distanza ravvicinata dietro un camion sulla strada." },
    answer: { de: "Gestrichelte Sichtlinie zeigt, dass die Sicht durch den Lastwagen versperrt ist; größerer Abstand hilft.", en: "A dashed sightline shows the view is blocked by the truck; more distance helps.", uk: "Пунктирна лінія огляду показує, що огляд перекритий вантажівкою; більша дистанція допомагає.", pl: "Przerywana linia widoczności pokazuje, że widok jest zasłonięty przez ciężarówkę; większy odstęp pomaga.", ar: "خط رؤية متقطع يظهر أن الرؤية محجوبة بسبب الشاحنة؛ زيادة المسافة تساعد.", zh: "虚线视线表明卡车遮挡了视野;拉大距离有助于改善视野。", hi: "एक धराशायी (डैश्ड) दृष्टि-रेखा दिखाती है कि ट्रक द्वारा नज़ारा अवरुद्ध है; अधिक दूरी बनाना मददगार है।", tr: "Kesikli görüş çizgisi, görüşün kamyon tarafından engellendiğini gösterir; daha fazla mesafe yardımcı olur.", fr: "Une ligne de visée en pointillés montre que la vue est bloquée par le camion ; une plus grande distance aide.", ru: "Пунктирная линия обзора показывает, что вид загорожен грузовиком; больший интервал помогает.", es: "Una línea de visión discontinua muestra que la vista está bloqueada por el camión; más distancia ayuda.", it: "Una linea di visuale tratteggiata mostra che la vista è bloccata dal camion; una maggiore distanza aiuta." },
  },
  "gefahr-20": {
    plain: { de: "Ein Kind steht am Fahrbahnrand, ein Auto nähert sich.", en: "A child stands at the edge of the road as a car approaches.", uk: "Дитина стоїть на краю проїжджої частини, наближається автомобіль.", pl: "Dziecko stoi przy krawędzi jezdni, zbliża się samochód.", ar: "طفل يقف عند حافة الطريق، وسيارة تقترب.", zh: "一名儿童站在路边,一辆车正驶近。", hi: "एक कार के आते समय एक बच्चा सड़क किनारे खड़ा है।", tr: "Bir araba yaklaşırken bir çocuk yolun kenarında duruyor.", fr: "Un enfant se tient au bord de la chaussée, une voiture approche.", ru: "Ребёнок стоит на краю проезжей части, приближается автомобиль.", es: "Un niño está de pie en el borde de la calzada, un coche se acerca.", it: "Un bambino si trova sul bordo della carreggiata, un'auto si avvicina." },
    answer: { de: "Der Bereich um das Kind ist als Vorsichtszone markiert, Auto ist bremsbereit.", en: "The area around the child is marked as a caution zone, car ready to brake.", uk: "Ділянка навколо дитини позначена як зона обережності, автомобіль готовий гальмувати.", pl: "Obszar wokół dziecka jest oznaczony jako strefa ostrożności, samochód gotowy do hamowania.", ar: "المنطقة حول الطفل موضحة كمنطقة حذر، والسيارة جاهزة للفرملة.", zh: "儿童周围区域被标为警戒区,车辆做好刹车准备。", hi: "बच्चे के आसपास के क्षेत्र को सावधानी क्षेत्र के रूप में चिह्नित किया गया है, कार ब्रेक लगाने के लिए तैयार है।", tr: "Çocuğun etrafındaki alan dikkat bölgesi olarak işaretlenmiş, araba fren yapmaya hazır.", fr: "La zone autour de l'enfant est marquée comme une zone de prudence, la voiture est prête à freiner.", ru: "Зона вокруг ребёнка обозначена как зона повышенного внимания, автомобиль готов к торможению.", es: "El área alrededor del niño está marcada como zona de precaución, el coche está listo para frenar.", it: "L'area intorno al bambino è indicata come zona di attenzione, l'auto è pronta a frenare." },
  },
  "gefahr-22": {
    plain: { de: "Eine Straßenbahn hält, eine Person steht in Fahrbahnnähe, ein Auto nähert sich.", en: "A tram is stopped, a person stands near the road, a car approaches.", uk: "Трамвай зупинився, людина стоїть біля дороги, наближається автомобіль.", pl: "Tramwaj stoi, osoba stoi w pobliżu jezdni, zbliża się samochód.", ar: "ترام متوقف، وشخص يقف بالقرب من الطريق، وسيارة تقترب.", zh: "一辆有轨电车停下,一人站在路边,一辆车正驶近。", hi: "एक ट्राम रुकी हुई है, एक व्यक्ति सड़क के पास खड़ा है, एक कार आ रही है।", tr: "Bir tramvay durmuş, bir kişi yolun yakınında duruyor, bir araba yaklaşıyor.", fr: "Un tramway est arrêté, une personne se tient près de la chaussée, une voiture approche.", ru: "Трамвай стоит, человек стоит вблизи проезжей части, приближается автомобиль.", es: "Un tranvía está parado, una persona está de pie cerca de la calzada, un coche se acerca.", it: "Un tram è fermo, una persona si trova vicino alla carreggiata, un'auto si avvicina." },
    answer: { de: "Die Person quert zur Haltestelle, Hinweis auf sehr langsames Fahren.", en: "The person is crossing to the stop, with a note to drive very slowly.", uk: "Людина переходить до зупинки, з вказівкою їхати дуже повільно.", pl: "Osoba przechodzi w kierunku przystanku, ze wskazówką o bardzo powolnej jeździe.", ar: "الشخص يعبر باتجاه المحطة، مع ملاحظة للقيادة ببطء شديد.", zh: "该行人正朝站台方向穿行,提示应非常缓慢地行驶。", hi: "व्यक्ति स्टॉप की ओर पार कर रहा है, साथ में बहुत धीरे चलाने का नोट है।", tr: "Kişi durağa doğru geçiyor, çok yavaş sürme notuyla birlikte.", fr: "La personne traverse vers l'arrêt, avec une indication de rouler très lentement.", ru: "Человек переходит к остановке, с указанием ехать очень медленно.", es: "La persona está cruzando hacia la parada, con una nota para conducir muy despacio.", it: "La persona sta attraversando verso la fermata, con una nota per procedere molto lentamente." },
  },
  "gefahr-23": {
    plain: { de: "Eine Fahrbahn mit verstreuten Laubblättern, ein Auto fährt darüber.", en: "A road with scattered leaves, a car driving over it.", uk: "Проїжджа частина з розсипаним листям, автомобіль їде по ньому.", pl: "Jezdnia z rozsypanymi liśćmi, samochód przejeżdża po nich.", ar: "طريق مغطى بأوراق شجر متناثرة، وسيارة تمر فوقها.", zh: "路面散布着落叶,一辆车正从上面驶过。", hi: "बिखरे हुए पत्तों वाली एक सड़क, जिस पर से एक कार गुजर रही है।", tr: "Üzerinde dağınık yapraklar olan bir yol, üzerinden bir araba geçiyor.", fr: "Une chaussée jonchée de feuilles mortes, une voiture roule dessus.", ru: "Проезжая часть с рассыпанными листьями, по ней едет автомобиль.", es: "Una calzada con hojas dispersas, un coche circulando sobre ella.", it: "Una carreggiata con foglie sparse, un'auto che ci passa sopra." },
    answer: { de: "Eine leichte Schlingerlinie zeigt reduzierten Grip auf dem nassen Laub.", en: "A slight swerving line shows reduced grip on the wet leaves.", uk: "Легка звивиста лінія показує знижене зчеплення на мокрому листі.", pl: "Lekka linia zygzakowata pokazuje zmniejszoną przyczepność na mokrych liściach.", ar: "خط تعرج طفيف يظهر انخفاض التماسك على الأوراق المبللة.", zh: "轻微摆动的行车线表明湿叶导致附着力下降。", hi: "एक हल्की लहरदार रेखा गीले पत्तों पर कम पकड़ (ग्रिप) को दर्शाती है।", tr: "Hafif bir savrulma çizgisi, ıslak yapraklar üzerinde tutuşun azaldığını gösterir.", fr: "Une légère ligne d'embardée montre l'adhérence réduite sur les feuilles mouillées.", ru: "Лёгкая петляющая линия показывает пониженное сцепление на мокрых листьях.", es: "Una ligera línea de bandazo muestra el agarre reducido sobre las hojas mojadas.", it: "Una leggera linea sbandata mostra la ridotta aderenza sulle foglie bagnate." },
  },
  "gefahr-24": {
    plain: { de: "Draufsicht auf einen Lastwagen mit einem schattierten Bereich seitlich daneben.", en: "Top-down view of a truck with a shaded area beside it.", uk: "Вигляд згори на вантажівку із затіненою ділянкою поруч із нею.", pl: "Widok z góry na ciężarówkę z zacienionym obszarem obok niej.", ar: "منظر علوي لشاحنة ومنطقة مظللة بجانبها.", zh: "俯视图显示一辆卡车,旁边有一块阴影区域。", hi: "एक ट्रक का टॉप-डाउन दृश्य जिसके बगल में एक छायांकित क्षेत्र है।", tr: "Yanında gölgeli bir alan bulunan bir kamyonun kuşbakışı görünümü.", fr: "Vue de dessus d'un camion avec une zone ombrée à côté.", ru: "Вид сверху на грузовик с затемнённой зоной рядом.", es: "Vista superior de un camión con una zona sombreada al lado.", it: "Vista dall'alto di un camion con una zona ombreggiata accanto." },
    answer: { de: "Ein Fahrrad-Symbol ist im schattierten Bereich versteckt und für den Lkw-Fahrer unsichtbar.", en: "A bicycle icon is hidden in the shaded area, invisible to the truck driver.", uk: "Символ велосипеда схований у затіненій ділянці і невидимий для водія вантажівки.", pl: "Symbol roweru jest ukryty w zacienionym obszarze i niewidoczny dla kierowcy ciężarówki.", ar: "رمز دراجة هوائية مخفي في المنطقة المظللة وغير مرئي لسائق الشاحنة.", zh: "阴影区域中隐藏着一个自行车图标,卡车司机无法看到。", hi: "छायांकित क्षेत्र में एक साइकिल आइकन छिपा है, जो ट्रक चालक को दिखाई नहीं देता।", tr: "Gölgeli alanda, kamyon şoförü tarafından görülemeyen bir bisiklet simgesi gizlenmiştir.", fr: "Un symbole de vélo est caché dans la zone ombrée, invisible pour le conducteur du camion.", ru: "Значок велосипеда скрыт в затемнённой зоне, невидим для водителя грузовика.", es: "Un icono de bicicleta está oculto en la zona sombreada, invisible para el conductor del camión.", it: "Un'icona di bicicletta è nascosta nella zona ombreggiata, invisibile per il conducente del camion." },
  },
  "gefahr-25": {
    plain: { de: "Eine Pfütze auf der Fahrbahn, ein Auto nähert sich.", en: "A puddle on the road, with a car approaching.", uk: "Калюжа на дорозі, наближається автомобіль.", pl: "Kałuża na jezdni, zbliża się samochód.", ar: "بركة ماء على الطريق، وسيارة تقترب.", zh: "路面有一处水坑,一辆车正驶近。", hi: "सड़क पर एक पोखर है, एक कार आ रही है।", tr: "Yolda bir su birikintisi var, bir araba yaklaşıyor.", fr: "Une flaque d'eau sur la chaussée, une voiture approche.", ru: "Лужа на проезжей части, приближается автомобиль.", es: "Un charco en la calzada, un coche se acerca.", it: "Una pozzanghera sulla carreggiata, un'auto si avvicina." },
    answer: { de: "Gestrichelte Linie zeigt die verborgene Tiefe der Pfütze und einen möglichen Lenkruck.", en: "A dashed line shows the puddle's hidden depth and a possible steering jolt.", uk: "Пунктирна лінія показує приховану глибину калюжі та можливий ривок керма.", pl: "Przerywana linia pokazuje ukrytą głębokość kałuży i możliwe szarpnięcie kierownicą.", ar: "خط متقطع يظهر عمق البركة المخفي وارتجاجًا محتملاً في المقود.", zh: "虚线表示水坑隐藏的深度以及可能出现的转向猛拉。", hi: "एक धराशायी (डैश्ड) रेखा पोखर की छिपी हुई गहराई और स्टीयरिंग में संभावित झटके को दर्शाती है।", tr: "Kesikli bir çizgi, su birikintisinin gizli derinliğini ve olası bir direksiyon sarsıntısını gösterir.", fr: "Une ligne en pointillés montre la profondeur cachée de la flaque et un possible à-coup de direction.", ru: "Пунктирная линия показывает скрытую глубину лужи и возможный рывок руля.", es: "Una línea discontinua muestra la profundidad oculta del charco y un posible tirón del volante.", it: "Una linea tratteggiata mostra la profondità nascosta della pozzanghera e un possibile scossone dello sterzo." },
  },
  "gefahr-26": {
    plain: { de: "Zwei Reifen im Querschnitt, einer mit tiefem, einer mit flachem Profil.", en: "Two tires in cross-section, one with deep tread, one with shallow tread.", uk: "Дві шини в перерізі, одна з глибоким протектором, одна з неглибоким.", pl: "Dwie opony w przekroju, jedna z głębokim, druga z płytkim bieżnikiem.", ar: "إطاران في مقطع عرضي، أحدهما بنقش عميق والآخر بنقش ضحل.", zh: "两条轮胎的截面图,一条花纹较深,一条花纹较浅。", hi: "दो टायरों का क्रॉस-सेक्शन, एक गहरे ट्रेड वाला, एक उथले ट्रेड वाला।", tr: "Kesit halinde iki lastik, biri derin diş izli, diğeri sığ diş izli.", fr: "Deux pneus en coupe transversale, l'un avec une sculpture profonde, l'autre avec une sculpture peu profonde.", ru: "Два шинных протектора в сечении: один с глубоким рисунком, другой с неглубоким.", es: "Dos neumáticos en sección transversal, uno con dibujo profundo y otro con dibujo poco profundo.", it: "Due pneumatici in sezione trasversale, uno con battistrada profondo e uno con battistrada poco profondo." },
    answer: { de: "Der neue Reifen leitet Wasser ab (grün), der abgefahrene hat hohes Aquaplaning-Risiko (rot).", en: "The new tire channels water away (green), the worn one has high hydroplaning risk (red).", uk: "Нова шина відводить воду (зелений), зношена має високий ризик аквапланування (червоний).", pl: "Nowa opona odprowadza wodę (zielony), zużyta ma wysokie ryzyko aquaplaningu (czerwony).", ar: "الإطار الجديد يصرّف الماء (أخضر)، والإطار المستهلك لديه خطر انزلاق مائي مرتفع (أحمر).", zh: "新轮胎能有效排水(绿色),磨损轮胎则水滑风险较高(红色)。", hi: "नया टायर पानी को दूर बहा देता है (हरा), घिसा हुआ टायर हाइड्रोप्लेनिंग के उच्च जोखिम में है (लाल)।", tr: "Yeni lastik suyu kanallara yönlendirir (yeşil), aşınmış lastikte yüksek aquaplaning riski vardır (kırmızı).", fr: "Le pneu neuf évacue l'eau (vert), le pneu usé présente un risque élevé d'aquaplanage (rouge).", ru: "Новая шина отводит воду (зелёный), изношенная имеет высокий риск аквапланирования (красный).", es: "El neumático nuevo canaliza el agua (verde), el desgastado tiene un alto riesgo de hidroplaneo (rojo).", it: "Il pneumatico nuovo canalizza l'acqua (verde), quello usurato ha un alto rischio di aquaplaning (rosso)." },
  },
  "gefahr-27": {
    plain: { de: "Ein Auto fährt in dichtem Nebel, ein weiteres Fahrzeug ist nur schwach sichtbar.", en: "A car driving in dense fog, with another vehicle barely visible ahead.", uk: "Автомобіль їде в густому тумані, інший транспортний засіб ледь видно попереду.", pl: "Samochód jadący w gęstej mgle, inny pojazd jest ledwo widoczny z przodu.", ar: "سيارة تسير في ضباب كثيف، ومركبة أخرى بالكاد تظهر أمامها.", zh: "一辆车在浓雾中行驶,前方另一辆车几乎无法看清。", hi: "घने कोहरे में चल रही एक कार, आगे एक और वाहन मुश्किल से दिखाई दे रहा है।", tr: "Yoğun sis içinde giden bir araba, önde başka bir araç zar zor görünüyor.", fr: "Une voiture roulant dans un épais brouillard, un autre véhicule à peine visible devant.", ru: "Автомобиль едет в густом тумане, впереди едва виден другой автомобиль.", es: "Un coche circulando en niebla densa, con otro vehículo apenas visible delante.", it: "Un'auto che guida in fitta nebbia, con un altro veicolo appena visibile davanti." },
    answer: { de: "Pfeile zeigen einen vergrößerten Abstand zum vorausfahrenden Fahrzeug.", en: "Arrows show an increased distance to the vehicle ahead.", uk: "Стрілки показують збільшену дистанцію до транспортного засобу попереду.", pl: "Strzałki pokazują zwiększony odstęp od pojazdu jadącego z przodu.", ar: "أسهم تظهر زيادة المسافة عن المركبة التي أمامها.", zh: "箭头表示与前车的距离已加大。", hi: "तीर आगे वाले वाहन से बढ़ी हुई दूरी को दर्शाते हैं।", tr: "Oklar, öndeki araçla artan mesafeyi gösteriyor.", fr: "Des flèches montrent une distance accrue par rapport au véhicule qui précède.", ru: "Стрелки показывают увеличенную дистанцию до впереди идущего автомобиля.", es: "Unas flechas muestran una distancia mayor respecto al vehículo de delante.", it: "Delle frecce mostrano una distanza maggiore rispetto al veicolo che precede." },
  },
  "gefahr-29": {
    plain: { de: "Eine Ost-West-Straße mit tiefstehender Sonne am Horizont, ein Auto fährt darauf zu.", en: "An east-west road with the sun low on the horizon, a car driving toward it.", uk: "Дорога зі сходу на захід із низьким сонцем на горизонті, автомобіль їде йому назустріч.", pl: "Droga wschód-zachód z nisko stojącym słońcem na horyzoncie, samochód jedzie w jego kierunku.", ar: "طريق يمتد من الشرق إلى الغرب مع شمس منخفضة عند الأفق، وسيارة تتجه نحوها.", zh: "一条东西走向的道路,太阳低悬于地平线,一辆车正朝其驶去。", hi: "पूर्व-पश्चिम दिशा वाली सड़क जिसमें सूरज क्षितिज पर नीचे है, एक कार उसकी ओर बढ़ रही है।", tr: "Güneşin ufukta alçakta olduğu doğu-batı yönlü bir yol, bir araba ona doğru gidiyor.", fr: "Une route est-ouest avec un soleil bas à l'horizon, une voiture roulant vers lui.", ru: "Дорога направления восток-запад с низким солнцем на горизонте, автомобиль едет навстречу ему.", es: "Una carretera este-oeste con el sol bajo en el horizonte, un coche circulando hacia él.", it: "Una strada est-ovest con il sole basso all'orizzonte, un'auto che vi si dirige." },
    answer: { de: "Hinweis, dass die Blendgefahr kurz nach Sonnenaufgang und vor Sonnenuntergang am höchsten ist.", en: "Note that glare risk is highest shortly after sunrise and before sunset.", uk: "Вказівка, що ризик засліплення найвищий невдовзі після сходу та перед заходом сонця.", pl: "Wskazówka, że ryzyko oślepienia jest największe krótko po wschodzie i przed zachodem słońca.", ar: "إشارة إلى أن خطر الوهج يكون في أعلى مستوياته بعد شروق الشمس بقليل وقبل غروبها.", zh: "提示:眩光风险在日出后不久及日落前最高。", hi: "नोट: चकाचौंध का जोखिम सूर्योदय के तुरंत बाद और सूर्यास्त से पहले सबसे अधिक होता है।", tr: "Not: kamaşma riski gün doğumundan kısa süre sonra ve gün batımından önce en yüksektir.", fr: "Indication que le risque d'éblouissement est le plus élevé juste après le lever et avant le coucher du soleil.", ru: "Указание, что риск ослепления наиболее высок вскоре после восхода и перед закатом солнца.", es: "Indicación de que el riesgo de deslumbramiento es mayor poco después del amanecer y antes del atardecer.", it: "Indicazione che il rischio di abbagliamento è massimo poco dopo l'alba e prima del tramonto." },
  },
  "gefahr-32": {
    plain: { de: "Eine Landstraße neben einer Weide mit grasenden Tieren, ohne sichtbaren Zaun.", en: "A rural road next to a pasture with grazing animals and no visible fence.", uk: "Сільська дорога поряд із пасовищем із тваринами, що пасуться, без видимої огорожі.", pl: "Droga wiejska obok pastwiska z pasącymi się zwierzętami, bez widocznego ogrodzenia.", ar: "طريق ريفي بجانب مرعى فيه حيوانات ترعى، دون سياج ظاهر.", zh: "一条乡间道路旁是牧场,牲畜正在吃草,看不到围栏。", hi: "एक ग्रामीण सड़क, जिसके बगल में चरती जानवरों वाला एक चरागाह है और कोई दिखाई देने वाली बाड़ नहीं है।", tr: "Otlayan hayvanların bulunduğu ve görünür bir çiti olmayan bir merada, kırsal bir yol.", fr: "Une route de campagne longeant un pâturage avec des animaux qui paissent, sans clôture visible.", ru: "Сельская дорога рядом с пастбищем с пасущимися животными, без видимого забора.", es: "Una carretera rural junto a un pasto con animales pastando, sin valla visible.", it: "Una strada di campagna accanto a un pascolo con animali al pascolo, senza recinzione visibile." },
    answer: { de: "Pfeil zeigt, dass Tiere ohne Zaun auf die Fahrbahn gelangen könnten.", en: "An arrow shows the animals could reach the road since there is no fence.", uk: "Стрілка показує, що тварини можуть вийти на дорогу, оскільки огорожі немає.", pl: "Strzałka pokazuje, że zwierzęta mogą wejść na jezdnię, ponieważ nie ma ogrodzenia.", ar: "سهم يظهر أن الحيوانات قد تصل إلى الطريق لعدم وجود سياج.", zh: "箭头表示由于没有围栏,牲畜可能进入道路。", hi: "एक तीर दिखाता है कि बाड़ न होने के कारण जानवर सड़क तक पहुंच सकते हैं।", tr: "Bir ok, çit olmadığı için hayvanların yola ulaşabileceğini gösterir.", fr: "Une flèche montre que les animaux pourraient accéder à la chaussée en l'absence de clôture.", ru: "Стрелка показывает, что животные могут выйти на дорогу из-за отсутствия ограждения.", es: "Una flecha muestra que los animales podrían llegar a la calzada al no haber valla.", it: "Una freccia mostra che gli animali potrebbero raggiungere la strada in assenza di recinzione." },
  },
  "gefahr-33": {
    plain: { de: "Eine Straße an einer Schule vorbei, Kinder verlassen das Gelände.", en: "A road past a school, with children leaving the premises.", uk: "Дорога біля школи, діти залишають територію.", pl: "Droga obok szkoły, dzieci opuszczają teren szkoły.", ar: "طريق بجانب مدرسة، وأطفال يغادرون المكان.", zh: "一条经过学校的道路,孩子们正离开校园。", hi: "एक स्कूल के पास से गुजरती सड़क, जहां बच्चे परिसर छोड़ रहे हैं।", tr: "Bir okulun önünden geçen bir yol, çocuklar okul bahçesinden ayrılıyor.", fr: "Une route passant devant une école, des enfants quittent l'établissement.", ru: "Дорога проходит мимо школы, дети покидают территорию.", es: "Una carretera que pasa junto a una escuela, con niños saliendo del recinto.", it: "Una strada che passa davanti a una scuola, con bambini che escono dall'edificio." },
    answer: { de: "Der Bereich vor der Schule ist als Gefahrenzone markiert, deutlich langsamer und bremsbereit.", en: "The area in front of the school is marked as a danger zone, drive much slower and stay ready to brake.", uk: "Ділянка перед школою позначена як небезпечна зона, їдьте значно повільніше і будьте готові гальмувати.", pl: "Obszar przed szkołą jest oznaczony jako strefa niebezpieczna, jedź znacznie wolniej i bądź gotowy do hamowania.", ar: "المنطقة أمام المدرسة موضحة كمنطقة خطر، مع القيادة بشكل أبطأ بكثير والاستعداد للفرملة.", zh: "学校前方区域被标为危险区域,应大幅减速并做好刹车准备。", hi: "स्कूल के सामने के क्षेत्र को खतरे के क्षेत्र के रूप में चिह्नित किया गया है, बहुत धीमी गति से चलाएं और ब्रेक लगाने के लिए तैयार रहें।", tr: "Okulun önündeki alan tehlike bölgesi olarak işaretlenmiştir, çok daha yavaş sürün ve fren yapmaya hazır olun.", fr: "La zone devant l'école est marquée comme zone de danger, rouler nettement plus lentement et être prêt à freiner.", ru: "Зона перед школой обозначена как опасная зона, следует ехать значительно медленнее и быть готовым тормозить.", es: "El área frente a la escuela está marcada como zona de peligro, conducir mucho más despacio y listo para frenar.", it: "L'area davanti alla scuola è indicata come zona di pericolo, procedere molto più lentamente e pronti a frenare." },
  },
  "gefahr-34": {
    plain: { de: "Eine unbefestigte Straße mit losen Steinen, ein Auto fährt darüber.", en: "An unpaved road with loose stones, a car driving over it.", uk: "Ґрунтова дорога з незакріпленим камінням, автомобіль їде по ній.", pl: "Nieutwardzona droga z luźnymi kamieniami, samochód przejeżdża po niej.", ar: "طريق غير معبد بحصى فضفاض، وسيارة تمر فوقه.", zh: "一条铺满松散碎石的未铺装道路,一辆车正驶过。", hi: "ढीले पत्थरों वाली एक कच्ची (अनपक्की) सड़क, जिस पर से एक कार गुजर रही है।", tr: "Gevşek taşları olan sıkıştırılmamış bir yol, üzerinden bir araba geçiyor.", fr: "Une route non goudronnée avec des pierres détachées, une voiture roulant dessus.", ru: "Грунтовая дорога с рассыпанными камнями, по ней едет автомобиль.", es: "Un camino sin asfaltar con piedras sueltas, un coche circulando sobre él.", it: "Una strada non asfaltata con pietre smosse, un'auto che vi transita." },
    answer: { de: "Eine Schlingerlinie zeigt die Ausbrechgefahr durch die losen Steine.", en: "A swerving line shows the risk of the car breaking loose on the loose stones.", uk: "Звивиста лінія показує ризик заносу через незакріплене каміння.", pl: "Linia zygzakowata pokazuje ryzyko utraty przyczepności na luźnych kamieniach.", ar: "خط تعرج يظهر خطر انزلاق السيارة بسبب الحصى الفضفاض.", zh: "摆动的行车线表明车辆在松散碎石上可能失控打滑的风险。", hi: "एक लहरदार रेखा ढीले पत्थरों पर कार के फिसलने के जोखिम को दर्शाती है।", tr: "Bir savrulma çizgisi, gevşek taşlar üzerinde arabanın kontrolden çıkma riskini gösterir.", fr: "Une ligne d'embardée montre le risque de dérapage dû aux pierres détachées.", ru: "Петляющая линия показывает риск заноса из-за рассыпанных камней.", es: "Una línea de bandazo muestra el riesgo de que el coche derrape por las piedras sueltas.", it: "Una linea sbandata mostra il rischio di sbandamento dovuto alle pietre smosse." },
  },
  "gefahr-35": {
    plain: { de: "Ein Auto auf einer erhöhten Brücke, seitliche Windpfeile treffen es.", en: "A car on an elevated bridge, with sideways wind arrows hitting it.", uk: "Автомобіль на високому мосту, бічні стрілки вітру б'ють по ньому.", pl: "Samochód na wysokim moście, boczne strzałki wiatru uderzają w niego.", ar: "سيارة على جسر مرتفع، وأسهم رياح جانبية تضربها.", zh: "一辆车行驶在高架桥上,侧向的风力箭头正冲击它。", hi: "एक ऊंचे पुल पर एक कार, जिस पर बगल से हवा के तीर लग रहे हैं।", tr: "Yüksek bir köprüde bir araba, yandan gelen rüzgar okları ona çarpıyor.", fr: "Une voiture sur un pont surélevé, des flèches de vent latéral la frappant.", ru: "Автомобиль на высоком мосту, боковые стрелки ветра ударяют по нему.", es: "Un coche en un puente elevado, con flechas de viento lateral golpeándolo.", it: "Un'auto su un ponte sopraelevato, con frecce di vento laterale che la colpiscono." },
    answer: { de: "Gestrichelter Pfeil zeigt, wie das Auto seitlich aus der Spur gedrückt wird.", en: "A dashed arrow shows the car being pushed sideways out of its lane.", uk: "Пунктирна стрілка показує, як автомобіль зсувається вбік зі своєї смуги.", pl: "Przerywana strzałka pokazuje, jak samochód jest spychany bokiem poza pas ruchu.", ar: "سهم متقطع يظهر كيف تُدفع السيارة جانبيًا خارج مسارها.", zh: "虚线箭头表示车辆被侧推出车道。", hi: "एक धराशायी (डैश्ड) तीर दिखाता है कि कार को उसकी लेन से बगल में धकेला जा रहा है।", tr: "Kesikli bir ok, arabanın şeridinden yana doğru itildiğini gösterir.", fr: "Une flèche en pointillés montre la voiture poussée latéralement hors de sa voie.", ru: "Пунктирная стрелка показывает, как автомобиль сносит вбок из полосы.", es: "Una flecha discontinua muestra al coche siendo empujado lateralmente fuera de su carril.", it: "Una freccia tratteggiata mostra l'auto spinta lateralmente fuori dalla propria corsia." },
  },
  "gefahr-36": {
    plain: { de: "Nachtszene mit einem Auto und dem Lichtkegel des Abblendlichts.", en: "A night scene with a car and its dipped-headlight beam.", uk: "Нічна сцена з автомобілем і конусом світла ближнього світла.", pl: "Nocna scena z samochodem i stożkiem światła mijania.", ar: "مشهد ليلي لسيارة ومخروط ضوء المصابيح المنخفضة.", zh: "夜间场景,一辆车及其近光灯光束。", hi: "रात का दृश्य जिसमें एक कार और उसकी डिप्ड-हेडलाइट की रोशनी है।", tr: "Bir araba ve kısa hüzmeli farlarının ışığını gösteren gece sahnesi.", fr: "Scène de nuit avec une voiture et le faisceau de ses feux de croisement.", ru: "Ночная сцена с автомобилем и лучом его ближнего света.", es: "Escena nocturna con un coche y el haz de sus luces de cruce.", it: "Scena notturna con un'auto e il fascio dei suoi fari anabbaglianti." },
    answer: { de: "Markierung zeigt, dass der Bremsweg innerhalb des Lichtkegels enden muss.", en: "A marker shows the braking distance must end within the headlight beam.", uk: "Позначка показує, що гальмівний шлях повинен закінчуватися в межах конуса світла.", pl: "Znacznik pokazuje, że droga hamowania musi kończyć się w zasięgu stożka światła.", ar: "علامة تظهر أن مسافة الفرملة يجب أن تنتهي ضمن مخروط الضوء.", zh: "标记表明制动距离必须在近光灯照射范围内结束。", hi: "एक मार्कर दिखाता है कि ब्रेकिंग दूरी हेडलाइट की रोशनी के दायरे में ही समाप्त होनी चाहिए।", tr: "Bir işaret, fren mesafesinin far ışığının içinde sona ermesi gerektiğini gösterir.", fr: "Un marqueur montre que la distance de freinage doit se terminer dans le faisceau lumineux.", ru: "Отметка показывает, что тормозной путь должен заканчиваться в пределах светового луча.", es: "Un marcador muestra que la distancia de frenado debe terminar dentro del haz de luz.", it: "Un indicatore mostra che la distanza di frenata deve terminare entro il fascio luminoso." },
  },
  "gefahr-37": {
    plain: { de: "Zwei Autos hintereinander in einem Tunnel.", en: "Two cars one behind the other inside a tunnel.", uk: "Два автомобілі один за одним у тунелі.", pl: "Dwa samochody jeden za drugim w tunelu.", ar: "سيارتان متتاليتان داخل نفق.", zh: "隧道内前后两辆车。", hi: "एक सुरंग के अंदर एक-दूसरे के पीछे दो कारें।", tr: "Bir tünel içinde art arda iki araba.", fr: "Deux voitures l'une derrière l'autre à l'intérieur d'un tunnel.", ru: "Два автомобиля друг за другом внутри туннеля.", es: "Dos coches uno detrás del otro dentro de un túnel.", it: "Due auto una dietro l'altra all'interno di una galleria." },
    answer: { de: "Pfeile zeigen einen vergrößerten Sicherheitsabstand im Tunnel.", en: "Arrows show an increased safety distance inside the tunnel.", uk: "Стрілки показують збільшену безпечну дистанцію в тунелі.", pl: "Strzałki pokazują zwiększony odstęp bezpieczeństwa w tunelu.", ar: "أسهم تظهر زيادة مسافة الأمان داخل النفق.", zh: "箭头表示隧道内应加大安全距离。", hi: "तीर सुरंग के अंदर बढ़ी हुई सुरक्षा दूरी को दर्शाते हैं।", tr: "Oklar, tünel içinde artan güvenlik mesafesini gösteriyor.", fr: "Des flèches montrent une distance de sécurité accrue à l'intérieur du tunnel.", ru: "Стрелки показывают увеличенную дистанцию безопасности внутри туннеля.", es: "Unas flechas muestran una distancia de seguridad mayor dentro del túnel.", it: "Delle frecce mostrano una distanza di sicurezza maggiore all'interno della galleria." },
  },
  "gefahr-38": {
    plain: { de: "Zwei Autos hintereinander, das vordere mit aufleuchtendem Bremslicht.", en: "Two cars one behind the other, the front one with its brake light lit.", uk: "Два автомобілі один за одним, передній зі стоп-сигналом, що світиться.", pl: "Dwa samochody jeden za drugim, przedni z zapalonym światłem hamowania.", ar: "سيارتان متتاليتان، والسيارة الأمامية بضوء الفرملة مضاء.", zh: "前后两辆车,前车的刹车灯已亮起。", hi: "एक-दूसरे के पीछे दो कारें, आगे वाली कार की ब्रेक लाइट जली हुई है।", tr: "Art arda iki araba, öndeki arabanın fren lambası yanıyor.", fr: "Deux voitures l'une derrière l'autre, celle de devant avec son feu de freinage allumé.", ru: "Два автомобиля друг за другом, у переднего горит стоп-сигнал.", es: "Dos coches uno detrás del otro, el de delante con la luz de freno encendida.", it: "Due auto una dietro l'altra, quella davanti con la luce dei freni accesa." },
    answer: { de: "Der Abstand zwischen beiden Autos ist als ausreichender Sicherheitsabstand markiert.", en: "The gap between the two cars is marked as an adequate safety distance.", uk: "Відстань між обома автомобілями позначена як достатня безпечна дистанція.", pl: "Odstęp między obydwoma samochodami jest oznaczony jako wystarczający odstęp bezpieczeństwa.", ar: "المسافة بين السيارتين موضحة كمسافة أمان كافية.", zh: "两车之间的间距被标为足够的安全距离。", hi: "दोनों कारों के बीच के गैप को पर्याप्त सुरक्षा दूरी के रूप में चिह्नित किया गया है।", tr: "İki araba arasındaki boşluk yeterli güvenlik mesafesi olarak işaretlenmiştir.", fr: "L'espace entre les deux voitures est marqué comme une distance de sécurité suffisante.", ru: "Промежуток между двумя автомобилями обозначен как достаточная дистанция безопасности.", es: "El espacio entre los dos coches está marcado como una distancia de seguridad adecuada.", it: "Lo spazio tra le due auto è indicato come una distanza di sicurezza adeguata." },
  },
  "gefahr-40": {
    plain: { de: "Ein voll beladenes Auto auf einer steilen Gefällstrecke.", en: "A fully loaded car on a steep downhill stretch.", uk: "Повністю завантажений автомобіль на крутому спуску.", pl: "W pełni załadowany samochód na stromym zjeździe.", ar: "سيارة محملة بالكامل على منحدر شديد الانحدار.", zh: "一辆满载的汽车行驶在陡峭的下坡路段。", hi: "एक खड़ी ढलान वाले हिस्से पर पूरी तरह से लदी हुई एक कार।", tr: "Dik bir iniş yolunda tam yüklü bir araba.", fr: "Une voiture entièrement chargée sur une forte pente en descente.", ru: "Полностью загруженный автомобиль на крутом спуске.", es: "Un coche completamente cargado en una pendiente pronunciada de bajada.", it: "Un'auto completamente carica su una ripida discesa." },
    answer: { de: "Ein rotes Symbol zeigt überhitzende Bremsen, Hinweis auf frühes Schalten in einen niedrigen Gang.", en: "A red icon shows overheating brakes, with a note to shift into a low gear early.", uk: "Червоний символ показує перегрів гальм, з вказівкою заздалегідь перейти на нижчу передачу.", pl: "Czerwony symbol pokazuje przegrzewające się hamulce, ze wskazówką o wczesnej zmianie na niski bieg.", ar: "رمز أحمر يظهر ارتفاع حرارة الفرامل، مع ملاحظة للتحول مبكرًا إلى ترس منخفض.", zh: "红色图标表示刹车过热,并提示应提前挂入低挡。", hi: "एक लाल आइकन ओवरहीटिंग ब्रेक्स को दर्शाता है, साथ में जल्दी लो गियर में शिफ्ट करने का नोट है।", tr: "Kırmızı bir simge, aşırı ısınan frenleri gösterir, erken düşük vitese geçme notuyla birlikte.", fr: "Un symbole rouge montre une surchauffe des freins, avec une indication de passer tôt à un rapport inférieur.", ru: "Красный значок показывает перегрев тормозов, с указанием заранее переключиться на пониженную передачу.", es: "Un icono rojo muestra el sobrecalentamiento de los frenos, con una nota para cambiar a una marcha baja con antelación.", it: "Un'icona rossa mostra il surriscaldamento dei freni, con una nota per scalare presto a una marcia bassa." },
  },
};

// Alt text for signs/diagrams is now translated into all 12 locales (DN-28
// was revisited 2026-08-08 - SIGN_ALT/DIAGRAM_ALT above now carry uk/pl/ar/
// zh/hi/tr/fr/ru/es/it alongside de/en). Still falls back to English, then
// German, in case a future addition to either table ever ships without a
// full locale set - so a gap degrades to a real description rather than
// showing nothing or the raw code.
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
// A locale missing for a given module (only hinweisgeberschutz is DE/EN-only
// for now, being a 20-question pilot - see its own comment below) simply
// isn't looked up - getTopicLabel() falls back through en-then-de-then-the
// raw topic string rather than indexing this directly with an unchecked
// locale. IMPORTANT, learned the hard way during a 2026-08-08 translation
// audit: a module missing ENTIRELY from this object (not just missing a
// locale) doesn't just fall back to a raw label - renderFilters() builds
// its filter-chip list from Object.keys(TOPIC_LABELS[examType] || {}), so a
// missing module gets NO topic filter row at all, silently. Check both
// failure modes when auditing this file, not just per-locale gaps.
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
    // 2026-08-08: found via a full translation audit (PO asked to check all
    // translations) - anhaenger_be (the Klasse BE trailer-towing topic, 26
    // real questions) had NO entry here at all, meaning it was invisible in
    // the topic filter row (which is built from this object's own keys, see
    // renderFilters()) and its badge fell back to raw German text in every
    // UI language. Real gap, not by design - fixed.
    anhaenger_be: { de: "Anhängerbetrieb (Klasse BE)", en: "Trailer operation (Class BE)", uk: "Причіп (категорія BE)", pl: "Przyczepa (kategoria BE)", ar: "القطر بمقطورة (فئة BE)", zh: "挂车驾驶（BE类）", hi: "ट्रेलर संचालन (क्लास BE)", tr: "Römork kullanımı (BE sınıfı)", fr: "Remorque (catégorie BE)", ru: "Прицеп (категория BE)", es: "Remolque (categoría BE)", it: "Rimorchio (categoria BE)" },
  },
  // 2026-08-06: extended these 5 modules' topic-filter labels from DE/EN
  // to the app's full 12-locale set (previously fell back silently to
  // English for the other 10 UI languages - see getTopicLabel() above,
  // whose fallback chain masked the gap rather than breaking anything).
  // fuehrerschein already had all 12; motorrad/lkw have no per-topic filter
  // at all (single topic), so neither needed this pass.
  angelschein: {
    tierschutz: { de: "Tierschutz und Waidgerechtigkeit", en: "Animal welfare & ethical practice", uk: "Захист тварин і етика рибальства", pl: "Ochrona zwierząt i etyka wędkarska", ar: "رفاهية الحيوان وأخلاقيات الصيد", zh: "动物福利与钓鱼道德", hi: "पशु कल्याण और नैतिक मछली पकड़ना", tr: "Hayvan refahı ve etik avcılık", fr: "Bien-être animal et pratique éthique", ru: "Защита животных и этика рыбалки", es: "Bienestar animal y pesca ética", it: "Benessere animale e pesca etica" },
    schonzeit: { de: "Schonzeiten und Mindestmaße", en: "Closed seasons & minimum sizes", uk: "Заборонені періоди та мінімальні розміри", pl: "Okresy ochronne i wymiary minimalne", ar: "فترات الحظر والأحجام الدنيا", zh: "禁渔期与最小尺寸", hi: "प्रतिबंधित मौसम और न्यूनतम आकार", tr: "Av yasağı dönemleri ve asgari boyutlar", fr: "Périodes de fermeture et tailles minimales", ru: "Запретные периоды и минимальные размеры", es: "Vedas y tallas mínimas", it: "Periodi di divieto e taglie minime" },
    geraete: { de: "Geräte und Methoden", en: "Tackle & methods", uk: "Спорядження та методи", pl: "Sprzęt i metody", ar: "المعدات والطرق", zh: "渔具与方法", hi: "उपकरण और तरीके", tr: "Ekipman ve yöntemler", fr: "Matériel et méthodes", ru: "Снаряжение и методы", es: "Equipo y métodos", it: "Attrezzatura e metodi" },
    gewaesser: { de: "Gewässerordnung und Angelschein", en: "Water rules & the licence itself", uk: "Правила водойм і посвідчення рибалки", pl: "Zasady dotyczące wód i karta wędkarska", ar: "قواعد المسطحات المائية ورخصة الصيد", zh: "水域规定与钓鱼证", hi: "जल नियम और मछली पकड़ने का लाइसेंस", tr: "Su alanı kuralları ve balıkçılık belgesi", fr: "Réglementation des eaux et permis de pêche", ru: "Правила водоёмов и удостоверение рыболова", es: "Normas de aguas y licencia de pesca", it: "Regole sulle acque e licenza di pesca" },
  },
  datenschutz: {
    grundprinzipien: { de: "Grundprinzipien und Rechtsgrundlagen", en: "Core principles & legal bases", uk: "Основні принципи та правові підстави", pl: "Zasady podstawowe i podstawy prawne", ar: "المبادئ الأساسية والأسس القانونية", zh: "基本原则与法律依据", hi: "मूल सिद्धांत और कानूनी आधार", tr: "Temel ilkeler ve hukuki dayanaklar", fr: "Principes de base et fondements juridiques", ru: "Основные принципы и правовые основания", es: "Principios básicos y bases jurídicas", it: "Principi fondamentali e basi giuridiche" },
    betroffenenrechte: { de: "Betroffenenrechte", en: "Data subject rights", uk: "Права суб'єктів даних", pl: "Prawa osób, których dane dotyczą", ar: "حقوق أصحاب البيانات", zh: "数据主体权利", hi: "डेटा विषय के अधिकार", tr: "Veri sahibi hakları", fr: "Droits des personnes concernées", ru: "Права субъектов данных", es: "Derechos de los interesados", it: "Diritti degli interessati" },
    datensicherheit: { de: "Datensicherheit (TOMs)", en: "Data security (TOMs)", uk: "Безпека даних (ТОЗ)", pl: "Bezpieczeństwo danych (środki TOM)", ar: "أمن البيانات (التدابير الفنية والتنظيمية)", zh: "数据安全(技术与组织措施)", hi: "डेटा सुरक्षा (तकनीकी एवं संगठनात्मक उपाय)", tr: "Veri güvenliği (teknik ve organizasyonel önlemler)", fr: "Sécurité des données (mesures techniques et organisationnelles)", ru: "Безопасность данных (технические и организационные меры)", es: "Seguridad de los datos (medidas técnicas y organizativas)", it: "Sicurezza dei dati (misure tecniche e organizzative)" },
    meldepflichten: { de: "Meldepflichten bei Datenpannen", en: "Breach notification duties", uk: "Обов'язок повідомлення про витік даних", pl: "Obowiązek zgłaszania naruszeń danych", ar: "واجب الإبلاغ عن خروقات البيانات", zh: "数据泄露报告义务", hi: "डेटा उल्लंघन सूचना दायित्व", tr: "Veri ihlali bildirim yükümlülüğü", fr: "Obligation de notification des violations de données", ru: "Обязанность уведомления об утечках данных", es: "Obligación de notificar violaciones de datos", it: "Obbligo di notifica delle violazioni dei dati" },
    auftragsverarbeitung: { de: "Auftragsverarbeitung und Drittländer", en: "Processor agreements & transfers", uk: "Обробка за дорученням і треті країни", pl: "Powierzenie przetwarzania i kraje trzecie", ar: "معالجة البيانات بالنيابة والدول الثالثة", zh: "受托处理与第三国传输", hi: "प्रसंस्करण अनुबंध और तीसरे देश", tr: "Veri işleme sözleşmeleri ve üçüncü ülkeler", fr: "Sous-traitance et transferts vers des pays tiers", ru: "Обработка по поручению и передача в третьи страны", es: "Encargados del tratamiento y transferencias a terceros países", it: "Trattamento per conto terzi e trasferimenti a paesi terzi" },
  },
  arbeitssicherheit: {
    grundpflichten: { de: "Grundpflichten", en: "Basic duties", uk: "Основні обов'язки", pl: "Obowiązki podstawowe", ar: "الواجبات الأساسية", zh: "基本义务", hi: "मूल कर्तव्य", tr: "Temel yükümlülükler", fr: "Obligations de base", ru: "Основные обязанности", es: "Obligaciones básicas", it: "Obblighi di base" },
    unterweisung: { de: "Unterweisungspflicht", en: "Instruction obligation", uk: "Обов'язок інструктажу", pl: "Obowiązek instruktażu", ar: "واجب التدريب والتوجيه", zh: "培训指导义务", hi: "प्रशिक्षण/निर्देश दायित्व", tr: "Bilgilendirme/eğitim yükümlülüğü", fr: "Obligation de formation/instruction", ru: "Обязанность инструктажа", es: "Obligación de formación/instrucción", it: "Obbligo di formazione/istruzione" },
    gefaehrdungsbeurteilung: { de: "Gefährdungsbeurteilung", en: "Risk assessment", uk: "Оцінка ризиків", pl: "Ocena ryzyka", ar: "تقييم المخاطر", zh: "风险评估", hi: "जोखिम मूल्यांकन", tr: "Risk değerlendirmesi", fr: "Évaluation des risques", ru: "Оценка рисков", es: "Evaluación de riesgos", it: "Valutazione dei rischi" },
    psa_notfall: { de: "PSA und Notfälle", en: "PPE & emergencies", uk: "ЗІЗ та надзвичайні ситуації", pl: "Środki ochrony indywidualnej i sytuacje awaryjne", ar: "معدات الحماية الشخصية وحالات الطوارئ", zh: "个人防护装备与紧急情况", hi: "व्यक्तिगत सुरक्षा उपकरण और आपात स्थिति", tr: "Kişisel koruyucu ekipman ve acil durumlar", fr: "EPI et situations d'urgence", ru: "СИЗ и чрезвычайные ситуации", es: "EPI y emergencias", it: "DPI ed emergenze" },
    bildschirmarbeit: { de: "Bildschirmarbeit und Ergonomie", en: "Screen work & ergonomics", uk: "Робота за екраном та ергономіка", pl: "Praca przy monitorze i ergonomia", ar: "العمل أمام الشاشة وبيئة العمل المريحة", zh: "屏幕工作与人体工学", hi: "स्क्रीन कार्य और एर्गोनॉमिक्स", tr: "Ekran başında çalışma ve ergonomi", fr: "Travail sur écran et ergonomie", ru: "Работа за экраном и эргономика", es: "Trabajo con pantallas y ergonomía", it: "Lavoro al videoterminale ed ergonomia" },
  },
  ki_act: {
    grundlagen: { de: "Grundlagen und Risikoklassen", en: "Basics & risk tiers", uk: "Основи та рівні ризику", pl: "Podstawy i poziomy ryzyka", ar: "الأساسيات ومستويات المخاطر", zh: "基础知识与风险等级", hi: "मूल बातें और जोखिम स्तर", tr: "Temel bilgiler ve risk düzeyleri", fr: "Bases et niveaux de risque", ru: "Основы и уровни риска", es: "Fundamentos y niveles de riesgo", it: "Basi e livelli di rischio" },
    ki_kompetenz: { de: "KI-Kompetenzpflicht", en: "AI-literacy obligation", uk: "Обов'язок щодо ШІ-грамотності", pl: "Obowiązek kompetencji w zakresie AI", ar: "واجب الكفاءة في الذكاء الاصطناعي", zh: "人工智能素养义务", hi: "एआई-दक्षता दायित्व", tr: "Yapay zeka okuryazarlığı yükümlülüğü", fr: "Obligation de maîtrise de l'IA", ru: "Обязанность по ИИ-грамотности", es: "Obligación de alfabetización en IA", it: "Obbligo di alfabetizzazione sull'IA" },
    verbotene_praktiken: { de: "Verbotene Praktiken", en: "Prohibited practices", uk: "Заборонені практики", pl: "Zakazane praktyki", ar: "الممارسات المحظورة", zh: "禁止的做法", hi: "निषिद्ध प्रथाएँ", tr: "Yasaklanmış uygulamalar", fr: "Pratiques interdites", ru: "Запрещённые практики", es: "Prácticas prohibidas", it: "Pratiche vietate" },
    transparenzpflichten: { de: "Transparenzpflichten", en: "Transparency obligations", uk: "Обов'язки щодо прозорості", pl: "Obowiązki dotyczące przejrzystości", ar: "واجبات الشفافية", zh: "透明度义务", hi: "पारदर्शिता दायित्व", tr: "Şeffaflık yükümlülükleri", fr: "Obligations de transparence", ru: "Обязанности по прозрачности", es: "Obligaciones de transparencia", it: "Obblighi di trasparenza" },
    ki_am_arbeitsplatz: { de: "KI am Arbeitsplatz", en: "AI at work", uk: "ШІ на робочому місці", pl: "AI w miejscu pracy", ar: "الذكاء الاصطناعي في مكان العمل", zh: "工作场所中的人工智能", hi: "कार्यस्थल पर एआई", tr: "İş yerinde yapay zeka", fr: "L'IA au travail", ru: "ИИ на рабочем месте", es: "La IA en el trabajo", it: "L'IA sul lavoro" },
  },
  it_sicherheit: {
    zugriffsschutz: { de: "Zugriffsschutz", en: "Access protection", uk: "Захист доступу", pl: "Ochrona dostępu", ar: "حماية الوصول", zh: "访问保护", hi: "एक्सेस सुरक्षा", tr: "Erişim koruması", fr: "Protection des accès", ru: "Защита доступа", es: "Protección de acceso", it: "Protezione degli accessi" },
    phishing: { de: "Phishing und Social Engineering", en: "Phishing & social engineering", uk: "Фішинг та соціальна інженерія", pl: "Phishing i socjotechnika", ar: "التصيّد والهندسة الاجتماعية", zh: "网络钓鱼与社会工程", hi: "फ़िशिंग और सोशल इंजीनियरिंग", tr: "Kimlik avı ve sosyal mühendislik", fr: "Hameçonnage et ingénierie sociale", ru: "Фишинг и социальная инженерия", es: "Phishing e ingeniería social", it: "Phishing e ingegneria sociale" },
    datensicherung: { de: "Datensicherung und Geräte", en: "Backups & devices", uk: "Резервне копіювання та пристрої", pl: "Kopie zapasowe i urządzenia", ar: "النسخ الاحتياطي والأجهزة", zh: "数据备份与设备", hi: "बैकअप और उपकरण", tr: "Yedekleme ve cihazlar", fr: "Sauvegardes et appareils", ru: "Резервное копирование и устройства", es: "Copias de seguridad y dispositivos", it: "Backup e dispositivi" },
    mobil_homeoffice: { de: "Mobile Geräte und Home-Office", en: "Mobile devices & home office", uk: "Мобільні пристрої та дистанційна робота", pl: "Urządzenia mobilne i praca zdalna", ar: "الأجهزة المحمولة والعمل عن بُعد", zh: "移动设备与居家办公", hi: "मोबाइल उपकरण और होम-ऑफिस", tr: "Mobil cihazlar ve evden çalışma", fr: "Appareils mobiles et télétravail", ru: "Мобильные устройства и удалённая работа", es: "Dispositivos móviles y teletrabajo", it: "Dispositivi mobili e lavoro da remoto" },
    meldepflicht_it: { de: "Meldung von Sicherheitsvorfällen", en: "Incident reporting", uk: "Повідомлення про інциденти безпеки", pl: "Zgłaszanie incydentów bezpieczeństwa", ar: "الإبلاغ عن حوادث الأمان", zh: "安全事件报告", hi: "सुरक्षा घटना की रिपोर्टिंग", tr: "Güvenlik olaylarının bildirilmesi", fr: "Signalement des incidents de sécurité", ru: "Уведомление об инцидентах безопасности", es: "Notificación de incidentes de seguridad", it: "Segnalazione di incidenti di sicurezza" },
  },
  // 2026-08-08: added via a full translation audit (PO asked to check all
  // translations) - motorrad/lkw had NO entry in this object at all, which
  // silently suppressed their topic-filter row entirely (renderFilters()
  // builds the filter chip list from this object's own keys) and made every
  // question's topic badge fall back to raw German text regardless of UI
  // language. A stale comment elsewhere claimed this was because these two
  // modules have "a single topic" - false: motorrad has 5, lkw has 4. Fixed.
  motorrad: {
    fahrphysik: { de: "Fahrphysik und Balance", en: "Riding physics & balance", uk: "Фізика керування та рівновага", pl: "Fizyka jazdy i równowaga", ar: "فيزياء القيادة والتوازن", zh: "骑行物理与平衡", hi: "सवारी भौतिकी और संतुलन", tr: "Sürüş fiziği ve denge", fr: "Physique de conduite et équilibre", ru: "Физика движения и баланс", es: "Física de conducción y equilibrio", it: "Fisica di guida ed equilibrio" },
    schutzausruestung: { de: "Schutzausrüstung und Sichtbarkeit", en: "Protective gear & visibility", uk: "Захисне спорядження та видимість", pl: "Odzież ochronna i widoczność", ar: "معدات الحماية والظهور", zh: "防护装备与能见度", hi: "सुरक्षा उपकरण और दृश्यता", tr: "Koruyucu ekipman ve görünürlük", fr: "Équipement de protection et visibilité", ru: "Защитная экипировка и видимость", es: "Equipo de protección y visibilidad", it: "Abbigliamento protettivo e visibilità" },
    verkehrsverhalten: { de: "Verkehrsverhalten für Kraftradfahrer", en: "Road behavior for motorcyclists", uk: "Поведінка на дорозі для мотоциклістів", pl: "Zachowanie na drodze motocyklistów", ar: "سلوك السائق على الطريق للدراجات النارية", zh: "摩托车骑手的道路行为", hi: "मोटरसाइकिल चालकों के लिए सड़क व्यवहार", tr: "Motosikletliler için trafik davranışı", fr: "Comportement routier des motards", ru: "Поведение на дороге для мотоциклистов", es: "Comportamiento vial para motociclistas", it: "Comportamento stradale per motociclisti" },
    fahrerlaubnis: { de: "Fahrerlaubnisklassen und technische Besonderheiten", en: "License classes & technical specifics", uk: "Категорії прав та технічні особливості", pl: "Kategorie prawa jazdy i specyfika techniczna", ar: "فئات الرخصة والخصائص الفنية", zh: "驾照类别与技术细节", hi: "लाइसेंस श्रेणियाँ और तकनीकी विशेषताएँ", tr: "Ehliyet sınıfları ve teknik özellikler", fr: "Catégories de permis et spécificités techniques", ru: "Категории прав и технические особенности", es: "Categorías de licencia y particularidades técnicas", it: "Categorie di patente e specifiche tecniche" },
    besondere_bedingungen: { de: "Fahren unter besonderen Bedingungen", en: "Riding under special conditions", uk: "Керування в особливих умовах", pl: "Jazda w szczególnych warunkach", ar: "القيادة في ظروف خاصة", zh: "特殊条件下的骑行", hi: "विशेष परिस्थितियों में सवारी", tr: "Özel koşullarda sürüş", fr: "Conduite dans des conditions particulières", ru: "Вождение в особых условиях", es: "Conducción en condiciones especiales", it: "Guida in condizioni particolari" },
  },
  lkw: {
    fahrdynamik: { de: "Fahrzeugabmessungen und Fahrdynamik", en: "Vehicle dimensions & dynamics", uk: "Габарити та динаміка транспортного засобу", pl: "Wymiary i dynamika pojazdu", ar: "أبعاد المركبة وديناميكيتها", zh: "车辆尺寸与动力学", hi: "वाहन आयाम और गतिकी", tr: "Araç boyutları ve dinamiği", fr: "Dimensions et dynamique du véhicule", ru: "Габариты и динамика транспортного средства", es: "Dimensiones y dinámica del vehículo", it: "Dimensioni e dinamica del veicolo" },
    vorschriften: { de: "Vorschriften, Kontrollen und Ankuppeln", en: "Regulations, inspections & coupling", uk: "Правила, перевірки та зчеплення", pl: "Przepisy, kontrole i sprzęganie", ar: "اللوائح والفحوصات والقرن", zh: "法规、检查与挂接", hi: "नियम, निरीक्षण और कपलिंग", tr: "Kurallar, kontroller ve bağlantı", fr: "Réglementation, contrôles et attelage", ru: "Правила, проверки и сцепка", es: "Normativa, controles y enganche", it: "Normative, controlli e aggancio" },
    ladungssicherung: { de: "Ladungssicherung", en: "Load securing", uk: "Кріплення вантажу", pl: "Mocowanie ładunku", ar: "تثبيت الحمولة", zh: "货物固定", hi: "भार सुरक्षा", tr: "Yük emniyeti", fr: "Arrimage du chargement", ru: "Крепление груза", es: "Sujeción de la carga", it: "Fissaggio del carico" },
    lenkzeiten: { de: "Lenk- und Ruhezeiten sowie Fahrtenschreiber", en: "Driving & rest times, and the tachograph", uk: "Час керування та відпочинку, тахограф", pl: "Czas jazdy i odpoczynku oraz tachograf", ar: "أوقات القيادة والراحة ومسجل السرعة", zh: "驾驶与休息时间及行车记录仪", hi: "ड्राइविंग और विश्राम समय, तथा टैकोग्राफ", tr: "Sürüş ve dinlenme süreleri ile takograf", fr: "Temps de conduite et de repos, et tachygraphe", ru: "Время вождения и отдыха, тахограф", es: "Tiempos de conducción y descanso, y tacógrafo", it: "Tempi di guida e riposo, e tachigrafo" },
  },
  // DN-50: 5th compliance module. DE/EN-only pilot (see
  // hinweisgeberschutz_pilot.json meta) - these topic labels are DE/EN only
  // for now too, matching getTopicLabel()'s existing EN/DE-then-raw
  // fallback chain (same situation angelschein was in before it got full
  // 12-locale topic labels).
  hinweisgeberschutz: {
    geltungsbereich: { de: "Geltungsbereich", en: "Scope & thresholds" },
    meldestellen: { de: "Meldestellen (intern/extern)", en: "Reporting channels (internal/external)" },
    vertraulichkeit: { de: "Vertraulichkeit", en: "Confidentiality" },
    repressalienschutz: { de: "Schutz vor Repressalien", en: "Protection from retaliation" },
    sanktionen: { de: "Sanktionen (Bußgeld)", en: "Sanctions (fines)" },
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
// The workplace-compliance modules carry a per-question `roles` array
// (see data/build_modules.py's CORE_FIELDS) - e.g. ["all"] for a question
// relevant to everyone, or ["it"]/["hr"]/["management"]/["all_staff"] for a
// more role-specific one. This is a SECOND, additive filter row shown only
// for those modules (originally 4 under DN-44, now 5 since DN-50 added
// hinweisgeberschutz with its own roles field), layered on top of the
// existing topic filter (a learner can combine both) rather than replacing it.
const COMPLIANCE_MODULES = new Set(["datenschutz", "arbeitssicherheit", "ki_act", "it_sicherheit", "hinweisgeberschutz"]);

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

// DN-14: manual star/bookmark strings - standalone rather than folded into
// UI_STRINGS, same reasoning SRS_STRINGS/ROLE_FILTER_STRINGS document (a
// self-contained additive feature). Covers the star toggle button (both
// states), its aria-label, the "starred only" filter chip in the topic
// filter row, and the empty-state message shown when that filter is active
// but nothing is starred yet.
const STAR_STRINGS = {
  de: { star: "☆ Merken", starred: "⭐ Gemerkt", starAria: "Diese Frage merken", starredAria: "Markierung entfernen", filterChip: "⭐ Nur markierte", filterAria: "Nur markierte Fragen anzeigen", emptyStarred: "Noch keine markierten Fragen in dieser Kategorie." },
  en: { star: "☆ Star", starred: "⭐ Starred", starAria: "Star this question", starredAria: "Remove star", filterChip: "⭐ Starred only", filterAria: "Show only starred questions", emptyStarred: "No starred questions in this category yet." },
  uk: { star: "☆ Позначити", starred: "⭐ Позначено", starAria: "Позначити це питання зіркою", starredAria: "Прибрати позначку", filterChip: "⭐ Лише позначені", filterAria: "Показати лише позначені питання", emptyStarred: "У цій категорії ще немає позначених питань." },
  pl: { star: "☆ Oznacz", starred: "⭐ Oznaczone", starAria: "Oznacz to pytanie gwiazdką", starredAria: "Usuń oznaczenie", filterChip: "⭐ Tylko oznaczone", filterAria: "Pokaż tylko oznaczone pytania", emptyStarred: "W tej kategorii nie ma jeszcze oznaczonych pytań." },
  ar: { star: "☆ تمييز", starred: "⭐ مميزة", starAria: "تمييز هذا السؤال", starredAria: "إزالة التمييز", filterChip: "⭐ المميزة فقط", filterAria: "عرض الأسئلة المميزة فقط", emptyStarred: "لا توجد أسئلة مميزة في هذه الفئة بعد." },
  zh: { star: "☆ 标记", starred: "⭐ 已标记", starAria: "标记此题", starredAria: "取消标记", filterChip: "⭐ 仅显示已标记", filterAria: "仅显示已标记的题目", emptyStarred: "该类别下暂无已标记的题目。" },
  hi: { star: "☆ चिह्नित करें", starred: "⭐ चिह्नित", starAria: "इस प्रश्न को चिह्नित करें", starredAria: "चिह्न हटाएं", filterChip: "⭐ केवल चिह्नित", filterAria: "केवल चिह्नित प्रश्न दिखाएं", emptyStarred: "इस श्रेणी में अभी तक कोई चिह्नित प्रश्न नहीं है।" },
  tr: { star: "☆ İşaretle", starred: "⭐ İşaretlendi", starAria: "Bu soruyu işaretle", starredAria: "İşareti kaldır", filterChip: "⭐ Yalnızca işaretliler", filterAria: "Yalnızca işaretli soruları göster", emptyStarred: "Bu kategoride henüz işaretli soru yok." },
  fr: { star: "☆ Marquer", starred: "⭐ Marquée", starAria: "Marquer cette question", starredAria: "Retirer le marquage", filterChip: "⭐ Marquées uniquement", filterAria: "Afficher uniquement les questions marquées", emptyStarred: "Aucune question marquée dans cette catégorie pour l'instant." },
  ru: { star: "☆ Отметить", starred: "⭐ Отмечено", starAria: "Отметить этот вопрос", starredAria: "Снять отметку", filterChip: "⭐ Только отмеченные", filterAria: "Показать только отмеченные вопросы", emptyStarred: "В этой категории пока нет отмеченных вопросов." },
  es: { star: "☆ Marcar", starred: "⭐ Marcada", starAria: "Marcar esta pregunta", starredAria: "Quitar marca", filterChip: "⭐ Solo marcadas", filterAria: "Mostrar solo preguntas marcadas", emptyStarred: "Todavía no hay preguntas marcadas en esta categoría." },
  it: { star: "☆ Contrassegna", starred: "⭐ Contrassegnata", starAria: "Contrassegna questa domanda", starredAria: "Rimuovi contrassegno", filterChip: "⭐ Solo contrassegnate", filterAria: "Mostra solo le domande contrassegnate", emptyStarred: "Nessuna domanda contrassegnata in questa categoria ancora." },
};
function starStrings(lang) {
  return STAR_STRINGS[lang] || STAR_STRINGS.en;
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
  // "Prepare for offline" button/status (DN-46): status is
  // "idle" | "checking" | "ready" | "unprepared" | "loading" | "error" -
  // see checkOfflineReadiness()/prepareOffline()/renderOfflinePrep() below.
  // done/total are only meaningful while status === "loading".
  offlinePrep: { status: "idle", done: 0, total: 0 },
  // Local profile switcher: which per-device profile is active, and the
  // full registry of profiles on this device (see migrateOrInitProfiles()).
  profiles: [],
  activeProfileId: null,
  // Spaced-repetition "Review due" mode (DN-16, see openReviewSession()):
  // while true, filteredQuestions() sources #detail-view from reviewQueue
  // (the due-question list) instead of the topic-filtered browsing list.
  reviewMode: false,
  reviewQueue: [],
  // "Try it yourself" (flashcard self-answer, requested after users found the
  // reveal-only flow and the review-mode know/don't-know buttons hard to
  // connect to anything - answering blind then being asked "did you know
  // it?" felt disconnected). Mirrors exam mode's answer-tracking shape:
  // a single string key for single_choice, an array of keys for
  // multi_choice. Cleared to null whenever the shown question changes (see
  // every "state.revealed = false" site above) so a stale pick from a
  // previous card never leaks into the next one.
  detailPick: null,
  // DN-14: "starred only" list filter. Deliberately NOT persisted like
  // topicFilter/roleFilter above - it's a quick, temporary lens on "what am I
  // looking at right now" rather than a durable per-profile preference, the
  // same reasoning reviewMode (also session-only) already follows. The
  // underlying starred/seen data itself IS persisted (loadStarredData()/
  // loadSeenData() below), just not which filter view is currently toggled.
  starredOnlyFilter: false,
  // Kickstart-learning-journey topic primers (DN-52 Phase 1, see
  // openPrimerReader()/renderPrimerReader() below): which topic's primer is
  // currently open, its chunks (already resolved to the active UI language),
  // and the current chunk index within it.
  primerTopic: null,
  primerChunks: [],
  primerChunkIndex: 0,
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

  // DN-46: re-check (read-only, no fetching) whether this module+language
  // combination is already fully offline-cached from a previous visit/prep,
  // so a returning visitor sees "already offline" immediately rather than a
  // stale "not prepared yet". Fire-and-forget - it repaints itself via
  // renderOfflinePrep() once the caches.match() calls resolve, independent
  // of the render() the caller does right after loadModuleData() returns.
  checkOfflineReadiness();
}

// DN-46 "prepare for offline" feature. This deliberately does NOT talk to
// the service worker at all (no postMessage/messaging) - service-worker.js's
// existing fetch handler already runtime-caches ANY successful fetch for a
// non-shell-asset URL (see the final `event.respondWith` branch there), so a
// plain page-side fetch() of a module/locale/sign URL gets cached as a side
// effect automatically. This code only needs to (a) know which URLs matter
// for the currently loaded module+language and (b) fetch them / read back
// their cache status via the plain `caches` API.

// Every URL needed for the CURRENTLY loaded module, in the CURRENTLY
// resolved content language, to work fully offline: core data, the locale
// file actually in use (which may differ from state.lang after a fallback -
// see fetchLocaleTextWithFallback()/state.contentLangFallback), and every
// unique sign SVG referenced by the loaded questions.
function offlineAssetUrls() {
  if (!state.examType) return [];
  const lang = state.contentLangFallback || state.lang;
  const urls = [
    `data/${state.examType}/core.json`,
    `data/${state.examType}/locales/${lang}.json`,
  ];
  const signUrls = new Set();
  state.questions.forEach((q) => {
    if (q.image_ref) {
      // Same resolution logic as resolveImage() above.
      const key = q.image_ref.split("/")[1];
      signUrls.add(`assets/signs/${key}.svg`);
    } else if (DIAGRAM_IDS.has(q.id)) {
      // Diagram questions render TWO variants (the plain pre-reveal scene
      // and the answer-revealed scene, see resolveImage() above) - both
      // need to be cached, not just whichever one happens to have been
      // viewed so far, otherwise revealing the answer offline for a
      // not-yet-revealed diagram question would fail (caught during
      // review of this feature - the initial pass only covered
      // image_ref/sign SVGs, not the separate diagram-id image path).
      signUrls.add(`assets/diagrams/${q.id}.svg`);
      signUrls.add(`assets/diagrams/${q.id}-answer.svg`);
    }
  });
  urls.push(...signUrls);

  // DN-52 Phase 1: the kickstart-learning-journey topic primers are their
  // own separate fetch (data/fuehrerschein/primers.json +
  // primers_locales/<lang>.json, not part of core.json/locales/*.json
  // above) - "prepare for offline" needs to know about them explicitly or a
  // learner who prepped a module for offline use would still hit the
  // network the first time they open a primer. Fuehrerschein-only, same
  // gating as the primers button itself.
  if (state.examType === "fuehrerschein") {
    urls.push(`data/fuehrerschein/primers.json`, `data/fuehrerschein/primers_locales/${lang}.json`);
  }

  return urls;
}

// Read-only: checks whether every URL the current module+language needs is
// already sitting in some cache at this origin (caches.match() with no
// cache name searches all of them), without fetching/writing anything.
async function checkOfflineReadiness() {
  const urls = offlineAssetUrls();
  if (urls.length === 0) return;
  state.offlinePrep = { status: "checking", done: 0, total: urls.length };
  renderOfflinePrep();
  const hits = await Promise.all(urls.map((u) => caches.match(u).then((r) => !!r)));
  const allCached = hits.every(Boolean);
  state.offlinePrep = { status: allCached ? "ready" : "unprepared", done: 0, total: urls.length };
  renderOfflinePrep();
}

// Actually fetches every needed URL (triggering the service worker's
// runtime-cache-on-success behavior). Uses allSettled so one failed file
// (e.g. a flaky connection mid-fetch) doesn't abort the rest - the button
// stays clickable to retry, and a retry simply re-fetches everything again,
// which is cheap for these small JSON/SVG files and keeps this logic simple.
async function prepareOffline() {
  const urls = offlineAssetUrls();
  if (urls.length === 0) return;
  state.offlinePrep = { status: "loading", done: 0, total: urls.length };
  renderOfflinePrep();
  let done = 0;
  let hadError = false;
  await Promise.allSettled(
    urls.map((u) =>
      fetch(u)
        .then((r) => {
          if (!r || !r.ok) hadError = true;
        })
        .catch(() => {
          hadError = true;
        })
        .finally(() => {
          done += 1;
          state.offlinePrep = { status: "loading", done, total: urls.length };
          renderOfflinePrep();
        })
    )
  );
  state.offlinePrep = { status: hadError ? "error" : "ready", done, total: urls.length };
  renderOfflinePrep();
}

// Paints the button/status span from state.offlinePrep - a pure repaint, it
// never itself touches the cache or network. Called both from render() (for
// visibility whenever the module or language changes) and standalone by
// checkOfflineReadiness()/prepareOffline() as their async work progresses.
function renderOfflinePrep() {
  const S = UI_STRINGS[state.lang];
  const btn = el("#offline-prep-btn");
  const status = el("#offline-prep-status");
  // Shown for every module (any module can be prepared for offline use,
  // unlike Sign Reference above which is Fuehrerschein-only) - only hidden
  // when no module is loaded yet at all, same as the other header controls.
  const hide = !state.examType;
  btn.hidden = hide;
  status.hidden = hide;
  if (hide) return;

  const st = state.offlinePrep || { status: "idle" };
  btn.disabled = st.status === "loading" || st.status === "checking";
  btn.textContent = S.offlinePrepBtn;
  btn.title = S.offlinePrepBtn;
  btn.setAttribute("aria-label", S.offlinePrepBtn);

  switch (st.status) {
    case "ready":
      status.textContent = S.offlinePrepReady;
      break;
    case "loading":
      status.textContent = S.offlinePrepLoading(st.done, st.total);
      break;
    case "error":
      status.textContent = S.offlinePrepError;
      break;
    case "checking":
    case "unprepared":
    case "idle":
    default:
      status.textContent = "";
  }
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
// reopenable any time via the header "About this module" button. This was
// a separate, unrelated DE/EN-only gap from DN-28 (which only ever covered
// sign/diagram alt text) - just never got its own card. Closed 2026-08-08
// alongside the DN-28 revisit, since it was a small, low-risk chrome-string
// table to translate while already in this area.
const MODULE_INTRO_STRINGS = {
  de: { next: "Weiter", back: "← Zurück", skip: "Überspringen", start: "Los geht's", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Über dieses Modul" },
  en: { next: "Next", back: "← Back", skip: "Skip", start: "Let's start", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "About this module" },
  uk: { next: "Далі", back: "← Назад", skip: "Пропустити", start: "Почати", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Про цей модуль" },
  pl: { next: "Dalej", back: "← Wstecz", skip: "Pomiń", start: "Zaczynajmy", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "O tym module" },
  ar: { next: "التالي", back: "← رجوع", skip: "تخطي", start: "لنبدأ", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "حول هذه الوحدة" },
  zh: { next: "下一步", back: "← 返回", skip: "跳过", start: "开始吧", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "关于本模块" },
  hi: { next: "आगे", back: "← वापस", skip: "छोड़ें", start: "चलिए शुरू करें", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "इस मॉड्यूल के बारे में" },
  tr: { next: "İleri", back: "← Geri", skip: "Atla", start: "Hadi başlayalım", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Bu modül hakkında" },
  fr: { next: "Suivant", back: "← Retour", skip: "Passer", start: "C'est parti", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "À propos de ce module" },
  ru: { next: "Далее", back: "← Назад", skip: "Пропустить", start: "Начнём", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Об этом модуле" },
  es: { next: "Siguiente", back: "← Atrás", skip: "Omitir", start: "Empecemos", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Sobre este módulo" },
  it: { next: "Avanti", back: "← Indietro", skip: "Salta", start: "Iniziamo", stepOf: (i, n) => `${i} / ${n}`, aboutBtn: "Informazioni su questo modulo" },
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
// Badge display (2026-08-07): a completion can now carry a REAL signature
// (record.verified === true, see trySignCompletion()/credentialJsonDoc()
// above) or stay a self-issued/unverified fallback (offline, signing
// function unreachable, or an older completion from before this feature
// existed) - verifiedLabel/selfIssuedLabel/verifiedHint/selfIssuedHint let
// renderCertificates() show which one a given card actually is, not just
// offer downloads with no visible distinction between a real badge and a
// placeholder one.
const CERT_STRINGS = {
  de: {
    btn: "Meine Zertifikate", title: "Meine Zertifikate", close: "← Zurück",
    intro: "Bestandene Prüfungssimulationen werden hier als Nachweis gespeichert (nur auf diesem Gerät). Lade eine Zertifikatsdatei herunter, um sie zu behalten oder weiterzugeben - das ist die eigentlich portable Datei, nicht der App-Zustand.",
    empty: "Noch keine bestandene Prüfungssimulation. Bestehe eine Prüfungssimulation (nicht den Übungsmodus), um hier ein Zertifikat zu erhalten.",
    passedOn: (d) => `Bestanden am ${d}`,
    downloadCert: "Zertifikat herunterladen (HTML)", downloadCred: "Berechtigungsnachweis herunterladen (JSON)",
    // DN-51: the raw signed JWT itself (not wrapped in JSON) - the actual
    // Open Badges 3.0-conformant artifact a real badge wallet (Credly,
    // Open Badges Passport, etc.) expects for file-upload import. Only
    // shown once a record is genuinely signed - see renderJwtDownloadBtn().
    downloadJwt: "Signiertes Credential herunterladen (JWT, für Wallets)",
    disclaimer: "Selbst erstellter Nachweis, nicht kryptographisch signiert oder extern verifiziert.",
    // DN-44: simple renewal-due note for compliance modules that carry a
    // renewal_months value in their meta - only shown once the due date has
    // passed or is within 30 days (see renewalStatusForRecord()), not a
    // countdown for every completion.
    renewalOverdue: (d) => `Auffrischung überfällig seit ${d}`,
    renewalDueSoon: (d) => `Auffrischung fällig bis ${d}`,
    verifiedLabel: "✅ Signiertes Abzeichen", selfIssuedLabel: "Unbestätigt",
    verifiedHint: "Kryptographisch signiert, von Dritten überprüfbar.",
    selfIssuedHint: "Selbst erstellt, nicht signiert.",
    // DN-49: permanent, publicly shareable verification link for compliance
    // certificates (0€ MVP - see docs/paid-verifiable-certificates-scoping.md).
    verifyRowTitle: "Permanenter Prüflink",
    verifyRowIntro: "Für Compliance-Zertifikate: Erstelle einen dauerhaften Link, unter dem jeder (z. B. dein Arbeitgeber) die Signatur direkt online prüfen kann.",
    verifyNamePlaceholder: "Name (optional)",
    verifyCreateBtn: "Prüflink erstellen",
    verifyCreating: "Wird erstellt …",
    verifyLinkLabel: "Dein Prüflink:",
    verifyCopyBtn: "Kopieren",
    verifyCopiedBtn: "Kopiert!",
    verifyError: "Der Prüflink konnte nicht erstellt werden. Bitte später erneut versuchen.",
  },
  en: {
    btn: "My certificates", title: "My certificates", close: "← Back",
    intro: "Passed exam simulations are recorded here as proof of completion (this device only). Download a certificate file to keep or share it - that file is the actual portable artifact, not the app's internal state.",
    empty: "No passed exam simulation yet. Pass an Exam Simulation (not Training mode) to get a certificate here.",
    passedOn: (d) => `Passed on ${d}`,
    downloadCert: "Download certificate (HTML)", downloadCred: "Download credential (JSON)",
    downloadJwt: "Download signed credential (JWT, for wallets)",
    disclaimer: "Self-generated record, not cryptographically signed or independently verified.",
    renewalOverdue: (d) => `Refresher overdue since ${d}`,
    renewalDueSoon: (d) => `Refresher due by ${d}`,
    verifiedLabel: "✅ Signed badge", selfIssuedLabel: "Unverified",
    verifiedHint: "Cryptographically signed, independently verifiable by a third party.",
    selfIssuedHint: "Self-generated, not signed.",
    verifyRowTitle: "Permanent verification link",
    verifyRowIntro: "For compliance certificates: create a permanent link where anyone (e.g. your employer) can check the signature directly online.",
    verifyNamePlaceholder: "Name (optional)",
    verifyCreateBtn: "Create verification link",
    verifyCreating: "Creating …",
    verifyLinkLabel: "Your verification link:",
    verifyCopyBtn: "Copy",
    verifyCopiedBtn: "Copied!",
    verifyError: "Could not create the verification link. Please try again later.",
  },
  uk: {
    btn: "Мої сертифікати", title: "Мої сертифікати", close: "← Назад",
    intro: "Пройдені симуляції іспитів зберігаються тут як підтвердження (лише на цьому пристрої). Завантажте файл сертифіката, щоб зберегти або поділитися ним - саме цей файл є портативним артефактом, а не стан застосунку.",
    empty: "Ще немає пройденої симуляції іспиту. Пройдіть Симуляцію іспиту (не режим тренування), щоб отримати тут сертифікат.",
    passedOn: (d) => `Складено ${d}`,
    downloadCert: "Завантажити сертифікат (HTML)", downloadCred: "Завантажити посвідчення (JSON)",
    downloadJwt: "Завантажити підписане посвідчення (JWT, для гаманців)",
    disclaimer: "Самостійно створений запис, не підписаний криптографічно і не перевірений незалежно.",
    renewalOverdue: (d) => `Оновлення прострочено з ${d}`,
    renewalDueSoon: (d) => `Оновлення потрібне до ${d}`,
    verifiedLabel: "✅ Підписаний бейдж", selfIssuedLabel: "Не підтверджено",
    verifiedHint: "Криптографічно підписано, може бути перевірено третьою стороною.",
    selfIssuedHint: "Створено самостійно, не підписано.",
    verifyRowTitle: "Постійне посилання для перевірки",
    verifyRowIntro: "Для сертифікатів комплаєнсу: створіть постійне посилання, за яким будь-хто (наприклад, ваш роботодавець) може перевірити підпис онлайн.",
    verifyNamePlaceholder: "Ім'я (необов'язково)",
    verifyCreateBtn: "Створити посилання для перевірки",
    verifyCreating: "Створення…",
    verifyLinkLabel: "Ваше посилання для перевірки:",
    verifyCopyBtn: "Копіювати",
    verifyCopiedBtn: "Скопійовано!",
    verifyError: "Не вдалося створити посилання для перевірки. Спробуйте пізніше.",
  },
  pl: {
    btn: "Moje certyfikaty", title: "Moje certyfikaty", close: "← Wstecz",
    intro: "Zaliczone symulacje egzaminów są tu zapisywane jako dowód ukończenia (tylko na tym urządzeniu). Pobierz plik certyfikatu, aby go zachować lub udostępnić - to właśnie ten plik jest realnym, przenośnym artefaktem, a nie stan aplikacji.",
    empty: "Jeszcze żadnej zaliczonej symulacji egzaminu. Zdaj Symulację egzaminu (nie tryb ćwiczeń), aby otrzymać tu certyfikat.",
    passedOn: (d) => `Zaliczono ${d}`,
    downloadCert: "Pobierz certyfikat (HTML)", downloadCred: "Pobierz poświadczenie (JSON)",
    downloadJwt: "Pobierz podpisane poświadczenie (JWT, do portfeli)",
    disclaimer: "Zapis wygenerowany samodzielnie, niepodpisany kryptograficznie ani niezweryfikowany zewnętrznie.",
    renewalOverdue: (d) => `Odświeżenie zaległe od ${d}`,
    renewalDueSoon: (d) => `Odświeżenie wymagane do ${d}`,
    verifiedLabel: "✅ Podpisana odznaka", selfIssuedLabel: "Niezweryfikowane",
    verifiedHint: "Podpisane kryptograficznie, możliwe do niezależnej weryfikacji.",
    selfIssuedHint: "Wygenerowane samodzielnie, niepodpisane.",
    verifyRowTitle: "Stały link weryfikacyjny",
    verifyRowIntro: "Dla certyfikatów zgodności: utwórz stały link, pod którym każdy (np. Twój pracodawca) może bezpośrednio online sprawdzić podpis.",
    verifyNamePlaceholder: "Imię (opcjonalnie)",
    verifyCreateBtn: "Utwórz link weryfikacyjny",
    verifyCreating: "Tworzenie…",
    verifyLinkLabel: "Twój link weryfikacyjny:",
    verifyCopyBtn: "Kopiuj",
    verifyCopiedBtn: "Skopiowano!",
    verifyError: "Nie udało się utworzyć linku weryfikacyjnego. Spróbuj ponownie później.",
  },
  ar: {
    btn: "شهاداتي", title: "شهاداتي", close: "→ رجوع",
    intro: "يتم تسجيل محاكاة الامتحانات الناجحة هنا كإثبات للإتمام (على هذا الجهاز فقط). قم بتنزيل ملف الشهادة للاحتفاظ بها أو مشاركتها - هذا الملف هو العنصر المحمول الفعلي، وليس حالة التطبيق.",
    empty: "لا توجد محاكاة امتحان ناجحة بعد. اجتز محاكاة امتحان (وليس وضع التدريب) للحصول على شهادة هنا.",
    passedOn: (d) => `اجتيز في ${d}`,
    downloadCert: "تنزيل الشهادة (HTML)", downloadCred: "تنزيل بيانات الاعتماد (JSON)",
    downloadJwt: "تنزيل بيانات الاعتماد الموقّعة (JWT، للمحافظ)",
    disclaimer: "سجل ذاتي الإصدار، غير موقّع تشفيريًا وغير موثّق من طرف مستقل.",
    renewalOverdue: (d) => `التجديد متأخر منذ ${d}`,
    renewalDueSoon: (d) => `التجديد مستحق بحلول ${d}`,
    verifiedLabel: "✅ شارة موقّعة", selfIssuedLabel: "غير موثّق",
    verifiedHint: "موقّعة تشفيريًا، ويمكن لطرف مستقل التحقق منها.",
    selfIssuedHint: "تم إنشاؤها ذاتيًا، غير موقّعة.",
    verifyRowTitle: "رابط تحقق دائم",
    verifyRowIntro: "لشهادات الامتثال: أنشئ رابطًا دائمًا يمكن لأي شخص (مثل صاحب العمل) من خلاله التحقق من التوقيع مباشرة عبر الإنترنت.",
    verifyNamePlaceholder: "الاسم (اختياري)",
    verifyCreateBtn: "إنشاء رابط تحقق",
    verifyCreating: "جارٍ الإنشاء…",
    verifyLinkLabel: "رابط التحقق الخاص بك:",
    verifyCopyBtn: "نسخ",
    verifyCopiedBtn: "تم النسخ!",
    verifyError: "تعذّر إنشاء رابط التحقق. يرجى المحاولة لاحقًا.",
  },
  zh: {
    btn: "我的证书", title: "我的证书", close: "← 返回",
    intro: "已通过的模拟考试会记录在此作为完成证明(仅保存在本设备)。下载证书文件以保存或分享——该文件才是真正可移植的凭证,而不是应用内部状态。",
    empty: "尚无已通过的模拟考试。通过一次模拟考试(而非练习模式)即可在此获得证书。",
    passedOn: (d) => `通过日期:${d}`,
    downloadCert: "下载证书(HTML)", downloadCred: "下载凭证(JSON)",
    downloadJwt: "下载已签名凭证(JWT,供钱包应用使用)",
    disclaimer: "自行生成的记录,未经加密签名,也未经第三方独立验证。",
    renewalOverdue: (d) => `续期已逾期,截止日期为 ${d}`,
    renewalDueSoon: (d) => `续期截止日期为 ${d}`,
    verifiedLabel: "✅ 已签名徽章", selfIssuedLabel: "未验证",
    verifiedHint: "已加密签名,可由第三方独立验证。",
    selfIssuedHint: "自行生成,未签名。",
    verifyRowTitle: "永久验证链接",
    verifyRowIntro: "适用于合规证书:创建一个永久链接,任何人(例如你的雇主)都可以直接在线核实签名。",
    verifyNamePlaceholder: "姓名(可选)",
    verifyCreateBtn: "创建验证链接",
    verifyCreating: "正在创建…",
    verifyLinkLabel: "你的验证链接:",
    verifyCopyBtn: "复制",
    verifyCopiedBtn: "已复制!",
    verifyError: "无法创建验证链接,请稍后重试。",
  },
  hi: {
    btn: "मेरे प्रमाणपत्र", title: "मेरे प्रमाणपत्र", close: "← वापस",
    intro: "पास की गई परीक्षा सिमुलेशन यहाँ पूर्णता के प्रमाण के रूप में दर्ज की जाती हैं (केवल इस डिवाइस पर)। इसे रखने या साझा करने के लिए प्रमाणपत्र फ़ाइल डाउनलोड करें - वही असली पोर्टेबल फ़ाइल है, ऐप की आंतरिक स्थिति नहीं।",
    empty: "अभी तक कोई पास की गई परीक्षा सिमुलेशन नहीं है। यहाँ प्रमाणपत्र पाने के लिए एक परीक्षा सिमुलेशन (अभ्यास मोड नहीं) पास करें।",
    passedOn: (d) => `${d} को उत्तीर्ण`,
    downloadCert: "प्रमाणपत्र डाउनलोड करें (HTML)", downloadCred: "क्रेडेंशियल डाउनलोड करें (JSON)",
    downloadJwt: "हस्ताक्षरित क्रेडेंशियल डाउनलोड करें (JWT, वॉलेट के लिए)",
    disclaimer: "स्व-निर्मित रिकॉर्ड, क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित या स्वतंत्र रूप से सत्यापित नहीं।",
    renewalOverdue: (d) => `नवीनीकरण ${d} से लंबित`,
    renewalDueSoon: (d) => `नवीनीकरण ${d} तक देय`,
    verifiedLabel: "✅ हस्ताक्षरित बैज", selfIssuedLabel: "असत्यापित",
    verifiedHint: "क्रिप्टोग्राफ़िक रूप से हस्ताक्षरित, किसी तीसरे पक्ष द्वारा स्वतंत्र रूप से सत्यापन योग्य।",
    selfIssuedHint: "स्वयं निर्मित, हस्ताक्षरित नहीं।",
    verifyRowTitle: "स्थायी सत्यापन लिंक",
    verifyRowIntro: "अनुपालन प्रमाणपत्रों के लिए: एक स्थायी लिंक बनाएं जिससे कोई भी (जैसे आपका नियोक्ता) सीधे ऑनलाइन हस्ताक्षर की जांच कर सके।",
    verifyNamePlaceholder: "नाम (वैकल्पिक)",
    verifyCreateBtn: "सत्यापन लिंक बनाएं",
    verifyCreating: "बनाया जा रहा है…",
    verifyLinkLabel: "आपका सत्यापन लिंक:",
    verifyCopyBtn: "कॉपी करें",
    verifyCopiedBtn: "कॉपी हो गया!",
    verifyError: "सत्यापन लिंक नहीं बनाया जा सका। कृपया बाद में पुनः प्रयास करें।",
  },
  tr: {
    btn: "Sertifikalarım", title: "Sertifikalarım", close: "← Geri",
    intro: "Geçilen sınav simülasyonları burada tamamlanma kanıtı olarak kaydedilir (yalnızca bu cihazda). Saklamak veya paylaşmak için bir sertifika dosyası indirin - gerçek taşınabilir belge budur, uygulamanın iç durumu değil.",
    empty: "Henüz geçilmiş bir sınav simülasyonu yok. Burada bir sertifika almak için bir Sınav Simülasyonunu (Alıştırma modunu değil) geçin.",
    passedOn: (d) => `${d} tarihinde geçildi`,
    downloadCert: "Sertifikayı indir (HTML)", downloadCred: "Belgeyi indir (JSON)",
    downloadJwt: "İmzalı belgeyi indir (JWT, cüzdanlar için)",
    disclaimer: "Kendiliğinden oluşturulmuş kayıt, kriptografik olarak imzalanmamış veya bağımsız olarak doğrulanmamıştır.",
    renewalOverdue: (d) => `Yenileme ${d} tarihinden beri gecikmiş`,
    renewalDueSoon: (d) => `Yenileme ${d} tarihine kadar gerekli`,
    verifiedLabel: "✅ İmzalı rozet", selfIssuedLabel: "Doğrulanmamış",
    verifiedHint: "Kriptografik olarak imzalanmış, üçüncü bir taraf tarafından bağımsız olarak doğrulanabilir.",
    selfIssuedHint: "Kendiliğinden oluşturulmuş, imzalanmamış.",
    verifyRowTitle: "Kalıcı doğrulama bağlantısı",
    verifyRowIntro: "Uyumluluk sertifikaları için: herkesin (ör. işvereniniz) imzayı doğrudan çevrimiçi kontrol edebileceği kalıcı bir bağlantı oluşturun.",
    verifyNamePlaceholder: "İsim (opsiyonel)",
    verifyCreateBtn: "Doğrulama bağlantısı oluştur",
    verifyCreating: "Oluşturuluyor…",
    verifyLinkLabel: "Doğrulama bağlantınız:",
    verifyCopyBtn: "Kopyala",
    verifyCopiedBtn: "Kopyalandı!",
    verifyError: "Doğrulama bağlantısı oluşturulamadı. Lütfen daha sonra tekrar deneyin.",
  },
  fr: {
    btn: "Mes certificats", title: "Mes certificats", close: "← Retour",
    intro: "Les simulations d'examen réussies sont enregistrées ici comme preuve d'accomplissement (sur cet appareil uniquement). Téléchargez un fichier de certificat pour le conserver ou le partager - c'est ce fichier qui est réellement portable, pas l'état interne de l'application.",
    empty: "Aucune simulation d'examen réussie pour l'instant. Réussissez une Simulation d'examen (pas le mode Entraînement) pour obtenir un certificat ici.",
    passedOn: (d) => `Réussi le ${d}`,
    downloadCert: "Télécharger le certificat (HTML)", downloadCred: "Télécharger l'attestation (JSON)",
    downloadJwt: "Télécharger l'attestation signée (JWT, pour portefeuilles)",
    disclaimer: "Enregistrement auto-généré, non signé cryptographiquement et non vérifié de manière indépendante.",
    renewalOverdue: (d) => `Renouvellement en retard depuis le ${d}`,
    renewalDueSoon: (d) => `Renouvellement à effectuer avant le ${d}`,
    verifiedLabel: "✅ Badge signé", selfIssuedLabel: "Non vérifié",
    verifiedHint: "Signé cryptographiquement, vérifiable de manière indépendante par un tiers.",
    selfIssuedHint: "Auto-généré, non signé.",
    verifyRowTitle: "Lien de vérification permanent",
    verifyRowIntro: "Pour les certificats de conformité : créez un lien permanent où n'importe qui (par ex. votre employeur) peut vérifier la signature directement en ligne.",
    verifyNamePlaceholder: "Nom (facultatif)",
    verifyCreateBtn: "Créer un lien de vérification",
    verifyCreating: "Création en cours…",
    verifyLinkLabel: "Votre lien de vérification :",
    verifyCopyBtn: "Copier",
    verifyCopiedBtn: "Copié !",
    verifyError: "Impossible de créer le lien de vérification. Veuillez réessayer plus tard.",
  },
  ru: {
    btn: "Мои сертификаты", title: "Мои сертификаты", close: "← Назад",
    intro: "Пройденные симуляции экзаменов сохраняются здесь как подтверждение прохождения (только на этом устройстве). Скачайте файл сертификата, чтобы сохранить или передать его - именно этот файл является настоящим переносимым артефактом, а не состояние приложения.",
    empty: "Пока нет пройденной симуляции экзамена. Пройдите Симуляцию экзамена (не режим тренировки), чтобы получить здесь сертификат.",
    passedOn: (d) => `Пройдено ${d}`,
    downloadCert: "Скачать сертификат (HTML)", downloadCred: "Скачать удостоверение (JSON)",
    downloadJwt: "Скачать подписанное удостоверение (JWT, для кошельков)",
    disclaimer: "Самостоятельно созданная запись, не подписана криптографически и не проверена независимо.",
    renewalOverdue: (d) => `Обновление просрочено с ${d}`,
    renewalDueSoon: (d) => `Обновление требуется до ${d}`,
    verifiedLabel: "✅ Подписанный значок", selfIssuedLabel: "Не подтверждено",
    verifiedHint: "Подписано криптографически, может быть независимо проверено третьей стороной.",
    selfIssuedHint: "Создано самостоятельно, не подписано.",
    verifyRowTitle: "Постоянная ссылка для проверки",
    verifyRowIntro: "Для сертификатов соответствия: создайте постоянную ссылку, по которой любой (например, ваш работодатель) может напрямую проверить подпись онлайн.",
    verifyNamePlaceholder: "Имя (необязательно)",
    verifyCreateBtn: "Создать ссылку для проверки",
    verifyCreating: "Создание…",
    verifyLinkLabel: "Ваша ссылка для проверки:",
    verifyCopyBtn: "Копировать",
    verifyCopiedBtn: "Скопировано!",
    verifyError: "Не удалось создать ссылку для проверки. Попробуйте позже.",
  },
  es: {
    btn: "Mis certificados", title: "Mis certificados", close: "← Atrás",
    intro: "Las simulaciones de examen aprobadas se registran aquí como comprobante de finalización (solo en este dispositivo). Descarga un archivo de certificado para conservarlo o compartirlo - ese archivo es el elemento realmente portátil, no el estado interno de la aplicación.",
    empty: "Todavía no hay ninguna simulación de examen aprobada. Aprueba una Simulación de examen (no el modo Entrenamiento) para obtener aquí un certificado.",
    passedOn: (d) => `Aprobado el ${d}`,
    downloadCert: "Descargar certificado (HTML)", downloadCred: "Descargar credencial (JSON)",
    downloadJwt: "Descargar credencial firmada (JWT, para carteras)",
    disclaimer: "Registro autogenerado, no firmado criptográficamente ni verificado de forma independiente.",
    renewalOverdue: (d) => `Renovación vencida desde el ${d}`,
    renewalDueSoon: (d) => `Renovación necesaria antes del ${d}`,
    verifiedLabel: "✅ Insignia firmada", selfIssuedLabel: "No verificado",
    verifiedHint: "Firmado criptográficamente, verificable de forma independiente por un tercero.",
    selfIssuedHint: "Autogenerado, no firmado.",
    verifyRowTitle: "Enlace de verificación permanente",
    verifyRowIntro: "Para certificados de cumplimiento: crea un enlace permanente donde cualquiera (p. ej. tu empleador) pueda comprobar la firma directamente en línea.",
    verifyNamePlaceholder: "Nombre (opcional)",
    verifyCreateBtn: "Crear enlace de verificación",
    verifyCreating: "Creando…",
    verifyLinkLabel: "Tu enlace de verificación:",
    verifyCopyBtn: "Copiar",
    verifyCopiedBtn: "¡Copiado!",
    verifyError: "No se pudo crear el enlace de verificación. Inténtalo de nuevo más tarde.",
  },
  it: {
    btn: "I miei certificati", title: "I miei certificati", close: "← Indietro",
    intro: "Le simulazioni d'esame superate vengono registrate qui come prova di completamento (solo su questo dispositivo). Scarica un file certificato per conservarlo o condividerlo - quel file è il vero elemento portatile, non lo stato interno dell'app.",
    empty: "Ancora nessuna simulazione d'esame superata. Supera una Simulazione d'esame (non la modalità Allenamento) per ottenere qui un certificato.",
    passedOn: (d) => `Superato il ${d}`,
    downloadCert: "Scarica certificato (HTML)", downloadCred: "Scarica credenziale (JSON)",
    downloadJwt: "Scarica credenziale firmata (JWT, per wallet)",
    disclaimer: "Registro autogenerato, non firmato crittograficamente né verificato in modo indipendente.",
    renewalOverdue: (d) => `Rinnovo scaduto dal ${d}`,
    renewalDueSoon: (d) => `Rinnovo da effettuare entro il ${d}`,
    verifiedLabel: "✅ Badge firmato", selfIssuedLabel: "Non verificato",
    verifiedHint: "Firmato crittograficamente, verificabile in modo indipendente da terzi.",
    selfIssuedHint: "Autogenerato, non firmato.",
    verifyRowTitle: "Link di verifica permanente",
    verifyRowIntro: "Per i certificati di conformità: crea un link permanente con cui chiunque (ad es. il tuo datore di lavoro) può verificare la firma direttamente online.",
    verifyNamePlaceholder: "Nome (facoltativo)",
    verifyCreateBtn: "Crea link di verifica",
    verifyCreating: "Creazione…",
    verifyLinkLabel: "Il tuo link di verifica:",
    verifyCopyBtn: "Copia",
    verifyCopiedBtn: "Copiato!",
    verifyError: "Impossibile creare il link di verifica. Riprova più tardi.",
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

// DN-49: once a permanent verification link has been created for a record
// (see createVerifyLink() below), remember it in the same localStorage
// completion record so re-opening "My certificates" later shows the
// existing link instead of silently offering to create a second one.
function persistVerifyUrl(record) {
  try {
    const all = getCompletions();
    const idx = all.findIndex((r) => r.id === record.id);
    if (idx === -1) return;
    all[idx] = { ...all[idx], verifyUrl: record.verifyUrl };
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

// DN-51 fix (see docs/badge-wallet-portability-scoping.md section 4): two
// external OB3 validators (CertLister, 1EdTech's own validator) run against
// a real signed credential earlier flagged two concrete spec-conformance
// gaps in this function's output:
//   1. `achievement` had no `id` (OB3 requires a URI here) - fixed below,
//      using a stable per-module+scope URI (the achievement DEFINITION,
//      shared by every earner, not this one earner's instance of it -
//      mirrors netlify/functions/sign-credential.js's buildCredentialClaims,
//      which needed the identical fix for the real signed JWT this
//      function's unsigned fallback is modeled on).
//   2. The old `proof: {type: "JsonWebSignature", jwt: ...}` field was a
//      custom shape that isn't what OB3/VC validators expect for a JOSE or
//      Data-Integrity proof - because OB3's actual JWT-secured form treats
//      the compact JWS itself (three dot-separated parts) as the
//      verifiable artifact, not a JSON document with the JWT nested inside
//      a `proof` field. Zettacard already ships that real artifact
//      separately via the "Download signed credential (JWT, for wallets)"
//      button (record.signedJwt as its own file, done 2026-08-07) - so
//      rather than inventing another non-standard `proof` shape here, this
//      JSON document now says plainly that it's a human-readable reference
//      copy and points at the real verifiable download instead of claiming
//      a proof mechanism it doesn't actually have.
function credentialJsonDoc(record) {
  const base = {
    "@context": ["https://www.w3.org/ns/credentials/v2", "https://purl.imsglobal.org/spec/ob/v3p0/context.json"],
    id: `${location.origin || ""}/credentials/${record.id}`,
    type: ["VerifiableCredential", "OpenBadgeCredential"],
    validFrom: record.passedAt,
    credentialSubject: {
      type: "AchievementSubject",
      achievement: {
        id: `${location.origin || ""}/achievements/${record.examType}-${record.scopeCode}`,
        type: "Achievement",
        name: `${record.moduleLabel} - ${record.scopeLabel}`,
        description: `Passed an Exam Simulation for ${record.moduleLabel} (${record.scopeLabel}) in the Zettacard app.`,
        criteria: { narrative: `${record.totalQuestions}-question simulated exam, ${record.errorPoints} error points, ${record.wrongHighStakes} wrong safety-critical answer(s).` },
      },
    },
  };

  // Real signature available (netlify/functions/sign-credential.js
  // succeeded at some point for this record - see trySignCompletion()):
  // note the signature's existence/metadata for reference, but this JSON
  // document is explicitly NOT presented as the verifiable artifact itself
  // - see the function-level comment above. Drop the
  // unverified/unverifiedReason fields since they'd be actively false.
  // See docs/open-badges-signing-verification.md for how a third party
  // checks the real signed JWT (the separate download) themselves.
  if (record.verified && record.signedJwt) {
    return {
      ...base,
      issuer: { type: "Profile", id: (location.origin || ""), name: "Zettacard" },
      verified: true,
      signedJwtNote: "This JSON document is a human-readable reference copy only, not itself the verifiable credential. Use the separate signed-JWT download (a compact JWS) for actual OB3/W3C-VC verification.",
      signedJwtAlg: record.signedAlg || "ES256",
      signedJwtKid: record.signedKid,
      jwksUrl: `${location.origin || ""}/.well-known/jwks.json`,
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
      <div class="cert-badge-row"></div>
      <div class="cert-card-title">${record.moduleLabel} · ${record.scopeLabel}</div>
      <div class="cert-card-date">${C.passedOn(dateStr)}</div>
      <div class="cert-card-renewal"></div>
      <div class="cert-card-actions">
        <button class="back-btn cert-dl-cert">${C.downloadCert}</button>
        <button class="back-btn cert-dl-cred">${C.downloadCred}</button>
      </div>
      <div class="cert-jwt-row"></div>
      <div class="cert-verify-row"></div>
    `;
    renderBadgeRow(card.querySelector(".cert-badge-row"), record, C);
    renderJwtDownloadBtn(card.querySelector(".cert-jwt-row"), record, C);
    renderVerifyLinkRow(card.querySelector(".cert-verify-row"), record, C);
    card.querySelector(".cert-dl-cert").addEventListener("click", () => {
      downloadTextFile(`${record.examType}-${record.scopeCode}-certificate.html`, certificateHtmlDoc(record), "text/html");
    });
    card.querySelector(".cert-dl-cred").addEventListener("click", async () => {
      // Give an unsigned/already-attempted record one more chance to get a
      // real signature (e.g. the device just came back online) before
      // building the download - falls back silently if it can't.
      await ensureSignedCredential(record);
      renderBadgeRow(card.querySelector(".cert-badge-row"), record, C);
      renderJwtDownloadBtn(card.querySelector(".cert-jwt-row"), record, C);
      renderVerifyLinkRow(card.querySelector(".cert-verify-row"), record, C);
      downloadTextFile(`${record.examType}-${record.scopeCode}-credential.json`, JSON.stringify(credentialJsonDoc(record), null, 2), "application/json");
    });
    list.appendChild(card);

    // If this record isn't signed yet (background attempt from
    // recordCompletion() may still be in flight, was offline at the time,
    // or this is an older completion from before real signing existed),
    // give it one more fresh, non-blocking attempt right here so a visitor
    // who opens "My certificates" shortly after passing doesn't see a
    // stale "unverified" badge that a moment later would actually be real.
    // Mirrors the same non-blocking upgrade-in-place pattern the renewal
    // check below already uses.
    if (!record.verified) {
      ensureSignedCredential(record).then(() => {
        renderBadgeRow(card.querySelector(".cert-badge-row"), record, C);
        renderJwtDownloadBtn(card.querySelector(".cert-jwt-row"), record, C);
        renderVerifyLinkRow(card.querySelector(".cert-verify-row"), record, C);
      });
    }

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

// Renders the actual visual "badge" for a completion: a circular emblem
// (gold + checkmark for a real cryptographically-signed credential, plain
// grey outline for a self-issued/unverified one) plus a short status label
// and one-line explanation - so a real signed badge is visibly, not just
// technically, distinguishable from the honest-but-unsigned fallback.
function renderBadgeRow(slot, record, C) {
  if (!slot) return;
  const verified = !!(record.verified && record.signedJwt);
  slot.innerHTML = `
    <span class="cert-badge-emblem ${verified ? "verified" : "self-issued"}" aria-hidden="true">${verified ? "🏅" : "🎫"}</span>
    <span class="cert-badge-text">
      <span class="badge ${verified ? "verified" : "self-issued"}">${verified ? C.verifiedLabel : C.selfIssuedLabel}</span>
      <span class="cert-badge-hint">${verified ? C.verifiedHint : C.selfIssuedHint}</span>
    </span>
  `;
}

// --- Permanent verification link (DN-49, 0€ MVP) ------------------------
// Calls save-verified-credential.js, which independently re-verifies the
// signature server-side before persisting anything (see that function's
// own comments) - this call is best-effort and offline-safe like the
// signing flow above: on any failure the record simply stays without a
// verifyUrl and the button remains available to retry later.
// Function is named "save-verified-credential-v2" (not
// "save-verified-credential") - see netlify.toml's /verify/* redirect
// comment for why (a stale deploy-caching issue with the original name).
const SAVE_VERIFIED_CREDENTIAL_ENDPOINT = "/.netlify/functions/save-verified-credential-v2";
const SAVE_VERIFIED_CREDENTIAL_TIMEOUT_MS = 8000;

async function createVerifyLink(record, participantName) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SAVE_VERIFIED_CREDENTIAL_TIMEOUT_MS);
  try {
    const res = await fetch(SAVE_VERIFIED_CREDENTIAL_ENDPOINT, {
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
        signedJwt: record.signedJwt,
        signedKid: record.signedKid,
        signedAlg: record.signedAlg,
        participantName: participantName || undefined,
      }),
      signal: controller.signal,
    });
    if (!res.ok) return null;
    const body = await res.json();
    if (!body || !body.verifyUrl) return null;
    record.verifyUrl = body.verifyUrl;
    persistVerifyUrl(record);
    return body.verifyUrl;
  } catch (e) {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

// Renders the "get a permanent, shareable verification link" row for a
// completion card. Only ever shown for the compliance modules (COMPLIANCE_
// MODULES - originally 4 under DN-44, now 5 since DN-50 added
// hinweisgeberschutz) AND only once the record actually has a real
// signature (verified + signedJwt) - a self-issued/unverified record isn't
// eligible, same gating the backend function independently enforces
// itself (see save-verified-credential-v2.mjs - this exact allowlist drift
// was a real bug found and fixed 2026-08-08: that function's own
// COMPLIANCE_EXAM_TYPES set had not been updated when hinweisgeberschutz
// was added, so this button would have shown but the request would have
// 400'd).
function renderVerifyLinkRow(slot, record, C) {
  if (!slot) return;
  if (!COMPLIANCE_MODULES.has(record.examType) || !(record.verified && record.signedJwt)) {
    slot.innerHTML = "";
    return;
  }
  if (record.verifyUrl) {
    slot.innerHTML = `
      <div class="cert-verify-title">${C.verifyRowTitle}</div>
      <div class="cert-verify-link-row">
        <a class="cert-verify-link" href="${record.verifyUrl}" target="_blank" rel="noopener">${record.verifyUrl}</a>
        <button type="button" class="back-btn cert-verify-copy-btn">${C.verifyCopyBtn}</button>
      </div>
    `;
    slot.querySelector(".cert-verify-copy-btn").addEventListener("click", async () => {
      const btn = slot.querySelector(".cert-verify-copy-btn");
      try {
        await navigator.clipboard.writeText(record.verifyUrl);
        btn.textContent = C.verifyCopiedBtn;
        setTimeout(() => { btn.textContent = C.verifyCopyBtn; }, 2000);
      } catch (e) { /* clipboard API unavailable - link is still selectable/openable */ }
    });
    return;
  }
  slot.innerHTML = `
    <div class="cert-verify-title">${C.verifyRowTitle}</div>
    <div class="cert-verify-intro">${C.verifyRowIntro}</div>
    <div class="cert-verify-form">
      <input type="text" class="cert-verify-name-input" placeholder="${C.verifyNamePlaceholder}" maxlength="100">
      <button type="button" class="back-btn cert-verify-create-btn">${C.verifyCreateBtn}</button>
    </div>
  `;
  slot.querySelector(".cert-verify-create-btn").addEventListener("click", async () => {
    const btn = slot.querySelector(".cert-verify-create-btn");
    const nameInput = slot.querySelector(".cert-verify-name-input");
    btn.disabled = true;
    btn.textContent = C.verifyCreating;
    const url = await createVerifyLink(record, nameInput.value.trim());
    if (url) {
      renderVerifyLinkRow(slot, record, C);
    } else {
      btn.disabled = false;
      btn.textContent = C.verifyCreateBtn;
      const err = document.createElement("div");
      err.className = "cert-verify-error";
      err.textContent = C.verifyError;
      slot.appendChild(err);
    }
  });
}

// DN-51 (docs/badge-wallet-portability-scoping.md): the raw signed JWT
// itself, as a standalone downloadable file - NOT wrapped in JSON like
// credentialJsonDoc()'s existing download. Real badge wallets (Credly,
// Open Badges Passport, etc.) that accept third-party badges via file
// upload expect the actual OB3-compliant compact JWS, which is exactly
// record.signedJwt - the JSON credential download is a human-readable
// reference copy (see credentialJsonDoc()'s own comment for the full
// history: it used to nest this same JWT inside a custom `proof.jwt`
// field, which a real wallet import would not recognize as a valid OB3
// proof - since fixed to stop claiming a proof shape it doesn't have).
// Only ever shown once a record is genuinely signed (same verified+
// signedJwt gate as the badge/verify-link rows) - a self-issued/unverified
// record has no JWT to offer.
function renderJwtDownloadBtn(slot, record, C) {
  if (!slot) return;
  if (!(record.verified && record.signedJwt)) {
    slot.innerHTML = "";
    return;
  }
  slot.innerHTML = `<button type="button" class="back-btn cert-dl-jwt">${C.downloadJwt}</button>`;
  slot.querySelector(".cert-dl-jwt").addEventListener("click", () => {
    downloadTextFile(`${record.examType}-${record.scopeCode}-credential.jwt`, record.signedJwt, "text/plain");
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

// --- DN-14: "seen" tracking + manual star/bookmark ---------------------
// Two independent, lightweight per-question-id-keyed localStorage maps,
// following the exact same profileKey()-namespaced convention as
// loadSrsData()/saveSrsData() above - neither one touches or is touched by
// the Leitner box logic, and neither depends on the exam-completion system.
//
// "Seen": { [questionId]: <epoch ms first seen> }. Pure bookkeeping for a
// future stat (e.g. "you've seen 120 of 500 questions") - no UI surfaces it
// directly yet, so this is intentionally just a reliable write, not a
// feature in itself.
function loadSeenData() {
  try {
    const raw = JSON.parse(localStorage.getItem(profileKey("seen")) || "{}");
    return raw && typeof raw === "object" ? raw : {};
  } catch (e) {
    return {};
  }
}

function markSeen(questionId) {
  const seen = loadSeenData();
  if (seen[questionId]) return; // already recorded - avoid a redundant write on every render
  seen[questionId] = Date.now();
  try { localStorage.setItem(profileKey("seen"), JSON.stringify(seen)); } catch (e) { /* non-fatal */ }
}

// "Starred": { [questionId]: true }. A manual bookmark independent of
// whether the user got the question right or wrong and independent of the
// Leitner box - purely "I want to find this again later." Surfaced via the
// star toggle button in #detail-view and the "starred only" filter chip in
// the main list (see renderFilters()/filteredQuestions() below).
function loadStarredData() {
  try {
    const raw = JSON.parse(localStorage.getItem(profileKey("starred")) || "{}");
    return raw && typeof raw === "object" ? raw : {};
  } catch (e) {
    return {};
  }
}

function saveStarredData(data) {
  try { localStorage.setItem(profileKey("starred"), JSON.stringify(data)); } catch (e) { /* non-fatal */ }
}

function isStarred(questionId) {
  return !!loadStarredData()[questionId];
}

function toggleStarred(questionId) {
  const starred = loadStarredData();
  if (starred[questionId]) delete starred[questionId];
  else starred[questionId] = true;
  saveStarredData(starred);
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
  de: { reviewBtn: (n) => `📅 Wiederholen (${n})`, reviewAria: "Fällige Wiederholungen", know: "Ich wusste es", dontKnow: "Ich wusste es nicht", caption: "Wie lief's mit dieser Karte?" },
  en: { reviewBtn: (n) => `📅 Review (${n})`, reviewAria: "Questions due for review", know: "I knew it", dontKnow: "I didn't know it", caption: "How did that go?" },
  uk: { reviewBtn: (n) => `📅 Повторення (${n})`, reviewAria: "Питання для повторення", know: "Я знав(ла) це", dontKnow: "Я не знав(ла) цього", caption: "Як пройшло з цією карткою?" },
  pl: { reviewBtn: (n) => `📅 Powtórka (${n})`, reviewAria: "Pytania do powtórki", know: "Wiedziałem/am to", dontKnow: "Nie wiedziałem/am tego", caption: "Jak poszło z tą kartą?" },
  ar: { reviewBtn: (n) => `📅 مراجعة (${n})`, reviewAria: "أسئلة مستحقة للمراجعة", know: "كنت أعرف ذلك", dontKnow: "لم أكن أعرف ذلك", caption: "كيف سارت الأمور مع هذه البطاقة؟" },
  zh: { reviewBtn: (n) => `📅 复习 (${n})`, reviewAria: "待复习的问题", know: "我知道", dontKnow: "我不知道", caption: "这张卡片答得怎么样？" },
  hi: { reviewBtn: (n) => `📅 पुनरावृत्ति (${n})`, reviewAria: "समीक्षा हेतु प्रश्न", know: "मुझे पता था", dontKnow: "मुझे नहीं पता था", caption: "इस कार्ड के साथ कैसा रहा?" },
  tr: { reviewBtn: (n) => `📅 Tekrar (${n})`, reviewAria: "Tekrar edilecek sorular", know: "Biliyordum", dontKnow: "Bilmiyordum", caption: "Bu kartla nasıl gitti?" },
  fr: { reviewBtn: (n) => `📅 Révision (${n})`, reviewAria: "Questions à réviser", know: "Je le savais", dontKnow: "Je ne le savais pas", caption: "Comment ça s'est passé avec cette carte ?" },
  ru: { reviewBtn: (n) => `📅 Повтор (${n})`, reviewAria: "Вопросы для повторения", know: "Я знал(а) это", dontKnow: "Я не знал(а) этого", caption: "Как прошло с этой карточкой?" },
  es: { reviewBtn: (n) => `📅 Repaso (${n})`, reviewAria: "Preguntas para repasar", know: "Lo sabía", dontKnow: "No lo sabía", caption: "¿Cómo te fue con esta tarjeta?" },
  it: { reviewBtn: (n) => `📅 Ripasso (${n})`, reviewAria: "Domande da ripassare", know: "Lo sapevo", dontKnow: "Non lo sapevo", caption: "Come è andata con questa carta?" },
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
      state.detailPick = null; // DN: clear any in-progress self-answer attempt when moving to a (possibly new) question
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
      state.detailPick = null; // DN: clear any in-progress self-answer attempt when moving to a (possibly new) question
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
// facts with that discipline. Extended to all 12 locales (follow-up to
// DN-28, 2026-08-08) - both the reference content itself (build_sign_
// reference.py now derives it from fuehrerschein's already-fully-
// translated question data, so no new translation was needed there) and
// this surrounding UI chrome (translated directly, same convention as
// MODULE_PICKER_STRINGS/CERT_STRINGS elsewhere).
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
  uk: {
    btn: "📚 Знаки", ariaLabel: "Довідник знаків", title: "Довідник знаків",
    intro: "Усі дорожні знаки, що зустрічаються у питаннях модуля Führerschein, з їхнім значенням - згруповані за типом знаку.",
    close: "← Назад", empty: "Довідник знаків недоступний.",
  },
  pl: {
    btn: "📚 Znaki", ariaLabel: "Katalog znaków", title: "Katalog znaków",
    intro: "Wszystkie znaki drogowe występujące w pytaniach modułu Führerschein, wraz ze znaczeniem - pogrupowane według rodzaju znaku.",
    close: "← Wstecz", empty: "Katalog znaków niedostępny.",
  },
  ar: {
    btn: "📚 الإشارات", ariaLabel: "دليل الإشارات", title: "دليل الإشارات",
    intro: "جميع إشارات المرور الواردة في أسئلة وحدة رخصة القيادة، مع معانيها - مصنفة حسب نوع الإشارة.",
    close: "← رجوع", empty: "دليل الإشارات غير متوفر.",
  },
  zh: {
    btn: "📚 标志", ariaLabel: "标志参考", title: "标志参考",
    intro: "驾照模块题目中出现的所有交通标志及其含义 - 按标志类别分组。",
    close: "← 返回", empty: "暂无标志参考资料。",
  },
  hi: {
    btn: "📚 संकेत", ariaLabel: "संकेत संदर्भ", title: "संकेत संदर्भ",
    intro: "ड्राइविंग-लाइसेंस मॉड्यूल के प्रश्नों में आने वाले सभी यातायात संकेत, उनके अर्थ सहित - संकेत प्रकार के अनुसार समूहीकृत।",
    close: "← वापस", empty: "कोई संकेत संदर्भ उपलब्ध नहीं है।",
  },
  tr: {
    btn: "📚 İşaretler", ariaLabel: "İşaret referansı", title: "İşaret referansı",
    intro: "Sürücü belgesi modülü sorularında geçen tüm trafik işaretleri, anlamlarıyla birlikte - işaret türüne göre gruplandırılmış.",
    close: "← Geri", empty: "İşaret referansı mevcut değil.",
  },
  fr: {
    btn: "📚 Panneaux", ariaLabel: "Référence des panneaux", title: "Référence des panneaux",
    intro: "Tous les panneaux de signalisation cités dans les questions du module Permis de conduire, avec leur signification - regroupés par catégorie.",
    close: "← Retour", empty: "Aucune référence de panneaux disponible.",
  },
  ru: {
    btn: "📚 Знаки", ariaLabel: "Справочник знаков", title: "Справочник знаков",
    intro: "Все дорожные знаки, встречающиеся в вопросах модуля «Водительские права», с их значением - сгруппированы по типу знака.",
    close: "← Назад", empty: "Справочник знаков недоступен.",
  },
  es: {
    btn: "📚 Señales", ariaLabel: "Referencia de señales", title: "Referencia de señales",
    intro: "Todas las señales de tráfico citadas en las preguntas del módulo de permiso de conducir, con su significado - agrupadas por categoría.",
    close: "← Atrás", empty: "No hay referencia de señales disponible.",
  },
  it: {
    btn: "📚 Segnali", ariaLabel: "Riferimento segnali", title: "Riferimento segnali",
    intro: "Tutti i segnali stradali citati nelle domande del modulo Patente di guida, con il loro significato - raggruppati per categoria.",
    close: "← Indietro", empty: "Nessun riferimento sui segnali disponibile.",
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
  gefahrzeichen: {
    de: "Gefahrzeichen", en: "Warning signs", uk: "Попереджувальні знаки", pl: "Znaki ostrzegawcze",
    ar: "إشارات التحذير", zh: "警告标志", hi: "चेतावनी संकेत", tr: "Tehlike/uyarı işaretleri",
    fr: "Panneaux de danger", ru: "Предупреждающие знаки", es: "Señales de peligro", it: "Segnali di pericolo",
  },
  verbotszeichen: {
    de: "Verbotszeichen", en: "Prohibition signs", uk: "Заборонні знаки", pl: "Znaki zakazu",
    ar: "إشارات المنع", zh: "禁令标志", hi: "निषेध संकेत", tr: "Yasaklama işaretleri",
    fr: "Panneaux d'interdiction", ru: "Запрещающие знаки", es: "Señales de prohibición", it: "Segnali di divieto",
  },
  gebotszeichen: {
    de: "Gebotszeichen", en: "Mandatory signs", uk: "Наказові знаки", pl: "Znaki nakazu",
    ar: "إشارات الإلزام", zh: "指示标志", hi: "आदेशात्मक संकेत", tr: "Zorunluluk işaretleri",
    fr: "Panneaux d'obligation", ru: "Предписывающие знаки", es: "Señales de obligación", it: "Segnali di obbligo",
  },
  richtzeichen: {
    de: "Richtzeichen", en: "Informational signs", uk: "Інформаційні знаки", pl: "Znaki informacyjne",
    ar: "إشارات إرشادية", zh: "指示标志（信息类）", hi: "सूचनात्मक संकेत", tr: "Bilgi işaretleri",
    fr: "Panneaux d'indication", ru: "Информационные знаки", es: "Señales informativas", it: "Segnali di indicazione",
  },
  sonstige: {
    de: "Sonstige", en: "Other", uk: "Інші", pl: "Pozostałe",
    ar: "أخرى", zh: "其他", hi: "अन्य", tr: "Diğer",
    fr: "Autres", ru: "Прочие", es: "Otras", it: "Altri",
  },
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
      // build_sign_reference.py now derives this catalog's name/desc for
      // all 12 locales (previously de/en-only - see that script's own
      // header comment), so read the current UI language directly with
      // the same en-then-de fallback chain used elsewhere in this file.
      const localized = entry[state.lang] || entry.en || entry.de;
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

// --- Kickstart-learning-journey topic primers (DN-52 Phase 1) -----------
// Short 5-10 minute "learn the basics" guides that bridge a total beginner
// to a Fuehrerschein exam topic before they start practicing real exam
// questions - one for sign shapes/categories plus one per topic (11 topics,
// matching TOPIC_LABELS.fuehrerschein exactly). Content is original,
// grounded in verified sample questions from pilot_questions.json plus
// well-established StVO/StVZO/StVG/StGB structure - see
// docs/kickstart-learning-journey-scoping.md and data/build_primers.py's
// header comment for the full sourcing/pipeline discipline. Fuehrerschein-
// only for now (Phase 5 of the scoping doc is the stretch goal of rolling
// primers out to other modules) - same visibility pattern as Sign Reference.
const PRIMER_STRINGS = {
  de: {
    btn: "🧭 Lernen", ariaLabel: "Grundlagen lernen", title: "Die Grundlagen lernen",
    intro: "Kurze 5-10-Minuten-Einführungen in jedes Prüfungsthema, bevor du mit echten Übungsfragen startest.",
    close: "← Zurück", empty: "Keine Einführungen verfügbar.",
    shapeCategoryLabel: "Schilderformen und -kategorien",
    next: "Weiter", back: "← Zurück", exit: "Beenden", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Jetzt Übungsfragen dazu starten",
  },
  en: {
    btn: "🧭 Learn", ariaLabel: "Learn the basics", title: "Learn the basics",
    intro: "Short 5-10 minute introductions to each exam topic, before you start practicing real exam questions.",
    close: "← Back", empty: "No introductions available.",
    shapeCategoryLabel: "Sign shapes & categories",
    next: "Next", back: "← Back", exit: "Exit", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Practice this topic now",
  },
  uk: {
    btn: "🧭 Навчання", ariaLabel: "Вивчити основи", title: "Вивчити основи",
    intro: "Короткі 5-10-хвилинні вступи до кожної теми іспиту, перш ніж почати практикувати реальні питання.",
    close: "← Назад", empty: "Немає доступних вступів.",
    shapeCategoryLabel: "Форми та категорії знаків",
    next: "Далі", back: "← Назад", exit: "Вийти", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Практикувати цю тему зараз",
  },
  pl: {
    btn: "🧭 Nauka", ariaLabel: "Poznaj podstawy", title: "Poznaj podstawy",
    intro: "Krótkie 5-10-minutowe wprowadzenia do każdego tematu egzaminu, zanim zaczniesz ćwiczyć prawdziwe pytania.",
    close: "← Wstecz", empty: "Brak dostępnych wprowadzeń.",
    shapeCategoryLabel: "Kształty i kategorie znaków",
    next: "Dalej", back: "← Wstecz", exit: "Zakończ", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Ćwicz ten temat teraz",
  },
  ar: {
    btn: "🧭 تعلّم", ariaLabel: "تعلّم الأساسيات", title: "تعلّم الأساسيات",
    intro: "مقدمات قصيرة من 5 إلى 10 دقائق لكل موضوع في الامتحان، قبل أن تبدأ بممارسة أسئلة الامتحان الحقيقية.",
    close: "← رجوع", empty: "لا توجد مقدمات متاحة.",
    shapeCategoryLabel: "أشكال وفئات الإشارات",
    next: "التالي", back: "← رجوع", exit: "خروج", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "تدرّب على هذا الموضوع الآن",
  },
  zh: {
    btn: "🧭 学习", ariaLabel: "学习基础知识", title: "学习基础知识",
    intro: "在开始练习真实考试题之前，先花5到10分钟简要了解每个考试主题。",
    close: "← 返回", empty: "暂无可用的入门介绍。",
    shapeCategoryLabel: "标志形状与分类",
    next: "下一步", back: "← 返回", exit: "退出", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "现在练习这个主题",
  },
  hi: {
    btn: "🧭 सीखें", ariaLabel: "बुनियादी बातें सीखें", title: "बुनियादी बातें सीखें",
    intro: "असली परीक्षा प्रश्नों का अभ्यास शुरू करने से पहले, हर विषय का 5-10 मिनट का संक्षिप्त परिचय।",
    close: "← वापस", empty: "कोई परिचय उपलब्ध नहीं है।",
    shapeCategoryLabel: "संकेत आकार और श्रेणियाँ",
    next: "आगे", back: "← वापस", exit: "बाहर निकलें", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "अभी इस विषय का अभ्यास करें",
  },
  tr: {
    btn: "🧭 Öğren", ariaLabel: "Temelleri öğren", title: "Temelleri öğren",
    intro: "Gerçek sınav sorularını pratik etmeye başlamadan önce her konuya kısa 5-10 dakikalık giriş.",
    close: "← Geri", empty: "Kullanılabilir giriş yok.",
    shapeCategoryLabel: "İşaret şekilleri ve kategorileri",
    next: "İleri", back: "← Geri", exit: "Çık", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Bu konuyu şimdi pratik et",
  },
  fr: {
    btn: "🧭 Apprendre", ariaLabel: "Apprendre les bases", title: "Apprendre les bases",
    intro: "De courtes introductions de 5 à 10 minutes à chaque thème d'examen, avant de pratiquer de vraies questions.",
    close: "← Retour", empty: "Aucune introduction disponible.",
    shapeCategoryLabel: "Formes et catégories des panneaux",
    next: "Suivant", back: "← Retour", exit: "Quitter", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Pratiquer ce thème maintenant",
  },
  ru: {
    btn: "🧭 Учиться", ariaLabel: "Изучить основы", title: "Изучить основы",
    intro: "Краткие введения по 5-10 минут в каждую тему экзамена, прежде чем начать практиковать реальные вопросы.",
    close: "← Назад", empty: "Нет доступных введений.",
    shapeCategoryLabel: "Формы и категории знаков",
    next: "Далее", back: "← Назад", exit: "Выйти", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Практиковать эту тему сейчас",
  },
  es: {
    btn: "🧭 Aprender", ariaLabel: "Aprender lo básico", title: "Aprender lo básico",
    intro: "Breves introducciones de 5 a 10 minutos a cada tema del examen, antes de practicar preguntas reales.",
    close: "← Atrás", empty: "No hay introducciones disponibles.",
    shapeCategoryLabel: "Formas y categorías de señales",
    next: "Siguiente", back: "← Atrás", exit: "Salir", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Practicar este tema ahora",
  },
  it: {
    btn: "🧭 Impara", ariaLabel: "Impara le basi", title: "Impara le basi",
    intro: "Brevi introduzioni di 5-10 minuti a ogni argomento d'esame, prima di iniziare a esercitarti con domande reali.",
    close: "← Indietro", empty: "Nessuna introduzione disponibile.",
    shapeCategoryLabel: "Forme e categorie dei segnali",
    next: "Avanti", back: "← Indietro", exit: "Esci", stepOf: (i, n) => `${i} / ${n}`,
    practiceNow: "Esercitati ora su questo argomento",
  },
};

function primerStrings(lang) {
  return PRIMER_STRINGS[lang] || PRIMER_STRINGS.en;
}

// Fixed display order: sign shapes/categories first (a prerequisite lens
// that applies to every other topic), then the 11 Fuehrerschein topics in
// the same order TOPIC_LABELS.fuehrerschein/renderFilters() already use.
const PRIMER_TOPIC_ORDER = ["shape_category", ...Object.keys(TOPIC_LABELS.fuehrerschein)];

function primerTopicLabel(topicCode, lang) {
  if (topicCode === "shape_category") return primerStrings(lang).shapeCategoryLabel;
  const entry = TOPIC_LABELS.fuehrerschein[topicCode];
  if (!entry) return topicCode;
  return entry[lang] || entry.en || entry.de || topicCode;
}

// Fetched once and cached per (core, locale) - core structural data (id/
// topic_code/order) never changes per language, only the locale text does,
// same split as app/data/fuehrerschein/{primers.json,primers_locales/*.json}
// on disk (see data/build_primers.py).
let primersCoreCache = null;
const primerLocaleCache = {};

async function loadPrimersCore() {
  if (primersCoreCache) return primersCoreCache;
  primersCoreCache = await fetchJson(`data/fuehrerschein/primers.json`);
  return primersCoreCache;
}

async function loadPrimerLocale(lang) {
  if (primerLocaleCache[lang]) return primerLocaleCache[lang];
  const data = await fetchJson(`data/fuehrerschein/primers_locales/${lang}.json`).catch(() => null);
  if (data) primerLocaleCache[lang] = data;
  return data;
}

// Returns an ordered array of {id, topic_code, order, title, body} for one
// topic, in the active UI language (falling back to en then de per chunk,
// same fallback chain used throughout this file, e.g. getTopicLabel()).
async function loadPrimerChunks(topicCode) {
  const core = await loadPrimersCore();
  const lang = state.lang;
  const localeData = (await loadPrimerLocale(lang)) || {};
  const enData = lang === "en" ? localeData : (await loadPrimerLocale("en")) || {};
  const deData = lang === "de" ? localeData : (await loadPrimerLocale("de")) || {};
  return core.primers
    .filter((p) => p.topic_code === topicCode)
    .sort((a, b) => a.order - b.order)
    .map((p) => {
      const text = localeData[p.id] || enData[p.id] || deData[p.id] || { title: p.id, body: "" };
      return { id: p.id, topic_code: p.topic_code, order: p.order, title: text.title, body: text.body };
    });
}

function openPrimersView() {
  el("#primers-view").hidden = false;
  history.pushState({ view: "primers" }, "");
  setInertBehindDialog(true);
  renderPrimersView();
}

function closePrimersView() {
  el("#primers-view").hidden = true;
  setInertBehindDialog(false);
}

async function renderPrimersView() {
  const S = primerStrings(state.lang);
  el("#primers-title").textContent = S.title;
  el("#primers-intro").textContent = S.intro;
  el("#primers-close-btn").textContent = S.close;

  const list = el("#primers-list");
  list.innerHTML = "";

  let core;
  try {
    core = await loadPrimersCore();
  } catch (e) {
    list.innerHTML = `<p class="empty">${S.empty}</p>`;
    el("#primers-title").focus();
    return;
  }

  const availableTopics = new Set(core.primers.map((p) => p.topic_code));
  const orderedTopics = PRIMER_TOPIC_ORDER.filter((t) => availableTopics.has(t));

  if (orderedTopics.length === 0) {
    list.innerHTML = `<p class="empty">${S.empty}</p>`;
    el("#primers-title").focus();
    return;
  }

  orderedTopics.forEach((topicCode) => {
    const btn = document.createElement("button");
    btn.className = "exam-mode-btn";
    btn.innerHTML = `<strong>${primerTopicLabel(topicCode, state.lang)}</strong>`;
    btn.addEventListener("click", () => openPrimerReader(topicCode));
    list.appendChild(btn);
  });

  el("#primers-title").focus();
}

async function openPrimerReader(topicCode) {
  const chunks = await loadPrimerChunks(topicCode);
  if (chunks.length === 0) return;
  state.primerTopic = topicCode;
  state.primerChunks = chunks;
  state.primerChunkIndex = 0;
  el("#primer-reader").hidden = false;
  history.pushState({ view: "primer-reader" }, "");
  setInertBehindDialog(true);
  renderPrimerReader();
  el("#primer-reader-title").focus();
}

function closePrimerReader() {
  el("#primer-reader").hidden = true;
  setInertBehindDialog(false);
}

function renderPrimerReader() {
  const S = primerStrings(state.lang);
  const chunks = state.primerChunks || [];
  const i = state.primerChunkIndex;
  const chunk = chunks[i];
  if (!chunk) return;

  el("#primer-reader-title").textContent = chunk.title;
  el("#primer-reader-body").textContent = chunk.body;

  const dots = el("#primer-reader-dots");
  dots.innerHTML = "";
  chunks.forEach((_, idx) => {
    const dot = document.createElement("span");
    dot.className = "dot" + (idx === i ? " active" : "");
    dots.appendChild(dot);
  });

  const backBtn = el("#primer-reader-back");
  backBtn.textContent = S.back;
  backBtn.disabled = i === 0;

  el("#primer-reader-exit").textContent = S.exit;

  const nextBtn = el("#primer-reader-next");
  const isLast = i === chunks.length - 1;
  nextBtn.innerHTML = `<strong>${isLast ? S.practiceNow : S.next}</strong>`;
}

// On the final chunk, "next" becomes a handoff into the existing topic
// filter (DN-52 §6/§8 Phase 1: "practice this topic now" reuses
// state.topicFilter rather than inventing a new mechanism) - closes the
// reader and jumps straight to that topic's filtered question list, exactly
// as if the learner had clicked that topic's chip in the header filter row.
function primerReaderHandoff() {
  const topicCode = state.primerTopic;
  // Close both dialogs synchronously first (rather than chaining
  // history.back() calls, whose popstate events fire asynchronously and
  // could race), then correct the history stack in one go() so the
  // in-app/browser back gesture still lands somewhere sane afterwards. The
  // popstate handler's own closePrimerReader()/closePrimersView() calls are
  // safe to run again once that fires - they no-op on an already-hidden view.
  const primersViewWasOpen = !el("#primers-view").hidden;
  closePrimerReader();
  if (primersViewWasOpen) closePrimersView();
  history.go(primersViewWasOpen ? -2 : -1);
  if (topicCode && TOPIC_LABELS.fuehrerschein[topicCode]) {
    state.topicFilter = topicCode;
    state.detailIndex = null;
    try { localStorage.setItem(profileKey(`filter-${state.examType}`), topicCode); } catch (e) { /* non-fatal */ }
  }
  render();
}

function wirePrimerControls() {
  el("#primers-btn").addEventListener("click", openPrimersView);
  el("#primers-close-btn").addEventListener("click", () => history.back());
  el("#primer-reader-back").addEventListener("click", () => {
    if (state.primerChunkIndex > 0) {
      state.primerChunkIndex -= 1;
      renderPrimerReader();
    }
  });
  el("#primer-reader-next").addEventListener("click", () => {
    const chunks = state.primerChunks || [];
    if (state.primerChunkIndex < chunks.length - 1) {
      state.primerChunkIndex += 1;
      renderPrimerReader();
    } else {
      primerReaderHandoff();
    }
  });
  el("#primer-reader-exit").addEventListener("click", () => history.back());
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
    // "Frage schieben" skip-and-revisit (Simulation mode only, see
    // examSkip()/renderExamQuestion() below): ids explicitly skipped during
    // the first pass, in the order they were skipped. A skipped question's
    // answer is left untouched in `answers` above - it stays unanswered
    // until (and unless) the user actually answers it in the second pass.
    skipped: [],
    // Once the first pass through `questions` completes, if `skipped` is
    // non-empty we enter a second, bounded pass over ONLY those questions
    // (reviewQueue, in their original exam order) before finishExam() is
    // allowed to run - see examNext(). reviewIndex is that pass's own
    // cursor, kept separate from `index` so the first pass's position isn't
    // disturbed. No skip button is offered on this second pass (must answer
    // or leave blank, same as any other question - no infinite skip loop).
    reviewPass: false,
    reviewQueue: [],
    reviewIndex: 0,
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

// Which question list/cursor is currently active: the normal first pass
// over the full drawn set, or (once skipped questions exist and the first
// pass has run out) the bounded second pass over just those skipped
// questions - see startExam()/examNext(). Kept as small helpers rather than
// inlined everywhere so renderExamQuestion()/examNext()/examSkip() can't
// drift out of sync on which list "the current question" means.
function examActiveList() {
  const ex = state.exam;
  return ex.reviewPass ? ex.reviewQueue : ex.questions;
}
function examActiveIndex() {
  const ex = state.exam;
  return ex.reviewPass ? ex.reviewIndex : ex.index;
}

function renderExamQuestion() {
  const S = UI_STRINGS[state.lang];
  const X = EXAM_STRINGS[state.lang];
  const ex = state.exam;
  const list = examActiveList();
  const idx = examActiveIndex();
  const q = list[idx];
  const t = q.text[state.lang];
  const topicLabel = getTopicLabel(q.topic_code, q.topic);

  const isMultiSelect = q.question_type === "multi_choice";
  // DN-14: the "review skipped questions" second pass gets its own,
  // unambiguous banner + progress-counter shape ("Übersprungene Fragen: 2
  // von 2") instead of the normal "Frage X von Y", so a test-taker can never
  // mistake it for a fresh run through the whole exam.
  const bannerEl = el("#exam-skip-banner");
  if (bannerEl) {
    bannerEl.hidden = !ex.reviewPass;
    bannerEl.textContent = ex.reviewPass ? X.skipBanner : "";
  }
  el("#exam-progress").textContent = ex.reviewPass
    ? X.skipProgress(idx + 1, list.length)
    : X.progress(idx + 1, list.length);
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

  const isLast = idx === list.length - 1;
  el("#exam-next-btn").textContent = isLast ? X.finish : X.next;
  el("#exam-exit-btn").textContent = X.exit;

  // "Frage schieben": only offered in Simulation mode, and only during the
  // first pass - the second pass (reviewing explicitly skipped questions)
  // must actually be answered or left blank, no further skipping.
  const skipBtn = el("#exam-skip-btn");
  if (skipBtn) {
    skipBtn.hidden = !(ex.mode === "simulation" && !ex.reviewPass);
    skipBtn.textContent = X.skip;
  }
}

function examNext() {
  const ex = state.exam;
  if (ex.reviewPass) {
    // Second pass: bounded to reviewQueue, no re-entry into skip logic.
    if (ex.reviewIndex < ex.reviewQueue.length - 1) {
      ex.reviewIndex += 1;
      renderExamQuestion();
      el("#exam-view").scrollTop = 0;
    } else {
      finishExam(false);
    }
    return;
  }
  if (ex.index < ex.questions.length - 1) {
    ex.index += 1;
    renderExamQuestion();
    el("#exam-view").scrollTop = 0;
  } else if (ex.skipped.length > 0) {
    // First pass just ran out with unresolved skips - enter the required
    // second pass over exactly those questions (original exam order)
    // instead of finishing yet. See startExam()'s state.exam.reviewPass doc
    // comment for why this is bounded (no infinite skip loop): the second
    // pass never offers its own skip button (see renderExamQuestion above).
    ex.reviewPass = true;
    const skippedSet = new Set(ex.skipped);
    ex.reviewQueue = ex.questions.filter((q) => skippedSet.has(q.id));
    ex.reviewIndex = 0;
    renderExamQuestion();
    el("#exam-view").scrollTop = 0;
  } else {
    finishExam(false);
  }
}

// Records the current question as explicitly skipped (Simulation mode's
// first pass only - see the skip button's own visibility guard in
// renderExamQuestion()) and advances exactly like examNext() does, without
// touching state.exam.answers for it. Deliberately a thin wrapper around
// examNext() rather than duplicating its advance/end-of-pass logic, so
// "what happens after skip" and "what happens after next" can never drift
// apart.
function examSkip() {
  const ex = state.exam;
  if (!ex || ex.reviewPass) return; // no skip once inside the skipped-question review pass
  const q = ex.questions[ex.index];
  if (!ex.skipped.includes(q.id)) ex.skipped.push(q.id);
  examNext();
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
        <div class="cert-badge-row"></div>
        <div class="cert-card-title">🎓 ${C.title}</div>
        <div class="cert-card-actions">
          <button class="back-btn" id="exam-results-cert-html">${C.downloadCert}</button>
          <button class="back-btn" id="exam-results-cert-json">${C.downloadCred}</button>
        </div>
        <div class="cert-jwt-row"></div>
        <div class="cert-verify-row"></div>
      </div>
    `;
    const record = state.exam.certRecord;
    const badgeSlot = certEl.querySelector(".cert-badge-row");
    const jwtSlot = certEl.querySelector(".cert-jwt-row");
    const verifySlot = certEl.querySelector(".cert-verify-row");
    renderBadgeRow(badgeSlot, record, C);
    renderJwtDownloadBtn(jwtSlot, record, C);
    renderVerifyLinkRow(verifySlot, record, C);
    // A fresh pass fires trySignCompletion() in the background right from
    // recordCompletion() (still in flight at the moment this results screen
    // first renders) - re-render the badge once that settles so a passing
    // user actually SEES the upgrade from "self-issued" to "signed badge"
    // happen live, rather than only finding out on a later visit to "My
    // certificates". The JWT-download and verify-link rows are re-rendered
    // alongside it since both only become eligible once the signature is
    // real.
    if (!record.verified) {
      ensureSignedCredential(record).then(() => {
        renderBadgeRow(badgeSlot, record, C);
        renderJwtDownloadBtn(jwtSlot, record, C);
        renderVerifyLinkRow(verifySlot, record, C);
      });
    }
    el("#exam-results-cert-html").addEventListener("click", () => {
      downloadTextFile(`zettacard-zertifikat-${record.id}.html`, certificateHtmlDoc(record), "text/html");
    });
    el("#exam-results-cert-json").addEventListener("click", async () => {
      await ensureSignedCredential(record);
      renderBadgeRow(badgeSlot, record, C);
      renderJwtDownloadBtn(jwtSlot, record, C);
      renderVerifyLinkRow(verifySlot, record, C);
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
  // ever meaningfully narrows anything for the compliance modules that
  // carry a "roles" field (every other module's questions have none, so
  // questionMatchesRole treats them as ["all"] and they always pass).
  if (state.roleFilter !== "all") qs = qs.filter((q) => questionMatchesRole(q, state.roleFilter));
  // DN-14: "starred only" filter, additive to the above two - narrows the
  // already topic/role-filtered list down to just the questions this
  // profile has manually starred.
  if (state.starredOnlyFilter) {
    const starred = loadStarredData();
    qs = qs.filter((q) => starred[q.id]);
  }
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

  // Kickstart-learning-journey topic primers (DN-52 Phase 1) - Fuehrerschein-
  // only for now, same visibility pattern as Sign Reference above.
  const primersBtn = el("#primers-btn");
  primersBtn.hidden = state.examType !== "fuehrerschein";
  const PS = primerStrings(state.lang);
  primersBtn.textContent = PS.btn;
  primersBtn.title = PS.title;
  primersBtn.setAttribute("aria-label", PS.ariaLabel);

  // DN-46: "prepare for offline" button/status - shown for every module
  // (not Fuehrerschein-only like Sign Reference above), hidden only when no
  // module is loaded. Pure repaint from state.offlinePrep - never re-checks
  // the cache itself (that only happens via checkOfflineReadiness(), called
  // from loadModuleData()/setLang()).
  renderOfflinePrep();

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
      // Scoped per module (2026-08-08 fix) - see loadActiveProfileState()'s
      // comment for why an unscoped key let one module's filter selection
      // leak into another after an app reload.
      try { localStorage.setItem(profileKey(`filter-${state.examType}`), code); } catch (e) { /* non-fatal */ }
      render();
    });
    container.appendChild(btn);
  });

  // DN-14: "starred only" toggle chip, appended after the topic buttons in
  // the same row/container - same button look (relies on the existing
  // `.filters button`/`.filters button.active` CSS, no new class needed),
  // just a distinct, independently-toggleable chip rather than one of the
  // mutually-exclusive topic options above.
  const SS = starStrings(state.lang);
  const starBtn = document.createElement("button");
  starBtn.textContent = SS.filterChip;
  starBtn.className = state.starredOnlyFilter ? "active" : "";
  starBtn.setAttribute("aria-pressed", String(state.starredOnlyFilter));
  starBtn.setAttribute("aria-label", SS.filterAria);
  starBtn.title = SS.filterAria;
  starBtn.addEventListener("click", () => {
    state.starredOnlyFilter = !state.starredOnlyFilter;
    state.detailIndex = null;
    render();
  });
  container.appendChild(starBtn);
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
      // Scoped per module (2026-08-08 fix) - same cross-module leak as the
      // topic filter above.
      try { localStorage.setItem(profileKey(`role-filter-${state.examType}`), code); } catch (e) { /* non-fatal */ }
      render();
    });
    container.appendChild(btn);
  });
}

function renderList() {
  const S = UI_STRINGS[state.lang];
  const SS = starStrings(state.lang);
  const list = el("#list");
  const qs = filteredQuestions();
  list.innerHTML = "";

  if (qs.length === 0) {
    // DN-14: a distinct empty-state message when the "starred only" filter
    // is the reason the list is empty, rather than the generic "no
    // questions in this category" text - a learner should understand THIS
    // is because they haven't starred anything yet, not that the category
    // itself is empty.
    list.innerHTML = `<div class="empty">${state.starredOnlyFilter ? SS.emptyStarred : S.empty}</div>`;
    return;
  }

  const starred = loadStarredData(); // one read for the whole list, not per-card
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
        ${starred[q.id] ? `<span class="badge star-badge" aria-label="${SS.starredAria}">⭐</span>` : ""}
        <span class="q-card-id">${q.id}</span>
      </div>
      <div class="q-card-text">${q.text[state.lang].question}</div>
    `;
    const open = () => {
      state.listScrollY = window.scrollY;
      state.lastOpenedIndex = i; // so focus can return to the same card on close
      state.detailIndex = i;
      state.revealed = false;
      state.detailPick = null; // DN: clear any in-progress self-answer attempt when moving to a (possibly new) question
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

  // DN-14: every time a question is actually shown in this detail/flashcard
  // view (initial open, prev/next navigation, review-mode cycling) counts
  // as "seen" - markSeen() itself no-ops after the first time, so this is a
  // cheap, idempotent call rather than something that needs its own guard
  // here.
  markSeen(q.id);

  const SS = starStrings(state.lang);
  const starBtn = el("#star-btn");
  const starred = isStarred(q.id);
  starBtn.textContent = starred ? SS.starred : SS.star;
  starBtn.setAttribute("aria-pressed", String(starred));
  starBtn.setAttribute("aria-label", starred ? SS.starredAria : SS.starAria);
  starBtn.title = starred ? SS.starredAria : SS.starAria;

  el("#detail-progress").textContent = S.progress(state.detailIndex + 1, qs.length);

  el("#detail-meta").innerHTML = `
    <span class="badge topic">${topicLabel}</span>
    <span class="badge points">${S.points(q.points)}</span>
    ${q.high_stakes ? `<span class="badge high-stakes">${S.highStakes}</span>` : ""}
    ${q.question_type === "multi_choice" ? `<span class="badge multi-select">${S.multiSelectHint}</span>` : ""}
    ${!state.revealed ? `<span class="badge try-it-hint">${S.tryItHint}</span>` : ""}
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

  // "Try it yourself": before reveal, options are clickable (checkbox-style
  // toggle for multi_choice, single-pick overwrite otherwise - exactly
  // mirroring exam mode's pick()/applySelection() so the interaction feels
  // like the same product). After reveal, clicking stops doing anything
  // (isRevealPending guards it) and every option shows its final state:
  // the real correct answer(s) always get the existing green check mark,
  // and - new - whichever option(s) the user actually picked get a second,
  // distinct mark if their pick was wrong (a plain reveal-only flow can't
  // tell a user "yes you had it right" or "no, that's not it" the way exam
  // mode already could).
  const isMultiSelectQ = q.question_type === "multi_choice";
  const pickedKeys = Array.isArray(state.detailPick)
    ? state.detailPick
    : (state.detailPick != null ? [state.detailPick] : []);

  const optionsEl = el("#options");
  optionsEl.innerHTML = "";
  Object.entries(t.options).forEach(([key, text]) => {
    const isCorrect = q.correct.includes(key);
    const showCorrect = state.revealed && isCorrect;
    const wasPicked = pickedKeys.includes(key);
    const showWrongPick = state.revealed && wasPicked && !isCorrect;
    const div = document.createElement("div");
    div.className = "option"
      + (showCorrect ? " correct" : "")
      + (showWrongPick ? " your-wrong-pick" : "")
      + (!state.revealed && wasPicked ? " picked" : "")
      + (isMultiSelectQ && !state.revealed ? " option-checkbox" : "");
    div.dataset.key = key;
    if (!state.revealed) {
      div.setAttribute("role", isMultiSelectQ ? "checkbox" : "button");
      if (isMultiSelectQ) div.setAttribute("aria-checked", String(wasPicked));
      else div.setAttribute("aria-pressed", String(wasPicked));
      div.tabIndex = 0;
    }
    // Marks are always text/icon + color together, never color alone -
    // same accessibility principle already applied to .correct-mark/
    // .selected-mark elsewhere in this app.
    div.innerHTML = `<span class="key">${key.toUpperCase()}</span><span>${text}</span>${
      showCorrect ? `<span class="correct-mark">✓ ${S.correctMark}</span>`
      : showWrongPick ? `<span class="wrong-pick-mark">✗ ${S.yourPickWrong}</span>`
      : ""
    }`;
    if (!state.revealed) {
      const pick = () => {
        if (isMultiSelectQ) {
          const current = Array.isArray(state.detailPick) ? state.detailPick : [];
          state.detailPick = current.includes(key)
            ? current.filter((k) => k !== key)
            : [...current, key];
        } else {
          state.detailPick = state.detailPick === key ? null : key; // click again to deselect
        }
        renderDetail();
      };
      div.addEventListener("click", pick);
      div.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); }
      });
    }
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
    el("#review-actions-caption").textContent = SR.caption;
    el("#review-know-btn").textContent = SR.know;
    el("#review-dontknow-btn").textContent = SR.dontKnow;
    // If the user actually tried answering this card themselves (pickedKeys,
    // computed above while rendering #options) before revealing, gently
    // suggest whichever button matches what really happened - still just a
    // suggestion (a highlighted ring, not a pre-click), since a single
    // right/wrong guess isn't automatically the same thing as genuinely
    // "knowing" a fact, and the user should always have the final say.
    const knowBtn = el("#review-know-btn");
    const dontKnowBtn = el("#review-dontknow-btn");
    knowBtn.classList.remove("suggested");
    dontKnowBtn.classList.remove("suggested");
    if (pickedKeys.length > 0) {
      const gotItRight = isMultiSelectQ
        ? (pickedKeys.length === q.correct.length && pickedKeys.every((k) => q.correct.includes(k)))
        : (pickedKeys.length === 1 && q.correct.includes(pickedKeys[0]));
      (gotItRight ? knowBtn : dontKnowBtn).classList.add("suggested");
    }
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
  wirePrimerControls();
  el("#offline-prep-btn").addEventListener("click", () => { prepareOffline(); });
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
    if (!el("#primer-reader").hidden) closePrimerReader();
    if (!el("#primers-view").hidden) closePrimersView();
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
  el("#exam-skip-btn").addEventListener("click", examSkip);
  el("#exam-results-close-btn").addEventListener("click", exitExam);

  el("#reveal-btn").addEventListener("click", () => {
    state.revealed = true;
    render();
    // Move focus to the newly-revealed explanation so keyboard/screen-reader
    // users land on the new content instead of losing focus entirely.
    el("#explanation").focus();
  });

  // DN-14: manual star/bookmark toggle - independent of reveal state and of
  // whether the user got the question right or wrong, so this can be
  // clicked at any point while a question is open.
  el("#star-btn").addEventListener("click", () => {
    const qs = filteredQuestions();
    const q = qs[state.detailIndex];
    if (!q) return;
    toggleStarred(q.id);
    render();
  });

  el("#prev-btn").addEventListener("click", () => {
    if (state.detailIndex > 0) {
      state.detailIndex -= 1;
      state.revealed = false;
      state.detailPick = null; // DN: clear any in-progress self-answer attempt when moving to a (possibly new) question
      render();
      el("#detail-view").scrollTop = 0;
    }
  });

  el("#next-btn").addEventListener("click", () => {
    const qs = filteredQuestions();
    if (state.detailIndex < qs.length - 1) {
      state.detailIndex += 1;
      state.revealed = false;
      state.detailPick = null; // DN: clear any in-progress self-answer attempt when moving to a (possibly new) question
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
  } catch (e) { /* storage unavailable, defaults are fine */ }

  document.documentElement.setAttribute("lang", state.lang);
  document.documentElement.setAttribute("dir", RTL_LANGS.has(state.lang) ? "rtl" : "ltr");

  let savedExamType = null, savedScopeCode = null;
  try {
    savedExamType = localStorage.getItem(profileKey("exam-type"));
    savedScopeCode = localStorage.getItem(profileKey("scope-code"));
  } catch (e) { /* non-fatal */ }

  // 2026-08-08 fix (real bug, found while auditing translations - PO flagged
  // seeing compliance-course categories appear while studying for the
  // driver's licence): topicFilter/roleFilter used to be saved under a
  // single profileKey("filter")/profileKey("role-filter"), shared across
  // EVERY module for a given profile, and were restored here BEFORE
  // savedExamType was even known - so switching modules mid-session
  // (selectModuleAndScope() resets both to "all" in memory, correctly) but
  // then closing the app without ever clicking a filter chip in the new
  // module left the OLD module's last-clicked filter code sitting in that
  // shared storage key. On the next app load, that stale code (e.g. a
  // Datenschutz topic_code like "grundprinzipien") got restored as the
  // driver's-licence module's topicFilter - a code no Fuehrerschein
  // question has, so the list silently filtered down to empty (no chip
  // ever showed as "active" for it, since renderFilters() only builds
  // chips from the CURRENT module's own TOPIC_LABELS, but the underlying
  // filter value was still wrong and invisible). Fixed by scoping both
  // keys per module, and only restoring them once savedExamType is known.
  try {
    if (savedExamType) {
      const savedFilter = localStorage.getItem(profileKey(`filter-${savedExamType}`));
      state.topicFilter = savedFilter || "all";
      const savedRoleFilter = localStorage.getItem(profileKey(`role-filter-${savedExamType}`));
      state.roleFilter = ROLE_FILTER_CODES.includes(savedRoleFilter) ? savedRoleFilter : "all";
    }
  } catch (e) { /* storage unavailable, defaults are fine */ }

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
