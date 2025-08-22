def dfs_search(task_list, target_id):
    for task in task_list:
        if task.id == target_id:
            return task
        result = dfs_search(task.children, target_id)
        if result:
            return result
    return None
