import os
import dearpygui.dearpygui as dpg
from scipy import spatial
import pymorphy2


# получаем номер документа из его названия
def get_file_number(filename_incoming):
    file_number_res = ""
    for char in filename_incoming:
        if char.isdigit():
            file_number_res = file_number_res + char
    return int(file_number_res)


def make_query_vector(incoming_query, incoming_vector):
    # вектор запроса (ключ - лемма, значение - 1 (есть) или 0 (нету))
    query_vector = dict()
    # список лемм запроса
    query_lemmas = []
    query_words = incoming_query.split(" ")
    all_lemmas = incoming_vector.keys()

    # делаем из слов запроса леммы
    for word in query_words:
        parsed_word = analyzer.parse(word)[0]
        words_lemma = parsed_word.normal_form
        # если лемма есть в списке всех лемм всех документов
        if words_lemma in all_lemmas:
            query_lemmas.append(words_lemma)

    # формируем вектор запроса
    for lemma in all_lemmas:
        if lemma in query_lemmas:
            query_vector[lemma] = 1.0
        else:
            query_vector[lemma] = 0.0

    return query_vector


# считывает из файлов данные и возвращает словарь (ключ - номер документа, значение - вектор этого документа)
def get_docs_vectors():
    # словарь документов (ключ - документ, значение - вектор в виде словаря)
    docs_vectors_dict = dict()

    # проходимся по всех документам директории
    for filename in os.listdir(directory_docs):
        file_path = os.path.join(directory_docs, filename)
        # проверка на тип
        if os.path.isfile(file_path):
            with open(file_path, encoding='cp1251', mode='r') as f_doc:
                # вектор документа (ключ - лемма, значение - tf-idf)
                vector_dict = dict()
                doc_lines = f_doc.readlines()
                for doc_line in doc_lines:
                    if doc_line == "\n":
                        continue
                    doc_line_split = doc_line.split(" ")
                    vector_dict[doc_line_split[0]] = float(doc_line_split[2])
                file_number = get_file_number(filename)
                docs_vectors_dict[file_number] = vector_dict

    return docs_vectors_dict


# вытаскиваем ссылки на документы
def get_docs_urls():
    docs_urls = dict()
    with open(index, encoding='cp1251', mode='r') as f_index:
        lines = f_index.readlines()
        for line in lines:
            if line == "\n":
                continue
            line_split = line.split(" ")
            docs_urls[int(line_split[0])] = line_split[1]
    return docs_urls


# поиск
def search_query(incoming_query):
    res = ""
    print(incoming_query)
    if incoming_query == "":
        return res
    docs_vectors_dict = get_docs_vectors()
    docs_urls_dict = get_docs_urls()
    # Если есть хотя бы один документ
    if len(docs_vectors_dict) != 0:
        cos_similarity_dict = dict()
        query_vector = make_query_vector(incoming_query, docs_vectors_dict[1])
        query_values_vector = list(query_vector.values())
        for doc_number, doc_vector in docs_vectors_dict.items():
            values_vector = list(doc_vector.values())
            # вычисляем косинусное сходство
            cos_similarity_dict[doc_number] = 1 - spatial.distance.cosine(query_values_vector, values_vector)

        # сортируем результаты по убыванию значения схожести
        cos_similarity_dict_sorted = (sorted(cos_similarity_dict.items(), key=lambda item: item[1], reverse=True))
        # выводим 5 самых релевантных страниц
        count = 0
        for key, value in cos_similarity_dict_sorted:
            if key in docs_urls_dict.keys():
                res = res + f"{key}: {docs_urls_dict[key]} cos similarity = {value}\n"
                count += 1
            if count > 5:
                break
    return res


# очистка предыдущих результатов
def delete_children():
    dpg.delete_item("search_group", children_only=True)


# по нажатию кнопки
def search_callback(sender, app_data):
    query = str(dpg.get_value(search_input)).lower()
    delete_children()
    res = search_query(query)
    dpg.add_text(res, parent="search_group")


if __name__ == '__main__':
    index = "index.txt"
    directory_docs = "lemmas-tf-idf"
    analyzer = pymorphy2.MorphAnalyzer()
    dpg.create_context()

    with dpg.font_registry():
        with dpg.font("my_font.ttf", 14) as font_cyrillic:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    with dpg.window(tag="Primary Window"):
        search_input = dpg.add_input_text(tag="search_input", hint='Input has to be: \"word\" \"word1\" \"word2\"...\n')
        dpg.add_button(label="Search", callback=search_callback)
        dpg.add_group(tag="search_group")
        dpg.bind_font(font_cyrillic)
        dpg.bind_item_font(search_input, font_cyrillic)

    dpg.create_viewport(title='War and peace searcher', width=600, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
