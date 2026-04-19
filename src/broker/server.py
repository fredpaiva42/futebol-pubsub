import grpc
from concurrent import futures
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc
from datetime import datetime
import threading
import queue


class GameServiceImpl(game_pb2_grpc.GameServiceServicer):
    def __init__(self):
        self.subscribers = {}
        self.lock = threading.Lock()

    def PublishUpdate(self, request, context):
        print(
            f"[BROKER] Atualização recebida: {request.home_team} {request.home_score}x{request.away_score} {request.away_team}"
        )

        game_update = game_pb2.GameUpdate(
            timestamp=datetime.now().isoformat(),
            home_team=request.home_team,
            away_team=request.away_team,
            home_score=request.home_score,
            away_score=request.away_score,
            match_time=request.match_time,
            home_yellow_cards=request.home_yellow_cards,
            away_yellow_cards=request.away_yellow_cards,
            home_red_cards=request.home_red_cards,
            away_red_cards=request.away_red_cards,
            home_corners=request.home_corners,
            away_corners=request.away_corners,
            home_shots_on_goal=request.home_shots_on_goal,
            away_shots_on_goal=request.away_shots_on_goal,
            home_shots_off_goal=request.home_shots_off_goal,
            away_shots_off_goal=request.away_shots_off_goal,
        )

        with self.lock:
            for subscriber_id, q in self.subscribers.items():
                try:
                    q.put(game_update)
                except Exception as e:
                    print(f"[BROKER] Erro ao enviar para subscriber: {e}")

        return game_pb2.UpdateResponse(success=True, message="Atualização distribuída")

    def Subscribe(self, request, context):
        subscriber_id = request.subscriber_id
        q = queue.Queue()
        
        with self.lock:
            self.subscribers[subscriber_id] = q
        
        print(f"[BROKER] Novo subscriber: {subscriber_id}")
        print(f"[BROKER] Total subscribers: {len(self.subscribers)}")

        try:
            while True:
                try:
                    update = q.get(timeout=1)
                    yield update
                except queue.Empty:
                    pass
        except Exception as e:
            print(f"[BROKER] Erro no subscriber: {e}")
        finally:
            with self.lock:
                if subscriber_id in self.subscribers:
                    del self.subscribers[subscriber_id]
            print(f"[BROKER] Subscriber desconectado: {subscriber_id}")


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServiceServicer_to_server(GameServiceImpl(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[BROKER] Servidor iniciado na porta 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    run()
