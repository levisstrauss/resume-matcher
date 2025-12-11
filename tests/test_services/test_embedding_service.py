import pytest
from unittest.mock import patch, MagicMock


def test_calculate_similarity():
    from src.resume_matcher.services.embedding_service import calculate_similarity

    # Identical vectors should have similarity 1.0
    vec = [1.0, 0.0, 0.0]
    assert calculate_similarity(vec, vec) == pytest.approx(1.0)

    # Orthogonal vectors should have similarity 0.0
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 0.0]
    assert calculate_similarity(vec1, vec2) == pytest.approx(0.0)


def test_calculate_similarity_with_zero_vector():
    from src.resume_matcher.services.embedding_service import calculate_similarity

    vec1 = [1.0, 2.0, 3.0]
    vec2 = [0.0, 0.0, 0.0]

    result = calculate_similarity(vec1, vec2)
    assert result == 0.0