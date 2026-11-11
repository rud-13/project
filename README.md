# 🤖 DevFlow AI — AI-Powered Code Review & PR Assistant

> **Free, open-source AI code reviewer for every developer.**  
> No paid plans. No enterprise gates. Just smarter code.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-green?logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)

---

## 🚀 What is DevFlow AI?

**DevFlow AI** is a command-line tool and GitHub Action that automatically reviews your Pull Requests using AI — detecting bugs, suggesting improvements, and generating changelogs.

Built for:
- 🎓 **Students** who don't have a senior dev to review their code
- 👤 **Solo developers** who want a second pair of eyes
- 🛠️ **Open-source maintainers** drowning in unreviewed PRs

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **AI Code Review** | Detects bugs, bad patterns, and logic errors |
| 📝 **Auto Changelog** | Generates changelogs from commit messages |
| 🔗 **GitHub Action** | Drop into any repo with 3 lines of YAML |
| 🌍 **Language Agnostic** | Works with Python, JS, Java, Go, and more |
| 🆓 **100% Free** | MIT licensed, no paywalls |

---

## 📦 Installation

```bash
pip install devflow-ai
```

Or add directly to your GitHub Actions:

```yaml
# .github/workflows/devflow.yml
name: DevFlow AI Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run DevFlow AI
        uses: rud-13/devflow-ai@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🖥️ CLI Usage

```bash
# Review a local diff
devflow review --diff git_diff.txt

# Generate changelog from commits
devflow changelog --from v1.0.0 --to HEAD

# Analyze code quality
devflow analyze --file src/main.py
```

---

## 📁 Project Structure

```
devflow-ai/
├── devflow/
│   ├── __init__.py        # Package init
│   ├── reviewer.py        # Core AI review logic
│   ├── github_api.py      # GitHub API integration
│   ├── changelog.py       # Changelog generator
│   └── analyzer.py        # Code quality analyzer
├── .github/
│   └── workflows/
│       └── devflow.yml    # GitHub Action definition
├── tests/
│   └── test_reviewer.py   # Unit tests
├── examples/
│   └── sample_review.md   # Sample review output
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🔧 How It Works

```
Your PR / Code
     │
     ▼
┌─────────────────┐
│  DevFlow AI     │
│  ─────────────  │
│  1. Parse diff  │
│  2. AI Review   │
│  3. Post report │
└─────────────────┘
     │
     ▼
📋 Review Comment on PR
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

```bash
git clone https://github.com/rud-13/devflow-ai.git
cd devflow-ai
pip install -r requirements.txt
python -m pytest tests/
```

---

## 📄 License

MIT © [rud-13](https://github.com/rud-13)

---

> ⭐ If this project helped you, please give it a star!
