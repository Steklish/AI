import json

from gigachat.models import Chat, Function, FunctionParameters, Messages, MessagesRole, FunctionCall
from gigachat import GigaChat

from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_community.tools.

def search_ddg(search_query):
    """Поиск в DuckDuckGo. Полезен, когда нужно ответить на вопросы о текущих событиях. Входными данными должен быть поисковый запрос."""
    return DuckDuckGoSearchRun().run(search_query)

API_KEY = "MTZiOWZkMjMtMzMzMS00NmM3LTg0ZjAtNWM0YmI2OTExZDZhOjFiOGUxYjc2LTVkNzYtNGQyMS1iNWYxLWVhMjIwYjUyMjczMg=="


from gigachat import GigaChat

# Укажите ключ авторизации, полученный в личном кабинете, в интерфейсе проекта GigaChat API
with GigaChat(
		credentials=API_KEY, 
		verify_ssl_certs=False
	) as giga:
    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
    print(response.choices[0].message.content)
    
    response = giga.embeddings(["Hello world!"]).data
    emb = []
    for i in response:
        emb.append(i.embedding)
    print(emb)
    
# """Пример - использование функций.
# Для работы поисковой системы используется утилита из пакета gigachain.
# Установите соответствующую библиотеку с помощью команды



# """



    search = Function(
        name="duckduckgo_search",
        description="""Поиск в DuckDuckGo.
Полезен, когда нужно ответить на вопросы о текущих событиях.
Входными данными должен быть поисковый запрос.""",
        parameters=FunctionParameters(
            type="object",
            properties={"query": {"type": "string", "description": "Поисковый запрос"}},
            required=["query"],
        ),
    )

    messages = []
    function_called = False
    while True:
        # Если предыдущий ответ LLM не был вызовом функции - просим пользователя продолжить диалог
        if not function_called:
            query = input("\033[92mUser: \033[0m")
            messages.append(Messages(role=MessagesRole.USER, content=query))

        chat = Chat(messages=messages, functions=[search])

        resp = giga.chat(chat).choices[0]
        mess = resp.message
        messages.append(mess)

        print("\033[93m" + f"Bot: \033[0m{mess.content}")

        function_called = False
        func_result = ""
        if resp.finish_reason == "function_call":
            print("\033[90m" + f"  >> Processing function call {mess.function_call}" + "\033[0m")
            if mess.function_call.name == "duckduckgo_search":
                query = mess.function_call.arguments.get("query", None)
                if query:
                    func_result = search_ddg(query)
            print("\033[90m" + f"  << Function result: {func_result}\n\n" + "\033[0m")

            messages.append(
                Messages(role=MessagesRole.FUNCTION,
                         content=json.dumps({"result": func_result}, ensure_ascii=False))
            )
            function_called = True
