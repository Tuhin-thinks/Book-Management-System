import traceback
import datetime
import os
import re
from dataclasses import field, dataclass
from typing import Optional, List

from colorama import Fore, Style, Back
from sqlalchemy import create_engine, Table, Column, Integer, String, UniqueConstraint, ForeignKey, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import registry, sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
# from .config import username, password
import settings
from DataLoader.ConfLoader import ConfLoader

config = ConfLoader(settings.CONFIG_FILE)
db_creds = config['db-credentials']
engine = create_engine(f"postgresql://{db_creds['db-user']}:{db_creds['db-password']}@localhost:5432/BooksManager",
                       echo=True, future=True)
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


@mapper_registry.mapped
@dataclass
class BookIndex:
    __table__ = Table(
        "BookIndex",
        mapper_registry.metadata,
        Column("book_id", Integer, ForeignKey("Books.id"), primary_key=True, unique=True),
        Column("keywords", String),
        UniqueConstraint('book_id')
    )

    book_id: int = field(init=False)
    keywords_list: List  # you can either pass keywords as a list of strings,
    keywords: Optional[str] = field(default=None)  # or you can send str with right formatting to keywords directly

    mapper_registry.metadata.create_all(engine)

    def __post_init__(self):
        if not self.keywords:
            pass
        else:
            self.keywords = "&&".join(self.keywords_list)


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
        if self.current_session:
            self.current_session.close()

    def fetch_book_byTitle(self, title: str):
        """
        Search for a specific book by title
        """
        word_filter_regex = re.compile(r"\w+", re.I)

        def match(*args):

            def to_tokens(title_str):
                """
                converts title_str in lower case tokens list
                :param title_str:
                :return:
                """
                return list(map(lambda x: x.lower().strip(), re.split(r'[\W\s]', title_str)))

            books_title, search_title = args
            # print(f"{Fore.LIGHTCYAN_EX}book_title:{books_title}, search_title:{search_title}{Style.RESET_ALL}\n")

            book_title_tokens = to_tokens(books_title)
            for word in to_tokens(search_title):
                if word in book_title_tokens:
                    pass
                elif word and word not in book_title_tokens:
                    # print(f"{Fore.LIGHTBLUE_EX}{word} not in {book_title_tokens}{Style.RESET_ALL}")
                    return False

            # print(f"{Fore.GREEN}Match found")
            return books_title

        try:
            self.current_session = self.session_maker()
            self.current_session: Session

            # match_validation = lambda Books_title, s_title: all([True if word in word_filter_regex.findall(Books_title)
            #                                                      else False
            #                                                      for word in word_filter_regex.findall(s_title)])

            fetch_res = self.current_session.execute(select(Books.title)).fetchall()  # fetch all available titles from db
            matched = list()
            for res in fetch_res:
                match_res = match(res[0], title)
                if match_res:
                    matched.append(match_res)
            self.close_session()
            return matched
        finally:
            self.close_session()


if __name__ == '__main__':
    books_manager = ManageBooks()

    """
    TEMP: ADDING...
    """
    inp = input("Want to add new books?")
    if inp.lower() == 'yes':
        allowed_extensions = [".pdf", '.epub', "djvu"]
        folder_name = input("Enter location to search for the books:")  # "~/Downloads/Books"
        for root, dir_name, files in os.walk(os.path.expanduser(folder_name)):
            for file in files:
                ext = os.path.splitext(file)[-1]
                if ext.lower() in allowed_extensions:
                    try:
                        books_manager.add_book(title=os.path.basename(file))
                        print(f"{Fore.GREEN}Added book :{file}{Style.RESET_ALL}")
                    except IntegrityError:
                        print(f"{Fore.LIGHTBLUE_EX}[-] SKIPPED BOOK :{file}{Style.RESET_ALL}")
                        pass  # skip rows with duplicate values

    """
    TEMP: Searching...
    """
    os.system('clear')
    try:
        while True:
            book_title = input("Search book title:")
            if book_title == 'over':
                print(f"{Fore.BLUE}Exiting...{Style.RESET_ALL}")
                break  # exit the program
            try:
                results = books_manager.fetch_book_byTitle(book_title)
                os.system('clear')
                print(16 * "---")
                for nr, result in enumerate(results, 1):
                    print(f"{nr}. {Fore.LIGHTCYAN_EX}{result}{Style.RESET_ALL}")
                print(16 * "---")
            except Exception as e:
                print(Fore.LIGHTRED_EX)
                traceback.print_exc()
                print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}\nExiting...{Style.RESET_ALL}")
        os.system('clear')
        print("done!")
