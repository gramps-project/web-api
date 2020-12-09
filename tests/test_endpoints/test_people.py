#
# Gramps Web API - A RESTful API for the Gramps genealogy program
#
# Copyright (C) 2020      David Straub
# Copyright (C) 2020      Christopher Horn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""Tests for the /api/people endpoints using example_gramps."""

import unittest

from . import BASE_URL, get_object_count, get_test_client
from .checks import (
    check_boolean_parameter,
    check_conforms_to_schema,
    check_invalid_semantics,
    check_invalid_syntax,
    check_keys_parameter,
    check_paging_parameters,
    check_requires_token,
    check_resource_missing,
    check_single_extend_parameter,
    check_skipkeys_parameter,
    check_sort_parameter,
    check_strip_parameter,
    check_success,
    check_totals,
)

TEST_URL = BASE_URL + "/people/"


class TestPeople(unittest.TestCase):
    """Test cases for the /api/people endpoint for a list of people."""

    @classmethod
    def setUpClass(cls):
        """Test class setup."""
        cls.client = get_test_client()

    def test_get_people_requires_token(self):
        """Test authorization required."""
        check_requires_token(self, TEST_URL)

    def test_get_people_conforms_to_schema(self):
        """Test conforms to schema."""
        check_conforms_to_schema(
            self, TEST_URL + "?extend=all&profile=all&backlinks=1", "Person"
        )

    def test_get_people_expected_results_total(self):
        """Test expected number of objects returned."""
        check_totals(self, TEST_URL + "?keys=handle", get_object_count("people"))

    def test_get_people_expected_results(self):
        """Test some expected results returned."""
        rv = check_success(self, TEST_URL)
        # check first expected record
        self.assertEqual(rv[0]["gramps_id"], "I2110")
        self.assertEqual(rv[0]["primary_name"]["first_name"], "محمد")
        self.assertEqual(rv[0]["primary_name"]["surname_list"][0]["surname"], "")
        # check last expected record
        self.assertEqual(rv[-1]["gramps_id"], "I0247")
        self.assertEqual(rv[-1]["primary_name"]["first_name"], "Allen")
        self.assertEqual(rv[-1]["primary_name"]["surname_list"][0]["surname"], "鈴木")

    def test_get_people_validate_semantics(self):
        """Test invalid parameters and values."""
        check_invalid_semantics(self, TEST_URL + "?junk_parm=1")

    def test_get_people_parameter_gramps_id_validate_semantics(self):
        """Test invalid gramps_id parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?gramps_id", check="base")

    def test_get_people_parameter_gramps_id_missing_content(self):
        """Test response for missing gramps_id object."""
        check_resource_missing(self, TEST_URL + "?gramps_id=doesnot")

    def test_get_people_parameter_gramps_id_expected_result(self):
        """Test gramps_id parameter returns expected result."""
        rv = check_success(self, TEST_URL + "?gramps_id=I0044")
        self.assertEqual(len(rv), 1)
        self.assertEqual(rv[0]["handle"], "GNUJQCL9MD64AM56OH")

    def test_get_people_parameter_strip_validate_semantics(self):
        """Test invalid strip parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?strip", check="boolean")

    def test_get_people_parameter_strip_expected_result(self):
        """Test strip parameter produces expected result."""
        check_strip_parameter(self, TEST_URL)

    def test_get_people_parameter_keys_validate_semantics(self):
        """Test invalid keys parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?keys", check="base")

    def test_get_people_parameter_keys_expected_result_single_key(self):
        """Test keys parameter for some single keys produces expected result."""
        check_keys_parameter(self, TEST_URL, ["address_list", "handle", "urls"])

    def test_get_people_parameter_keys_expected_result_multiple_keys(self):
        """Test keys parameter for multiple keys produces expected result."""
        check_keys_parameter(
            self, TEST_URL, [",".join(["address_list", "handle", "urls"])]
        )

    def test_get_people_parameter_skipkeys_validate_semantics(self):
        """Test invalid skipkeys parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?skipkeys", check="base")

    def test_get_people_parameter_skipkeys_expected_result_single_key(self):
        """Test skipkeys parameter for some single keys produces expected result."""
        check_skipkeys_parameter(self, TEST_URL, ["address_list", "handle", "urls"])

    def test_get_people_parameter_skipkeys_expected_result_multiple_keys(self):
        """Test skipkeys parameter for multiple keys produces expected result."""
        check_skipkeys_parameter(
            self, TEST_URL, [",".join(["address_list", "handle", "urls"])]
        )

    def test_get_people_parameter_page_validate_semantics(self):
        """Test invalid page parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?page", check="number")

    def test_get_people_parameter_pagesize_validate_semantics(self):
        """Test invalid pagesize parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?pagesize", check="number")

    def test_get_people_parameter_page_pagesize_expected_result(self):
        """Test page and pagesize parameters produce expected result."""
        check_paging_parameters(self, TEST_URL + "?keys=handle", 4, join="&")

    def test_get_people_parameter_soundex_validate_semantics(self):
        """Test invalid soundex parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?soundex", check="boolean")

    def test_get_people_parameter_soundex_expected_result(self):
        """Test soundex parameter produces expected result."""
        rv = check_boolean_parameter(
            self, TEST_URL + "?keys=handle,soundex", "soundex", join="&"
        )
        self.assertEqual(rv[0]["soundex"], "Z000")
        self.assertEqual(rv[244]["soundex"], "B260")

    def test_get_people_parameter_sort_validate_semantics(self):
        """Test invalid sort parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?sort", check="list")

    def test_get_people_parameter_sort_birth_ascending_expected_result(self):
        """Test sort parameter birth ascending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=+birth")
        self.assertEqual(rv[0]["handle"], "NRLKQCM1UUI9O8AMGQ")
        self.assertEqual(rv[-1]["handle"], "9BXKQC1PVLPYFMD6IX")

    def test_get_people_parameter_sort_birth_descending_expected_result(self):
        """Test sort parameter birth descending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=-birth")
        self.assertEqual(rv[0]["handle"], "9BXKQC1PVLPYFMD6IX")
        self.assertEqual(rv[-1]["handle"], "NRLKQCM1UUI9O8AMGQ")

    def test_get_people_parameter_sort_change_ascending_expected_result(self):
        """Test sort parameter change ascending result."""
        check_sort_parameter(self, TEST_URL, "change")

    def test_get_people_parameter_sort_change_descending_expected_result(self):
        """Test sort parameter change descending result."""
        check_sort_parameter(self, TEST_URL, "change", direction="-")

    def test_get_people_parameter_sort_death_ascending_expected_result(self):
        """Test sort parameter death ascending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=+death")
        self.assertEqual(rv[0]["handle"], "NRLKQCM1UUI9O8AMGQ")
        self.assertEqual(rv[-1]["handle"], "d583a5ba4be3acdd312")

    def test_get_people_parameter_sort_death_descending_expected_result(self):
        """Test sort parameter death descending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=-death")
        self.assertEqual(rv[0]["handle"], "d583a5ba4be3acdd312")
        self.assertEqual(rv[-1]["handle"], "NRLKQCM1UUI9O8AMGQ")

    def test_get_people_parameter_sort_gender_ascending_expected_result(self):
        """Test sort parameter gender ascending result."""
        check_sort_parameter(self, TEST_URL, "gender")

    def test_get_people_parameter_sort_gender_descending_expected_result(self):
        """Test sort parameter gender descending result."""
        check_sort_parameter(self, TEST_URL, "gender", direction="-")

    def test_get_people_parameter_sort_gramps_id_ascending_expected_result(self):
        """Test sort parameter gramps_id ascending result."""
        rv = check_sort_parameter(self, TEST_URL, "gramps_id")
        self.assertEqual(rv[0]["gramps_id"], "I0000")
        self.assertEqual(rv[-1]["gramps_id"], "I2156")

    def test_get_people_parameter_sort_gramps_id_descending_expected_result(self):
        """Test sort parameter gramps_id descending result."""
        rv = check_sort_parameter(self, TEST_URL, "gramps_id", direction="-")
        self.assertEqual(rv[0]["gramps_id"], "I2156")
        self.assertEqual(rv[-1]["gramps_id"], "I0000")

    def test_get_people_parameter_sort_name_ascending_expected_result(self):
        """Test sort parameter name ascending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=+name")
        self.assertEqual(rv[0]["handle"], "cc82060504445ab6deb")
        self.assertEqual(rv[-1]["handle"], "B5QKQCZM5CDWEV4SP4")

    def test_get_people_parameter_sort_name_descending_expected_result(self):
        """Test sort parameter name descending result."""
        rv = check_success(self, TEST_URL + "?keys=handle&sort=-name")
        self.assertEqual(rv[0]["handle"], "B5QKQCZM5CDWEV4SP4")
        self.assertEqual(rv[-1]["handle"], "cc82060504445ab6deb")

    def test_get_people_parameter_sort_private_ascending_expected_result(self):
        """Test sort parameter private ascending result."""
        check_sort_parameter(self, TEST_URL, "private")

    def test_get_people_parameter_sort_private_descending_expected_result(self):
        """Test sort parameter private descending result."""
        check_sort_parameter(self, TEST_URL, "private", direction="-")

    def test_get_people_parameter_sort_soundex_ascending_expected_result(self):
        """Test sort parameter soundex ascending result."""
        check_sort_parameter(self, TEST_URL + "?soundex=1", "soundex", join="&")

    def test_get_people_parameter_sort_soundex_descending_expected_result(self):
        """Test sort parameter soundex descending result."""
        rv = check_sort_parameter(
            self, TEST_URL + "?soundex=1", "soundex", join="&", direction="-"
        )
        self.assertEqual(rv[0]["soundex"], "Z565")
        self.assertEqual(rv[-1]["soundex"], "A130")

    def test_get_people_parameter_sort_surname_ascending_expected_result(self):
        """Test sort parameter surname ascending result."""
        rv = check_success(self, TEST_URL + "?keys=primary_name&sort=+surname")
        self.assertEqual(rv[0]["primary_name"]["surname_list"][0]["surname"], "Abbott")
        self.assertEqual(rv[-1]["primary_name"]["surname_list"][0]["surname"], "鈴木")

    def test_get_people_parameter_sort_surname_descending_expected_result(self):
        """Test sort parameter surname descending result."""
        rv = check_success(self, TEST_URL + "?keys=primary_name&sort=-surname")
        self.assertEqual(rv[0]["primary_name"]["surname_list"][0]["surname"], "鈴木")
        self.assertEqual(rv[-1]["primary_name"]["surname_list"][0]["surname"], "Abbott")

    def test_get_people_parameter_sort_surname_ascending_expected_result_with_locale(
        self,
    ):
        """Test sort parameter surname ascending result using different locale."""
        rv = check_success(
            self, TEST_URL + "?keys=primary_name&sort=+surname&locale=zh_CN"
        )
        self.assertEqual(rv[0]["primary_name"]["surname_list"][0]["surname"], "渡辺")
        self.assertEqual(rv[-1]["primary_name"]["surname_list"][0]["surname"], "บุญ")

    def test_get_people_parameter_sort_surname_descending_expected_result_with_locale(
        self,
    ):
        """Test sort parameter surname descending result using different locale."""
        rv = check_success(
            self, TEST_URL + "?keys=primary_name&sort=-surname&locale=zh_CN"
        )
        self.assertEqual(rv[0]["primary_name"]["surname_list"][0]["surname"], "บุญ")
        self.assertEqual(rv[-1]["primary_name"]["surname_list"][0]["surname"], "渡辺")

    def test_get_people_parameter_filter_validate_semantics(self):
        """Test invalid rules parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?filter", check="base")

    def test_get_people_parameter_filter_missing_content(self):
        """Test response when missing the filter."""
        check_resource_missing(self, TEST_URL + "?filter=ReallyNotARealFilterYouSee")

    def test_get_people_parameter_rules_validate_syntax(self):
        """Test invalid rules syntax."""
        check_invalid_syntax(self, TEST_URL + '?rules={"rules"[{"name":"IsMale"}]}')

    def test_get_people_parameter_rules_validate_semantics(self):
        """Test invalid rules parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?rules", check="base")
        check_invalid_semantics(
            self, TEST_URL + '?rules={"some":"where","rules":[{"name":"IsMale"}]}'
        )
        check_invalid_semantics(
            self, TEST_URL + '?rules={"function":"none","rules":[{"name":"IsMale"}]}'
        )

    def test_get_people_parameter_rules_missing_content(self):
        """Test rules parameter missing request content."""
        check_resource_missing(
            self, TEST_URL + '?rules={"rules":[{"name":"Mirkwood"}]}'
        )

    def test_get_people_parameter_rules_expected_response_single_rule(self):
        """Test rules parameter expected response for a single rule."""
        rv = check_success(
            self,
            TEST_URL + '?keys=gender&rules={"rules":[{"name":"HasUnknownGender"}]}',
        )
        for item in rv:
            self.assertEqual(item["gender"], 2)

    def test_get_people_parameter_rules_expected_response_multiple_rules(self):
        """Test rules parameter expected response for multiple rules."""
        rv = check_success(
            self,
            TEST_URL
            + '?keys=gender,family_list&rules={"rules":[{"name":"IsMale"},{"name":"MultipleMarriages"}]}',
        )
        for item in rv:
            self.assertEqual(item["gender"], 1)
            self.assertGreater(len(item["family_list"]), 1)

    def test_get_people_parameter_rules_expected_response_or_function(self):
        """Test rules parameter expected response for or function."""
        rv = check_success(self, BASE_URL + "/tags/")
        tag_handles = []
        for item in rv:
            if item["name"] in ["complete", "ToDo"]:
                tag_handles.append(item["handle"])
        rv = check_success(
            self,
            TEST_URL
            + '?keys=tag_list&rules={"function":"or","rules":[{"name":"HasTag","values":["complete"]},{"name":"HasTag","values":["ToDo"]}]}',
        )
        for item in rv:
            for tag in item["tag_list"]:
                self.assertIn(tag, tag_handles)

    def test_get_people_parameter_rules_expected_response_xor_function(self):
        """Test rules parameter expected response for xor function."""
        rv = check_success(
            self,
            TEST_URL
            + '?keys=gender,family_list&rules={"function":"xor","rules":[{"name":"IsFemale"},{"name":"MultipleMarriages"}]}',
        )
        for item in rv:
            if item["gender"] == 0:
                self.assertLess(len(item["family_list"]), 2)
            if len(item["family_list"]) > 1:
                self.assertNotEqual(item["gender"], 0)

    def test_get_people_parameter_rules_expected_response_one_function(self):
        """Test rules parameter expected response for one function."""
        rv = check_success(
            self,
            TEST_URL
            + '?keys=gender,family_list&rules={"function":"one","rules":[{"name":"IsFemale"},{"name":"MultipleMarriages"}]}',
        )
        for item in rv:
            if item["gender"] == 0:
                self.assertLess(len(item["family_list"]), 2)
            if len(item["family_list"]) > 1:
                self.assertNotEqual(item["gender"], 0)

    def test_get_people_parameter_rules_expected_response_invert(self):
        """Test rules parameter expected response for invert option."""
        rv = check_success(
            self,
            TEST_URL
            + '?keys=gender,family_list&rules={"invert":true,"rules":[{"name":"IsMale"},{"name":"MultipleMarriages"}]}',
        )
        for item in rv:
            if item["gender"] == 1:
                self.assertLess(len(item["family_list"]), 2)

    def test_get_people_parameter_extend_validate_semantics(self):
        """Test invalid extend parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?extend", check="list")

    def test_get_people_parameter_extend_expected_result_citation_list(self):
        """Test extend citation_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "?gramps_id=I0044", "citation_list", "citations", join="&"
        )

    def test_get_people_parameter_extend_expected_result_event_ref_list(self):
        """Test extend event_ref_list result."""
        check_single_extend_parameter(
            self,
            TEST_URL + "?gramps_id=I0044",
            "event_ref_list",
            "events",
            join="&",
            reference=True,
        )

    def test_get_people_parameter_extend_expected_result_family_list(self):
        """Test extend family_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "?gramps_id=I0044", "family_list", "families", join="&"
        )

    def test_get_people_parameter_extend_expected_result_media_list(self):
        """Test extend media_list result."""
        check_single_extend_parameter(
            self,
            TEST_URL + "?gramps_id=I0044",
            "media_list",
            "media",
            join="&",
            reference=True,
        )

    def test_get_people_parameter_extend_expected_result_notes(self):
        """Test extend notes result."""
        check_single_extend_parameter(
            self, TEST_URL + "?gramps_id=I0044", "note_list", "notes", join="&"
        )

    def test_get_people_parameter_extend_expected_result_parent_family_list(self):
        """Test extend parent_family_list result."""
        rv = check_success(
            self,
            TEST_URL
            + "?gramps_id=I0044&extend=parent_family_list&keys=parent_family_list,extended",
        )
        self.assertEqual(len(rv[0]["extended"]), 1)
        if len(rv[0]["parent_family_list"]) > 1:
            self.assertEqual(
                len(rv[0]["parent_family_list"]) - 1,
                len(rv[0]["extended"]["parent_families"]),
            )
        for item in rv[0]["extended"]["parent_families"]:
            self.assertIn(item["handle"], rv[0]["parent_family_list"])

    def test_get_people_parameter_extend_expected_result_person_ref_list(self):
        """Test extend person_ref_list result."""
        check_single_extend_parameter(
            self,
            TEST_URL + "?gramps_id=I0044",
            "person_ref_list",
            "people",
            join="&",
            reference=True,
        )

    def test_get_people_parameter_extend_expected_result_primary_parent_family(self):
        """Test extend primary_parent_family result."""
        rv = check_success(
            self,
            TEST_URL
            + "?gramps_id=I0044&extend=primary_parent_family&keys=parent_family_list,extended",
        )
        self.assertEqual(len(rv[0]["extended"]), 1)
        self.assertIn(
            rv[0]["extended"]["primary_parent_family"]["handle"],
            rv[0]["parent_family_list"],
        )

    def test_get_people_parameter_extend_expected_result_tag_list(self):
        """Test extend tag_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "?gramps_id=I0044", "tag_list", "tags", join="&"
        )

    def test_get_people_parameter_extend_expected_result_all(self):
        """Test extend all result."""
        rv = check_success(self, TEST_URL + "?gramps_id=I0044&extend=all&keys=extended")
        self.assertEqual(len(rv[0]["extended"]), 9)
        for key in [
            "citations",
            "events",
            "families",
            "media",
            "notes",
            "parent_families",
            "people",
            "primary_parent_family",
            "tags",
        ]:
            self.assertIn(key, rv[0]["extended"])

    def test_get_people_parameter_extend_expected_result_multiple_keys(self):
        """Test extend result for multiple keys."""
        rv = check_success(
            self,
            TEST_URL
            + "?gramps_id=I0044&extend=note_list,tag_list&keys=note_list,tag_list,extended",
        )
        self.assertEqual(len(rv[0]["extended"]), 2)
        self.assertIn("notes", rv[0]["extended"])
        self.assertIn("tags", rv[0]["extended"])

    def test_get_people_parameter_profile_validate_semantics(self):
        """Test invalid profile parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?profile", check="list")

    def test_get_people_parameter_profile_expected_result(self):
        """Test expected response."""
        rv = check_success(self, TEST_URL + "?page=1&profile=all")
        self.assertEqual(
            rv[0]["profile"],
            {
                "birth": {
                    "age": "0 days",
                    "date": "570-04-19",
                    "place": "",
                    "type": "Birth",
                },
                "death": {
                    "age": "62 years, 1 months, 19 days",
                    "date": "632-06-08",
                    "place": "",
                    "type": "Death",
                },
                "events": [
                    {
                        "age": "0 days",
                        "date": "570-04-19",
                        "place": "",
                        "type": "Birth",
                    },
                    {
                        "age": "62 years, 1 months, 19 days",
                        "date": "632-06-08",
                        "place": "",
                        "type": "Death",
                    },
                    {
                        "age": "39 years, 8 months, 13 days",
                        "date": "610",
                        "place": "",
                        "type": "Marriage",
                    },
                ],
                "families": [
                    {
                        "children": [],
                        "divorce": {},
                        "events": [],
                        "family_surname": "",
                        "father": {
                            "birth": {
                                "age": "0 days",
                                "date": "570-04-19",
                                "place": "",
                                "type": "Birth",
                            },
                            "death": {
                                "age": "62 years, 1 months, 19 days",
                                "date": "632-06-08",
                                "place": "",
                                "type": "Death",
                            },
                            "handle": "cc8205d872f532ab14e",
                            "gramps_id": "I2110",
                            "name_given": "محمد",
                            "name_surname": "",
                            "sex": "M",
                        },
                        "handle": "cc8205d874433c12fd8",
                        "gramps_id": "F0743",
                        "marriage": {},
                        "mother": {
                            "birth": {},
                            "death": {},
                            "handle": "cc8205d87831c772e87",
                            "gramps_id": "I2105",
                            "name_given": "عائشة",
                            "name_surname": "",
                            "sex": "F",
                        },
                        "relationship": "Married",
                    },
                    {
                        "children": [
                            {
                                "birth": {},
                                "death": {},
                                "handle": "cc8205d87fd529000ff",
                                "gramps_id": "I2107",
                                "name_given": "القاسم",
                                "name_surname": "",
                                "sex": "M",
                            },
                            {
                                "birth": {},
                                "death": {},
                                "handle": "cc8205d883763f02abd",
                                "gramps_id": "I2108",
                                "name_given": "عبد الله",
                                "name_surname": "",
                                "sex": "M",
                            },
                            {
                                "birth": {},
                                "death": {},
                                "handle": "cc8205d887376aacba2",
                                "gramps_id": "I2109",
                                "name_given": "أم كلثوم",
                                "name_surname": "",
                                "sex": "F",
                            },
                        ],
                        "divorce": {},
                        "events": [],
                        "family_surname": "",
                        "father": {
                            "birth": {
                                "age": "0 days",
                                "date": "570-04-19",
                                "place": "",
                                "type": "Birth",
                            },
                            "death": {
                                "age": "62 years, 1 months, 19 days",
                                "date": "632-06-08",
                                "place": "",
                                "type": "Death",
                            },
                            "handle": "cc8205d872f532ab14e",
                            "gramps_id": "I2110",
                            "name_given": "محمد",
                            "name_surname": "",
                            "sex": "M",
                        },
                        "gramps_id": "F0744",
                        "handle": "cc8205d87492b90b437",
                        "marriage": {},
                        "mother": {
                            "birth": {},
                            "death": {},
                            "gramps_id": "I2106",
                            "handle": "cc8205d87c20350420b",
                            "name_given": "خديجة",
                            "name_surname": "",
                            "sex": "F",
                        },
                        "relationship": "Married",
                    },
                ],
                "handle": "cc8205d872f532ab14e",
                "gramps_id": "I2110",
                "name_given": "محمد",
                "name_surname": "",
                "other_parent_families": [],
                "primary_parent_family": {},
                "sex": "M",
            },
        )

    def test_get_people_parameter_profile_expected_result_with_locale(self):
        """Test expected profile response for a locale."""
        rv = check_success(self, TEST_URL + "?page=1&profile=all&locale=de")
        self.assertEqual(rv[0]["profile"]["birth"]["age"], "0 Tage")
        self.assertEqual(rv[0]["profile"]["birth"]["type"], "Geburt")
        self.assertEqual(rv[0]["profile"]["families"][0]["relationship"], "Verheiratet")
        self.assertEqual(rv[0]["profile"]["events"][2]["type"], "Hochzeit")

    def test_get_people_parameter_backlinks_validate_semantics(self):
        """Test invalid backlinks parameter and values."""
        check_invalid_semantics(self, TEST_URL + "?backlinks", check="boolean")

    def test_get_people_parameter_backlinks_expected_result(self):
        """Test backlinks expected result."""
        rv = check_boolean_parameter(self, TEST_URL + "?page=1", "backlinks", join="&")
        self.assertIn("cc8205d874433c12fd8", rv[0]["backlinks"]["family"])
        self.assertIn("cc8205d87492b90b437", rv[0]["backlinks"]["family"])


