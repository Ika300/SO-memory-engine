# GitHub Publication Steps

This file is a practical checklist for publishing SO Memory Engine as a new GitHub repository.

## Current local status

Local folder:

```text
C:\Users\Ika300\Desktop\SO_Memory_Engine
```

Recommended GitHub repository name:

```text
so-memory-engine
```

Recommended owner:

```text
Ika300
```

## 1. Create the GitHub repository

In GitHub:

1. Open GitHub.
2. Click `New repository`.
3. Repository name: `so-memory-engine`.
4. Visibility: public or private, depending on release timing.
5. Do not add README, license, or .gitignore on GitHub. They already exist locally.
6. Create repository.

## 2. Connect local repository to GitHub

After GitHub shows the remote URL, run from this folder:

```bash
git remote add origin https://github.com/Ika300/so-memory-engine.git
```

## 3. Push initial commit

```bash
git branch -M main
git push -u origin main
```

If a sign-in window appears, approve it in the browser or GitHub Desktop credential prompt.

## 4. After publication

Check the GitHub page:

- README renders correctly
- LICENSE appears
- docs links work
- examples are visible
- `outputs/` is not uploaded

## 5. Optional next step

After Engine is public, update SO Memory Kernel README to mention:

```text
For AI-app-facing memory context, see SO Memory Engine.
```

Do not do this until the Engine repository URL exists.
