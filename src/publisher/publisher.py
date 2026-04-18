import grpc
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = game_pb2_grpc.GameServiceStub(channel)

    print("=== Publicador de Placares ===")
    while True:
        print("\n Digite os dados do jogo:")
        home_team = input("Time da casa: ")
        away_team = input("Time visitante: ")
        home_score = int(input("Gols time casa: "))
        away_score = int(input("Gols time visitante: "))
        match_time = input("Tempo de jogo (ex:45')")
        yellow_cards = int(input("Cartões amarelos: "))
        red_cards = int(input("Cartões vermelhos: "))
        corners = int(input("Escanteios: "))
        shots_on_goal = int(input("Finalizações no gol: "))

        request = game_pb2.UpdateRequest(
            home_team = home_team,
            away_team = away_team,
            home_score = home_score,
            away_score = away_score,
            match_time = match_time,
            yellow_cards = yellow_cards,
            red_cards = red_cards,
            corners = corners,
            shots_on_goal = shots_on_goal
        )

        response = stub.PublishUpdate(request)
        print(f"Resposta do Broker: {response.message}")

        continuar = input("Publicar outra atualização? (s/n): ")
        if continuar.lower() != 's':
            break

if __name__ == '__main__':
    run()