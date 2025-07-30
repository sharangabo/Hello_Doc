import collections.abc
import collections
collections.Callable = collections.abc.Callable

"""
Counter API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import json
from unittest import TestCase
from service.common import status  # HTTP Status Codes
from service.routes import app, reset_counters, COUNTERS_FILE


######################################################################
#  T E S T   C A S E S
######################################################################
class CounterTest(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.testing = True

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        reset_counters()
        self.app = app.test_client()

    def tearDown(self):
        """This runs after each test"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the index call"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        resp = self.app.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_counters(self):
        """It should Create a counter"""
        name = "foo"
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["name"], name)
        self.assertEqual(data["counter"], 0)

    def test_create_duplicate_counter(self):
        """It should not Create a duplicate counter"""
        name = "foo"
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["name"], name)
        self.assertEqual(data["counter"], 0)
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_list_counters(self):
        """It should List counters"""
        resp = self.app.get("/counters")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)
        # create a counter and name sure it appears in the list
        self.app.post("/counters/foo")
        resp = self.app.get("/counters")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 1)

    def test_read_counters(self):
        """It should Read a counter"""
        name = "foo"
        self.app.post(f"/counters/{name}")
        resp = self.app.get(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], name)
        self.assertEqual(data["counter"], 0)

    def test_update_counters(self):
        """It should Update a counter"""
        name = "foo"
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.app.get(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], name)
        self.assertEqual(data["counter"], 0)
        # now update it
        resp = self.app.put(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], name)
        self.assertEqual(data["counter"], 1)

    def test_update_missing_counters(self):
        """It should not Update a missing counter"""
        name = "foo"
        resp = self.app.put(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_counters(self):
        """It should Delete a counter"""
        name = "foo"
        # Create a counter
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Delete it twice should return the same
        resp = self.app.delete(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.app.delete(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Gte it to make sure it's really gone
        resp = self.app.get(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  P E R S I S T E N C E   T E S T   C A S E S
    ######################################################################

    def _get_json_file_content(self):
        """Helper to read counters.json if it exists"""
        if not os.path.exists(COUNTERS_FILE):
            return None
        with open(COUNTERS_FILE, "r", encoding="utf-8") as json_file:
            return json.load(json_file)

    def test_reset_counters_clears_file(self):
        """It should clear counters.json when reset_counters is called"""
        # Create a counter, which should create the file
        self.app.post("/counters/dummy_for_reset_test")
        self.assertTrue(os.path.exists(COUNTERS_FILE))

        # Call reset_counters (called by setUp, but we test its effect here explicitly too)
        reset_counters()
        self.assertFalse(os.path.exists(COUNTERS_FILE))

    def test_create_counter_persists_to_file(self):
        """It should persist a new counter to counters.json"""
        name = "created_counter"
        resp = self.app.post(f"/counters/{name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        file_content = self._get_json_file_content()
        self.assertIsNotNone(file_content)
        self.assertIn(name, file_content)
        self.assertEqual(file_content[name], 0)

    def test_update_counter_persists_to_file(self):
        """It should persist an updated counter to counters.json"""
        name = "updated_counter"
        self.app.post(f"/counters/{name}")  # Create it first

        resp = self.app.put(f"/counters/{name}")  # Now update it
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        file_content = self._get_json_file_content()
        self.assertIsNotNone(file_content)
        self.assertIn(name, file_content)
        self.assertEqual(file_content[name], 1)

    def test_delete_counter_persists_to_file(self):
        """It should persist changes to counters.json after deleting a counter"""
        name = "deleted_counter"
        self.app.post(f"/counters/{name}")  # Create it first

        file_content_before_delete = self._get_json_file_content()
        self.assertIn(name, file_content_before_delete)

        resp = self.app.delete(f"/counters/{name}")  # Now delete it
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        file_content_after_delete = self._get_json_file_content()
        self.assertIsNotNone(file_content_after_delete) # File should still exist if other counters are there
                                                       # or be an empty dict if it was the only one
        self.assertNotIn(name, file_content_after_delete)


    def test_load_from_preexisting_file_on_startup(self):
        """It should load counters from a preexisting counters.json on startup"""
        # Ensure no file from previous tests via reset_counters in setUp
        # Create a seed counters.json file
        seed_data = {"seed_counter_1": 10, "seed_counter_2": 20}
        with open(COUNTERS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed_data, f)

        # This is the critical part: we need to make the app reload its COUNTER
        # The simplest way in a testing context is to directly manipulate the
        # module's global variable after it has been imported.
        # We need to import the specific functions for this test.
        from service.routes import load_counters_from_file
        import service.routes as routes_module
        routes_module.COUNTER = load_counters_from_file()

        # Now the app's in-memory COUNTER should reflect the file
        resp = self.app.get("/counters/seed_counter_1")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "seed_counter_1")
        self.assertEqual(data["counter"], 10)

        resp = self.app.get("/counters/seed_counter_2")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "seed_counter_2")
        self.assertEqual(data["counter"], 20)

        # Check if a non-existent counter from the seed file is handled
        resp = self.app.get("/counters/non_seed_counter")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # Clean up: reset_counters() in the next test's setUp will handle removing the file.