class TestPeopleHandle(unittest.TestCase):
    """Test cases for the /api/people/{handle} endpoint for a specific person."""

    @classmethod
    def setUpClass(cls):
        """Test class setup."""
        cls.client = get_test_client()

    def test_get_people_handle_requires_token(self):
        """Test authorization required."""
        check_requires_token(self, TEST_URL + "GNUJQCL9MD64AM56OH")

    def test_get_people_handle_conforms_to_schema(self):
        """Test conforms to schema."""
        check_conforms_to_schema(
            self,
            TEST_URL + "0PWJQCZYFXOS0HGREE?extend=all&profile=all&backlinks=1",
            "Person",
        )

    def test_get_people_handle_missing_content(self):
        """Test response for missing content."""
        check_resource_missing(self, TEST_URL + "does_not_exist")

    def test_get_people_handle_expected_result(self):
        """Test response for specific person."""
        rv = check_success(self, TEST_URL + "GNUJQCL9MD64AM56OH")
        self.assertEqual(rv["gramps_id"], "I0044")
        self.assertEqual(rv["primary_name"]["first_name"], "Lewis Anderson")
        self.assertEqual(rv["primary_name"]["surname_list"][1]["surname"], "Zieliński")

    def test_get_people_handle_validate_semantics(self):
        """Test invalid parameters and values."""
        check_invalid_semantics(self, TEST_URL + "GNUJQCL9MD64AM56OH?junk_parm=1")

    def test_get_people_handle_parameter_strip_validate_semantics(self):
        """Test invalid strip parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK?strip", check="boolean"
        )

    def test_get_people_handle_parameter_strip_expected_result(self):
        """Test strip parameter produces expected result."""
        check_strip_parameter(self, TEST_URL + "1QTJQCP5QMT2X7YJDK")

    def test_get_people_handle_parameter_keys_validate_semantics(self):
        """Test invalid keys parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK?keys", check="base"
        )

    def test_get_people_handle_parameter_keys_expected_result_single_key(self):
        """Test keys parameter for some single keys produces expected result."""
        check_keys_parameter(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK", ["address_list", "handle", "urls"]
        )

    def test_get_people_handle_parameter_keys_expected_result_multiple_keys(self):
        """Test keys parameter for multiple keys produces expected result."""
        check_keys_parameter(
            self,
            TEST_URL + "1QTJQCP5QMT2X7YJDK",
            [",".join(["address_list", "handle", "urls"])],
        )

    def test_get_people_handle_parameter_skipkeys_validate_semantics(self):
        """Test invalid skipkeys parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK?skipkeys", check="base"
        )

    def test_get_people_handle_parameter_skipkeys_expected_result_single_key(self):
        """Test skipkeys parameter for some single keys produces expected result."""
        check_skipkeys_parameter(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK", ["address_list", "handle", "urls"]
        )

    def test_get_people_handle_parameter_skipkeys_expected_result_multiple_keys(self):
        """Test skipkeys parameter for multiple keys produces expected result."""
        check_skipkeys_parameter(
            self,
            TEST_URL + "1QTJQCP5QMT2X7YJDK",
            [",".join(["address_list", "handle", "urls"])],
        )

    def test_get_people_handle_parameter_soundex_validate_semantics(self):
        """Test invalid soundex parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "1QTJQCP5QMT2X7YJDK?soundex", check="boolean"
        )

    def test_get_people_handle_parameter_soundex_expected_result(self):
        """Test soundex parameter produces expected result."""
        rv = check_boolean_parameter(
            self,
            TEST_URL + "1QTJQCP5QMT2X7YJDK?keys=handle,soundex",
            "soundex",
            join="&",
        )
        self.assertEqual(rv["soundex"], "B400")

    def test_get_people_parameter_extend_validate_semantics(self):
        """Test invalid extend parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?extend", check="list"
        )

    def test_get_people_parameter_extend_expected_result_citation_list(self):
        """Test extend citation_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE", "citation_list", "citations"
        )

    def test_get_people_parameter_extend_expected_result_event_ref_list(self):
        """Test extend event_ref_list result."""
        check_single_extend_parameter(
            self,
            TEST_URL + "0PWJQCZYFXOS0HGREE",
            "event_ref_list",
            "events",
            reference=True,
        )

    def test_get_people_parameter_extend_expected_result_family_list(self):
        """Test extend family_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE", "family_list", "families"
        )

    def test_get_people_parameter_extend_expected_result_media_list(self):
        """Test extend media_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE", "media_list", "media", reference=True
        )

    def test_get_people_parameter_extend_expected_result_notes(self):
        """Test extend notes result."""
        check_single_extend_parameter(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE", "note_list", "notes"
        )

    def test_get_people_parameter_extend_expected_result_parent_family_list(self):
        """Test extend parent_family_list result."""
        rv = check_success(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?extend=parent_family_list"
        )
        self.assertEqual(len(rv["extended"]), 1)
        if len(rv["parent_family_list"]) > 1:
            self.assertEqual(
                len(rv["parent_family_list"]) - 1,
                len(rv["extended"]["parent_families"]),
            )
        for item in rv["extended"]["parent_families"]:
            self.assertIn(item["handle"], rv["parent_family_list"])

    def test_get_people_parameter_extend_expected_result_person_ref_list(self):
        """Test extend person_ref_list result."""
        check_single_extend_parameter(
            self,
            TEST_URL + "0PWJQCZYFXOS0HGREE",
            "person_ref_list",
            "people",
            reference=True,
        )

    def test_get_people_parameter_extend_expected_result_primary_parent_family(self):
        """Test extend primary_parent_family result."""
        rv = check_success(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?extend=primary_parent_family"
        )
        self.assertEqual(len(rv["extended"]), 1)
        self.assertIn(
            rv["extended"]["primary_parent_family"]["handle"], rv["parent_family_list"]
        )

    def test_get_people_parameter_extend_expected_result_tag_list(self):
        """Test extend tag_list result."""
        check_single_extend_parameter(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE", "tag_list", "tags"
        )

    def test_get_people_parameter_extend_expected_result_all(self):
        """Test extend all result."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?extend=all")
        self.assertEqual(len(rv["extended"]), 9)
        for key in [
            "citations",
            "events",
            "families",
            "media",
            "notes",
            "parent_families",
            "people",
            "primary_parent_family",
            "tags",
        ]:
            self.assertIn(key, rv["extended"])

    def test_get_people_parameter_extend_expected_result_multiple_keys(self):
        """Test extend result for multiple keys."""
        rv = check_success(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?extend=note_list,tag_list"
        )
        self.assertEqual(len(rv["extended"]), 2)
        self.assertIn("notes", rv["extended"])
        self.assertIn("tags", rv["extended"])

    def test_get_people_handle_parameter_profile_validate_semantics(self):
        """Test invalid profile parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile", check="list"
        )

    def test_get_people_handle_parameter_profile_expected_result_self(self):
        """Test profile parameter self option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=self")
        self.assertNotIn("events", rv["profile"])
        self.assertNotIn("families", rv["profile"])
        self.assertNotIn("age", rv["profile"]["birth"])
        self.assertEqual(
            rv["profile"],
            {
                "birth": {
                    "date": "1906-09-05",
                    "place": "Central City, Muhlenberg, KY, USA",
                    "type": "Birth",
                },
                "death": {
                    "date": "1993-06-06",
                    "place": "Sevierville, TN, USA",
                    "type": "Death",
                },
                "gramps_id": "I0138",
                "handle": "0PWJQCZYFXOS0HGREE",
                "name_given": "Mary Grace Elizabeth",
                "name_surname": "Warner",
                "sex": "F",
            },
        )

    def test_get_people_handle_parameter_profile_expected_result_age(self):
        """Test profile parameter age option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=age")
        self.assertNotIn("events", rv["profile"])
        self.assertNotIn("families", rv["profile"])
        self.assertIn("age", rv["profile"]["birth"])
        self.assertEqual(rv["profile"]["birth"]["age"], "0 days")

    def test_get_people_handle_parameter_profile_expected_result_families(self):
        """Test profile parameter families option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=families")
        self.assertNotIn("events", rv["profile"])
        self.assertIn("families", rv["profile"])
        self.assertNotIn("age", rv["profile"]["birth"])
        self.assertEqual(
            rv["profile"]["primary_parent_family"]["handle"], "LOTJQC78O5B4WQGJRP"
        )
        self.assertNotIn("span", rv["profile"]["primary_parent_family"]["marriage"])

    def test_get_people_handle_parameter_profile_expected_result_span(self):
        """Test profile parameter families with span option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=families,span")
        self.assertNotIn("events", rv["profile"])
        self.assertIn("families", rv["profile"])
        self.assertNotIn("age", rv["profile"]["birth"])
        self.assertEqual(
            rv["profile"]["primary_parent_family"]["handle"], "LOTJQC78O5B4WQGJRP"
        )
        self.assertIn("span", rv["profile"]["primary_parent_family"]["marriage"])
        self.assertEqual(
            rv["profile"]["primary_parent_family"]["marriage"]["span"], "0 days"
        )

    def test_get_people_handle_parameter_profile_expected_result_events(self):
        """Test profile parameter events option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=events")
        self.assertIn("events", rv["profile"])
        self.assertNotIn("families", rv["profile"])
        self.assertNotIn("age", rv["profile"]["birth"])
        self.assertEqual(
            rv["profile"]["events"][0]["place"], "Central City, Muhlenberg, KY, USA"
        )

    def test_get_people_handle_parameter_profile_expected_result_all(self):
        """Test profile parameter all option."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=all")
        for key in [
            "birth",
            "death",
            "events",
            "families",
            "handle",
            "name_given",
            "name_surname",
            "other_parent_families",
            "primary_parent_family",
            "sex",
        ]:
            self.assertIn(key, rv["profile"])

    def test_get_people_handle_parameter_profile_expected_result_with_locale(self):
        """Test expected profile response for a locale."""
        rv = check_success(self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile=all&locale=de")
        self.assertEqual(rv["profile"]["birth"]["age"], "0 Tage")
        self.assertEqual(rv["profile"]["birth"]["type"], "Geburt")
        self.assertEqual(
            rv["profile"]["primary_parent_family"]["relationship"], "Verheiratet"
        )
        self.assertEqual(rv["profile"]["events"][2]["type"], "Beerdigung")

    def test_get_people_handle_parameter_backlinks_validate_semantics(self):
        """Test invalid backlinks parameter and values."""
        check_invalid_semantics(
            self, TEST_URL + "0PWJQCZYFXOS0HGREE?profile", check="boolean"
        )

    def test_get_people_handle_parameter_backlinks_expected_result(self):
        """Test backlinks expected result."""
        rv = check_boolean_parameter(self, TEST_URL + "SOTJQCKJPETYI38BRM", "backlinks")
        self.assertEqual(
            rv["backlinks"], {"family": ["LOTJQC78O5B4WQGJRP", "UPTJQC4VPCABZUDB75"]}
        )

    def test_get_people_handle_parameter_backlinks_expected_results_extended(self):
        """Test the people handle endpoint with extended backlinks."""
        rv = check_success(
            self, TEST_URL + "SOTJQCKJPETYI38BRM?backlinks=1&extend=backlinks"
        )
        self.assertIn("backlinks", rv)
        self.assertIn("extended", rv)
        self.assertIn("backlinks", rv["extended"])
        backlinks = rv["extended"]["backlinks"]
        self.assertEqual(backlinks["family"][0]["handle"], "LOTJQC78O5B4WQGJRP")
        self.assertEqual(backlinks["family"][1]["handle"], "UPTJQC4VPCABZUDB75")
