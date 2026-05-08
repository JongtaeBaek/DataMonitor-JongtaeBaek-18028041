from model.order import OrderStatus
from repository.sample_repository import SampleRepository
from repository.order_repository import OrderRepository


class DataMonitor:
    def __init__(self, sample_repo: SampleRepository, order_repo: OrderRepository):
        self._sample_repo = sample_repo
        self._order_repo = order_repo

    def show_samples(self) -> None:
        samples = self._sample_repo.load()
        print("=== 시료 현황 ===")
        if not samples:
            print("등록된 시료가 없습니다.")
            return
        print(f"{'ID':<12} {'이름':<20} {'평균생산시간(h)':>14} {'수율':>8} {'재고':>6}")
        print("-" * 65)
        for s in samples:
            print(f"{s.sample_id:<12} {s.name:<20} {s.avg_production_time:>14.1f} {s.yield_rate:>8.1%} {s.stock:>6}")

    def show_orders(self) -> None:
        orders = self._order_repo.load()
        print("=== 주문 현황 ===")
        counts = {
            OrderStatus.RESERVED:  0,
            OrderStatus.PRODUCING: 0,
            OrderStatus.CONFIRMED: 0,
            OrderStatus.RELEASE:   0,
        }
        for o in orders:
            if o.status in counts:
                counts[o.status] += 1
        for status, count in counts.items():
            print(f"  {status.value:<12}: {count}건")

    def show_stock(self) -> None:
        samples = self._sample_repo.load()
        orders = self._order_repo.load()
        print("=== 재고 현황 ===")
        if not samples:
            print("등록된 시료가 없습니다.")
            return
        active = {OrderStatus.RESERVED, OrderStatus.PRODUCING}
        demand: dict[str, int] = {}
        for o in orders:
            if o.status in active:
                demand[o.sample_id] = demand.get(o.sample_id, 0) + o.quantity
        print(f"{'ID':<12} {'이름':<20} {'재고':>6}  상태")
        print("-" * 44)
        for s in samples:
            if s.stock == 0:
                state = "고갈"
            elif s.stock < demand.get(s.sample_id, 0):
                state = "부족"
            else:
                state = "여유"
            print(f"{s.sample_id:<12} {s.name:<20} {s.stock:>6}  {state}")

    def show_all(self) -> None:
        self.show_samples()
        print()
        self.show_orders()
        print()
        self.show_stock()
