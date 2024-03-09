#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
from app.models import User, DatasetInfo, Pair


def add_new_dataset(user_id, new_dataset_name):
    # created new database = return 1
    # dataset name already used = return 0

    #check if name is already used
    is_name_used = db.session.query(User).filter_by(id=user_id).join(User.dataset).filter(DatasetInfo.name == new_dataset_name).first()

    if is_name_used is None:
        new = DatasetInfo(name=new_dataset_name, author=db.session.get(User, user_id))
        db.session.add(new)
        db.session.commit()
        return 1
    else:
        return 0