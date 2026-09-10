"""
Hybrid Matching & Explainability Engine
Calculates compatibility score (0-100%) between candidates and opportunities (jobs/internships).
Generates explainable rationale ("Why this opportunity matches you" / "Why this candidate is a top match").
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, Any, List, Optional
from ai.normalizer import normalizer

class MatchingEngine:
    def __init__(
        self,
        weight_mandatory_skills: float = 0.50,
        weight_preferred_skills: float = 0.15,
        weight_eligibility: float = 0.15,
        weight_mode_location: float = 0.10,
        weight_verification_quality: float = 0.10
    ):
        self.w_mand = weight_mandatory_skills
        self.w_pref = weight_preferred_skills
        self.w_elig = weight_eligibility
        self.w_loc = weight_mode_location
        self.w_veri = weight_verification_quality
        self.normalizer = normalizer

    def compute_match(
        self,
        candidate_profile: Dict[str, Any],
        opportunity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate candidate fit for an opportunity.
        Returns match_score (0-100), key matched skills, missing skills, and explainable summary.
        """
        cand_skills = {s.get("skill_id"): s for s in candidate_profile.get("skills", [])}
        req_skills = opportunity.get("required_skills", [])
        
        mandatory_reqs = [s for s in req_skills if s.get("is_mandatory", True)]
        preferred_reqs = [s for s in req_skills if not s.get("is_mandatory", True)]

        matched_mandatory = []
        missing_mandatory = []
        mandatory_scores = []
        verification_scores = []

        tier_weights = {"self_declared": 0.5, "ai_assessed": 0.8, "faculty_verified": 0.95, "industry_verified": 1.0}

        for req in mandatory_reqs:
            sid = req.get("skill_id")
            sname = req.get("name") or (self.normalizer.get_skill_by_id(sid) or {}).get("name", sid)
            min_prof = req.get("min_proficiency", 60)

            if sid in cand_skills:
                cs = cand_skills[sid]
                prof = cs.get("proficiency", 0)
                v_level = cs.get("verification_level", "self_declared")
                
                ratio = min(1.0, prof / min_prof) if min_prof > 0 else 1.0
                mandatory_scores.append(ratio * 100)
                verification_scores.append(tier_weights.get(v_level, 0.5) * 100)
                
                matched_mandatory.append({
                    "skill_id": sid,
                    "name": sname,
                    "proficiency": prof,
                    "verification_level": v_level
                })
            else:
                mandatory_scores.append(0.0)
                verification_scores.append(0.0)
                missing_mandatory.append({
                    "skill_id": sid,
                    "name": sname,
                    "required_level": min_prof
                })

        mand_score = (sum(mandatory_scores) / len(mandatory_scores)) if mandatory_scores else 100.0

        # Preferred skills
        preferred_scores = []
        matched_preferred = []
        for req in preferred_reqs:
            sid = req.get("skill_id")
            sname = req.get("name") or (self.normalizer.get_skill_by_id(sid) or {}).get("name", sid)
            if sid in cand_skills:
                preferred_scores.append(100.0)
                matched_preferred.append(sname)
            else:
                preferred_scores.append(0.0)
        
        pref_score = (sum(preferred_scores) / len(preferred_scores)) if preferred_scores else 80.0

        # Eligibility: CGPA/Degree/Year
        elig_score = 100.0
        min_cgpa = opportunity.get("min_cgpa", 0.0)
        cand_cgpa = candidate_profile.get("cgpa", 8.0)
        if cand_cgpa < min_cgpa:
            elig_score = max(30.0, 100 - (min_cgpa - cand_cgpa) * 30)

        # Work Mode & Location
        loc_score = 100.0
        opp_mode = opportunity.get("work_mode", "Remote").lower()
        cand_mode = candidate_profile.get("preferred_work_mode", "Remote").lower()
        if opp_mode != "remote" and opp_mode != cand_mode and cand_mode != "any":
            loc_score = 70.0

        # Average verification
        avg_veri = (sum(verification_scores) / len(verification_scores)) if verification_scores else 50.0

        # Total Weighted Match
        final_match = (
            (mand_score * self.w_mand) +
            (pref_score * self.w_pref) +
            (elig_score * self.w_elig) +
            (loc_score * self.w_loc) +
            (avg_veri * self.w_veri)
        )
        final_match = round(min(100.0, max(0.0, final_match)), 1)

        # Generate Explainable Rationale
        reasons = []
        if len(matched_mandatory) == len(mandatory_reqs):
            reasons.append(f"Candidate meets 100% of the {len(mandatory_reqs)} mandatory skill requirements.")
        else:
            reasons.append(f"Candidate satisfies {len(matched_mandatory)} out of {len(mandatory_reqs)} mandatory skills.")

        verified_high = [m["name"] for m in matched_mandatory if m["verification_level"] in ("faculty_verified", "industry_verified")]
        if verified_high:
            reasons.append(f"Demonstrates faculty/industry verified proficiency in {', '.join(verified_high[:3])}.")

        if missing_mandatory:
            reasons.append(f"Skill bridge required in: {', '.join([m['name'] for m in missing_mandatory[:2]])}.")

        if final_match >= 85:
            fit_category = "Strong Match"
            badge_color = "emerald"
        elif final_match >= 70:
            fit_category = "High Potential"
            badge_color = "blue"
        elif final_match >= 50:
            fit_category = "Moderate Match"
            badge_color = "amber"
        else:
            fit_category = "Low Match"
            badge_color = "rose"

        return {
            "match_score": final_match,
            "fit_category": fit_category,
            "badge_color": badge_color,
            "matched_mandatory_skills": matched_mandatory,
            "missing_mandatory_skills": missing_mandatory,
            "matched_preferred_skills": matched_preferred,
            "score_factors": {
                "mandatory_skills": round(mand_score, 1),
                "preferred_skills": round(pref_score, 1),
                "eligibility": round(elig_score, 1),
                "mode_location": round(loc_score, 1),
                "verification_quality": round(avg_veri, 1)
            },
            "why_matched": " • ".join(reasons)
        }

matching_engine = MatchingEngine()

if __name__ == "__main__":
    test_candidate = {
        "name": "Isha Malhotra",
        "cgpa": 8.8,
        "preferred_work_mode": "Remote",
        "skills": [
            {"skill_id": "skill_py", "proficiency": 90, "verification_level": "faculty_verified"},
            {"skill_id": "skill_langchain", "proficiency": 80, "verification_level": "ai_assessed"},
            {"skill_id": "skill_vector_db", "proficiency": 75, "verification_level": "self_declared"}
        ]
    }
    test_opportunity = {
        "title": "Generative AI Research Intern",
        "company": "DeepCognition Labs",
        "work_mode": "Remote",
        "min_cgpa": 7.5,
        "required_skills": [
            {"skill_id": "skill_py", "min_proficiency": 80, "is_mandatory": True},
            {"skill_id": "skill_langchain", "min_proficiency": 70, "is_mandatory": True},
            {"skill_id": "skill_mlops", "min_proficiency": 65, "is_mandatory": True}
        ]
    }
    match = matching_engine.compute_match(test_candidate, test_opportunity)
    print("Match Evaluation Result:")
    print(f"  Match Score: {match['match_score']}% ({match['fit_category']})")
    print(f"  Why it matches: {match['why_matched']}")
    print(f"  Missing Skills: {[s['name'] for s in match['missing_mandatory_skills']]}")
