"""
Skill Gap Engine
1. Micro: Computes individual student skill gaps against target roles.
2. Macro: Computes institutional student supply vs. real-time industry demand.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, Any, List, Optional
from ai.normalizer import normalizer

def classify_gap_severity(gap: float) -> Dict[str, str]:
    if gap <= 0:
        return {"level": "Proficient", "color": "emerald", "badge": "Met / Exceeded"}
    elif gap <= 15:
        return {"level": "Low", "color": "blue", "badge": "Minor Refinement"}
    elif gap <= 35:
        return {"level": "Medium", "color": "amber", "badge": "Skill Bridge Needed"}
    elif gap <= 55:
        return {"level": "High", "color": "orange", "badge": "Significant Gap"}
    else:
        return {"level": "Critical", "color": "rose", "badge": "Urgent Pre-requisite"}

class SkillGapEngine:
    def __init__(self):
        self.normalizer = normalizer

    def analyze_student_gaps(
        self,
        student_skills: List[Dict[str, Any]],
        target_role_skills: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare student profile skills against required skills for a target role/job.
        """
        student_map = {s.get("skill_id"): s for s in student_skills}
        gaps = []
        total_gap = 0
        critical_count = 0

        for req in target_role_skills:
            skill_id = req.get("skill_id")
            skill_info = self.normalizer.get_skill_by_id(skill_id) or {
                "name": req.get("name", "Unknown"),
                "category": "Domain"
            }
            required_level = req.get("min_proficiency", 70)
            is_mandatory = req.get("is_mandatory", True)

            student_entry = student_map.get(skill_id)
            current_level = student_entry.get("proficiency", 0) if student_entry else 0
            verification_level = student_entry.get("verification_level", "unverified") if student_entry else "not_started"

            gap_points = max(0, required_level - current_level)
            severity = classify_gap_severity(gap_points)

            if severity["level"] in ("High", "Critical"):
                critical_count += 1
            total_gap += gap_points

            gaps.append({
                "skill_id": skill_id,
                "skill_name": skill_info["name"],
                "category": skill_info.get("category", "General"),
                "is_mandatory": is_mandatory,
                "required_level": required_level,
                "current_level": current_level,
                "gap_points": gap_points,
                "verification_level": verification_level,
                "severity": severity["level"],
                "badge_color": severity["color"],
                "badge_label": severity["badge"]
            })

        # Sort gaps by severity (Critical first, then High, etc.)
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Proficient": 4}
        gaps.sort(key=lambda x: (severity_order.get(x["severity"], 5), -x["gap_points"]))

        avg_gap = round(total_gap / len(gaps), 1) if gaps else 0
        readiness_estimate = max(0, min(100, 100 - avg_gap))

        return {
            "target_role_evaluated": True,
            "overall_gap_index": avg_gap,
            "readiness_estimate": readiness_estimate,
            "critical_gap_count": critical_count,
            "total_skills_evaluated": len(gaps),
            "gaps": gaps
        }

    def compute_macro_institution_gaps(
        self,
        student_skill_distribution: List[Dict[str, Any]],
        industry_postings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Aggregates batch student supply % against industry demand % to pinpoint institutional shortages.
        """
        demand_counts: Dict[str, int] = {}
        total_postings = max(1, len(industry_postings))

        for post in industry_postings:
            for s in post.get("required_skills", []):
                sid = s.get("skill_id")
                demand_counts[sid] = demand_counts.get(sid, 0) + 1

        student_supply_counts: Dict[str, int] = {}
        total_students = max(1, len(student_skill_distribution))

        for student in student_skill_distribution:
            for s in student.get("skills", []):
                if s.get("proficiency", 0) >= 50:  # count only competent supply
                    sid = s.get("skill_id")
                    student_supply_counts[sid] = student_supply_counts.get(sid, 0) + 1

        macro_insights = []
        all_skills = set(list(demand_counts.keys()) + list(student_supply_counts.keys()))

        for sid in all_skills:
            skill = self.normalizer.get_skill_by_id(sid)
            if not skill:
                continue

            demand_pct = round((demand_counts.get(sid, 0) / total_postings) * 100, 1)
            supply_pct = round((student_supply_counts.get(sid, 0) / total_students) * 100, 1)
            net_delta = round(demand_pct - supply_pct, 1)

            if net_delta > 25:
                status = "Critical Shortage"
                color = "rose"
                recommendation = f"Urgent institutional boot-camp required: 4-week intensive module on {skill['name']}."
            elif net_delta > 10:
                status = "Moderate Deficit"
                color = "amber"
                recommendation = f"Integrate practical lab coursework for {skill['name']} into 5th/6th semester curriculum."
            elif net_delta < -15:
                status = "Surplus"
                color = "blue"
                recommendation = f"Healthy talent pool in {skill['name']}; channel students into advanced specializations."
            else:
                status = "Balanced"
                color = "emerald"
                recommendation = f"Current supply matches market absorption rate for {skill['name']}."

            macro_insights.append({
                "skill_id": sid,
                "skill_name": skill["name"],
                "category": skill["category"],
                "cluster": skill.get("cluster", "General"),
                "industry_demand_pct": demand_pct,
                "student_supply_pct": supply_pct,
                "net_deficit": net_delta,
                "status": status,
                "badge_color": color,
                "curriculum_recommendation": recommendation
            })

        macro_insights.sort(key=lambda x: -x["net_deficit"])
        return macro_insights

gap_engine = SkillGapEngine()

if __name__ == "__main__":
    test_student_skills = [
        {"skill_id": "skill_py", "proficiency": 80, "verification_level": "faculty_verified"},
        {"skill_id": "skill_mlops", "proficiency": 25, "verification_level": "self_declared"}
    ]
    test_target_role = [
        {"skill_id": "skill_py", "min_proficiency": 75, "is_mandatory": True},
        {"skill_id": "skill_mlops", "min_proficiency": 70, "is_mandatory": True},
        {"skill_id": "skill_docker", "min_proficiency": 65, "is_mandatory": True}
    ]
    
    result = gap_engine.analyze_student_gaps(test_student_skills, test_target_role)
    print("Individual Skill Gap Test Result:")
    for g in result["gaps"]:
        print(f"  Skill: {g['skill_name']} | Current: {g['current_level']} | Req: {g['required_level']} | Gap: {g['gap_points']} ({g['severity']})")
