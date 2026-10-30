# prayer-screen-data

بيانات مباريات اليوم لتطبيق «شاشة الصلاة». مستودع عام، يُحدَّث تلقائيًا كل ٢٠ دقيقة.

## الملفات

| الملف | الوظيفة |
|---|---|
| `tools/fetch_fixtures.py` | ينادي API-Football ويكتب ملفًا صغيرًا |
| `.github/workflows/fixtures.yml` | يشغّله كل ٢٠ دقيقة |
| `docs/latest.json` | الناتج الذي يقرأه التطبيق (~٥٤ ك.ب) |
| `docs/archive/YYYY-MM-DD.json` | نسخة لكل يوم |

المفتاح **لا يُكتب في الملف**؛ يأتي من `Secrets`.

## خطوات التجهيز (٥ دقائق، مرة واحدة)

1. **أنشئ مستودعًا عامًّا** باسم `prayer-screen-data`:
   - github.com ← New repository ← Public ← Create.

2. **ارفع الملفات الثلاثة** (اسحبها وأفلتها في صفحة المستودع):
   - `tools/fetch_fixtures.py`
   - `.github/workflows/fixtures.yml`
   - `docs/latest.json` (يمكن تركه فارغًا؛ سيُملأ تلقائيًا)

3. **أضف المفتاح**:
   - Settings ← Secrets and variables ← Actions ← New repository secret
   - الاسم: `API_FOOTBALL_KEY`
   - القيمة: مفتاحك

4. **شغّل مرة يدويًا**:
   - تبويب Actions ← «fixtures» ← Run workflow.

5. **الرابط النهائي**:
   ```
   https://raw.githubusercontent.com/<USER>/prayer-screen-data/main/docs/latest.json
   ```

## شكل الملف

```json
{
  "date": "2026-10-30",
  "updated": "2026-10-30T12:24:18+00:00",
  "count": 397,
  "fixtures": [
    {"l": 307, "n": "Pro League", "h": "Al-Nassr", "a": "Al-Kholood",
     "s": "2H", "e": 63, "gh": 3, "ga": 1, "t": "2026-10-29T18:00:00+03:00"}
  ]
}
```

## ملاحظات

- الحصة: ٧٢ طلبًا في اليوم (كل ٢٠ دقيقة) — تحت حد API-Football المجاني (١٠٠).
- عدد المباريات لا يؤثر: كل المستخدمين يقرؤون نفس الملف.
- إن توقّف الـworkflow، يعرض التطبيق آخر نسخة محفوظة على الجهاز.
