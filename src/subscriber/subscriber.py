import grpc
import uuid
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = game_pb2_grpc.GameServiceStub(channel)

    subscriber_id = str(uuid.uuid4())[:8]
    filter_team = input("Time para filtrar (deixe vazio para todos): ").strip()

    print(f"[SUBSCRIBER {subscriber_id}] Conectando ao Broker...")

    request = game_pb2.SubscribeRequest(
        subscriber_id=subscriber_id, filter_team=filter_team if filter_team else None
    )

    try:
        for update in stub.Subscribe(request):
            print(f"\n[SUBSCRIBER {subscriber_id}] NOVA ATUALIZAÇÃO")
            print(f"  Timestamp: {update.timestamp}")
            print(
                f"  {update.home_team} {update.home_score}x{update.away_score} {update.away_team}"
            )
            print(f"  Tempo: {update.match_time}")
            print("")
            print("  Cartões amarelos")
            print(f"  {update.home_yellow_cards} x {update.away_yellow_cards}")
            print("  Cartões vermelhos")
            print(f"  {update.home_red_cards} x {update.away_red_cards}")
            print("  Escanteios")
            print(f"  {update.home_corners} x {update.away_corners}")
            print("  Finalizações no gol")
            print(f"  {update.home_shots_on_goal} x {update.away_shots_on_goal}")
            print("  Finalizações para fora")
            print(f"  {update.home_shots_off_goal} x {update.away_shots_off_goal}")
    except grpc.RpcError as e:
        print(f"[SUBSCRIBER {subscriber_id}] Erro: {e.details()}")


if __name__ == "__main__":
    run()
