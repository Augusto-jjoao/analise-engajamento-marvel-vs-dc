import os
import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import movies  # Seu arquivo de IDs

# Carrega ambiente
load_dotenv()

# --- GESTÃO DE CHAVES API (MANTIDO IGUAL) ---
keys_string = os.getenv("YOUTUBE_API_KEYS")
# Garante que funciona mesmo se tiver só uma chave ou várias
if keys_string:
    API_KEYS = [k.strip() for k in keys_string.split(",") if k.strip()]
else:
    # Fallback caso o usuário tenha mantido a variável antiga no .env
    API_KEYS = [os.getenv("YOUTUBE_API_KEY")]

CURRENT_KEY_INDEX = 0

if not API_KEYS or not API_KEYS[0]:
    raise ValueError("Nenhuma chave encontrada no .env!")

def get_youtube_client():
    global CURRENT_KEY_INDEX
    return build("youtube", "v3", developerKey=API_KEYS[CURRENT_KEY_INDEX])

def rotate_key():
    global CURRENT_KEY_INDEX
    CURRENT_KEY_INDEX += 1
    if CURRENT_KEY_INDEX >= len(API_KEYS):
<<<<<<< HEAD
        print("Todas as chaves API foram esgotadas,")
=======
        print("!!! CRÍTICO: Todas as chaves API foram esgotadas !!!")
>>>>>>> 4159c885078ad451710417403037900a182a7431
        return False
    print(f"Trocando para a chave API numero: {CURRENT_KEY_INDEX + 1}")
    return True

# --- FUNÇÃO DE COLETA (MANTIDA IGUAL) ---
def get_comments_safe(video_id, max_results=100000):
    comments_data = []
    youtube = get_youtube_client()
    next_page_token = None
    
    while len(comments_data) < max_results:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                order="time", #"relevance"
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments_data.append({
                    "text": snippet["textDisplay"],
                    "likes": snippet["likeCount"],
                    "date": snippet["publishedAt"]
                })
            
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
                
            if len(comments_data) % 1000 == 0:
<<<<<<< HEAD
                print(f"   ...Coletados {len(comments_data)} comentarios...")
=======
                print(f"   ...Coletados {len(comments_data)} comentários...")
>>>>>>> 4159c885078ad451710417403037900a182a7431

        except HttpError as e:
            if e.resp.status == 403 and "quotaExceeded" in str(e):
                print(f"Erro de Cota na chave {CURRENT_KEY_INDEX + 1}. Tentando trocar...")
                if rotate_key():
                    youtube = get_youtube_client()
                    continue
                else:
                    break
            elif e.resp.status == 404:
                print("Vídeo não encontrado.")
                break
            else:
                print(f"Erro desconhecido: {e}")
                break
                
    return comments_data[:max_results]

# --- NOVA EXECUÇÃO PRINCIPAL (SEPARANDO ARQUIVOS) ---
def main():
<<<<<<< HEAD
    print("--- INICIANDO COLETA (ARQUIVOS SEPARADOS POR ESTUDIO) ---")
=======
    print("--- INICIANDO COLETA (ARQUIVOS SEPARADOS POR ESTÚDIO) ---")
>>>>>>> 4159c885078ad451710417403037900a182a7431

    # Loop pelas franquias (Marvel, DC)
    for franchise, movies_dict in movies.movie_data.items():
        # Define o nome do arquivo dinamicamente: dataset_Marvel.json ou dataset_DC.json
        arquivo_saida = f"dataset_{franchise}.json"
        
        # Carrega dados existentes ESPECÍFICOS DESTA FRANQUIA
        if os.path.exists(arquivo_saida):
            with open(arquivo_saida, "r", encoding="utf-8") as f:
                dataset_franquia = json.load(f)
        else:
            dataset_franquia = {}

        print(f"\n>>> INICIANDO FRANQUIA: {franchise}")
        print(f">>> Arquivo de destino: {arquivo_saida}")

        for movie_name, video_id in movies_dict.items():
            # Verifica se o filme já está salvo neste arquivo específico
            if movie_name in dataset_franquia and dataset_franquia[movie_name]["total_collected"] > 0:
                print(f"  [Pular] {movie_name} já coletado.")
                continue

            print(f"  > Coletando: {movie_name}...")
            
            # --- LEMBRE-SE: Mude aqui para 20 (teste) ou tire o argumento (pegar tudo) ---
            comments = get_comments_safe(video_id, max_results=100000) 
            
            # Salva no dicionário local da franquia
            dataset_franquia[movie_name] = {
                "video_id": video_id,
                "total_collected": len(comments),
                "comments": comments 
            }
            
            # Salva APENAS o arquivo da franquia atual
            with open(arquivo_saida, "w", encoding="utf-8") as f:
                json.dump(dataset_franquia, f, indent=4, ensure_ascii=False)
                
            print(f"    Dados salvos em {arquivo_saida}.")

    print("\n--- TODAS AS FRANQUIAS PROCESSADAS ---")

if __name__ == "__main__":
    main()