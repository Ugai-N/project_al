class Problem:

    problems_list = []

    def __init__(self, contestId, index, name, rating, tags, solvedCount):
        self.__search_code = self.get_search_code(contestId, index)
        self.name = name
        self.rating = rating
        self.tags = tags
        self.solvedCount = solvedCount
        Problem.problems_list.append(self)

    def get_search_code(self, contestId, index):
        return '-'.join([contestId, index])

    @property
    def search_code(self):
        """Геттер для приватного атрибута __search_code"""
        return self.__search_code

#     Problem
#     "contestId": 988,
#     "index": "A",
#     "name": "Максимальный непрерывный отдых",
#     "rating": 900,
#     "tags": [
#         "implementation"
#     ]
#
#     ProblemStatistics
#     "contestId": 988,
#     "index": "A",
#     "solvedCount": 10317

    @classmethod
    def class_init_handler(cls, json_response) -> None:
        """для каждой задачи инициализирует экземпляр Problem"""
        problems_list = json_response['result']['problems']
        statistics_list = json_response['result']['problemStatistics']
        for p in problems_list: #contestId, index, name, rating, tags, solvedCount
            cls(
                contestId=p['contestId'],
                index=p['index'],
                name=p['name'],
                rating=p['rating'],
                tags=p['tags'],
                solvedCount=cls.get_solvedCount(statistics_list, p['contestId'], p['index'])
            )

    @staticmethod
    def get_solvedCount(statistics_list, contestId, index):
        for st in statistics_list:
            if st['contestId'] == contestId and st['index'] == index:
                return st['solvedCount']
            else:
                print('ooooops')
                return 0
