# 🚀 SAMANVAY (समन्वय)

> **Assess. Build. Verify. Connect.**  
> *AI-powered Academia–Industry Skill Intelligence & Collaboration Platform*  
> **Smart India Hackathon (SIH)** — Academia–Industry Collaboration Solution

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Language-Python%203.11-3776ab?logo=python)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38bdf8?logo=tailwindcss)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20Supabase-336791?logo=postgresql)](https://www.postgresql.org/)

---

## 📌 Executive Summary

**Samanvay** is an enterprise-grade skill intelligence network designed to bridge the structural disconnect between higher education institutions and industry demand. 

Unlike traditional job boards that rely on unverified, self-reported resumes, Samanvay establishes an **empirical, evidence-backed skill ecosystem** connecting four key stakeholders:
* 🎓 **Students** seeking targeted career readiness and verified opportunities.
* 🏢 **Industry** seeking high-precision candidate matching with verifiable proof of competence.
* 👨‍🏫 **Academicians & Faculty** validating student projects, driving joint research, and upskilling through FDPs.
* 🏛️ **Institutions & Leadership** tracking macro skill supply vs. industry demand deficits and restructuring curricula.

---

## ⚡ Core Differentiator: Evidence-Driven Skill Intelligence

In Samanvay, skills are not static buzzwords on a resume; they exist on a **4-Tier Empirical Verification Ladder**:

```
[ Tier 1: Self-Declared ]
         │ (Student claims knowledge)
         ▼
[ Tier 2: AI-Assessed ]
         │ (Validated via standardized technical quizzes & code analysis)
         ▼
[ Tier 3: Faculty-Verified ]
         │ (Vouched by academic mentors via verifiable project repositories & capstone reviews)
         ▼
[ Tier 4: Industry-Verified ]
           (Earned via completed internships, corporate hackathons, or live sponsored challenges)
```

### The "SkillForge" Core Loop
```
[ASSESS] ➔ [PROFILE] ➔ [UNDERSTAND] ➔ [IDENTIFY GAPS] ➔ [LEARN] ➔ [BUILD EVIDENCE]
    ▲                                                                      │
    │                                                                      ▼
[UPDATE PROFILE] ◄── [EXPERIENCE] ◄── [APPLY] ◄── [MATCH] ◄── [VERIFY]
```

---

## 🧠 Core Intelligence Engines

### 1. Canonical Skill Normalizer & Taxonomies
* Automatically resolves aliases, typos, and abbreviations into canonical taxonomy IDs.
* *Examples:* `ReactJS`, `react.js`, `React` $ightarrow$ `React` | `ML`, `machine-learning` $ightarrow$ `Machine Learning` | `k8s` $ightarrow$ `Kubernetes`.
* Eliminates fragmented and duplicate skill records across candidate profiles and job postings.

### 2. Deterministic 0–100 Readiness Scoring
* Readiness scores are computed using an objective weighted algorithm—**never hallucinated by an LLM**:
  $$	ext{Readiness} = (0.35 	imes S_{	ext{fit}}) + (0.20 	imes A_{	ext{test}}) + (0.15 	imes E_{	ext{veri}}) + (0.15 	imes P_{	ext{proj}}) + (0.08 	imes C_{	ext{cert}}) + (0.07 	imes X_{	ext{exp}})$$
* An explainability engine generates actionable summaries: *"Why you scored 82/100, your top verified strengths, and high-priority improvement areas."*

### 3. Dual-Lens Skill Gap Engine
* **Micro (Student):** Detects exact proficiency deficits against target role requirements (e.g., MLOps student level 25 vs. required 70 $ightarrow$ 45-point gap $ightarrow$ classified as **High Severity**).
* **Macro (Institution):** Aggregates college-wide student supply % against live industry job demand % (e.g., 63% demand vs. 29% student supply $ightarrow$ **Critical Shortage Alert**).

### 4. Goal-Oriented Learning Roadmap Generator
* Converts identified skill gaps into step-by-step milestone learning sequences with concrete deliverables and verifiable artifacts (e.g., Docker containerization $ightarrow$ Kubernetes manifests $ightarrow$ CI/CD automation $ightarrow$ Deployed MLOps inference pipeline).

### 5. Hybrid Matching & Explainable Recruiting
* Computes candidate-opportunity compatibility based on mandatory skill thresholds, preferred competencies, academic eligibility, and work mode preferences.
* Generates clear recruiter insights: *"Candidate meets 3/3 mandatory requirements with faculty-verified credentials in Python & FastAPI."*

---

## 👥 Multi-Stakeholder Role Architecture

Every stakeholder accesses a dedicated portal while sharing a unified, cohesive design system:

| Role | Primary Features | Target Routes |
| :--- | :--- | :--- |
| **🎓 Student** | Skill radar, assessment engine, gap analysis, roadmap, 1-click verified apply | `/student/dashboard`<br>`/student/skills`<br>`/student/gaps`<br>`/student/roadmap`<br>`/student/opportunities` |
| **🏢 Industry** | Role posting with weighted skills, AI candidate match, Kanban pipeline, academia collaboration | `/industry/dashboard`<br>`/industry/opportunities/new`<br>`/industry/candidates`<br>`/industry/matching` |
| **👨‍🏫 Academician** | Student evidence verification queue, FDP programs, faculty internships, joint industry research | `/academician/dashboard`<br>`/academician/verifications`<br>`/academician/research`<br>`/academician/mentorship` |
| **🏛️ Institution** | Macro skill supply vs. demand analytics, placement forecasts, automated curriculum recommendations | `/institution/dashboard`<br>`/institution/skills`<br>`/institution/demand`<br>`/institution/analytics`<br>`/institution/training` |
| **🛡️ Admin** | System audit logs, RBAC authorization, master skill taxonomy & alias management | `/admin/dashboard`<br>`/admin/taxonomies`<br>`/admin/users` |

---

## 🏗️ Technical Architecture & Monorepo Layout

```
Samanvay/
├── frontend/                     # Next.js 14 App Router, TypeScript, Tailwind CSS
│   ├── src/
│   │   ├── app/                  # RBAC route groups: (auth), (dashboard)
│   │   ├── components/
│   │   │   ├── ui/               # Base primitives (shadcn/ui)
│   │   │   ├── shared/           # SkillCard, ReadinessScore, SkillGapCard, etc.
│   │   │   └── layout/           # Role-aware Sidebar, Topbar, Demo Role-Switcher
│   │   ├── lib/                  # Utilities & API client
│   │   └── types/                # TypeScript schema contracts
│   └── package.json
│
├── backend/                      # FastAPI (Python 3.11), Pydantic v2
│   ├── app/
│   │   ├── api/v1/               # Modular REST endpoints (auth, students, matching, etc.)
│   │   ├── core/                 # Config, security, database session
│   │   ├── models/               # SQLAlchemy ORM models (20+ core entities)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   └── services/             # Scoring, matching & analytics logic
│   ├── requirements.txt
│   └── main.py
│
├── ai/                           # Modular AI Intelligence Layer
│   ├── normalizer.py             # Canonical skill & alias resolver
│   ├── skill_extractor.py        # Unstructured resume & project entity extraction
│   ├── scoring_engine.py         # Deterministic readiness calculation
│   ├── gap_engine.py             # Micro & Macro skill gap analysis
│   ├── roadmap_generator.py      # Actionable milestone curriculum paths
│   └── matching_engine.py        # Hybrid candidate compatibility & explainability
│
├── demo-data/                    # High-fidelity realistic seed data
│   ├── skills_taxonomy.json      # 69+ canonical tech skills with 300+ aliases
│   └── build_taxonomy.py         # Automated taxonomy builder
│
├── docs/                         # Architectural specs & SIH evaluation guides
├── TODO.md                       # Comprehensive Master Engineering Checklist
└── README.md
```

---

## 🎬 The SIH Demonstration Flow (12 Steps)

1. **Student Login:** Student signs in and completes a baseline skill assessment.
2. **AI Skill Extraction:** Resume and portfolio text are parsed and mapped to canonical skills.
3. **Career Goal Selection:** Student designates "AI Systems Engineer" as their target trajectory.
4. **Skill Gap Detection:** System detects a critical 45-point deficit in MLOps (Level 25 vs. Required 70).
5. **Personalized Roadmap:** System generates an actionable 4-milestone curriculum (Docker $ightarrow$ K8s $ightarrow$ CI/CD $ightarrow$ MLflow).
6. **Industry Job Posting:** Tech recruiter posts an "AI Engineer Internship" with weighted skill requirements.
7. **AI Candidate Matching:** Engine ranks candidate compatibility (88%) with human-readable rationale.
8. **1-Click Application:** Student applies; application enters recruiter's live recruitment pipeline.
9. **Faculty Verification:** Academic professor reviews student's capstone repository and signs off on verification.
10. **Readiness Recalculation:** Skill status upgrades to `Faculty-Verified`, boosting student readiness index.
11. **Institutional Macro Radar:** Dean views institutional analytics showing a 63% demand vs. 29% supply deficit for MLOps.
12. **Curriculum Intervention:** System delivers an automated training recommendation: *"Host a 4-week Docker & Kubernetes BootCamp"*.

---

## 🛠️ Quickstart & Local Setup

### Prerequisites
* **Node.js:** v18.0.0 or higher (v22+ recommended)
* **Python:** 3.10 or higher (3.11 recommended)
* **Git**

### 1. Clone Repository
```bash
git clone https://github.com/MasterManoj9/Samanvay.git
cd Samanvay
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the application.

---

## 🎯 Engineering Rules & Quality Standards

* **Zero Arbitrary Redesigns:** Strict adherence to the Stitch design system, typography, component language, and spacing hierarchy.
* **Deterministic Intelligence:** Scores and matching metrics are computed algorithmically; AI generates the natural-language explainability layer.
* **No Unnecessary Complexity:** Clean modular monolith architecture without unwarranted microservices.
* **Strict RBAC:** Role-based access control protecting student, industry, faculty, and institutional routes.

---

## 📄 License & Attribution

Developed for the **Smart India Hackathon (SIH)**.  
Lead Developer & Maintainer: **[MasterManoj9](https://github.com/MasterManoj9)** (`yoursmanoj171@gmail.com`)
