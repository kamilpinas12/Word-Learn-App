#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
from app.models import User, DatasetInfo, Pair


def add_new_dataset(user_id, new_dataset_name):
    # created new database = return 1
    # dataset name already used = return 0

    is_name_used = db.session.query(User).filter_by(id=user_id).join(User.dataset)\
        .filter(DatasetInfo.name == new_dataset_name).first()

    if is_name_used is None:
        new = DatasetInfo(name=new_dataset_name, author=db.session.get(User, user_id))
        db.session.add(new)
        db.session.commit()
        return 1
    else:
        return 0


def add_word_to_dataset(dataset_id, question, answer):
    is_pair_in_dataset = db.session.query(DatasetInfo).filter_by(id=dataset_id).\
        join(DatasetInfo.pair).filter(Pair.question == question).first()

    if is_pair_in_dataset is None:
        new = Pair(question=question, answer=answer, factor=0, correct=0, wrong=0,
                   dataset_info=db.session.get(DatasetInfo, dataset_id))
        db.session.add(new)
        db.session.commit()
        return 1
    else:
        return 0
