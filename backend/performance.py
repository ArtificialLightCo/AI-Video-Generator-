# backend/performance.py
import psutil
import torch

class PerformanceMonitor:
    """
    Hardware profiling and live metrics for CPU, GPU, and RAM.
    """
    def stats(self) -> dict:
        return {
            'cpu': psutil.cpu_percent(interval=None),
            'memory': psutil.virtual_memory()._asdict(),
            'gpu_available': torch.cuda.is_available(),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        }
