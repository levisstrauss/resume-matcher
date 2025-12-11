import logging
from typing import List, Optional
import openai

from ..core.config import settings

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingError(Exception):
    """Raised when embedding generation fails."""
    pass


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text.

    Args:
        text: Text to embed

    Returns:
        List of floats representing the embedding vector

    Raises:
        EmbeddingError: If embedding generation fails
    """
    try:
        # Truncate text if too long (OpenAI has ~8k token limit)
        # Roughly 4 chars per token, so ~32k chars max
        max_chars = 30000
        if len(text) > max_chars:
            logger.warning(f"Text truncated from {len(text)} to {max_chars} chars")
            text = text[:max_chars]

        response = client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )

        embedding = response.data[0].embedding
        logger.info(f"Generated embedding with {len(embedding)} dimensions")

        return embedding

    except openai.APIError as e:
        raise EmbeddingError(f"OpenAI API error: {e}")
    except Exception as e:
        raise EmbeddingError(f"Failed to generate embedding: {e}")


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in one API call.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors

    Raises:
        EmbeddingError: If embedding generation fails
    """
    try:
        # Truncate each text
        max_chars = 30000
        processed_texts = []
        for text in texts:
            if len(text) > max_chars:
                text = text[:max_chars]
            processed_texts.append(text)

        response = client.embeddings.create(
            model=settings.embedding_model,
            input=processed_texts,
        )

        # Sort by index to maintain order
        sorted_data = sorted(response.data, key=lambda x: x.index)
        embeddings = [item.embedding for item in sorted_data]

        logger.info(f"Generated {len(embeddings)} embeddings in batch")

        return embeddings

    except openai.APIError as e:
        raise EmbeddingError(f"OpenAI API error: {e}")
    except Exception as e:
        raise EmbeddingError(f"Failed to generate embeddings: {e}")


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Similarity score between 0 and 1
    """
    import math

    # Dot product
    dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

    # Magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in embedding1))
    magnitude2 = math.sqrt(sum(b * b for b in embedding2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    similarity = dot_product / (magnitude1 * magnitude2)

    # Clamp to [0, 1] (cosine similarity for normalized vectors)
    return max(0.0, min(1.0, similarity))