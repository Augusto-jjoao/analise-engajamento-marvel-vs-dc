import os
import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import movies  # Seu arquivo de IDs

# Carrega ambiente
load_dotenv()

# --- GESTÃO DE CHAVES API ---
keys_string = os.getenv("YOUTUBE_API_KEYS")
API_KEYS = [k.strip() for k in keys_string.split(",") if k.strip()]
CURRENT_KEY_INDEX = 0

if not API_KEYS:
    raise ValueError("Nenhuma chave encontrada no .env!")

def get_youtube_client():
    """Cria o cliente usando a chave atual da lista."""
    global CURRENT_KEY_INDEX
    print(f"--> Usando a chave API numero: {CURRENT_KEY_INDEX + 1}")
    return build("youtube", "v3", developerKey=API_KEYS[CURRENT_KEY_INDEX])

def rotate_key():
    """Muda para a próxima chave da lista. Retorna False se acabarem as chaves."""
    global CURRENT_KEY_INDEX
    CURRENT_KEY_INDEX += 1
    if CURRENT_KEY_INDEX >= len(API_KEYS):
        print("!!! CRÍTICO: Todas as chaves API foram esgotadas/expiraram !!!")
        return False
    print(f"!!! Trocando para a chave API número: {CURRENT_KEY_INDEX + 1} !!!")
    return True

# --- FUNÇÃO DE COLETA ---
def get_comments_safe(video_id, max_results=100000): # Valor alto para pegar "tudo"
    """
    Coleta comentários com sistema de retry e rotação de chaves.
    """
    comments_data = []
    youtube = get_youtube_client()
    next_page_token = None
    
    # Loop infinito até acabar os comentários ou o limite
    while len(comments_data) < max_results:
        try:
            # Monta a requisição
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100, # Máximo da API por página
                textFormat="plainText",
                order="relevance",
                pageToken=next_page_token
            )
            
            response = request.execute()
            
            # Processa os itens da página atual
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments_data.append({
                    "text": snippet["textDisplay"],
                    "likes": snippet["likeCount"],
                    "date": snippet["publishedAt"]
                })
            
            # Verifica paginação
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break # Acabaram os comentários do vídeo
                
            # Feedback visual a cada 1000 comentários para você saber que não travou
            if len(comments_data) % 1000 == 0:
                print(f"   ...Coletados {len(comments_data)} comentários até agora...")

        except HttpError as e:
            # Verifica se o erro é de COTA (403 + reason 'quotaExceeded')
            if e.resp.status == 403 and "quotaExceeded" in str(e):
                print(f"Erro de Cota na chave {CURRENT_KEY_INDEX + 1}. Tentando trocar...")
                if rotate_key():
                    youtube = get_youtube_client() # Recria o cliente com a nova chave
                    continue # Tenta a MESMA página de novo com a nova chave
                else:
                    break # Acabaram as chaves, sai do loop salvando o que tem
            elif e.resp.status == 404:
                print("Vídeo não encontrado ou comentários desativados.")
                break
            else:
                print(f"Erro desconhecido: {e}")
                break # Para evitar loops infinitos de outros erros
                
    return comments_data

# --- EXECUÇÃO PRINCIPAL ---
def main():
    # Carrega dados existentes se houver (para não sobrescrever se rodar de novo)
    arquivo_saida = "dataset_marvel_vs_dc_full.json"
    if os.path.exists(arquivo_saida):
        with open(arquivo_saida, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    else:
        dataset = {"Marvel": {}, "DC": {}}

    print("--- INICIANDO COLETA MASSIVA (COM ROTAÇÃO DE CHAVES) ---")

    for franchise, movies_dict in movies.movie_data.items():
        if franchise not in dataset: 
            dataset[franchise] = {}

        for movie_name, video_id in movies_dict.items():
            # Verifica se já coletamos esse filme para não repetir
            if movie_name in dataset[franchise] and dataset[franchise][movie_name]["total_collected"] > 0:
                print(f"Pulinho {movie_name} (já coletado).")
                continue

            print(f"\nIniciando: {movie_name} (ID: {video_id})")
            
            # Chama a função segura
            comments = get_comments_safe(video_id, max_results=20) ########################AQUI É ONDE MUDA A QUANTIDADE DE COMENTÁRIOS PER VIDEO
            
            # Salva na estrutura
            dataset[franchise][movie_name] = {
                "video_id": video_id,
                "total_collected": len(comments),
                "comments": comments
            }
            
            print(f"--> Finalizado {movie_name}: {len(comments)} comentários salvos.")
            
            # SALVA O ARQUIVO A CADA FILME (Segurança contra falhas)
            with open(arquivo_saida, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=4, ensure_ascii=False)

    print("\n--- COLETA TOTALMENTE CONCLUÍDA ---")

if __name__ == "__main__":
    main()