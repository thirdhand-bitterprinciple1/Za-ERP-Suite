# Contributing

Thank you for contributing to ZA ERP Suite.

## Workflow

1. Fork and create a feature branch.
2. Keep changes focused and atomic.
3. Add/update tests where possible.
4. Run checks before submitting PR.
5. Open PR with clear summary, screenshots/logs if needed.

## Branch Naming

Use descriptive names, for example:

- `feature/audit-log-filters`
- `fix/report-download-path`
- `docs/install-guide-improvements`

## Commit Style

Prefer clear, imperative commit messages:

- `Add notification mark-all-read endpoint`
- `Fix reports module download action`
- `Update README and install docs`

## Local Validation Checklist

From `backend/`:

```bash
source .venv/bin/activate
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
python3 -m compileall apps config manage.py
```

If frontend exists in your branch, also run build checks there.

## Pull Request Checklist

- Code follows existing project style.
- No secrets committed.
- README/docs updated for behavior changes.
- Migrations included for model changes.
- Backward compatibility considered.

## Label Taxonomy

This repository uses a standardized label scheme:

- Type labels:
	- `type: bug`
	- `type: feature`
	- `type: docs`
	- `type: security`
	- `type: question`
- Area labels:
	- `area: backend`
	- `area: docs`
	- `area: github`
	- `area: ci`
	- `area: migrations`
	- `area: security`

Auto-labeling workflow applies these labels based on PR file paths and issue keywords.

## Security

If you discover a security issue, do not open a public issue with exploit details.
Share details privately with project maintainers.
