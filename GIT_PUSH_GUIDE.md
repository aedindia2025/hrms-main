# Git Push Guide - Next Time Steps

## 🔄 Next Time Git Push செய்யும்போது Follow செய்ய வேண்டிய Steps:

### ✅ Step 1: Check Status
```bash
git status
```

### ✅ Step 2: Changes-ஐ Add செய்ய
```bash
# Specific files add செய்ய
git add <file1> <file2> ...

# அல்லது அனைத்தும் add செய்ய
git add .
```

### ✅ Step 3: Commit செய்ய
```bash
git commit -m "Your commit message here"
```

### ✅ Step 4: Remote Changes Pull செய்ய (Important!)
```bash
git pull origin main
```

### ✅ Step 5: Push செய்ய
```bash
git push origin main
```

---

## ⚠️ Conflicts வந்தால்:

### Option 1: Current Changes-ஐ Keep செய்ய
```bash
git checkout --ours <file>
git add <file>
```

### Option 2: Remote Changes-ஐ Accept செய்ய
```bash
git checkout --theirs <file>
git add <file>
```

### Option 3: Manual Resolve
- File open செய்து conflicts resolve செய்ய
- `git add <file>` செய்ய

---

## 🚫 __pycache__ Files Auto Remove:

```bash
# All __pycache__ files remove செய்ய
git rm -r --cached --ignore-unmatch **/__pycache__/
git rm --cached --ignore-unmatch **/*.pyc
```

---

## 📝 Quick Push Commands:

```bash
# Quick workflow
git add .
git commit -m "Your changes"
git pull origin main
git push origin main
```

---

## ✅ .gitignore Check:

`.gitignore` file-ல் இவை உள்ளன:
- `__pycache__/` - All cache directories
- `*.py[cod]` - All .pyc, .pyo, .pyd files
- `.env` - Environment files
- `db.sqlite3` - Database files
- `/media` - Media files
- `/staticfiles` - Static files

**Next time __pycache__ files automatically ignore ஆகும்!**

