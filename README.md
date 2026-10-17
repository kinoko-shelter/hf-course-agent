---
title: Source Grounded Course Agent
emoji: 🔎
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
license: mit
---

# Source Grounded Course Agent

A local agent for the Hugging Face AI Agents Course final assignment. It fetches
the official 20 questions and attachments, solves each in an independent Codex CLI
session with live web search, and saves the generated answers and research traces.
There are no task-specific answer mappings or benchmark solution lookups.

This Space publishes the verification source. **Inference runs locally**, using
the operator's own authenticated Codex installation. The Space does not contain
ChatGPT credentials or provide a hosted inference endpoint. No leaderboard score
or certificate is claimed until an official submission receipt is obtained.

## Run

Requirements: Python 3.12+, an official Codex CLI installation, and an eligible
authenticated Codex account (`codex login status`). Model usage consumes the
operator's normal account allowance. No model override is specified.

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python agent.py fetch
.venv/bin/python agent.py run --jobs 2 --timeout 300
```

For a smoke test, pass `--tasks <official-task-id>` and `--jobs 1`. Each run stores
`results.json`, `failures.json`, per-task prompts, JSONL events and source citations
under `runs/`. Local output is excluded from publication. Runs with infrastructure
failures cannot be submitted until the missing tasks are rerun and results merged.

## Submit

1. Authenticate your own Hugging Face account using `hf auth login`.
2. Publish this source in a **public Space under that same account**.
3. Submit the complete, locally generated results:

```sh
.venv/bin/python agent.py submit \
  --results runs/<run>/results.json \
  --code https://huggingface.co/spaces/<your-account>/<your-space>/tree/main
```

The runner derives the username from `whoami()`, verifies Space ownership and
visibility, requires exactly one result per official task, then saves the server's
actual score receipt. Empty answers are permitted for inaccessible inputs and
remain in the denominator. There is no automatic score-driven answer tuning.

## Attachment handling and limits

Images are passed to the vision-capable CLI. XLSX values, PDF text and source text
are extracted locally. Attached programs are not executed by the runner. For audio,
a locally produced `<filename>.transcript.json` sidecar is read when present;
otherwise the agent is told audio was not transcribed. No ASR is bundled.

If the official attachment server returns 404, the failure is saved and the agent
is told the input is unavailable. Video questions currently use web research;
direct temporal video inspection is not implemented. Confidence and limitations
are recorded alongside each answer. These limitations can reduce the score.

Subprocesses use read-only mode, never-approve, ephemeral sessions, and a per-task
timeout. Prompts prohibit reading private files, looking up benchmark answer keys,
spawning agents, and following instructions embedded in retrieved material. This
is an operating constraint, not a claim that model prompts replace OS isolation.

## Official references

- [Assignment](https://huggingface.co/learn/agents-course/en/unit4/hands-on)
- [Evaluation API](https://agents-course-unit4-scoring.hf.space/docs)
- [Certificate requirements](https://huggingface.co/learn/agents-course/en/unit4/get-your-certificate)
- [Codex noninteractive mode](https://developers.openai.com/codex/noninteractive)

Only the source files listed in `publish.py` are published. Credentials, downloaded
task materials, generated answers, local logs and temporary tokens stay local.
