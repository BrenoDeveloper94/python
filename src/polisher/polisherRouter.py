from fastapi import APIRouter
from pydantic import BaseModel
import spacy
from typing import List, Optional
import nltk
from nltk.corpus import wordnet as wn
#from transformers import BertModel, BertTokenizer
#import torch

router = APIRouter(prefix='/polisher')

class Comment(BaseModel):
    text: str
    like_count: int

class Item(BaseModel):
    caption: Optional[str] = None
    comments: Optional[List[Comment]] = None


@router.post('/')
def polisher(input: List[Item]):

    def summary(phrase):
        # Carregar o modelo de português
        nlp = spacy.load("pt_core_news_sm")
    
        # Processar o texto
        doc = nlp(phrase)
    
    
        # Função para ler arquivos e retornar uma lista de palavras
        def read_file(path):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    return content.split(',')
            except Exception as e:
                print(f"Erro na leitura do arquivo {path}: {e}")
                return []
            
            
        # Lendo o arquivo com as palavras indesejadas
        unwanted_words = read_file('src/polisher/words/unwanted_words.txt')
        
    
        # Extrair apenas os substantivos que não estão na lista de palavras indesejadas
        nouns = [token.text for token in doc if token.pos_ == "NOUN" and token.text.lower() not in unwanted_words]
    
        # Remover duplicatas mantendo a ordem
        single_words = list(dict.fromkeys(nouns))
        
        # Juntar de volta em uma string separada por vírgula
        phrase_completed = ','.join(single_words)
    
        return phrase_completed
    
    
    # Extraindo dados para tratar
    caption = input[0].caption
    comments = input[1].comments

    # Resume o caption
    summary_caption = summary(caption)  

    array_comments_summary = []

    for comment in comments:
        summary_comment_text = summary(comment.text)
        array_comments_summary.append({"text": summary_comment_text,"like_count": comment.like_count})


    # Array do post resumido
    summary_post = []

    # Conjunto para rastrear palavras únicas
    unique_words = set()
    
    # Lista para armazenar objetos de comentários únicos
    unique_comments_data = []

    # Adicionando o caption do post
    summary_post.append({"caption": summary_caption})
    # Adicionando o comentários do post
    summary_post.append({"comments": unique_comments_data})
    
    # Função para extrair palavras de um texto
    def extract_words(text):
        # Remove pontuações e converte para minúsculas
        clean_text = text.replace(',', ' ').replace('.', '').lower()
        return set(clean_text.split())
    
    # Iterar sobre os dados
    for data in array_comments_summary:
        if data["text"]:  # Verifica se o texto não está vazio
            words = extract_words(data["text"])
            # Verificar se há interseção entre as palavras e palavras_unicas
            if not words.intersection(unique_words):
                # Se não houver interseção, adicionar palavras ao conjunto de palavras unicas e dado à lista de dados unicos
                unique_words.update(words)
                unique_comments_data.append(data)
    

    return summary_post


























    
    

#####################################################################################################

    ## Carregar o modelo BERT pré-treinado e o tokenizador para português
    #model_name = 'neuralmind/bert-base-portuguese-cased'
    #tokenizer = BertTokenizer.from_pretrained(model_name)
    #model = BertModel.from_pretrained(model_name)
    #
    ## Texto de exemplo em português
    #texto = comment_filtered
    #
    ## Tokenizar o texto e preparar para entrada no modelo
    #tokens = tokenizer(texto, return_tensors='pt')
    #with torch.no_grad():
    #    # Obter embeddings a partir do modelo BERT
    #    outputs = model(**tokens)
    #    embeddings = outputs.last_hidden_state
    #
    ## 'embeddings' agora contém os embeddings das palavras no texto
    ##print(embeddings)