import random
import asyncio
from typing import List

from Infrastructure.Infra.dal.data_reposetory.data_rep import DataRep
from Infrastructure.objects.data_classes.character import Character
from Infrastructure.objects.data_classes.episode_response import EpisodeResponse, Episode
from Infrastructure.Infra.dal.api_access.api_accsess import ApiAccess

class EpisodePageApi:

    def __init__(self) -> None:
        self.api_access = ApiAccess()

    async def get_all_episodes(self, url: str) -> EpisodeResponse:
        data = await self.api_access.execute_get_request_async(url)
        episodes = [Episode(**episode) for episode in data['results']]
        return EpisodeResponse(results=episodes, info=data['info'])

    async def fetch_character_details(self, url: str) -> Character:
        character_data = await self.api_access.execute_get_request_async(url)

        character = Character(
            id=character_data['id'],
            name=character_data['name'],
            status=character_data.get('status', 'unknown'),
            species=character_data.get('species', 'unknown'),
            location=character_data['location']['name'] if 'location' in character_data else None,
            gender=character_data.get('gender', 'unknown'),
            origin=character_data.get('origin', 'unknown'),
            image=character_data.get('image', 'unknown'),
            episode=character_data.get('episode', []),
            url=character_data.get('url', 'unknown'),
            created=character_data.get('created', 'unknown')
        )
        return character

    async def fetch_all_characters_async(self, selected_character_urls: List[str]) -> List[Character]:
        tasks = [self.fetch_character_details(url) for url in selected_character_urls]
        return await asyncio.gather(*tasks)

    @staticmethod
    def select_random_characters(characters: List[Character], num: int = 2) -> List[Character]:
        return random.sample(characters, num)

    @staticmethod
    def get_character_details(characters: List[Character]) -> List[str]:
        return [
            f"Character name is: {character.name}, Character ID is: {character.id}, "
            f"Character location is: {character.location}, Character status is: {character.status}, "
            f"Character species is: {character.species}."
            for character in characters
        ]

    @staticmethod
    def write_character_details_to_file(characters: List[Character], filename: str = "characters_introduction.txt") -> None:
        with open(filename, "w") as file:
            for character in characters:
                file.write(f"Character name is: {character.name}, Character ID is: {character.id}, "
                           f"Character location is: {character.location}, Character status is: {character.status}, "
                           f"Character species is: {character.species}.\n")

    @staticmethod
    def print_character_details(characters: List[Character]) -> None:
        for character in characters:
            print(f"Character name is: {character.name}, Character ID is: {character.id}, "
                  f"Character location is: {character.location}, Character status is: {character.status}, "
                  f"Character species is: {character.species}.")

    async def get_episode_urls_async(self) -> List[str]:
        episode_url = f"{DataRep.rick_and_morty_base_url}episode"
        data = await self.api_access.execute_get_request_async(episode_url)
        episode_urls = [episode['url'] for episode in data['results'][:2]]

        return episode_urls

    async def get_selected_character_urls_async(self, episode_urls: List[str]) -> List[str]:
        selected_character_urls = []
        for episode_url in episode_urls:
            episode_data = await self.api_access.execute_get_request_async(episode_url)
            character_urls = episode_data.get('characters', [])
            selected_character_urls.extend(character_urls)

        return selected_character_urls

    async def randomly_choose_two_characters_pipe_async(self) -> List[Character]:
        episode_urls = await self.get_episode_urls_async()
        selected_character_urls = await self.get_selected_character_urls_async(episode_urls)
        characters = await self.fetch_all_characters_async(selected_character_urls)
        selected_characters = self.select_random_characters(characters)
        self.print_character_details(selected_characters)
        self.write_character_details_to_file(selected_characters)

        return selected_characters

