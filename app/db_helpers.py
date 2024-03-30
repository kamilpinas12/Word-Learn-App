#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import db
from app.models import User, DatasetInfo, Pair


def add_new_dataset(user_id, new_dataset_name):
    # created new database = return 1
    # dataset name taken = return 0

    is_name_used = db.session.query(User).filter_by(id=user_id).join(User.dataset)\
        .filter(DatasetInfo.name == new_dataset_name).first()

    if is_name_used is None:
        new = DatasetInfo(name=new_dataset_name, most_appearances=1, most_lst_appearances=1, author=db.session.get(User, user_id))
        db.session.add(new)
        db.session.commit()
        return 1
    else:
        return 0


def add_word_to_dataset(dataset_id, question, answer):
    is_pair_in_dataset = db.session.query(DatasetInfo).filter_by(id=dataset_id).\
        join(DatasetInfo.pair).filter(Pair.question == question).first()

    if is_pair_in_dataset is None:
        new = Pair(question=question, answer=answer, factor=1, correct=0, wrong=0, lst_appearance=0,
                   dataset_info=db.session.get(DatasetInfo, dataset_id))
        db.session.add(new)
        db.session.commit()
        return 1
    else:
        return 0


def update_stats(pair_id: int, is_correct: bool, dataset_id):
    pair = db.session.get(Pair, pair_id)

    if is_correct:
        setattr(pair, 'correct', Pair.correct + 1)
    else:
        setattr(pair, 'wrong', Pair.wrong + 1)
    setattr(pair, 'lst_appearance', 0)
    db.session.commit()

    pair = db.session.get(Pair, pair_id)
    dataset = db.session.get(DatasetInfo, dataset_id)

    if dataset.most_appearances < pair.correct + pair.wrong:
        setattr(dataset, 'most_appearances', pair.correct + pair.wrong)
        db.session.commit()
        dataset = db.session.get(DatasetInfo, dataset_id)

    pairs = db.session.query(Pair).join(DatasetInfo).filter(DatasetInfo.id == dataset_id).all()

    for p in pairs:
        appearances = p.correct + p.wrong
        if appearances == 0:
            continue

        if p.lst_appearance + 1 > dataset.most_lst_appearances:
            setattr(dataset, "max_lst_appearances", pair.lst_appearance + 1)
            db.session.commit()
            dataset = db.session.get(DatasetInfo, dataset_id)

        accuracy = p.correct / appearances
        lst_appearance_factor = 0.1 * (p.lst_appearance / dataset.most_lst_appearances)
        accuracy_factor = 0.75 * (1 - accuracy)
        appearances_factor = 0.15 * (1 - (appearances / dataset.most_appearances))
        factor = lst_appearance_factor + accuracy_factor + appearances_factor
        setattr(p, 'lst_appearance', Pair.lst_appearance + 1)
        setattr(p, 'factor', factor)

    db.session.commit()


