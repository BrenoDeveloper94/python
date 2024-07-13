from fastapi import APIRouter, Depends
from pydantic import BaseModel
import spacy
from typing import List, Optional
from functools import lru_cache

router = APIRouter(prefix='/polisher')

class Comment(BaseModel):
    text: str
    like_count: int

class Item(BaseModel):
    caption: Optional[str] = None
    comments: Optional[List[Comment]] = None

# Carregar o modelo de português uma vez durante a inicialização
nlp = spacy.load("pt_core_news_sm")

# Cache para palavras indesejadas
@lru_cache(maxsize=None)
def load_unwanted_words():
    try:
        with open('src/polisher/words/unwanted_words.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            return content.split(',')
    except Exception as e:
        print(f"Erro na leitura do arquivo de palavras indesejadas: {e}")
        return []

@router.post('/')
def polisher(input: List[Item], unwanted_words: List[str] = Depends(load_unwanted_words)):
    
    def summary(phrase):
        # Processar o texto
        doc = nlp(phrase)
    
        # Extrair apenas os substantivos que não estão na lista de palavras indesejadas
        nouns = [token.text for token in doc if token.pos_ == "NOUN" and token.text.lower() not in unwanted_words]
    
        # Remover duplicatas mantendo a ordem
        single_words = list(dict.fromkeys(nouns))
        
        # Juntar de volta em uma string separada por vírgula
        phrase_completed = ','.join(single_words)
    
        return phrase_completed
    
    # Implementando a lógica de sumarização
    def summarize_data(caption, comments):
        # Resumo da legenda
        summary_caption = summary(caption) if caption else None
        
        # Resumo dos comentários
        summary_comments = []
        for comment in comments:
            summary_text = summary(comment.text)
            summary_comments.append({"text": summary_text, "like_count": comment.like_count})
        
        return summary_caption, summary_comments
    
    # Extraindo dados para tratar
    caption = input[0].caption if input[0].caption else ""
    comments = input[1].comments if input[1].comments else []

    # Chamando a função de sumarização
    summary_caption, summary_comments = summarize_data(caption, comments)
    
    # Retornando os dados sumarizados
    return {"caption": summary_caption, "comments": summary_comments}
