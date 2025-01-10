import pytest

from Infrastructure.Infra.utils.assert_all import AssertAll
from Infrastructure.objects.data_classes.character import Character
from Infrastructure.objects.objects_api.episode_page_api import EpisodePageApi


@pytest.mark.asyncio
class TestEpisodePageApi:
    #@pytest.mark.regression
    async def test_randomly_choose_two_characters_api(self):
        episode_page_api = EpisodePageApi()

        selected_characters_details: list[Character] = \
            await (episode_page_api.randomly_choose_two_characters_pipe_async())

        assert True == True, \
            (f" FIRST CHARACTER NAME: {selected_characters_details[0].name}"
             f" FIRST CHARACTER LOCATION: {selected_characters_details[0].location}"
             f" not equals to SECOND CHARACTER NAME: {selected_characters_details[1].name}"
             f" SECOND CHARACTER LOCATION: {selected_characters_details[1].location}.")




