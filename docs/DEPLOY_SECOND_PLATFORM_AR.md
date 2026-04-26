# نشر المشروع على منصة ثانية

هذا الإصدار لا يقتصر على GitHub فقط. أصبح المشروع قابلًا للتشغيل والنشر كـ **Web App**.

## الخيار 1: Streamlit Community Cloud

1. ارفع المشروع إلى GitHub.
2. ادخل إلى Streamlit Community Cloud.
3. اختر المستودع الخاص بالمشروع.
4. ضع قيمة **Main file path**:

```text
app.py
```

5. اضغط Deploy.

سيقرأ Streamlit ملف `requirements.txt` تلقائيًا ويثبت الحزم المطلوبة.

## الخيار 2: Hugging Face Spaces

1. أنشئ Space جديدًا.
2. اختر SDK: Streamlit.
3. ارفع ملفات المشروع كاملة.
4. اجعل ملف التشغيل هو:

```text
app.py
```

سيتم تثبيت المتطلبات من `requirements.txt`.

## الخيار 3: Docker / Render / أي منصة حاويات

المشروع يحتوي على `Dockerfile` جاهز.

للتشغيل محليًا:

```bash
docker build -t poly-equation-solver .
docker run -p 8501:8501 poly-equation-solver
```

ثم افتح:

```text
http://localhost:8501
```

## التشغيل المحلي بدون Docker

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## الملفات التي أضيفت للمنصة الثانية

```text
app.py
requirements.txt
Dockerfile
render.yaml
.streamlit/config.toml
docs/DEPLOY_SECOND_PLATFORM_AR.md
```

## ملاحظة مهمة

الكود الأساسي للحل الرياضي بقي منفصلًا داخل:

```text
python/poly_solver/solver.py
src/equations.cpp
```

أي أن واجهة الويب لا تكسر منطق المشروع، بل تستخدمه كطبقة عرض فقط.
