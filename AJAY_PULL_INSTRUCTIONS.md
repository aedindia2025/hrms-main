# Ajay - Main Branch Changes Pull பண்ண Instructions

## 📋 **Scenario:**
- ✅ Main branch-ல new changes push ஆகியுள்ளது
- 🔄 Ajay `ajay_hrms` branch-ல work பண்ணிகிட்டு இருக்கார்
- ❓ Ajay எப்படி main branch changes-ஐ pull பண்ணலாம்?

---

## 🎯 **Option 1: Ajay_hrms Branch-ல Main Changes Merge பண்ண (Recommended)**

### **Step 1: Ajay_hrms Branch-ல Switch பண்ணு**
```bash
git checkout ajay_hrms
```

### **Step 2: Latest Changes Fetch பண்ணு**
```bash
git fetch origin
```

### **Step 3: Main Branch Changes-ஐ Ajay_hrms-ல Merge பண்ணு**
```bash
git merge origin/main
```

**அல்லது Rebase Use பண்ணலாம் (Clean History):**
```bash
git rebase origin/main
```

### **Step 4: Conflicts Resolve பண்ணு (if any)**
- Conflicts இருந்தா resolve பண்ணு
- Then commit பண்ணு

### **Step 5: Ajay_hrms Branch-ல Push பண்ணு**
```bash
git push origin ajay_hrms
```

---

## 🎯 **Option 2: Main Branch-ல Pull பண்ணி, Then Ajay_hrms-ல Merge**

### **Step 1: Main Branch-ல Switch பண்ணு**
```bash
git checkout main
```

### **Step 2: Latest Changes Pull பண்ணு**
```bash
git pull origin main
```

### **Step 3: Ajay_hrms Branch-ல Switch பண்ணு**
```bash
git checkout ajay_hrms
```

### **Step 4: Main Branch-ஐ Merge பண்ணு**
```bash
git merge main
```

### **Step 5: Push பண்ணு**
```bash
git push origin ajay_hrms
```

---

## 🔧 **Complete Command Sequence (Option 1 - Recommended):**

```bash
# 1. Ajay_hrms branch-ல switch பண்ணு
git checkout ajay_hrms

# 2. Latest changes fetch பண்ணு
git fetch origin

# 3. Main branch changes-ஐ merge பண்ணு
git merge origin/main

# 4. Conflicts resolve பண்ணு (if any)
# Edit conflicted files
# Then:
git add .
git commit -m "Merge main branch changes into ajay_hrms"

# 5. Push பண்ணு
git push origin ajay_hrms
```

---

## ⚠️ **Important Notes:**

### **1. Conflicts Handle பண்ண:**
- Conflicts வந்தா, files manually edit பண்ணி resolve பண்ணனும்
- Then `git add` and `git commit` பண்ணனும்

### **2. Rebase vs Merge:**
- **Merge:** History-ல merge commit create ஆகும் (simpler)
- **Rebase:** Clean history, but conflicts resolve பண்ணனும் (advanced)

### **3. Backup:**
- Merge பண்ண முன்னாடி backup எடுத்துக்கோ:
```bash
git branch ajay_hrms_backup
```

---

## 📝 **Step-by-Step Example:**

### **Scenario: Ajay ajay_hrms branch-ல work பண்ணிகிட்டு இருக்கார்**

```bash
# Current branch check பண்ணு
git branch

# Ajay_hrms branch-ல switch பண்ணு (if not already)
git checkout ajay_hrms

# Latest changes fetch பண்ணு
git fetch origin

# Main branch changes-ஐ merge பண்ணு
git merge origin/main

# If conflicts:
# 1. Check which files have conflicts
git status

# 2. Open conflicted files and resolve
# Look for <<<<<<< HEAD, =======, >>>>>>> markers

# 3. After resolving:
git add .
git commit -m "Merge main branch changes"

# 4. Push to ajay_hrms
git push origin ajay_hrms
```

---

## ✅ **Verification:**

Merge பிறகு verify பண்ண:
```bash
# Check if main branch changes are in ajay_hrms
git log --oneline --graph --all

# Check current status
git status
```

---

## 🎯 **Summary for Ajay:**

1. ✅ `git checkout ajay_hrms` - Ajay branch-ல switch பண்ணு
2. ✅ `git fetch origin` - Latest changes fetch பண்ணு
3. ✅ `git merge origin/main` - Main changes merge பண்ணு
4. ✅ Conflicts resolve பண்ணு (if any)
5. ✅ `git push origin ajay_hrms` - Push பண்ணு

**Done!** 🎉

