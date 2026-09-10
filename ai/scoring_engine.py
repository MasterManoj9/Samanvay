"""
Deterministic Readiness Scoring Engine
Calculates an objective 0-100 career/role readiness score with explainability.
Does NOT hallucinate scores; uses empirical weighted factors.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, Any, List, Optional

VERIFICATION_TIER_WEIGHTS = {
    "self_declared": 0.40,
    "ai_assessed": 0.70,
    "faculty_verified": 0.90,
    "industry_verified": 1.00
}

class ReadinessScoringEngine:
    def __init__(
        self,
        weight_skills: float = 0.35,
        weight_assessment: float = 0.20,
        weight_evidence: float = 0.15,
        weight_projects: float = 0.15,
        weight_certs: float = 0.08,
        weight_experience: float = 0.07
    ):
        self.w_skills = weight_skills
        self.w_assessment = weight_assessment
        self.w_evidence = weight_evidence
        self.w_projects = weight_projects
        self.w_certs = weight_certs
        self.w_experience = weight_experience

    def calculate_readiness(
        self,
        student_profile: Dict[str, Any],
        target_role: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compute deterministic readiness score (0-100) and explainability breakdown.
        """
        student_skills = student_profile.get("skills", [])
        assessments = student_profile.get("assessments", [])
        projects = student_profile.get("projects", [])
        certs = student_profile.get("certifications", [])
        internships = student_profile.get("internships", [])

        # 1. Skill Score (Coverage & Proficiency)
        if target_role and "required_skills" in target_role:
            req_skills = target_role["required_skills"]
            student_skill_map = {s.get("skill_id"): s.get("proficiency", 0) for s in student_skills}
            
            matched_scores = []
            for req in req_skills:
                req_id = req.get("skill_id")
                req_min = req.get("min_proficiency", 60)
                curr_prof = student_skill_map.get(req_id, 0)
                ratio = min(1.0, curr_prof / req_min) if req_min > 0 else 1.0
                matched_scores.append(ratio * 100)
            
            skill_score = sum(matched_scores) / len(matched_scores) if matched_scores else 50.0
        else:
            if student_skills:
                profs = [s.get("proficiency", 50) for s in student_skills]
                skill_score = min(100.0, (sum(profs) / len(profs)) * 1.1)
            else:
                skill_score = 20.0

        # 2. Assessment Score
        if assessments:
            ass_scores = [a.get("score_percentage", 0) for a in assessments]
            assessment_score = sum(ass_scores) / len(ass_scores)
        else:
            assessment_score = 40.0

        # 3. Evidence Quality & Verification Tier
        if student_skills:
            verification_factors = [
                VERIFICATION_TIER_WEIGHTS.get(s.get("verification_level", "self_declared"), 0.40)
                for s in student_skills
            ]
            evidence_score = (sum(verification_factors) / len(verification_factors)) * 100
        else:
            evidence_score = 30.0

        # 4. Projects Quality
        if projects:
            proj_points = 0
            for p in projects:
                pts = 40
                if p.get("github_url"):
                    pts += 30
                if p.get("live_demo_url"):
                    pts += 20
                if p.get("is_verified"):
                    pts += 10
                proj_points += min(100, pts)
            project_score = min(100.0, proj_points / max(1, len(projects)) * (1.0 if len(projects) >= 2 else 0.75))
        else:
            project_score = 15.0

        # 5. Certifications
        cert_score = min(100.0, len(certs) * 35.0)

        # 6. Internship / Industry Experience
        exp_score = min(100.0, len(internships) * 50.0)

        # Weighted Total
        total_readiness = (
            (skill_score * self.w_skills) +
            (assessment_score * self.w_assessment) +
            (evidence_score * self.w_evidence) +
            (project_score * self.w_projects) +
            (cert_score * self.w_certs) +
            (exp_score * self.w_experience)
        )
        total_readiness = round(min(100.0, max(0.0, total_readiness)), 1)

        # Generate Explainable Insights
        strengths = []
        improvements = []

        if evidence_score >= 80:
            strengths.append("High verification quotient across core skills (Faculty / Industry verified).")
        elif evidence_score < 60:
            improvements.append("Most skills are self-declared; request faculty verification or pass skill quizzes to boost credibility.")

        if project_score >= 75:
            strengths.append(f"Strong practical portfolio with {len(projects)} repos/live deployments.")
        else:
            improvements.append("Add verified live capstone projects with public GitHub repositories.")

        if assessment_score >= 80:
            strengths.append(f"Outstanding assessment track record ({assessment_score:.0f}% average).")
        elif assessment_score < 65:
            improvements.append("Take technical skill & aptitude tests to elevate your verified baseline.")

        if total_readiness >= 80:
            tier = "Ready for Elite Industry Roles"
            color = "emerald"
        elif total_readiness >= 65:
            tier = "Job & Internship Ready with Minor Gaps"
            color = "blue"
        elif total_readiness >= 45:
            tier = "Intermediate Competency (Developing)"
            color = "amber"
        else:
            tier = "Foundational Stage (Skill Bridge Required)"
            color = "rose"

        return {
            "readiness_score": total_readiness,
            "readiness_tier": tier,
            "badge_color": color,
            "breakdown": {
                "skill_fit": round(skill_score, 1),
                "assessment_score": round(assessment_score, 1),
                "evidence_quality": round(evidence_score, 1),
                "project_portfolio": round(project_score, 1),
                "certifications": round(cert_score, 1),
                "industry_experience": round(exp_score, 1)
            },
            "weights": {
                "skills": self.w_skills,
                "assessment": self.w_assessment,
                "evidence": self.w_evidence,
                "projects": self.w_projects,
                "certs": self.w_certs,
                "experience": self.w_experience
            },
            "strengths": strengths,
            "improvement_areas": improvements,
            "explanation": f"Candidate demonstrates a {total_readiness}/100 readiness index. "
                           f"Strongest pillar: {strengths[0] if strengths else 'practical portfolio foundation'}. "
                           f"Primary leverage area: {improvements[0] if improvements else 'maintain active project commits'}."
        }

scoring_engine = ReadinessScoringEngine()

if __name__ == "__main__":
    sample_student = {
        "name": "Devansh Roy",
        "skills": [
            {"skill_id": "skill_py", "proficiency": 85, "verification_level": "faculty_verified"},
            {"skill_id": "skill_fastapi", "proficiency": 80, "verification_level": "ai_assessed"},
            {"skill_id": "skill_docker", "proficiency": 45, "verification_level": "self_declared"}
        ],
        "assessments": [
            {"topic": "Python & Backend Systems", "score_percentage": 88}
        ],
        "projects": [
            {"title": "Automated Microservice Orchestrator", "github_url": "https://github.com/test/orch", "live_demo_url": "https://orch.io", "is_verified": True}
        ],
        "certifications": [
            {"title": "AWS Certified Cloud Practitioner"}
        ],
        "internships": [
            {"company": "InnoTech Labs", "role": "Backend Intern", "duration_months": 3}
        ]
    }
    
    res = scoring_engine.calculate_readiness(sample_student)
    print("Readiness Calculation Test:")
    print(f"  Score: {res['readiness_score']}/100 ({res['readiness_tier']})")
    print(f"  Breakdown: {res['breakdown']}")
    print(f"  Explanation: {res['explanation']}")
