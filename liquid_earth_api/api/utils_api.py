def find_space_item(all_projects: list, space_name: str):
    found_project = None
    for project in all_projects:
        if project["Name"] == space_name:
            found_project = project
    if found_project is None:
        raise ValueError("project not found")
    return found_project
