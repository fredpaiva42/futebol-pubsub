import grpc
import proto.game_pb2 as game_pb2
import proto.game_pb2_grpc as game_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = game_pb2_grpc.GameServiceStub(channel)
    
    print("=== Publicador de Placares ===")
    while True:
        print("\nDigite os dados do jogo:")
        home_team = input("Time da casa: ")
        away_team = input("Time visitante: ")
        home_score = int(input("Gols time casa: "))
        away_score = int(input("Gols time visitante: "))
        match_time = input("Tempo de jogo (ex: 45' + 2): ")
        home_yellow_cards = int(input("Cartões amarelos (casa): "))
        away_yellow_cards = int(input("Cartões amarelos (visitante): "))
        home_red_cards = int(input("Cartões vermelhos (casa): "))
        away_red_cards = int(input("Cartões vermelhos (visitante): "))
        home_corners = int(input("Escanteios (casa): "))
        away_corners = int(input("Escanteios (visitante): "))
        home_shots_on_goal = int(input("Finalizações no gol (casa): "))
        away_shots_on_goal = int(input("Finalizações no gol (visitante): "))
        home_shots_off_goal = int(input("Finalizações para fora (casa): "))
        away_shots_off_goal = int(input("Finalizações para fora (visitante): "))
        
        request = game_pb2.UpdateRequest(
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            match_time=match_time,
            home_yellow_cards=home_yellow_cards,
            away_yellow_cards=away_yellow_cards,
            home_red_cards=home_red_cards,
            away_red_cards=away_red_cards,
            home_corners=home_corners,
            away_corners=away_corners,
            home_shots_on_goal=home_shots_on_goal,
            away_shots_on_goal=away_shots_on_goal,
            home_shots_off_goal=home_shots_off_goal,
            away_shots_off_goal=away_shots_off_goal,
        )
        
        response = stub.PublishUpdate(request)
        print(f"Resposta do Broker: {response.message}")
        
        continuar = input("Publicar outra atualização? (s/n): ")
        if continuar.lower() != 's':
            break

if __name__ == '__main__':
    run()