from datetime import datetime, timezone


def investment(target, sources):
    """Распределяет доступные средства между объектами."""
    updated_sources = []
    for source in sources:
        if source.fully_invested:
            continue
        if target.fully_invested:
            break
        free_target = (
            target.full_amount - target.invested_amount
        )
        free_source = (
            source.full_amount - source.invested_amount
        )
        amount = min(free_target, free_source)
        target.invested_amount += amount
        source.invested_amount += amount

        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now(timezone.utc)

        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.now(timezone.utc)

        updated_sources.append(source)

    return updated_sources
