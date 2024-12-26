import pytest

from Infrastructure.Infra.utils.assert_all import AssertAll
from Infrastructure.objects.objects_api.episode_page_api import EpisodePageApi

@pytest.mark.asyncio
class TestEpisodePageApi:
    @pytest.mark.regression
    async def test_randomly_choose_two_characters_api(self):
        episode_page_api = EpisodePageApi()

        selected_characters_details: list[str] = await (episode_page_api
                                             .randomly_choose_two_characters_pipe_async())

        def check_first_character():
            assert len(selected_characters_details) == 2, \
                (f" Expected num of characters: 2"
                 f" Actual num of characters: {len(selected_characters_details)}")

            assert "Character name is:" in selected_characters_details[0], \
                (f" Expected 'Character name is:' in first character detail"
                 f" Actual detail: {selected_characters_details[0]}")

            assert "Character ID is:" in selected_characters_details[0], \
                (f" Expected 'Character ID is:' in first character detail"
                 f" Actual detail: {selected_characters_details[0]}")

            assert "Character species is:" in selected_characters_details[0], \
                (f" Expected 'Character species is:' in first character detail"
                 f" Actual detail: {selected_characters_details[0]}")

        # Function to check the second character
        def check_second_character():
            assert "Character name is:" in selected_characters_details[1], \
                (f" Expected 'Character name is:' in second character detail"
                 f" Actual detail: {selected_characters_details[1]}")

            assert "Character ID is:" in selected_characters_details[1], \
                (f" Expected 'Character ID is:' in second character detail"
                 f" Actual detail: {selected_characters_details[1]}")

            assert "Character species is:" in selected_characters_details[1], \
                (f" Expected 'Character species is:' in second character detail"
                 f" Actual detail: {selected_characters_details[1]}")

        assertions = [check_first_character, check_second_character]
        assert_all = AssertAll(assertions)
        assert_all.run()

