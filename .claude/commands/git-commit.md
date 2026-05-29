---
name: git-commit
description: Use this skill whenever the user asks to commit, create a commit, generate a commit message, or stage changes in git. Trigger on phrases like "faz o commit", "commita", "commita isso", "cria o commit", "quero commitar", "make a commit", "commit these changes", or any variation in Portuguese or English. Always follow this workflow — never commit everything at once or skip the logical grouping step.
---

# Git Workflow – Context-Aware Commits

## Objective
Commits must be **small, logical, and single-responsibility** — never group unrelated changes into one commit.

---

## Workflow

### 1. Inspect Changes

```bash
git status
git diff
git diff --staged
```

Identify logical groups: features, fixes, refactors, tests, docs, config.
Each group becomes **one separate commit**.

If only one file was changed, skip grouping and go straight to step 3.

---

### 2. Stage Selectively

Stage only related files per group:

```bash
git add path/to/file1 path/to/file2
```

If a single file contains mixed concerns (e.g. fix + refactor), use partial staging:

```bash
git add -p path/to/file
```

Repeat for each logical group.

---

### 3. Write the Commit Message

Follow **Conventional Commits**. Subject line is always required; body is optional.

```
type(scope): short imperative description

Explain why, not what — only when the change needs context.
Keep lines under 72 characters.
```

Types: `feat` · `fix` · `refactor` · `chore` · `docs` · `style` · `test` · `perf`

For simple, self-explanatory changes, the subject line alone is sufficient.

---

### 4. Commit and Repeat

```bash
git commit -m "type(scope): description"
```

Repeat steps 2–4 for each remaining group.

---

### 5. Final Validation

```bash
git log --oneline -n 5
```

Each commit should be small, focused, and readable in isolation.

---

## Rules

- **No push** — always left to the user.
- **No proactive commits** — only commit when explicitly asked.
- **No `Co-Authored-By`** lines.
- **English only** — type, scope, description, and body.
- **No repo, no commit** — if there's nothing staged or no changes, inform the user instead of proceeding.