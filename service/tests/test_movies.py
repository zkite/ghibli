from asynctest import patch

from service.tests import BaseTestCase, CM, from_json, get_file_path

castle_in_the_sky_characters = [
    "Pazu",
    "Lusheeta Toel Ul Laputa",
    "Dola",
    "Romska Palo Ul Laputa",
    "Uncle Pom",
    "General Muoro",
    "Duffi",
    "Louis",
    "Charles",
    "Henri",
    "Motro",
    "Okami",
    "Colonel Muska",
]


class TestMovie(BaseTestCase):
    @patch("service.ghibli_client.films.FilmsClient.get_films", new=CM(from_json(get_file_path("films.json"))))
    @patch("service.ghibli_client.people.PeopleClient.get_people", new=CM(from_json(get_file_path("people.json"))))
    def test_get_movies_200_ok(self):
        request, response = self.app.test_client.get("/ghibli/v1/movies", headers={})
        films = response.json
        self.assertEqual(200, response.status)
        self.assertTrue(films)
        self.assertEqual("Castle in the Sky", films[0]["film"])
        self.assertListEqual(castle_in_the_sky_characters, films[0]["people"])
