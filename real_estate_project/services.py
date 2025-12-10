import time
import concurrent.futures
from django.db import connections
from realty.models import Contract

class BenchmarkService:
    def __init__(self, query_count=100):
        self.query_count = query_count

    def _single_db_query(self):
        try:
            count = Contract.objects.filter(payment_amount__gt=5000).count()
            return count
        except OperationalError:
            connections.close_all()
            return 0

    def run_sync(self):
        start_time = time.time()
        for _ in range(self.query_count):
            self._single_db_query()
        return time.time() - start_time

    def run_multithreaded(self, max_workers=4):
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._single_db_query) for _ in range(self.query_count)]
            concurrent.futures.wait(futures)
        return time.time() - start_time

    def run_benchmark_experiment(self):
        worker_options = [1, 2, 4, 8, 16, 32, 64]
        results = []

        for workers in worker_options:
            connections.close_all()

            duration = self.run_multithreaded(workers)
            rps = self.query_count / duration

            results.append({
                'workers': workers,
                'duration': round(duration, 4),
                'rps': round(rps, 2),
            })

        return results
