import pytest
from time import sleep
import logging

from Infrastructure.Infra.dal.data_reposetory.data_rep import DataRep
from Infrastructure.objects.objects_api.episode_page_api import EpisodePageApi
from Infrastructure.objects.objects_ui.google_home_page_ui import GoogleHomePageUi

# Create a logger for this module
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
class TestVerifyCharacterLocation:
    """Test class to verify character locations."""

    @pytest.mark.regression
    async def test_verify_characters_location_is_the_same_ui(self, driver_fixture):
        """Verify that two randomly selected characters have the same location."""
        try:
            driver = driver_fixture

            # Fetch character details from the API
            logger.info("Fetching character details from API")
            episode_page_api = EpisodePageApi()
            character_details = await episode_page_api.randomly_choose_two_characters_pipe_async()

            # Validate character details
            assert len(character_details) == 2, "Failed to retrieve two characters"

            # Character 1 details
            character_1 = character_details[0]
            character_1_id = character_1.id
            character_1_name = character_1.name
            character_1_location = character_1.location

            logger.info(f"Character 1: {character_1_name} (ID: {character_1_id}, Location: {character_1_location})")

            # Navigate to Google Home Page and search for Character 1
            logger.info(f"Navigating to Google Home Page and searching for {character_1_name}")
            driver.get(DataRep.google_home_page_url)
            google_home_page = GoogleHomePageUi(driver)
            google_search_image_page = google_home_page.click_on_images_link()

            # Add explicit wait or retry mechanism
            sleep(2)  # Consider replacing with WebDriverWait

            google_search_image_page.set_image_name(character_1_name)
            google_images_page = google_search_image_page.click_on_search_images_button()

            # Character 2 details
            character_2 = character_details[1]
            character_2_id = character_2.id
            character_2_name = character_2.name
            character_2_location = character_2.location
            character_2_image_url = character_2.image

            logger.info(f"Character 2: {character_2_name} (ID: {character_2_id}, Location: {character_2_location})")

            # Navigate to Character 2's image URL
            logger.info(f"Navigating to Character 2's image URL: {character_2_image_url}")
            driver.get(character_2_image_url)

            # Compare locations
            if character_1_location != character_2_location:
                logger.warning(
                    f"Location mismatch - "
                    f"Character 1 location: {character_1_location} ({character_1_name}) vs "
                    f"Character 2 location: {character_2_location} ({character_2_name})"
                )
            else:
                logger.info(f"Both characters are from the same location: {character_1_location}")

            # Assert that both characters have the same location
            assert character_1_location == character_2_location, (
                f"Mismatch: Character 1 location: {character_1_location}, "
                f"Character 2 location: {character_2_location}"
            )

        except AssertionError as ae:
            logger.error(f"Assertion Error: {ae}")
            # Capture screenshot on failure
            screenshot_path = f"/app/test-results/screenshots/{self.__class__.__name__}_failure.png"
            driver_fixture.save_screenshot(screenshot_path)
            logger.error(f"Screenshot saved to {screenshot_path}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            # Capture screenshot on unexpected error
            screenshot_path = f"/app/test-results/screenshots/{self.__class__.__name__}_error.png"
            driver_fixture.save_screenshot(screenshot_path)
            logger.error(f"Screenshot saved to {screenshot_path}")
            raise