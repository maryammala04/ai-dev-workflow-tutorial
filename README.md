# AI-Assisted Development Workflow Tutorial

This tutorial teaches you a professional development workflow by having you build and deploy a real project: an e-commerce sales dashboard.

You'll work through it in two parts:

| Part | What you do | Time |
|------|-------------|------|
| [Part 1: Setup](pre-work-setup.md) | Set up accounts, install tools, get your repo ready | 70–100 min |
| [Part 2: Build & Deploy](workshop-build-deploy.md) | Plan with [Superpowers](https://github.com/obra/superpowers) (a skills add-on for Claude Code), track work in `TASKS.md`, build with Claude Code, deploy live | ~3 hours |

## Why this matters

Building with technology in 2026 looks different than it did two years ago. AI assistants have moved from experimental to essential, and companies are looking for people who can work with them effectively.

Claude Code, the tool you'll use throughout this tutorial, is Anthropic's AI coding agent. Unlike a chatbot that only suggests code, it works in your terminal to read your project, edit files, run commands, and debug with you. Getting fluent with it now is the kind of skill companies are starting to hire for.

You're not here to become a software engineer. You're here to learn how to build things when your work calls for it: a dashboard, an automated workflow, a rough prototype. Those skills carry over whether you go into analytics, consulting, or product management.

You're learning this now, at the start of your career. That puts you ahead of many experienced professionals who are still adapting.

| Traditional approach | AI-assisted approach |
|---------------------|---------------------|
| Search Google, copy from Stack Overflow | Ask Claude Code to explain and implement |
| Hours debugging with print statements | AI analyzes errors and suggests fixes |
| Write boilerplate code manually | AI generates scaffolding; you focus on business logic |
| Learn frameworks by reading documentation | AI teaches you as you build |
| Work alone, limited by your own knowledge | AI as a second perspective when you get stuck |

## What you'll build

A Streamlit dashboard with KPI (key performance indicator) scorecards, a sales trend chart, and breakdowns by category and region. Streamlit is an open-source Python framework for building web apps from plain Python scripts.

```
┌─────────────────────────────────────────────────────────────┐
│                E-Commerce Sales Dashboard                    │
├────────────────────────────┬────────────────────────────────┤
│       Total Sales          │       Total Orders             │
│       $1,234,567           │       8,432                    │
├────────────────────────────┴────────────────────────────────┤
│                   Sales Trend (Line Chart)                   │
│    $                                                         │
│    │      ╱╲        ╱╲                                       │
│    │     ╱  ╲      ╱  ╲      ╱                              │
│    │    ╱    ╲    ╱    ╲    ╱                               │
│    │   ╱      ╲  ╱      ╲  ╱                                │
│    │  ╱        ╲╱        ╲╱                                 │
│    └──────────────────────────────────────────── time       │
├────────────────────────────┬────────────────────────────────┤
│    Sales by Category       │    Sales by Region             │
│    (Bar Chart)             │    (Bar Chart)                 │
└────────────────────────────┴────────────────────────────────┘
```

See the finished version: https://sales-dashboard-greg-lontok.streamlit.app/

The dashboard itself is straightforward. The point is the workflow you use to build it.

## The workflow

Every technology company uses a variation of this workflow. You'll experience the entire cycle:

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────┐
│   PRD   │ -> │   TASKS.md   │ -> │ brainstorming│ -> │writing-plans │ -> │  Code  │
│(written)│    │ (milestones) │    │ (design doc) │    │ (impl plan)  │    │(Claude)│
└─────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └────────┘
                                                                              │
┌─────────┐    ┌───────────┐    ┌─────────┐    ┌───────────────────────────────┐
│  Live!  │ <- │  Deploy   │ <- │  Push   │ <- │ executing-plans (TDD + commit)│
│(public) │    │(Streamlit)│    │(GitHub) │    │ on a feature branch           │
└─────────┘    └───────────┘    └─────────┘    └───────────────────────────────┘
```

1. **PRD** (Product Requirements Document): Start with a written specification of what to build
2. **TASKS.md**: Draft your milestones (the deliverables, with IDs like TASK-1) from the PRD into a Markdown board in your repo
3. **brainstorming**: A Superpowers skill that asks clarifying questions and produces a design document
4. **writing-plans**: A Superpowers skill that turns the design into a bite-sized implementation plan covering your milestones
5. **executing-plans**: A Superpowers skill that builds the feature with Claude Code, implementing each task (test-first where the plan flags it)
6. **Commit**: Save your changes with a meaningful message linked to the milestone ID
7. **Push**: Upload your code to GitHub
8. **Deploy**: Make your dashboard publicly accessible

## Key concepts

**Traceability.** Every piece of code traces back to a requirement. When you commit, you include the milestone ID (like TASK-1) in the message, and because `TASKS.md` is versioned in the repo, `git log` shows the whole chain from requirement to code to deployed feature.

**Skill-driven development.** Instead of jumping straight to code, you let Claude's Superpowers skills run a structured process: brainstorming explores what to build, writing-plans turns that into a bite-sized plan, then executing-plans implements task by task, using TDD on the tasks the plan flags for it (test-driven development: write a failing test first, then the code to pass it). This prevents the most common failure mode: building the wrong thing fast.

**AI as a partner.** Claude Code isn't just a code generator. You set the direction and make the judgment calls; it supplies the speed and technical know-how, and explains its reasoning so you learn as you go.

## What you need

- Basic Python knowledge (if you've used pandas or written a few scripts, you're fine)
- A computer running macOS or Windows
- No prior experience with Git or AI coding tools

## Where to start

Open [pre-work-setup.md](pre-work-setup.md) and work through it first, then continue to Part 2.

## Project materials

| Resource | Description |
|----------|-------------|
| [E-Commerce PRD](prd/ecommerce-analytics.md) | The product requirements document you'll build from |
| [Sales data](data/sales-data.csv) | Sample dataset for the dashboard |
| [Live dashboard](https://ai-dev-workflow-tutorial-ggtxcytqgrrybwg4ge5cd3.streamlit.app/) | The deployed sales dashboard, built through this tutorial's workflow |

## License

This tutorial is provided for educational purposes.
