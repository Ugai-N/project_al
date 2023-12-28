# from sqlalchemy.orm import Session
#
# from db import models
#
#
# def get_db_problem_by_id(db: Session, id):
#     return db.query(models.DB_problem_class).filter(models.DB_problem_class.problem_id == id).first()
#
#
# def create_problem(db: Session, problem: schemas.Problem):
#     problem_in_db = models.DB_problem_class(
#         name=problem.name,
#         rating=problem.rating,
#         tags=problem.tags,
#         search_code=problem.search_code,
#         solvedCount=problem.solvedCount
#     )
#     db.add(problem_in_db)
#     db.commit()
#     db.refresh(problem_in_db)
#     return problem_in_db
