import grpc
import uuid
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = game_pb2_grpc.GameServiceStub(channel)

    subscriber_id = str(uuid.uuid4())[:8]
    print(f"[SUBSCRIBER {subscriber_id}] Subscribing to game updates...")

    request = game_pb2.SubscribeRequest(subscriber_id=subscriber_id)

    try:
        for update in stub.Subscribe(request):
            print(f"[SUBSCRIBER {subscriber_id}] Nova atualização")
            print(f" Timestamp: {update.timestamp}")
            print(
                f" {update.home_team} {update.home_score}x{update.away_score} {update.away_team}"
            )
            print(f" Tempo: {update.match_time}")
            print(
                f" Cartões: {update.yellow_cards} amarelos, {update.red_cards} vermelhos"
            )
            print(f" Escanteios: {update.corners}")
            print(f" Finalizações: {update.shots_on_goal} no alvo")

    except grpc.RpcError as e:
        print(f"[SUBSCRIBER {subscriber_id}] Erro: {e.details()}")


if __name__ == "__main__":
    run()
