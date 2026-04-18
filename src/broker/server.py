import grpc
from concurrent import futures
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc
from datetime import datetime

class GameServiceImpl(game_pb2_grpc.GameServiceServicer):
    def __init__(self):
        self.subscribers = []

    def PublishUpdate(self, request, context):
        print(f"[BROKER] Atualização recebida: {request.home_team} {request.home_score}x{request.away_score} {request.away_team}")

        game_update = game_pb2.GameUpdate(
            timestamp = datetime.now().isoformat(),
            home_team = request.home_team,
            away_team = request.away_team,
            home_score = request.home_score,
            away_score = request.away_score,
            match_time = request.match_time,
            yellow_cards = request.yellow_cards,
            red_cards = request.red_cards,
            corners = request.corners,
            shots_on_goal = request.shots_on_goal
        )

        for subscriber in self.subscribers:
            try:
                subscriber.write(game_update)
            except Exception as e:
                print(f"[BROKER] Erro ao enviar para subscriber: {e}")
                self.subscribers.remove(subscriber)

        return game_pb2.UpdateResponse(success=True, message="Atualização distribuída")

    def Subscribe(self, request, context):
        subscriber_id = request.subscriber_id
        print(f"[BROKER] Novo subscriber: {subscriber_id}")
        self.subscribers.append(context)
        print(f"[BROKER] Total subscribers: {len(self.subscribers)}")

        try:
            context.wait_for_termination()
        except:
            self.subscribers.remove(context)
            print(f"[BROKER] Subscriber desconectado: {subscriber_id}")

def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServiceServicer_to_server(
        GameServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print(f"[BROKER] Servidor iniciado na porta 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    run()