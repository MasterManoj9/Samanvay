"""
Canonical Skill Normalization Engine
Resolves free-text skill strings, aliases, and abbreviations into canonical skill entities.
"""

import json
import os
import re
from typing import Optional, Dict, Any, List

TAXONOMY_PATH = os.path.join(os.path.dirname(__file__), "..", "demo-data", "skills_taxonomy.json")

class SkillNormalizer:
    def __init__(self, taxonomy_file: Optional[str] = None):
        path = taxonomy_file or TAXONOMY_PATH
        with open(path, "r", encoding="utf-8") as f:
            self.taxonomy: List[Dict[str, Any]] = json.load(f)
        
        self.alias_to_skill: Dict[str, Dict[str, Any]] = {}
        self.id_to_skill: Dict[str, Dict[str, Any]] = {}
        self._build_index()

    def _clean_token(self, text: str) -> str:
        text = text.lower().strip()
        # Remove extra whitespace and special chars except +, #, -, .
        text = re.sub(r"[^\w\+\#\-\.\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _build_index(self):
        for skill in self.taxonomy:
            self.id_to_skill[skill["id"]] = skill
            
            # Map canonical name
            canonical_clean = self._clean_token(skill["name"])
            self.alias_to_skill[canonical_clean] = skill
            
            # Map all aliases
            for alias in skill.get("aliases", []):
                alias_clean = self._clean_token(alias)
                self.alias_to_skill[alias_clean] = skill

    def normalize(self, raw_skill: str) -> Optional[Dict[str, Any]]:
        """
        Normalize a raw skill string into a canonical skill object.
        Returns the canonical skill dict, or None if not recognized.
        """
        if not raw_skill or not isinstance(raw_skill, str):
            return None
        
        clean = self._clean_token(raw_skill)
        if clean in self.alias_to_skill:
            return self.alias_to_skill[clean]
        
        # Exact match attempts without punctuation
        simplified = re.sub(r"[\W_]+", "", clean)
        for alias, skill in self.alias_to_skill.items():
            if re.sub(r"[\W_]+", "", alias) == simplified:
                return skill

        return None

    def normalize_list(self, raw_skills: List[str]) -> List[Dict[str, Any]]:
        """Normalize a list of raw skills and remove duplicates."""
        seen_ids = set()
        normalized = []
        for raw in raw_skills:
            canonical = self.normalize(raw)
            if canonical and canonical["id"] not in seen_ids:
                seen_ids.add(canonical["id"])
                normalized.append(canonical)
        return normalized

    def get_skill_by_id(self, skill_id: str) -> Optional[Dict[str, Any]]:
        return self.id_to_skill.get(skill_id)

    def get_all_skills(self) -> List[Dict[str, Any]]:
        return self.taxonomy

# Singleton instance
normalizer = SkillNormalizer()

if __name__ == "__main__":
    test_cases = [
        "ReactJS", "react.js", "React",
        "ML", "machine-learning", "Machine Learning",
        "k8s", "Kubernetes",
        "py", "python 3", "Python",
        "Docker Engine", "docker",
        "lang-chain", "LangChain"
    ]
    print("Testing Skill Normalization:")
    for test in test_cases:
        res = normalizer.normalize(test)
        name = res["name"] if res else "UNKNOWN"
        print(f"  '{test}' -> '{name}'")
