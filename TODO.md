# SAMANVAY — MASTER ENGINEERING TODO LIST

> **Tagline:** Assess. Build. Verify. Connect.  
> **Positioning:** AI-powered Academia–Industry Skill Intelligence & Collaboration Platform (Smart India Hackathon).  
> **Core Differentiator:** Evidence-driven Skill Intelligence (Not a generic job board).

---

## 🔄 The "SkillForge" Core Loop
```
ASSESS ➔ PROFILE ➔ UNDERSTAND ➔ IDENTIFY GAPS ➔ LEARN ➔ BUILD EVIDENCE ➔ VERIFY ➔ MATCH ➔ APPLY ➔ EXPERIENCE ➔ UPDATE PROFILE
```

---

## 📋 Phase-by-Phase Roadmap

### Phase 1: Foundation, Data Architecture & Taxonomies
- [ ] **1.1 Monorepo Architecture Setup**
  - [ ] Configure directory structure: `frontend/`, `backend/`, `ai/`, `database/`, `docs/`, `demo-data/`
  - [ ] Setup root environment templates (`.env.example`) and Git ignore rules
  - [ ] Establish Git commit conventions (`feat:`, `fix:`, `refactor:`, `ui:`, `test:`, `docs:`, `chore:`)
- [ ] **1.2 Relational Database Schema (Core 20+ Entities)**
  - [ ] `users` & `profiles` (Auth, RBAC roles: STUDENT, INDUSTRY, ACADEMICIAN, INSTITUTION, ADMIN)
  - [ ] `skills` & `skill_aliases` (Canonical taxonomy, aliases, categories, clusters)
  - [ ] `student_skills` (Proficiency 0–100, verification tier, verified date)
  - [ ] `skill_evidence` (Evidence types: Assessment, Project, Cert, Internship; verifier notes)
  - [ ] `assessments` & `assessment_results` (Quiz bank, scores, topic breakdowns)
  - [ ] `projects` (Title, description, tech stack, GitHub repo URL, live URL, verification flag)
  - [ ] `certifications` & `internships_completed` (Credentials, duration, certificates)
  - [ ] `opportunities` & `opportunity_skills` (Jobs/Internships, min proficiency, mandatory vs preferred)
  - [ ] `applications` (Recruitment stages: applied, shortlisted, interview, offered, rejected)
  - [ ] `learning_programs` & `learning_skills` (Gap-based roadmaps, milestone deliverables)
  - [ ] `industry_profiles` (Company details, domain, active postings)
  - [ ] `faculty_profiles` (Department, research interests, verification history)
  - [ ] `academic_opportunities` (FDPs, consulting, joint research statements)
  - [ ] `skill_demand` & `institution_analytics` (Aggregated supply vs demand metrics)
  - [ ] `notifications` (Cross-role alerts)
- [ ] **1.3 Master Skill Taxonomy & Aliases**
  - [ ] Curate canonical tech, soft, and domain skills
  - [ ] Map real-world aliases (e.g., `React.js` / `ReactJS` → `React`; `k8s` → `Kubernetes`)
- [ ] **1.4 Realistic Demo Seed Dataset**
  - [ ] Indian academia dataset (Institutions, departments, student batches)
  - [ ] Realistic companies & tech job/internship listings
  - [ ] Faculty research profiles & pending verification queue
  - [ ] Pre-calculated aggregate demand and supply benchmarks

---

### Phase 2: Core AI & Intelligence Engines
- [ ] **2.1 Skill Normalization Service**
  - [ ] Exact alias lookup & punctuation/casing sanitizer
  - [ ] Duplicate skill prevention filter
- [ ] **2.2 Skill Extraction Pipeline**
  - [ ] Unstructured text parsing (Resume, project abstracts, certificates)
  - [ ] Confidence scoring and occurrence frequency tracking
  - [ ] Context snippet extraction
- [ ] **2.3 Deterministic Readiness Scoring Engine (0–100)**
  - [ ] Weighted formula computation:
    - Skill Compatibility (35%)
    - Assessment Performance (20%)
    - Evidence Verification Tier (15%)
    - Project Portfolio Quality (15%)
    - Certifications (8%)
    - Industry Experience (7%)
  - [ ] Explainability generator: "Why you scored X" with strengths and improvement priorities
- [ ] **2.4 Skill Gap Engine (Dual-Lens)**
  - [ ] *Student Micro-Lens:* Compare current vs target role levels → categorize gaps into Low, Medium, High, Critical
  - [ ] *Institution Macro-Lens:* Compare batch-wide student supply % vs industry demand % → detect critical skill shortages
- [ ] **2.5 Goal-Oriented Learning Roadmap Generator**
  - [ ] Map identified gaps to step-by-step milestone sequences
  - [ ] Assign concrete deliverables per milestone (e.g., Dockerize ML model, deploy API)
  - [ ] Estimate completion timelines
- [ ] **2.6 Hybrid Matching & Explainability Engine**
  - [ ] Calculate candidate-opportunity compatibility score
  - [ ] Evaluate mandatory skills, preferred skills, CGPA eligibility, work mode, and verification tiers
  - [ ] Generate natural language explanation: "Why this opportunity matches you"

---

