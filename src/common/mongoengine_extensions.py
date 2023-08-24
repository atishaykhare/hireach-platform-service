from pymongo import UpdateOne
from mongoengine import ValidationError
from mongoengine import Q
from mongoengine.queryset.visitor import QCombination


def generate_update_query(document,
                          match_query):
    """
    Generates a match query for update operation using mongoengine
    style query input

    TODO: add match query support fields(which exists in document's root)
    """

    final_query = {}

    for match_field in match_query:
        final_query[match_field] = \
            getattr(document, match_field.split('__')[0])

    query = Q(**final_query)

    return query, query.to_query(document)


def check_sanity(document,
                 match_query,
                 set_on_insert):
    """
    checks arguments sanity before running the operation
    :param document: any document instance
    :param match_query: list of fields to be matched in case of update
    :param set_on_insert: dict which is to be set if it's an insert operation
    :return: nothing
    """

    invalid_keys = []

    for i in set_on_insert.keys():

        if not hasattr(document, i):
            invalid_keys.append(i)

    if invalid_keys:
        raise Exception('set_on_insert has invalid keys - {keys}'.format(
            keys=invalid_keys))

    if not match_query:
        raise Exception(
            "If not using a match query please mongoengine's"
            "bulk insert functionality."
        )


def validate_document(document):
    """
    Validates if the document contains all the
    required fields and if the field values are valid.
    Allows 'created_by' to be 'None' since it's only set
    at the time of insertion for new documents
    """

    try:
        document.validate()

    except ValidationError as ve:
        errors = ve.to_dict()
        fields = list(errors.keys())
        if not (len(fields) == 1 and fields[0] == 'created_by'):
            return fields


def bulk_upsert(documents,
                match_query,
                set_on_insert={}):
    """
    general function for performing bulk upsertions for mongoengine documents
    :param documents: Mongoengine documents
    :param match_query: list of fields to be matched in case of update
    :param set_on_insert: dict which is to be set if it's an insert operation
    :return: PyMongo BulkResult
    """

    bulk_operations = []
    match_queries = []
    docs_with_errors = {}

    if not match_query:
        raise Exception('If not using a match query please use insert '
                               'functionality.')

    check_sanity(documents[0], match_query, set_on_insert) \
        if len(documents) > 0 else None

    for i, doc in enumerate(documents):
        error_fields = validate_document(doc)

        if error_fields:
            docs_with_errors[i] = error_fields
            continue

        doc_dict = doc.to_mongo().to_dict()

        if set_on_insert:
            ignore_keys = list(set_on_insert.keys())
            [doc_dict.pop(key, None) for key in ignore_keys]
            set_and_insert_dict = {
                '$set': doc_dict,
                '$setOnInsert': set_on_insert
            }

        else:
            set_and_insert_dict = {
                '$set': doc_dict,
            }

        mongoengine_query, final_match_query = \
            generate_update_query(doc, match_query)
        match_queries.append(mongoengine_query)

        bulk_operations.append(
            UpdateOne(
                final_match_query,
                set_and_insert_dict,
                upsert=True
            )
        )

    if docs_with_errors:
        raise Exception(
            'Validation errors occurred {}'.format(docs_with_errors)
        )

    elif not bulk_operations:
        raise Exception('no operations to execute')

    model_class = type(documents[0])
    results = model_class._get_collection() \
        .bulk_write(bulk_operations)

    return results
