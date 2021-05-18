import sqlalchemy.exc
from colorama import Fore, Back, Style
import datetime
import logging
import os
from dataclasses import dataclass
from dataclasses import field
from typing import List, Optional

from sqlalchemy import create_engine, Table, Column, Integer, String, log, UniqueConstraint
from sqlalchemy.orm import registry, sessionmaker, Session, configure_mappers
from sqlalchemy_utils import database_exists, create_database
# from .config import username, password
from config import username, password

engine = create_engine(f"postgresql://{username}:{password}@localhost:5432/BooksManager", echo=True, future=True)
if not database_exists(engine.url):
    create_database(engine.url)
mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Books:
    __table__ = Table(
        "Books",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("title", String, unique=True),
        Column("ISBN", String(30), unique=True),
        Column("date_added", String),
        UniqueConstraint("title", "ISBN")
    )

    id: int = field(init=False)
    title: str
    ISBN: Optional[str] = field(init=False)
    date_added: Optional[str] = datetime.datetime.today().date().isoformat()  # '2021-05-19'

    mapper_registry.metadata.create_all(engine)


class ManageBooks:
    session_maker = sessionmaker()

    def __init__(self):
        self.create_session()
        self.current_session = None

    def create_session(self):
        self.session_maker.configure(bind=engine)

    def add_book(self, **kwargs):
        """
        :param kwargs: (title, ISBN)
        :return:
        """

        # create book instance
        book = Books(**kwargs)

        try:
            self.current_session = self.session_maker()
            self.current_session.add(book)
            self.current_session.commit()
        finally:
            self.close_session()

    def close_session(self):
        self.current_session.close()


if __name__ == '__main__':
    books_manager = ManageBooks()

    allowed_extensions = [".pdf", '.epub', "djvu"]
    folder_name = "~/Downloads/Books"
    for root, dir_name, files in os.walk(os.path.expanduser(folder_name)):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext.lower() in allowed_extensions:
                try:
                    books_manager.add_book(title=os.path.basename(file))
                    print(f"{Fore.GREEN}Added book :{file}{Style.RESET_ALL}")
                except sqlalchemy.exc.IntegrityError:
                    print(f"{Fore.LIGHTBLUE_EX}[-] SKIPPED BOOK :{file}{Style.RESET_ALL}")
                    pass  # skip rows with duplicate values
