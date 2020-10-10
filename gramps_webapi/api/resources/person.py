"""Person API resource."""

import gramps.gen.filters.rules.person as rule_classes

from .base import (GrampsObjectProtectedResource, GrampsObjectResourceHelper,
                   GrampsObjectsProtectedResource)
from .filter import apply_filter_rules, list_filter_rules
from .util import (get_events_for_references, get_family_by_handle,
                   get_media_for_references, get_people_for_references,
                   get_person_profile_for_object)


class PersonResourceHelper(GrampsObjectResourceHelper):
    """Person resource helper."""

    gramps_class_name = "Person"

    def object_extend(self, obj):  # pylint: disable=no-self-use
        """Extend person attributes as needed."""
        db = self.db
        if self.build_profile:
            obj.profile = get_person_profile_for_object(
                db, obj, with_family=True, with_events=True
            )
        if self.extend_object:
            obj.extended = {
                "citations": [
                    db.get_citation_from_handle(handle) for handle in obj.citation_list
                ],
                "events": get_events_for_references(db, obj),
                "families": [
                    get_family_by_handle(db, handle) for handle in obj.family_list
                ],
                "parent_families": [
                    get_family_by_handle(db, handle)
                    for handle in obj.parent_family_list
                ],
                "primary_parent_family": get_family_by_handle(
                    db, obj.get_main_parents_family_handle()
                ),
                "media": get_media_for_references(db, obj),
                "notes": [db.get_note_from_handle(handle) for handle in obj.note_list],
                "people": get_people_for_references(db, obj),
                "tags": [db.get_tag_from_handle(handle) for handle in obj.tag_list],
            }
        return obj

    def object_filter_rules(self):
        """Build and return list of filter rules."""
        return list_filter_rules(rule_classes)

    def object_filter(self, args):
        """Build and apply a filter."""
        db = self.db
        return apply_filter_rules(db, args, rule_classes)


class PersonResource(GrampsObjectProtectedResource, PersonResourceHelper):
    """Person resource."""


class PeopleResource(GrampsObjectsProtectedResource, PersonResourceHelper):
    """People resource."""
