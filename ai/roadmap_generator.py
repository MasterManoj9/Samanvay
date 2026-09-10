"""
Learning Roadmap Generator
Generates evidence-driven, goal-oriented learning roadmaps to close specific student skill gaps.
Constructs ordered milestones with projects, assessments, and verifiable outcomes.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Dict, Any, Optional
from ai.normalizer import normalizer

# Pre-defined curated learning sequences for common critical gaps
CURATED_ROADMAP_PATHS: Dict[str, List[Dict[str, Any]]] = {
    "skill_mlops": [
        {
            "step": 1,
            "title": "Containerization Essentials with Docker",
            "skill": "Docker",
            "est_hours": 12,
            "description": "Containerize a Python machine learning inference service using Dockerfile, multi-stage builds, and volume mounting.",
            "deliverable": "GitHub Repo with Dockerized Fast-API ML model and passing container healthchecks.",
            "evidence_target": "Project Artifact"
        },
        {
            "step": 2,
            "title": "Container Orchestration with Kubernetes",
            "skill": "Kubernetes",
            "est_hours": 16,
            "description": "Deploy ML containers to local Minikube/K8s cluster with Deployments, Services, and horizontal pod autoscalers.",
            "deliverable": "Kubernetes YAML manifests for model serving with rolling update strategy.",
            "evidence_target": "Project Artifact"
        },
        {
            "step": 3,
            "title": "Automated Testing & CI/CD Pipelines",
            "skill": "CI/CD",
            "est_hours": 10,
            "description": "Build automated GitHub Actions workflow to run unit tests, build Docker image, and push to container registry.",
            "deliverable": "Green GitHub Actions workflow badge and automated test suite.",
            "evidence_target": "Project Artifact"
        },
        {
            "step": 4,
            "title": "Model Tracking & Deployment (MLflow / BentoML)",
            "skill": "MLOps",
            "est_hours": 18,
            "description": "Track model metrics, hyperparameters, and artifacts using MLflow. Package and serve production endpoint.",
            "deliverable": "Live hosted MLflow experiment dashboard and deployed inference REST API.",
            "evidence_target": "Faculty/Industry Verifiable Capstone"
        }
    ],
    "skill_rag": [
        {
            "step": 1,
            "title": "Vector Embeddings & Semantic Search",
            "skill": "Vector Databases",
            "est_hours": 8,
            "description": "Generate embeddings with sentence-transformers and index them into ChromaDB/Pinecone.",
            "deliverable": "Colab notebook / repo demonstrating cosine similarity search over custom PDFs.",
            "evidence_target": "Project Artifact"
        },
        {
            "step": 2,
            "title": "Orchestrating RAG Pipelines with LangChain",
            "skill": "LangChain",
            "est_hours": 14,
            "description": "Implement chunking strategies, multi-query retrievers, and re-ranking pipelines.",
            "deliverable": "Working Python CLI querying a localized document store with context injection.",
            "evidence_target": "Project Artifact"
        },
        {
            "step": 3,
            "title": "Production RAG App with FastAPI & React UI",
            "skill": "Retrieval-Augmented Generation",
            "est_hours": 20,
            "description": "Full-stack enterprise document Q&A portal with streaming tokens, citation footnotes, and hallucinations guardrails.",
            "deliverable": "Deployed full-stack app with GitHub repository & demo video.",
            "evidence_target": "Faculty/Industry Verifiable Capstone"
        }
    ],
    "skill_docker": [
        {
            "step": 1,
            "title": "Docker Core Concepts & CLI",
            "skill": "Docker",
            "est_hours": 6,
            "description": "Understand images, containers, layers, networking, and daemon architecture.",
            "deliverable": "Completed interactive terminal challenges and containerized web app.",
            "evidence_target": "Assessment Quiz"
        },
        {
            "step": 2,
            "title": "Multi-Container Applications with Docker Compose",
            "skill": "Docker",
            "est_hours": 10,
            "description": "Orchestrate a multi-tier app: FastAPI backend, PostgreSQL database, and Redis cache with healthchecks.",
            "deliverable": "Working docker-compose.yml running entire multi-service stack in 1 command.",
            "evidence_target": "Project Artifact"
        }
    ]
}

class RoadmapGenerator:
    def __init__(self):
        self.normalizer = normalizer

    def generate_roadmap_for_gaps(
        self,
        gaps: List[Dict[str, Any]],
        target_role_title: str = "Target Role"
    ) -> Dict[str, Any]:
        """
        Generate structured milestone roadmap addressing the student's highest severity gaps.
        """
        milestones = []
        total_hours = 0
        milestone_counter = 1

        # Focus primarily on Critical, High, and Medium gaps
        actionable_gaps = [g for g in gaps if g.get("gap_points", 0) > 15]

        for gap in actionable_gaps:
            sid = gap.get("skill_id")
            sname = gap.get("skill_name")
            curated = CURATED_ROADMAP_PATHS.get(sid)

            if curated:
                for step in curated:
                    milestones.append({
                        "id": f"milestone_{milestone_counter}",
                        "step_number": milestone_counter,
                        "title": step["title"],
                        "target_skill": step["skill"],
                        "estimated_hours": step["est_hours"],
                        "severity_addressed": gap.get("severity", "High"),
                        "description": step["description"],
                        "deliverable": step["deliverable"],
                        "evidence_target": step["evidence_target"],
                        "status": "in_progress" if milestone_counter == 1 else "locked"
                    })
                    total_hours += step["est_hours"]
                    milestone_counter += 1
            else:
                # Generic structured 2-phase module for any canonical skill
                milestones.append({
                    "id": f"milestone_{milestone_counter}",
                    "step_number": milestone_counter,
                    "title": f"Core Competencies: {sname}",
                    "target_skill": sname,
                    "estimated_hours": 12,
                    "severity_addressed": gap.get("severity", "Medium"),
                    "description": f"Master foundational syntax, paradigms, and architecture patterns for {sname}.",
                    "deliverable": f"Pass the {sname} Skill Verification Assessment (80%+ score).",
                    "evidence_target": "Skill Assessment",
                    "status": "in_progress" if milestone_counter == 1 else "locked"
                })
                total_hours += 12
                milestone_counter += 1

                milestones.append({
                    "id": f"milestone_{milestone_counter}",
                    "step_number": milestone_counter,
                    "title": f"Applied Project: {sname} Implementation",
                    "target_skill": sname,
                    "estimated_hours": 18,
                    "severity_addressed": gap.get("severity", "Medium"),
                    "description": f"Build and deploy an end-to-end practical project highlighting {sname}.",
                    "deliverable": f"Public GitHub repository with documentation, test coverage, and live demo.",
                    "evidence_target": "Faculty Verified Project",
                    "status": "locked"
                })
                total_hours += 18
                milestone_counter += 1

        weeks_est = max(1, round(total_hours / 15))  # based on 15h study/week

        return {
            "target_role": target_role_title,
            "total_milestones": len(milestones),
            "estimated_total_hours": total_hours,
            "estimated_weeks": weeks_est,
            "milestones": milestones,
            "summary": f"Personalized {weeks_est}-week gap-closing roadmap comprising {len(milestones)} verifiable milestones."
        }

roadmap_generator = RoadmapGenerator()

if __name__ == "__main__":
    test_gaps = [
        {"skill_id": "skill_mlops", "skill_name": "MLOps", "gap_points": 45, "severity": "High"},
        {"skill_id": "skill_rag", "skill_name": "Retrieval-Augmented Generation", "gap_points": 30, "severity": "Medium"}
    ]
    rm = roadmap_generator.generate_roadmap_for_gaps(test_gaps, "AI Systems Engineer")
    print(f"Roadmap generated: {rm['summary']}")
    for m in rm["milestones"]:
        print(f"  Step {m['step_number']}: {m['title']} ({m['estimated_hours']} hrs, Status: {m['status']})")
