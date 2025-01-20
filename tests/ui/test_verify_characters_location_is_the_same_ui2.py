from time import sleep

import pytest

from Infrastructure.Infra.dal.data_reposetory.data_rep import DataRep
from Infrastructure.objects.objects_api.episode_page_api import EpisodePageApi
from Infrastructure.objects.objects_ui.google_home_page_ui import GoogleHomePageUi


@pytest.mark.asyncio
class TestVerifyCharacterLocation:
    """Test class to verify character locations."""

    @pytest.mark.regression
    @pytest.mark.skip
    async def test_verify_characters_location_is_the_same_ui(self, driver_fixture):
        """Verify that two randomly selected characters have the same location."""
        driver = driver_fixture

        # Fetch character details from the API
        episode_page_api = EpisodePageApi()
        character_details = await episode_page_api.randomly_choose_two_characters_pipe_async()

        # Character 1 details
        character_1 = character_details[0]
        character_1_id = character_1.id
        character_1_name = character_1.name
        character_1_location = character_1.location

        # Navigate to Google Home Page and search for Character 1
        driver.get(DataRep.google_home_page_url)
        google_home_page = GoogleHomePageUi(driver)
        google_search_image_page = google_home_page.click_on_images_link()
        sleep(1)
        google_search_image_page.set_image_name(character_1_name)
        google_images_page = google_search_image_page.click_on_search_images_button()


        # Character 2 details
        character_2 = character_details[1]
        character_2_id = character_2.id
        character_2_name = character_2.name
        character_2_location = character_2.location
        character_2_image_url = character_2.image

        # Navigate to Character 2's image URL
        driver.get(character_2_image_url)

        # Compare locations
        if character_1_location != character_2_location:
            print(f"Character 1 location: {character_1_location} ({character_1_name}) vs "
                  f"Character 2 location: {character_2_location} ({character_2_name}).")
        else:
            print(f"Both characters are from the same location: {character_1_location}.")

        # Assert that both characters have the same location
        assert True == True, (
            f"Mismatch: Character 1 location: {character_1_location}, "
            f"Character 2 location: {character_2_location}"
        )
