from model.sample import Sample
from model.order import Order, OrderStatus
from repository.sample_repository import SampleRepository
from repository.order_repository import OrderRepository


def test_sample_repo_load_missing_file(tmp_path):
    repo = SampleRepository(str(tmp_path / "samples.json"))
    assert repo.load() == []


def test_sample_repo_save_and_load(tmp_path):
    path = str(tmp_path / "sub" / "samples.json")
    repo = SampleRepository(path)
    samples = [
        Sample("S1", "Alpha", 2.0, 0.9, 5),
        Sample("S2", "Beta", 1.5, 0.8, 0),
    ]
    repo.save(samples)
    loaded = repo.load()
    assert len(loaded) == 2
    assert loaded[0].sample_id == "S1"
    assert loaded[0].stock == 5
    assert loaded[1].sample_id == "S2"
    assert loaded[1].stock == 0


def test_order_repo_load_missing_file(tmp_path):
    repo = OrderRepository(str(tmp_path / "orders.json"))
    assert repo.load() == []


def test_order_repo_save_and_load(tmp_path):
    path = str(tmp_path / "sub" / "orders.json")
    repo = OrderRepository(path)
    orders = [
        Order("O1", "S1", "Alice", 10, OrderStatus.RESERVED),
        Order("O2", "S1", "Bob", 5, OrderStatus.PRODUCING),
        Order("O3", "S2", "Charlie", 3, OrderStatus.CONFIRMED),
        Order("O4", "S2", "Dave", 2, OrderStatus.RELEASE),
        Order("O5", "S1", "Eve", 1, OrderStatus.REJECTED),
    ]
    repo.save(orders)
    loaded = repo.load()
    assert len(loaded) == 5
    assert loaded[0].status == OrderStatus.RESERVED
    assert loaded[1].status == OrderStatus.PRODUCING
    assert loaded[2].status == OrderStatus.CONFIRMED
    assert loaded[3].status == OrderStatus.RELEASE
    assert loaded[4].status == OrderStatus.REJECTED
