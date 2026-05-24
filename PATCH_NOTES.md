# Patch Notes

This bundle assumes the status synthesis tool directory is named:

```text
slack-canvas-status-synthesis
```

If you chose a different directory name, keep the file contents and update the directory reference in the root README.

## What Changed

- Updated the root `README.md` so the repo now lists Slack Canvas Status Synthesis under Scripts and Automation.
- Rebuilt the tool `README.md` because the uploaded `README.md` was the template-storage README, not the tool README.
- Rewrote `EXAMPLES.md` to remove unsupported success claims and make the human review bar explicit.
- Reworked both Python scripts so Claude returns content to stdout and the Python wrapper writes local files.
- Removed the default `--allowedTools *` and default `--permission-mode bypassPermissions` behavior.
- Added narrow default read-tool allowlists that can be overridden with `CLAUDE_ALLOWED_TOOLS`.
- Added dry-run and prompt-save support.
- Added a safer `.gitignore` that does not ignore every `.txt` file.
- Added `.canvas_templates/README.md` so generated templates stay out of git unless reviewed and sanitized.

## Install

From the repo root:

```bash
cp README.md /path/to/tpm-toolbox/README.md
cp -R slack-canvas-status-synthesis /path/to/tpm-toolbox/
cd /path/to/tpm-toolbox/slack-canvas-status-synthesis
chmod +x canvas_template_extractor.py canvas_generator_from_template.py
```

Then commit:

```bash
git add README.md slack-canvas-status-synthesis
git commit -m "Add Slack canvas status synthesis workflow"
```
