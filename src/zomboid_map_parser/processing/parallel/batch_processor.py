# processing/parallel/batch_processor.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import TypeVar, Generic, List, Callable, Iterator, Optional
import logging

T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type


@dataclass
class BatchProcessingConfig:
    """Configuration settings for batch processing operations."""
    max_workers: int
    batch_size: int
    retry_count: int = 3
    log_progress: bool = True


class BatchProcessor(Generic[T, R]):
    """
    Handles parallel processing of items in batches.

    This processor is designed to efficiently handle large datasets by processing
    them in manageable batches using parallel execution. It provides built-in
    error handling, progress tracking, and memory management features.
    """

    def __init__(self, config: BatchProcessingConfig):
        """Initialize the batch processor with the provided configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.processed_count = 0
        self.failed_count = 0
        self.current_batch = 0

    def process_items(
            self,
            items: List[T],
            process_func: Callable[[T], R],
            filter_func: Optional[Callable[[R], bool]] = None
    ) -> Iterator[List[R]]:
        """
        Process a list of items in parallel batches.

        Args:
            items: List of items to process
            process_func: Function to apply to each item
            filter_func: Optional function to filter results

        Yields:
            Lists of processed results, one batch at a time
        """
        total_items = len(items)
        self.processed_count = 0
        self.failed_count = 0
        self.current_batch = 0

        for batch_start in range(0, total_items, self.config.batch_size):
            self.current_batch += 1
            batch = items[batch_start:batch_start + self.config.batch_size]

            results = self._process_batch(batch, process_func, filter_func)
            if results:
                yield results

            if self.config.log_progress:
                self._log_progress(total_items)

    def _process_batch(
            self,
            batch: List[T],
            process_func: Callable[[T], R],
            filter_func: Optional[Callable[[R], bool]]
    ) -> List[R]:
        """Process a single batch of items in parallel."""
        results = []
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {
                executor.submit(self._process_with_retry, process_func, item): item
                for item in batch
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result is not None and (
                            filter_func is None or filter_func(result)
                    ):
                        results.append(result)
                    self.processed_count += 1
                except Exception as e:
                    self.failed_count += 1
                    self.logger.error(
                        f"Failed to process item: {futures[future]} - {str(e)}"
                    )

        return results

    def _process_with_retry(
            self,
            process_func: Callable[[T], R],
            item: T
    ) -> Optional[R]:
        """Process an item with retry logic."""
        for attempt in range(self.config.retry_count):
            try:
                return process_func(item)
            except Exception as e:
                if attempt == self.config.retry_count - 1:
                    raise
                self.logger.warning(
                    f"Retry {attempt + 1} for item {item}: {str(e)}"
                )
        return None

    def _log_progress(self, total_items: int) -> None:
        """Log the current processing progress."""
        progress = (self.processed_count / total_items) * 100
        self.logger.info(
            f"Processed {self.processed_count}/{total_items} items "
            f"({progress:.1f}%) - Batch {self.current_batch}"
        )

    def get_statistics(self) -> dict:
        """Get current processing statistics."""
        return {
            'processed_items': self.processed_count,
            'failed_items': self.failed_count,
            'total_batches': self.current_batch
        }