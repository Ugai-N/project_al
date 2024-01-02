from models import Tag


def create_tag(db, name: str) -> Tag:
    """creates a new Tag in DB"""
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.commit()
    print(f'--->>> added tag to DB: {new_tag}')
    return new_tag


def get_tags_to_attach(db, tags: list) -> list:
    """check every tag for a particular Problem: if no such tag in DB yet -> add new tag to DB.
    Returns a list of Tag instances to the Problem"""
    tag_instances_to_attach = []
    for item in tags:
        """if no such tag in DB yet -> add to DB"""
        if db.query(Tag).filter(Tag.name == item).count() == 0:
            tag_to_attach = create_tag(db, name=item)
        else:
            """if such tag exists in DB -> return to Problem"""
            tag_to_attach = db.query(Tag).filter(Tag.name == item).first()
        tag_instances_to_attach.append(tag_to_attach)
    return list(set(tag_instances_to_attach))
