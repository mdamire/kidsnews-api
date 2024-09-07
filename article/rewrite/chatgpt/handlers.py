import logging

from article.models import ArticleRecord, ModifiedArticleRecord
from .client import send_request_to_chatgpt


_log = logging.getLogger(__name__)


def rewrite_article_for_kids(article: ArticleRecord) -> ModifiedArticleRecord:
    modified_record = ModifiedArticleRecord(id=article.id)
    
    # Skip article with bad words
    if article.title_bad_words:
        _log.info(f'Skipping rewrite. article id: {article.id} for bad words')
        return
    
    # Construct the prompt for ChatGPT for a single article
    prompt = (
        "Rewrite the following article for kids in simple language:\n\n"
        f"Title: {article.original_title}\n"
        f"Description: {article.original_description}\n"
        f"Content: {article.original_content}\n\n"
    )

    # Send the request to ChatGPT for the single article
    response_dict = send_request_to_chatgpt(prompt)
    response = response_dict['choices'][0]['message']['content']

    # Split the response into lines for the single article
    lines = response.split("\n")

    # Extract rewritten title, description, and content from the response
    rw_title = lines[0].replace("Title: ", "").strip()
    rw_description = lines[1].replace("Description: ", "").strip()
    rw_content = "\n".join(lines[2:]).replace("Content: ", "").strip()

    # Update the article record with the rewritten content
    modified_record.title = rw_title
    modified_record.content = rw_content
    modified_record.description = rw_description
    modified_record.save()

    return modified_record
