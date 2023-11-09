#!/usr/bin/env python3
"""
list_all
"""


def list_all(mongo_collection):
    """
    Return an empty list if no document in the collection
    """
    documents = mongo_collection.find()
    if documents.count() == 0:
        return []
    return documents