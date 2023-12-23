import json
import os



def get_from_file(file) -> list:

    """Возвращает список из указанного json файла"""
    with open(file, 'r', encoding='utf-8') as f:
        filelist = json.load(f)
        return filelist


def save_to_file(file, results):
    """Сохраняет/добавляет в файл json значения"""
    results_list = []
    for r in results:
        data = {"id": r.search_code,
                    "имя": r.name,
                    "сложность": r.rating,
                    "теги": r.tags,
                "решения":r.solvedCount
                    }
        results_list.append(data)

    with open(file, 'a', encoding='utf-8') as f:
        if os.stat(file).st_size == 0:
            json.dump(results_list, f, ensure_ascii=False)
        else:
            with open(file, 'r', encoding='utf-8') as f:
                results_list = json.load(f)
                results_list += results_list
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(results_list, f, ensure_ascii=False)


def get_solvedCount(statistics_list, contestId, index):
    for st in statistics_list:
        if st['contestId'] == contestId:
            if st['index'] == index:
                return st['solvedCount']
        continue
    return 0



