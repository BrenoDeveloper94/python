from fastapi import APIRouter
from pydantic import BaseModel
import unicodedata
import re
import emoji
import difflib


router = APIRouter(prefix='/categorization')

class InputCategorizationResponse(BaseModel):
    comment: str


@router.post('/')
def categorization(input: InputCategorizationResponse):
    # Função para ler arquivos e retornar uma lista de palavras
    def read_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content.split(',')
        except Exception as e:
            print(f"Erro na leitura do arquivo {path}: {e}")
            return []
    
        
    # Função para ler comentários e retornar uma lista de palavras
    def read_comment(comment: str):
        normalized = unicodedata.normalize('NFD', comment)
        comment_normalized = normalized.encode('ascii', 'ignore').decode('utf8').casefold()
        comment_normalized = re.sub(r'[^a-zA-Z0-9 ?]', '', comment_normalized)  # Remover caracteres indesejados
        comment_normalized = re.sub(r'\.{2,}', ' ', comment_normalized)  # Substituir múltiplos pontos por um espaço
        comment_normalized = re.sub(r'\?', ' ? ', comment_normalized) # Adicionar espaços ao redor de pontos de interrogação para tratá-los como palavras isoladas
        return comment_normalized.split(' ')
    

    # Função para ler emojis
    def read_emojis(comment: str):
        emojis = []

        matches = re.findall(r'[\U0001F600-\U0001F64F\u2702-\u27B0\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]', comment)

        for match in matches:
            try:
                # Verifica se o caractere é um emoji válido
                if emoji.is_emoji(match):
                    name: str = emoji.demojize(match)  # Converte o emoji em nome de emoji
                    emojis.append(name)
            except Exception as e:
                emojis.append({
                    "emoji": match,
                    "type": str(e)
                })
    
        return emojis
    
    # Caminhos dos arquivos
    path_negative = 'src/categorization/words/negative.txt'
    path_positive = 'src/categorization/words/positive.txt'
    path_suggestion = 'src/categorization/words/suggestion.txt'
    path_negative_emoji = 'src/categorization/words/negative_emoji.txt'
    path_positive_emoji = 'src/categorization/words/positive_emoji.txt'
    
    # Lendo os arquivos
    array_negative = read_file(path_negative)
    array_positive = read_file(path_positive)
    array_suggestion = read_file(path_suggestion)
    array_negative_emoji = read_file(path_negative_emoji)
    array_positive_emoji = read_file(path_positive_emoji)

    # Texto de entrada do comentário
    input_text = input.comment

    array_coment = read_comment(input_text)
    emoji_name = read_emojis(input_text)
    
    # Função para verificar se uma palavra está na lista
    def compare_words(words, list):
        counter = 0
        for coment in words:
            matches = difflib.get_close_matches(coment, list)
            if not matches:
                pass
            else:
                counter += 1
            if coment in list:
                counter += 1
            
        return counter
    
    # Chamando as funções que realizam as verificações
    result_negative = compare_words(array_coment, array_negative)
    result_positive = compare_words(array_coment, array_positive)
    result_suggestion = compare_words(array_coment, array_suggestion)
    result_negative_emoji = compare_words(emoji_name, array_negative_emoji)
    result_positive_emoji = compare_words(emoji_name, array_positive_emoji)

    comment_string = ''.join(array_coment)

    if len(comment_string) == 0 and len(emoji_name) > 0:

        if result_negative_emoji > result_positive_emoji:
            print('negativo:', result_negative_emoji)
            print('positivo:', result_positive_emoji)
            return {'negative'}
        elif result_negative_emoji < result_positive_emoji:
            print('negativo:', result_negative_emoji)
            print('positivo:', result_positive_emoji)
            return {'positive'}
        else:
            print('negativo:', result_negative_emoji)
            print('positivo:', result_positive_emoji)
            return {'neutral'}

    else:
        
        # Verificações e saídas
        if result_negative == result_positive == result_suggestion:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'neutral'}
        
        if result_negative == result_positive and result_suggestion < result_negative:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'negative'}
        
        if result_negative == result_suggestion and result_positive < result_negative:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'suggestion'}
        
        if result_positive == result_suggestion and result_negative < result_positive:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'suggestion'}
        
        if result_negative > result_positive and result_negative > result_suggestion:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'negative'}
        elif result_positive > result_negative and result_positive > result_suggestion:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'positive'}
        elif result_suggestion > result_negative and result_suggestion > result_positive:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'suggestion'}
        else:
            print('negativo:', result_negative)
            print('positivo:', result_positive)
            print('sugestao:', result_suggestion)
            return {'neutral'}