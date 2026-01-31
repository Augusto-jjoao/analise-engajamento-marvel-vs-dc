import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv
import movies  # Importa o arquivo que acabamos de criar

# Configurações
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    if not API_KEY:
        raise ValueError("ERRO: A chave da API não foi encontrada no arquivo .env")
    return build("youtube", "v3", developerKey=API_KEY)

def get_comments(youtube, video_id, max_results=100):
    """
    Coleta comentários de um vídeo específico.
    Retorna uma lista de dicionários com texto e likes.
    """
    comments_data = []
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            order="relevance" # Pega os mais relevantes primeiro
        )
        response = request.execute()

        while response and len(comments_data) < max_results:
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments_data.append({
                    "text": snippet["textDisplay"],
                    "likes": snippet["likeCount"],
                    "publishedAt": snippet["publishedAt"]
                })

            # Verifica se precisamos de mais páginas
            if "nextPageToken" in response and len(comments_data) < max_results:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    textFormat="plainText",
                    order="relevance",
                    pageToken=response["nextPageToken"]
                )
                response = request.execute()
            else:
                break
                
    except Exception as e:
        print(f"Erro ao processar vídeo {video_id}: {e}")

    return comments_data[:max_results]

def main():
    youtube = get_youtube_client()
    
    # Estrutura para salvar todos os dados
    dataset = {}

    print("--- INICIANDO COLETA DE DADOS ---")

    # Loop pelas franquias (Marvel, DC)
    for franchise, movies_dict in movies.movie_data.items():
        dataset[franchise] = {}
        print(f"\nProcessando franquia: {franchise}")
        
        for movie_name, video_id in movies_dict.items():
            print(f"  > Coletando: {movie_name}...")
            
            # quantos comentários pegar por filme
            # Para testes, use 20. Para o trabalho final, aumente para 100, 200, etc.
            comments = get_comments(youtube, video_id, max_results=20)
            
            dataset[franchise][movie_name] = {
                "video_id": video_id,
                "total_collected": len(comments),
                "comments": comments
            }

    # Salva tudo em um arquivo JSON final
    with open("dataset_marvel_vs_dc.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print("\n--- PROCESSO CONCLUÍDO! ---")
    print("Dados salvos em 'dataset_marvel_vs_dc.json'")

if __name__ == "__main__":
    main()