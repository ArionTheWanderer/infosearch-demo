import pymorphy2


analyzer = pymorphy2.MorphAnalyzer()


def find_pages(word):
    # Поиск леммы
    parsed_word = analyzer.parse(word)[0]
    lemma = parsed_word.normal_form

    # Поиск леммы в файле с индексами
    with open('inverted_index.txt', encoding='cp1251', mode='r') as f_index:
        lines = f_index.readlines()
        for line in lines:
            if lemma in line:
                # список номеров страниц, соответствующих лемме
                return list(map(int, line.split(' ')[1:]))
    return []


def search(inp):
    if len(inp.split(' ')) == 3 and ('или' in inp or 'и' in inp):
        words = inp.split(' ')
        pages1 = find_pages(words[0])
        pages2 = find_pages(words[2])

        if 'или' in inp:
            return str(inp + ': ' + str(set(pages1 + pages2)))
        else:
            return str(inp + ': ' + str([page for page in pages1 if page in pages2]))
    elif len(inp.split(' ')) == 1:
        return str(inp + ': ' + str(find_pages(inp)))
    else:
        return str("Ошибка формата. Должен быть: \"слово\" или \"слово1 и|или слово2\"")

# def search():
#     if len(inp.split(' ')) == 3 and ('или' in inp or 'и' in inp):
#         words = inp.split(' ')
#         pages1 = find_pages(words[0])
#         pages2 = find_pages(words[2])
#
#         if 'или' in inp:
#             print(inp + ': ' + str(set(pages1 + pages2)))
#         else:
#             print(inp + ': ' + str([page for page in pages1 if page in pages2]))
#     elif len(inp.split(' ')) == 1:
#         print(inp + ': ' + str(find_pages(inp)))
#     else:
#         print("Ошибка формата. Должен быть: \"слово\" или \"слово1 и|или слово2\"")
#
#
# if __name__ == '__main__':
#     analyzer = pymorphy2.MorphAnalyzer()
#     print('Формат запроса: \"слово\" или \"слово1 и|или слово2\"\n'
#           'Для выхода введите \"стоп\"')
#
#     inp = input().lower()
#     while inp != "стоп":
#         search()
#         inp = input().lower()
