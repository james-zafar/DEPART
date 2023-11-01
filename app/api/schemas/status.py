from enum import Enum


class Status(Enum):
    COMPLETED = 'completed'
    FAILED = 'failed'
    PENDING = 'pending'
    RUNNING = 'running'
