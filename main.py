from db_updater.tasks import testing_celery


# --> вынести в конфиги и env
api_url = 'https://codeforces.com/api/problemset.problems'


def main():
    # --> get json file from API or from file:

    # results = APIresponse().get_problems(api_url)
    # save_to_file('new_db_file.json', results)
    # results = get_from_file('test_data.json')
    # print('--->>> uploaded json file via API request')

    # --> create all tables for models (not needed as tables are created by migrations)
    # Base.metadata.create_all(bind=engine)
    # print('--->>> created tables in DB')

    # --> open DB session
    # with SessionLocal() as db:

        # --> launch update of DB
        # parser_handler(db, results)

    result = testing_celery.delay()
    # print(result.get())
    # print(result.ready())



        # --> check how many contests are ready + how many tags are available + how many problems are in DB
        # stmt = (
        #     select(Contest)
        #     .options(
        #         selectinload(Contest.problems),
        #     )
        #     .order_by(Contest.id)
        # )
        # all_contests_with_problems = list(db.scalars(stmt))
        # full_contests = []
        # for con in all_contests_with_problems:
        #     if len([pro for pro in con.problems]) == 10:
        #         full_contests.append(con)
        # print(f'qty of ready contests: {len(full_contests)}')
        # full_contest_tags = [i.tag for i in full_contests]
        # print(f'qty of available tags of ready contests: {len(set(full_contest_tags))}')
        # stmt = (
        #     select(Problem)
        # )
        # all_problems = list(db.scalars(stmt))
        # print(f'qty of problems in DB: {len(all_problems)}')

# --> check how many and what problems are in every contest
        # stmt = (
        #     select(Contest)
        #     .options(
        #         selectinload(Contest.problems),
        #     )
        #     .order_by(Contest.id)
        # )
        # all_contests_with_problems = list(db.scalars(stmt))
        # for con in all_contests_with_problems:
        #     print(f'\n{con}')
        #     for pr in con.problems:
        #         print(f'@{pr}')

# --> черновое - УДАЛИТЬ
        # Problem().test_methond('dddd')

        # # pro = db.query(Problem).filter(Problem.id == 7).first() --> равнозначно строчке ниже
        # pro = db.scalar(select(Problem).where(Problem.id == 2534))   # type: Problem
        # handle_contest(db, pro)


if __name__ == '__main__':
    main()
