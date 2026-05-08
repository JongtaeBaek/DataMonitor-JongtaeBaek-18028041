from unittest.mock import MagicMock
from model.sample import Sample
from model.order import Order, OrderStatus
from monitor.data_monitor import DataMonitor


def _make_monitor(samples=None, orders=None):
    sample_repo = MagicMock()
    order_repo = MagicMock()
    sample_repo.load.return_value = samples if samples is not None else []
    order_repo.load.return_value = orders if orders is not None else []
    return DataMonitor(sample_repo, order_repo)


def test_show_samples_empty(capsys):
    monitor = _make_monitor()
    monitor.show_samples()
    out = capsys.readouterr().out
    assert "등록된 시료가 없습니다." in out


def test_show_samples_with_data(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 5)]
    monitor = _make_monitor(samples=samples)
    monitor.show_samples()
    out = capsys.readouterr().out
    assert "S1" in out
    assert "Alpha" in out
    assert "5" in out


def test_show_orders_empty(capsys):
    monitor = _make_monitor()
    monitor.show_orders()
    out = capsys.readouterr().out
    assert "0건" in out


def test_show_orders_counts(capsys):
    orders = [
        Order("O1", "S1", "Alice", 10, OrderStatus.RESERVED),
        Order("O2", "S1", "Bob", 5, OrderStatus.PRODUCING),
        Order("O3", "S2", "Charlie", 3, OrderStatus.CONFIRMED),
        Order("O4", "S2", "Dave", 2, OrderStatus.RELEASE),
        Order("O5", "S1", "Eve", 1, OrderStatus.REJECTED),  # 집계 제외
    ]
    monitor = _make_monitor(orders=orders)
    monitor.show_orders()
    out = capsys.readouterr().out
    assert "RESERVED" in out
    assert "PRODUCING" in out
    assert "CONFIRMED" in out
    assert "RELEASE" in out


def test_show_stock_empty_samples(capsys):
    monitor = _make_monitor()
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "등록된 시료가 없습니다." in out


def test_show_stock_gokal(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 0)]
    monitor = _make_monitor(samples=samples)
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "고갈" in out


def test_show_stock_bugjok(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 3)]
    orders = [Order("O1", "S1", "Alice", 10, OrderStatus.RESERVED)]
    monitor = _make_monitor(samples=samples, orders=orders)
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "부족" in out


def test_show_stock_yooyoo(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 10)]
    orders = [Order("O1", "S1", "Alice", 5, OrderStatus.RESERVED)]
    monitor = _make_monitor(samples=samples, orders=orders)
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "여유" in out


def test_show_stock_no_active_orders(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 10)]
    orders = [Order("O1", "S1", "Alice", 5, OrderStatus.CONFIRMED)]
    monitor = _make_monitor(samples=samples, orders=orders)
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "여유" in out


def test_show_stock_producing_demand(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 2)]
    orders = [Order("O1", "S1", "Alice", 3, OrderStatus.PRODUCING)]
    monitor = _make_monitor(samples=samples, orders=orders)
    monitor.show_stock()
    out = capsys.readouterr().out
    assert "부족" in out


def test_show_all(capsys):
    samples = [Sample("S1", "Alpha", 2.0, 0.9, 5)]
    orders = [Order("O1", "S1", "Alice", 3, OrderStatus.RESERVED)]
    monitor = _make_monitor(samples=samples, orders=orders)
    monitor.show_all()
    out = capsys.readouterr().out
    assert "시료 현황" in out
    assert "주문 현황" in out
    assert "재고 현황" in out
