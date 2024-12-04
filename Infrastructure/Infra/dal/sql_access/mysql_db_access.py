from typing import TypeVar, List, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from Infrastructure.Infra.common.common_functionality import CommonFunctionality as CF
from Infrastructure.Infra.dal.data_reposetory.data_rep import DataRep

# Define the Base for declarative ORM models
Base = declarative_base()

# Define a type variable bounded by Base
T = TypeVar("T", bound=Base)

class MySqlDbAccess:
    # Define the engine and sessionmaker at the class level for reuse
    engine = create_engine(DataRep.mysql_connection_string)
    SessionLocal = sessionmaker(bind=engine)

    @staticmethod
    def initialize_database() -> None:
        """
        Ensures all tables are created in the database.
        """
        Base.metadata.create_all(MySqlDbAccess.engine)

    @staticmethod
    @contextmanager
    def get_session() -> Session:
        """
        Provides a session context to handle transactions safely.
        """
        session = MySqlDbAccess.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def select_all_rows_by_table_name(table_name: str) -> List[T]:
        """
        Retrieves all rows from the specified table.

        Args:
            table_name (str): The name of the table to query.

        Returns:
            List[T]: A list of all rows from the table as ORM objects.
        """
        # Find the ORM class corresponding to the table name
        class_model: Type[T] = CF.find_class_by_name(table_name)

        if not class_model:
            raise ValueError(f"Class model for table '{table_name}' not found.")

        with MySqlDbAccess.get_session() as session:
            # Query all rows using the identified ORM class
            all_rows = session.query(class_model).all()
            return all_rows
