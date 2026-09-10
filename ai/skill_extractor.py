"""
Skill Extraction Engine
Extracts canonical skills from unstructured text (resumes, project abstracts, certificates).
Works fully offline with regex/n-gram dictionary matching, with optional LLM augmentation.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
from typing import List, Dict, Any, Optional
from ai.normalizer import normalizer, SkillNormalizer

class SkillExtractor:
    def __init__(self, norm: Optional[SkillNormalizer] = None):
        self.normalizer = norm or normalizer

    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Scan text for all canonical skills and aliases.
        Returns a list of extracted skills with frequency, context snippet, and confidence.
        """
        if not text:
            return []

        clean_text = text.lower()
        extracted: Dict[str, Dict[str, Any]] = {}

        for skill in self.normalizer.get_all_skills():
            skill_id = skill["id"]
            names_to_check = [skill["name"]] + skill.get("aliases", [])
            
            for alias in names_to_check:
                pattern = r"(?:\b|_)" + re.escape(alias.lower()) + r"(?:\b|_)"
                matches = list(re.finditer(pattern, clean_text))
                
                if matches:
                    if skill_id not in extracted:
                        first_match = matches[0]
                        start = max(0, first_match.start() - 35)
                        end = min(len(text), first_match.end() + 35)
                        snippet = text[start:end].replace("\n", " ").strip()
                        
                        extracted[skill_id] = {
                            "skill_id": skill_id,
                            "name": skill["name"],
                            "category": skill["category"],
                            "cluster": skill["cluster"],
                            "occurrences": len(matches),
                            "confidence": round(min(1.0, 0.70 + (0.10 * len(matches))), 2),
                            "context_snippet": f"...{snippet}..."
                        }
                    else:
                        extracted[skill_id]["occurrences"] += len(matches)
                        extracted[skill_id]["confidence"] = round(min(1.0, extracted[skill_id]["confidence"] + 0.05), 2)

        return sorted(list(extracted.values()), key=lambda x: x["occurrences"], reverse=True)

    def extract_from_project(self, title: str, description: str, tech_stack: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        combined_text = f"{title} {description} {' '.join(tech_stack or [])}"
        return self.extract_from_text(combined_text)

extractor = SkillExtractor()

if __name__ == "__main__":
    sample_resume = """
    Aarav Sharma - AI Engineer
    Experience building RAG pipelines with LangChain, LlamaIndex, and Vector Databases (Pinecone, ChromaDB).
    Fine-tuned Llama-3 models using PyTorch and Hugging Face transformers with LoRA/PEFT.
    Deployed production microservices using FastAPI, Docker, and Kubernetes on AWS.
    Implemented CI/CD pipelines with GitHub Actions. Proficient in Python, TypeScript, and React.
    """
    print("Testing Skill Extraction on Sample AI Resume:")
    extracted_skills = extractor.extract_from_text(sample_resume)
    for s in extracted_skills[:12]:
        print(f"  [{s['category']}] {s['name']} (Occurrences: {s['occurrences']}, Conf: {s['confidence']:.2f})")
