# طريقة رفع المشروع على GitHub

هذا الملف يشرح بسرعة كيف ترفع المشروع كمستودع جديد على GitHub.

---

## 1. افتح Terminal داخل مجلد المشروع

بعد فك ضغط ملف ZIP، ادخل إلى مجلد المشروع:

```bash
cd poly-equation-solver
```

---

## 2. جرّب المشروع محليًا

### Python

```bash
PYTHONPATH=python python -m poly_solver.cli quadratic 1 -5 6
PYTHONPATH=python python -m poly_solver.cli cubic 1 -6 11 -6
```

أو ثبته محليًا:

```bash
python -m pip install -e .
poly-solver cubic 1 -6 11 -6
```

### C++

```bash
cmake -S . -B build
cmake --build build
./build/eqsolver cubic 1 -6 11 -6
```

على Windows قد يكون المسار:

```powershell
.\build\Debug\eqsolver.exe cubic 1 -6 11 -6
```

---

## 3. اختبر المشروع قبل الرفع

```bash
PYTHONPATH=python python -m unittest discover -s tests/python
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

---

## 4. إنشاء مستودع Git محلي

```bash
git init
git add .
git commit -m "Initial commit: quadratic and cubic equation solver"
```

---

## 5. ربط المشروع مع GitHub

أنشئ Repository جديدًا في GitHub باسم مثل:

```text
poly-equation-solver
```

ثم نفّذ الأوامر التي يعطيك إياها GitHub، وغالبًا تكون مثل:

```bash
git branch -M main
git remote add origin https://github.com/alaafmasoud-create/poly-equation-solver.git
git push -u origin main
```

غيّر الرابط حسب اسم المستودع الذي أنشأته.

---

## 6. GitHub Actions

المشروع يحتوي مسبقًا على ملف:

```text
.github/workflows/ci.yml
```

بعد الرفع، GitHub سيشغّل الاختبارات تلقائيًا عند كل `push` أو `pull request`.
