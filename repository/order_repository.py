import json
from dataclasses import asdict
from pathlib import Path

from model.order import Order, OrderStatus


class OrderRepository:
    def __init__(self, filepath: str = "data/orders.json"):
        self._path = Path(filepath)

    def load(self) -> list[Order]:
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            Order(
                order_id=item["order_id"],
                sample_id=item["sample_id"],
                customer_name=item["customer_name"],
                quantity=item["quantity"],
                status=OrderStatus(item["status"]),
            )
            for item in data
        ]

    def save(self, orders: list[Order]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        serialized = []
        for o in orders:
            d = asdict(o)
            d["status"] = o.status.value
            serialized.append(d)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(serialized, f, ensure_ascii=False, indent=2)
