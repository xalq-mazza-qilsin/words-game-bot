from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, telegram_id):
        sql = "INSERT INTO users (full_name, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, full_name, telegram_id, fetchrow=True)

    async def add_game(self, user, status, chat_type, word):
        sql = "INSERT INTO games (user_id, status, chat_type, word_id) VALUES ($1, $2, $3, $4) returning *"
        return await self.execute(sql, user, status, chat_type, word, fetchrow=True)

    async def add_guessed_letter(self, game_id, guessed_letters):
        sql = "INSERT INTO guessed_letters (game_id, guessed_letters) VALUES ($1, $2) returning *"
        return await self.execute(sql, game_id, guessed_letters, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_words(self):
        sql = "SELECT * FROM words"
        return await self.execute(sql, fetch=True)

    async def select_user_games(self, user_id):
        sql = "SELECT * FROM games WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_word(self, **kwargs):
        sql = "SELECT * FROM words WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_guessed_letter(self, **kwargs):
        sql = "SELECT * FROM guessed_letters WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_guessed_letter(self, guessed_letters, game_id):
        sql = "UPDATE guessed_letters SET guessed_letters=$1 WHERE game_id=$2"
        return await self.execute(sql, guessed_letters, game_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
