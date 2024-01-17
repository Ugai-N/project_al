import json
import os


def get_solvedCount(statistics_list, contestId, index):
    """checks the json-file and gets the attribute 'solvedCount' for a Problem if it exists,
    otherwise returns 0"""
    for st in statistics_list:
        if st['contestId'] == contestId:
            if st['index'] == index:
                return st['solvedCount']
        continue
    return 0


def get_rating_group(pro_rating: int) -> int:
    """Basing on the rating of a Problem -> forms a rating level, which is used when grouping problems into contests
    Problem rating starts from 800 (unless is null(0)) and is usually divisible by 100 (800/900/1000 etc).
    Problems are grouped in contests by rating level step of 300 (e.g. 800-1099, 1100-1399 etc)"""
    if pro_rating is None or pro_rating < 800:
        pro_rating_level = 0
    else:
        rating_level = 800
        while True:
            if rating_level <= pro_rating <= rating_level + 300 - 1:
                pro_rating_level = rating_level
                break
            else:
                rating_level += 300
    return pro_rating_level


def get_from_file(file) -> list:
    """returns the list results from json-file"""
    with open(file, 'r', encoding='utf-8') as f:
        filelist = json.load(f)
        return filelist


def save_to_file(file, results):
    """saves/adds the data into json-file"""
    results_list = []
    for r in results:
        data = {"id": r.search_code,
                "имя": r.name,
                "сложность": r.rating,
                "теги": r.tags,
                "решения": r.solvedCount
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
