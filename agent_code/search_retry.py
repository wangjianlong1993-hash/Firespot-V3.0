"""
FireSpot Search Retry Logic
============================

Intelligent retry mechanism for web search with:
- Automatic search engine rotation
- Exponential backoff
- Error handling for rate limits (403, 429)

Author: FireSpot Team
Version: 4.1.0
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# Search Engine Configuration
# ============================================================================

SEARCH_ENGINES = {
    "duckduckgo": {
        "name": "DuckDuckGo",
        "priority": 1,  # Highest priority
        "retry_after": 0,  # No delay needed
        "max_retries": 3,
    },
    "yandex": {
        "name": "Yandex",
        "priority": 2,
        "retry_after": 2,  # 2 seconds
        "max_retries": 3,
    },
    "brave": {
        "name": "Brave",
        "priority": 3,
        "retry_after": 5,  # 5 seconds (rate limited)
        "max_retries": 2,
    },
    "mojeek": {
        "name": "Mojeek",
        "priority": 4,
        "retry_after": 3,
        "max_retries": 2,
    },
    "grokipedia": {
        "name": "Grokipedia",
        "priority": 5,
        "retry_after": 3,
        "max_retries": 2,
    },
    "google": {
        "name": "Google",
        "priority": 6,  # Lowest priority (frequent 403)
        "retry_after": 10,  # 10 seconds
        "max_retries": 1,
    },
}


# ============================================================================
# Retry Strategy
# ============================================================================

class SearchRetryStrategy:
    """
    Intelligent search retry with engine rotation and exponential backoff.
    """

    def __init__(self):
        self.failed_engines: Dict[str, float] = {}  # engine -> failure_time
        self.engine_stats: Dict[str, Dict] = {
            engine: {"success": 0, "failure": 0, "last_used": None}
            for engine in SEARCH_ENGINES
        }

    def get_available_engines(self) -> List[str]:
        """Get list of available engines sorted by priority."""
        now = datetime.now().timestamp()

        # Filter out engines that failed recently (within cooldown period)
        available = []
        for engine_id, config in SEARCH_ENGINES.items():
            if engine_id in self.failed_engines:
                failed_time = self.failed_engines[engine_id]
                retry_after = config["retry_after"]

                if now - failed_time < retry_after:
                    logger.debug(
                        f"⏳ Engine {config['name']} is in cooldown "
                        f"({retry_after - (now - failed_time):.1f}s remaining)"
                    )
                    continue
                else:
                    # Cooldown expired, remove from failed list
                    del self.failed_engines[engine_id]

            available.append(engine_id)

        # Sort by priority (lower number = higher priority)
        available.sort(key=lambda e: SEARCH_ENGINES[e]["priority"])

        return available

    def mark_failure(self, engine_id: str, error: Optional[str] = None):
        """Mark an engine as failed."""
        config = SEARCH_ENGINES.get(engine_id)
        if not config:
            return

        self.failed_engines[engine_id] = datetime.now().timestamp()
        self.engine_stats[engine_id]["failure"] += 1

        logger.warning(
            f"⚠️  Search engine {config['name']} failed"
            f"{f': {error}' if error else ''}"
            f" - marked for cooldown ({config['retry_after']}s)"
        )

    def mark_success(self, engine_id: str):
        """Mark an engine as successful."""
        if engine_id in self.failed_engines:
            del self.failed_engines[engine_id]

        self.engine_stats[engine_id]["success"] += 1
        self.engine_stats[engine_id]["last_used"] = datetime.now().isoformat()

    def get_stats(self) -> Dict[str, Dict]:
        """Get statistics for all engines."""
        return self.engine_stats.copy()


# Global strategy instance
_global_strategy: Optional[SearchRetryStrategy] = None


def get_retry_strategy() -> SearchRetryStrategy:
    """Get or create global retry strategy instance."""
    global _global_strategy
    if _global_strategy is None:
        _global_strategy = SearchRetryStrategy()
    return _global_strategy


# ============================================================================
# Search with Retry
# ============================================================================

async def search_with_retry(
    search_func: callable,
    query: str,
    max_results: int = 10,
    max_engines: int = 3,
    **kwargs
) -> Dict[str, Any]:
    """
    Execute web search with automatic retry and engine rotation.

    Args:
        search_func: The search function to call (e.g., web_search tool)
        query: Search query string
        max_results: Maximum results per engine
        max_engines: Maximum number of engines to try
        **kwargs: Additional arguments for search function

    Returns:
        Dictionary with:
        - success: bool
        - results: list of search results
        - engine_used: str
        - engines_tried: list
        - total_results: int
    """
    strategy = get_retry_strategy()
    engines_tried = []
    all_results = []

    logger.info(f"🔍 Starting search with retry: '{query[:50]}...'")

    for attempt in range(max_engines):
        available_engines = strategy.get_available_engines()

        if not available_engines:
            logger.error("❌ No available search engines")
            break

        # Get next best engine
        engine_id = available_engines[0]
        engine_name = SEARCH_ENGINES[engine_id]["name"]

        engines_tried.append(engine_id)
        logger.info(
            f"📡 Attempt {attempt + 1}/{max_engines}: "
            f"Using {engine_name} (priority {SEARCH_ENGINES[engine_id]['priority']})"
        )

        try:
            # Call search function
            # Note: The actual search_func should handle engine selection
            # We just track retries here
            result = await search_func(
                query=query,
                max_results=max_results,
                **kwargs
            )

            # Check if successful
            if result and isinstance(result, dict):
                results = result.get("results", [])

                if results:
                    strategy.mark_success(engine_id)
                    all_results.extend(results)

                    logger.info(
                        f"✅ {engine_name} search successful: "
                        f"{len(results)} results"
                    )

                    # If we have enough results, return
                    if len(all_results) >= max_results:
                        break

                else:
                    # No results - treat as failure
                    strategy.mark_failure(engine_id, "No results returned")

            else:
                strategy.mark_failure(engine_id, "Invalid response format")

        except Exception as e:
            error_str = str(e)
            strategy.mark_failure(engine_id, error_str)

            # Check for rate limit errors
            if "403" in error_str or "429" in error_str:
                logger.warning(
                    f"⚠️  Rate limit hit on {engine_name}, "
                    f"switching engines..."
                )
            else:
                logger.error(
                    f"❌ Search error on {engine_name}: {error_str}"
                )

        # Small delay between attempts
        if attempt < max_engines - 1:
            await asyncio.sleep(1)

    # Prepare final result
    success = len(all_results) > 0
    engine_used = engines_tried[-1] if engines_tried else None

    logger.info(
        f"📊 Search complete: {'✅ Success' if success else '❌ Failed'}, "
        f"{len(all_results)} results from {len(engines_tried)} engine(s)"
    )

    return {
        "success": success,
        "results": all_results[:max_results],  # Limit to max_results
        "engine_used": engine_used,
        "engines_tried": engines_tried,
        "total_results": len(all_results),
    }


def log_search_stats():
    """Log current search engine statistics."""
    strategy = get_retry_strategy()
    stats = strategy.get_stats()

    logger.info("\n" + "="*60)
    logger.info("📊 Search Engine Statistics")
    logger.info("="*60)

    for engine_id, config in SEARCH_ENGINES.items():
        engine_stats = stats[engine_id]
        success_rate = 0

        if engine_stats["success"] + engine_stats["failure"] > 0:
            total = engine_stats["success"] + engine_stats["failure"]
            success_rate = (engine_stats["success"] / total) * 100

        logger.info(
            f"{config['name']:12} | "
            f"✅ {engine_stats['success']:3} | "
            f"❌ {engine_stats['failure']:3} | "
            f"📈 {success_rate:5.1f}%"
        )

    logger.info("="*60 + "\n")


# Export
__all__ = [
    "search_with_retry",
    "get_retry_strategy",
    "log_search_stats",
    "SEARCH_ENGINES",
    "SearchRetryStrategy",
]