### Phase 3: Shared "Stitch" Design System & Primitives
- [ ] **3.1 Global Shell & Navigation**
  - [ ] Role-aware responsive Sidebar & Topbar
  - [ ] Quick Role-Switcher Bar (Student ↔ Industry ↔ Faculty ↔ Institution) for demo presentations
  - [ ] Notifications center & user profile menu
- [ ] **3.2 Shared Component Library**
  - [ ] `SkillCard` (Proficiency meter, verification tier indicator, evidence count)
  - [ ] `ReadinessScore` (Radial gauge, radar breakdown, tier status)
  - [ ] `SkillGapCard` (Required vs actual level comparison, severity badge)
  - [ ] `OpportunityCard` (Role details, match score badge, missing skill warning, 1-click apply)
  - [ ] `CandidateCard` (Recruiter card with compatibility %, verified evidence badges, quick review)
  - [ ] `AIInsightCard` (Highlighted summary with explainability bullet points)
  - [ ] `MetricCard` (KPI value, trend %, icon, sparkline)
  - [ ] `VerificationBadge` (Self-declared, AI-assessed, Faculty-verified, Industry-verified)
  - [ ] `ApplicationTimeline` (Visual step tracker from application to offer)
  - [ ] `ChartCard` (Recharts wrapper for skill radar, supply-demand delta, pipeline funnels)
  - [ ] `DataTable`, `ProfileCard`, `Search`, `Filters`, `Modal`, `EmptyState`, `Toast`

---

### Phase 4: Role-Specific Portals & Routes

#### 4.1 Student Portal (`/student/*`)
- [ ] `/student/dashboard`: High-level readiness index, top verified skills, active gaps, top opportunity matches
- [ ] `/student/profile` & `/student/portfolio`: Resume upload & parser, project repository links, certifications, verified badges
- [ ] `/student/skills`: Skill matrix with verification status & request verification button for faculty
- [ ] `/student/assessments`: Technical & aptitude skill verification quizzes with instant scoring
- [ ] `/student/gaps`: Target career goal selector with live gap breakdown (Low/Med/High/Critical)
- [ ] `/student/roadmap`: Interactive personalized milestone roadmap with deliverables
- [ ] `/student/opportunities`: Search & filter jobs/internships with match scores and "Why You Match" drawer
- [ ] `/student/applications`: Application status tracking pipeline with employer feedback

#### 4.2 Industry Portal (`/industry/*`)
- [ ] `/industry/dashboard`: Active postings, candidate pool stats, top matched talent
- [ ] `/industry/opportunities/new`: Opportunity creation wizard with weighted skill requirements and eligibility
- [ ] `/industry/candidates`: Talent search filtered by verified skills, readiness score, and institution
- [ ] `/industry/matching`: AI candidate ranking with explainable compatibility scores
- [ ] `/industry/applications`: Kanban recruitment pipeline (Applied → Shortlisted → Interview → Offer)
- [ ] `/industry/collaboration`: Post research problem statements, invite faculty consultants, propose guest lectures

#### 4.3 Academician / Faculty Portal (`/academician/*`)
- [ ] `/academician/dashboard`: Pending student verification requests, active mentees, industry research invites
- [ ] `/academician/verifications`: Review student project evidence (GitHub repo, demo, report) with 1-click verify & remarks
- [ ] `/academician/opportunities`: Faculty Development Programs (FDPs) and industry sabbatical internships
- [ ] `/academician/research`: Industry research collaboration problem statements & joint grant submissions
- [ ] `/academician/mentorship`: Capstone project oversight and student guidance tracking

#### 4.4 Institution / Leadership Portal (`/institution/*`)
- [ ] `/institution/dashboard`: Institutional skill health, placement readiness index, industry partner network
- [ ] `/institution/skills`: Department-wise skill inventory and competency distribution
- [ ] `/institution/demand`: Industry Demand vs Student Supply radar with critical shortage alerts (e.g., MLOps deficit)
- [ ] `/institution/analytics`: Placement projections, internship conversion rates, hiring partner breakdown
- [ ] `/institution/training`: AI-recommended curriculum interventions and targeted boot-camps

---

### Phase 5: End-to-End Demo Story Integration & Polish
- [ ] **5.1 Execute the 14-Step End-to-End SIH Demo Flow**
  1. Student logs in → takes technical assessment
  2. Profile auto-updates with AI-extracted & normalized skills
  3. Student sets "AI Systems Engineer" target role → views MLOps gap (25 vs 70)
  4. Personalized learning roadmap generates to bridge MLOps gap
  5. Industry recruiter logs in → posts "AI Engineer Internship" demanding MLOps & LangChain
  6. Matching engine calculates candidate compatibility & generates "Why this candidate matches"
  7. Student applies in 1 click → status updates across both portals
  8. Faculty logs in → reviews student's capstone project → approves verification
  9. Skill status upgrades to `Faculty-verified` → Student readiness score increases
  10. Institution leadership logs in → views 63% demand vs 29% supply for MLOps
  11. System presents institutional training recommendation: "Host 4-week Docker & Kubernetes BootCamp"
  12. Academician discovers relevant industry research collaboration
- [ ] **5.2 Hackathon Presentation Features**
  - [ ] Global persistent "Role Switcher" bar for instant 1-click switching during judging
  - [ ] Fully responsive layout with enterprise dark/light theme consistency
  - [ ] Zero runtime console errors, clean loading skeletons, and informative empty states
