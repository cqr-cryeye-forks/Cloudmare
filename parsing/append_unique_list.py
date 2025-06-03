def append_unique_list(container, key, value):
    """Append dict `value` to container[key] list without duplicates."""
    if key not in container:
        container[key] = []
    if value not in container[key]:
        container[key].append(value)
