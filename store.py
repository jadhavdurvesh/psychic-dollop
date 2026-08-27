from typing import List
from models import Link

class Store:
    def __init__(self):
        # In‑memory storage; in a real app this would be a DB.
        self._links: List[Link] = []

    def add_link(self, original_url: str, short_code: str) -> Link:
        link = Link(original_url=original_url, short_code=short_code)
        self._links.append(link)
        return link

    def get_link_by_code(self, short_code: str) -> Link | None:
        for link in self._links:
            if link.short_code == short_code:
                return link
        return None

    def get_all_links(self) -> List[Link]:
        """Return all stored Link objects without any particular ordering."""
        return list(self._links)

    def get_all_links_sorted(self) -> List[Link]:
        """
        Return all stored Link objects ordered by click_count descending.
        """
        # Sort by click_count descending; ties preserve insertion order.
        return sorted(self._links, key=lambda l: l.click_count, reverse=True)

    # Existing helper methods (e.g., increment_click, delete_link) would go here.