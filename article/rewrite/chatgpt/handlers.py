from article.article import ArticlePage
from .client import send_request_to_chatgpt


async def rewrite_articles_for_kids(article_page: ArticlePage):
    # Construct the prompt for ChatGPT
    prompt = "Rewrite the following articles for kids in simple language. Maintain the ID for each article:\n\n"
    
    for idx, article in enumerate(article_page.articles):
        # skip article with bad words
        if article.has_bad_words:
            continue
        
        prompt += f"ID: {idx}\n"
        prompt += f"Title: {article.title}\n"
        prompt += f"Description: {article.description}\n"
        prompt += f"Content: {article.content}\n\n"
    
    # Send the request to ChatGPT
    response_dict = await send_request_to_chatgpt(prompt)
    response = response_dict['choices'][0]['message']['content']
    
    # Split the response into sections for each article
    rewritten_sections = response.split("\n\n")

    for rewritten_section in rewritten_sections:
        if not rewritten_section:
            continue
        
        lines = rewritten_section.split("\n")
        
        # Extract rewritten ID, title, description, and content from the response
        rw_id = int(lines[0].replace("ID: ", "").strip())
        rw_title = lines[1].replace("Title: ", "").strip()
        rw_description = lines[2].replace("Description: ", "").strip()
        rw_content = "\n".join(lines[3:]).replace("Content: ", "").strip()

        article_page.articles[rw_id].modified_title = rw_title
        article_page.articles[rw_id].modified_content = rw_content
        article_page.articles[rw_id].modified_description = rw_description
        
    return article_page
