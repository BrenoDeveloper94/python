from fastapi import APIRouter
from pydantic import BaseModel
import unicodedata
import re

router = APIRouter(prefix='/dialog')

class InputDialogResponse(BaseModel):
    question: str


@router.post('/')
def polisher(input: InputDialogResponse):
    # Função para ler arquivos e retornar uma lista de palavras
    def read_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content.split(',')
        except Exception as e:
            print(f"Erro na leitura do arquivo {path}: {e}")
            return []
    
        
    # Função para ler a pergunta e retornar uma lista de palavras contida nela
    def read_question(question: str):
           normalized = unicodedata.normalize('NFD', question)
           question_normalized = normalized.encode('ascii', 'ignore').decode('utf8').casefold()
           question_normalized_regex = re.sub(r'[^a-zA-Z0-9 ]', '', question_normalized)
           return question_normalized_regex.split(' ')
    
    # Caminhos dos arquivos
    path_least_liked_comment = 'src/dialog/wordspost/least_liked_comment.txt'
    path_most_liked_comment = 'src/dialog/wordspost/most_liked_comment.txt'
    path_most_relevant_comment = 'src/dialog/wordspost/most_relevant_comment.txt'
    path_ten_least_liked_comment = 'src/dialog/wordspost/ten_least_liked_comment.txt'
    path_ten_most_liked_comment = 'src/dialog/wordspost/ten_most_liked_comment.txt'
    path_ten_negative_comments = 'src/dialog/wordspost/ten_negative_comments.txt'
    path_ten_positive_comments = 'src/dialog/wordspost/ten_positive_comments.txt'
    path_ten_suggestion_comments = 'src/dialog/wordspost/ten_suggestion_comments.txt'
    
    
    # Lendo os arquivos
    array_least_liked_comment = read_file(path_least_liked_comment)
    array_most_liked_comment = read_file(path_most_liked_comment)
    array_most_relevant_comment = read_file(path_most_relevant_comment)
    array_ten_least_liked_comment = read_file(path_ten_least_liked_comment)
    array_ten_most_liked_comment = read_file(path_ten_most_liked_comment)
    array_ten_negative_comments = read_file(path_ten_negative_comments)
    array_ten_positive_comments = read_file(path_ten_positive_comments)
    array_ten_suggestion_comments = read_file(path_ten_suggestion_comments)

    # Texto de entrada da pergunta
    input_text = input.question

    array_question = read_question(input_text)
    
    
    # Função para verificar se uma palavra está na lista
    def compare_words(words, list):
        counter = 0
        for question in words:
            if question in list:
                counter += 1
            
        return counter
    
    # Chamando as funções que realizam as verificações
    result_least_liked_comment = compare_words(array_question, array_least_liked_comment)
    result_most_liked_comment = compare_words(array_question, array_most_liked_comment)
    result_most_relevant_comment = compare_words(array_question, array_most_relevant_comment)
    result_ten_least_liked_comment = compare_words(array_question, array_ten_least_liked_comment)
    result_ten_most_liked_comment = compare_words(array_question, array_ten_most_liked_comment)
    result_ten_negative_comments = compare_words(array_question, array_ten_negative_comments)
    result_ten_positive_comments = compare_words(array_question, array_ten_positive_comments)
    result_ten_suggestion_comments = compare_words(array_question, array_ten_suggestion_comments)


    #print('least_liked_comment:', result_least_liked_comment)
    #print('most_liked_comment:', result_most_liked_comment)
    #print('most_relevant_comment:', result_most_relevant_comment)
    #print('ten_least_liked_comment:', result_ten_least_liked_comment)
    #print('ten_most_liked_comment:', result_ten_most_liked_comment)
    #print('ten_negative_comments:', result_ten_negative_comments)
    #print('ten_positive_comments:', result_ten_positive_comments)
    #print('ten_suggestion_comments:', result_ten_suggestion_comments)

    options = {
        'least_liked_comment': result_least_liked_comment,
        'most_liked_comment': result_most_liked_comment,
        'most_relevant_comment': result_most_relevant_comment,
        'ten_least_liked_comment': result_ten_least_liked_comment,
        'ten_most_liked_comment': result_ten_most_liked_comment,
        'ten_negative_comments': result_ten_negative_comments,
        'ten_positive_comments': result_ten_positive_comments,
        'ten_suggestion_comments': result_ten_suggestion_comments,
    }

    for name, value in options.items():
        print(f"Nome: {name}, Valor: {value}")

    max_value = max(options.items(), key=lambda item: item[1])

    print(f"Nome da variável com maior valor: {max_value[0]}, Valor: {max_value[1]}")

    #duplicated_values = {value: names for value, names in value_to_vars.items() if len(names) > 1}

    return {max_value[0]}