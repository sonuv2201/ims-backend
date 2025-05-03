from typing import Dict
from difflib import get_close_matches
import json

with open("configuration.json", "r") as file:
    data = json.load(file)


def generate_dashboard_config(entity: str, icon: str = None) -> Dict:
    """
    Generate a dashboard configuration object based on the input entity.
    Matches the provided icon with available Lucide React icons.

    Args:
        entity (str): The API endpoint or entity identifier (e.g., '/api/gen-ai/')
        icon (str, optional): The desired icon name. Defaults to None.

    Returns:
        Dict: Dashboard configuration object
    """
    # Available Lucide React icons (update this list as needed)

    def clean_entity_path(entity: str) -> str:
        """Clean the entity path to get a usable identifier."""
        cleaned = entity.strip("/").replace("api/", "")
        cleaned = cleaned.replace("/", "-")
        return cleaned

    def generate_label(identifier: str) -> str:
        """Generate a human-readable label from the identifier."""
        words = identifier.replace("-", " ").split()
        return " ".join(word.capitalize() for word in words)

    # Clean the entity path to get the identifier
    identifier = clean_entity_path(entity)

    # Generate the base URL for the dashboard
    dashboard_url = f"/dashboard/{identifier}"

    # Handle icon matching

    # Generate the configuration object
    config = {
        "id": hash(identifier)
        % 1000,  # Generate a pseudo-random ID based on identifier
        "template": (
            data[entity]["template_name"]
            if entity in data and "template_name" in data[entity]
            else "dashboard-generic-grid"
        ),
        "label": (
            data[entity]["label"]
            if entity in data and "label" in data[entity]
            else generate_label(identifier)
        ),
        "url": (
            data[entity]["url"]
            if entity in data and "url" in data[entity]
            else dashboard_url
        ),
        "entity": entity,
        "icon": (
            data[entity]["icon"]
            if entity in data and "icon" in data[entity]
            else "Wrench"
        ),
        "user_identifier": identifier,
        "caches": False,
        "key": identifier,
        "order": (
            data[entity]["order"]
            if entity in data and "order" in data[entity]
            else 1 if entity == "/lcnc-management/" else len(identifier) % 20
        ),  # Generate a pseudo-random order
        "hide": (
            data[entity]["hide"] if entity in data and "hide" in data[entity] else False
        ),
        # "sub_menu": (
        #     data[entity]["sub_menu"]
        #     if entity in data and "sub_menu" in data[entity]
        #     else []
        # ),
        "parent": (
            data[entity]["parent"]
            if entity in data and "parent" in data[entity]
            else None
        ),
        "order": (
            data[entity]["order"]
            if entity in data and "order" in data[entity]
            else None
        ),
        "default": (
            data[entity]["default"]
            if entity in data and "default" in data[entity]
            else None
        ),
    }

    return config
