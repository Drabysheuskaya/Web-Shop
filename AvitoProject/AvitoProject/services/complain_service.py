from sqlalchemy.orm import Session
from database.models import ProblemReport


def save_problem_report(db: Session, description: str, product_id: int, user_id: int):
    existing_report = db.query(ProblemReport).filter(
        ProblemReport.product_id == product_id,
        ProblemReport.user_id == user_id
    ).first()

    if existing_report:
        return "Already exist"
    problem_report = ProblemReport(
        description=description,
        product_id=product_id,
        user_id=user_id
    )
    db.add(problem_report)
    db.commit()
    db.refresh(problem_report)
    return "Successfully sent"
