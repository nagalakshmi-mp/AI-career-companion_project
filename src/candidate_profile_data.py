def format_profile(profile):
    """
    Format the structured candidate profile
    for displaying in the application.
    """

    formatted = {}

    formatted["Name"] = profile.get("name", "")
    formatted["Email"] = profile.get("email", "")
    formatted["Phone"] = profile.get("phone", "")

    formatted["Education"] = profile.get(
        "education",
        []
    )

    formatted["Skills"] = profile.get(
        "skills",
        []
    )

    formatted["Experience"] = profile.get(
        "experience",
        []
    )

    formatted["Projects"] = profile.get(
        "projects",
        []
    )

    formatted["Qualifications"] = profile.get(
        "qualifications",
        []
    )

    return formatted