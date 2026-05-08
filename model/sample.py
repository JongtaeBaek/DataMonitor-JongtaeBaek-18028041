from dataclasses import dataclass


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: float  # 단위: 시간
    yield_rate: float           # 0.0 ~ 1.0
    stock: int = 0
