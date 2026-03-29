def paginate_query(query, page, per_page=10):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [item.to_dict() for item in pagination.items],
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "total": pagination.total
    }