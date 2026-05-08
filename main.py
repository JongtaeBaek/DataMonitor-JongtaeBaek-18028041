from repository.sample_repository import SampleRepository
from repository.order_repository import OrderRepository
from monitor.data_monitor import DataMonitor


def main():
    sample_repo = SampleRepository()
    order_repo = OrderRepository()
    monitor = DataMonitor(sample_repo, order_repo)

    while True:
        print("\n=== 데이터 모니터 ===")
        print("1. 시료 현황")
        print("2. 주문 현황")
        print("3. 재고 현황")
        print("4. 전체 조회")
        print("0. 종료")
        choice = input("선택: ").strip()
        if choice == "1":
            monitor.show_samples()
        elif choice == "2":
            monitor.show_orders()
        elif choice == "3":
            monitor.show_stock()
        elif choice == "4":
            monitor.show_all()
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
