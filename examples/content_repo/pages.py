from api.content_repo import pyContent

pages = pyContent().pages.get_pages()

pages.head(5)
