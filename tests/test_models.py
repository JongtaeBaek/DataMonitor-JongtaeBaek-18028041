from model.sample import Sample
from model.order import Order, OrderStatus
from model.production import ProductionJob, ProductionQueue


def test_sample_default_stock():
    s = Sample("S1", "Alpha", 2.0, 0.9)
    assert s.sample_id == "S1"
    assert s.name == "Alpha"
    assert s.avg_production_time == 2.0
    assert s.yield_rate == 0.9
    assert s.stock == 0


def test_sample_with_stock():
    s = Sample("S2", "Beta", 1.5, 0.8, 10)
    assert s.stock == 10


def test_order_default_status():
    o = Order("O1", "S1", "Customer", 5)
    assert o.status == OrderStatus.RESERVED


def test_order_status_values():
    assert OrderStatus.RESERVED.value == "RESERVED"
    assert OrderStatus.REJECTED.value == "REJECTED"
    assert OrderStatus.PRODUCING.value == "PRODUCING"
    assert OrderStatus.CONFIRMED.value == "CONFIRMED"
    assert OrderStatus.RELEASE.value == "RELEASE"


def test_production_job_fields():
    job = ProductionJob("O1", "S1", 5, 6, 12.0)
    assert job.order_id == "O1"
    assert job.sample_id == "S1"
    assert job.required_quantity == 5
    assert job.actual_production == 6
    assert job.total_time == 12.0


def test_production_queue_empty():
    q = ProductionQueue()
    assert q.is_empty()
    assert q.peek() is None
    assert q.dequeue() is None
    assert q.all() == []


def test_production_queue_enqueue_dequeue():
    q = ProductionQueue()
    job1 = ProductionJob("O1", "S1", 5, 6, 12.0)
    job2 = ProductionJob("O2", "S2", 3, 4, 8.0)
    q.enqueue(job1)
    q.enqueue(job2)
    assert not q.is_empty()
    assert q.peek() == job1
    assert q.all() == [job1, job2]
    assert q.dequeue() == job1
    assert q.dequeue() == job2
    assert q.is_empty()
