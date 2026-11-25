"""
Mathematical Set-Based Similarity Metrics for Text Analysis.

Provides:
- Jaccard Similarity Coefficient: |A ∩ B| / |A ∪ B|
- Containment Index: |A ∩ B| / |B| (proportion of suspect document found in reference)
- Overlap (Simpson) Coefficient: |A ∩ B| / min(|A|, |B|)
"""

from typing import Set, Any, Dict


def jaccard_similarity(set_a: Set[Any], set_b: Set[Any]) -> float:
    """
    Computes Jaccard Similarity coefficient between two sets.
    Formula: |A ∩ B| / |A ∪ B|

    Returns:
        float: Similarity percentage from 0.0 to 100.0 rounded to 2 decimal places.
    """
    if not set_a and not set_b:
        return 100.0  # Two empty sets are identical
    if not set_a or not set_b:
        return 0.0

    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))

    if union == 0:
        return 0.0

    return round((intersection / union) * 100.0, 2)


def containment_index(reference_set: Set[Any], suspect_set: Set[Any]) -> float:
    """
    Computes Containment index of suspect_set inside reference_set.
    Formula: |Reference ∩ Suspect| / |Suspect|

    Measures what fraction of the suspect document is borrowed from reference.
    """
    if not suspect_set:
        return 0.0

    intersection = len(reference_set.intersection(suspect_set))
    return round((intersection / len(suspect_set)) * 100.0, 2)


def compute_all_metrics(doc1_shingles: Set[str], doc2_shingles: Set[str]) -> Dict[str, float]:
    """Computes Jaccard, Containment, and Overlap coefficients simultaneously."""
    if not doc1_shingles and not doc2_shingles:
        return {"jaccard": 100.0, "containment": 100.0, "overlap": 100.0}

    intersection = len(doc1_shingles.intersection(doc2_shingles))
    union = len(doc1_shingles.union(doc2_shingles))
    min_size = min(len(doc1_shingles), len(doc2_shingles)) if doc1_shingles and doc2_shingles else 0

    jaccard = round((intersection / union * 100.0), 2) if union > 0 else 0.0
    containment = round((intersection / len(doc2_shingles) * 100.0), 2) if len(doc2_shingles) > 0 else 0.0
    overlap = round((intersection / min_size * 100.0), 2) if min_size > 0 else 0.0

    return {
        "jaccard": jaccard,
        "containment": containment,
        "overlap": overlap
    }
