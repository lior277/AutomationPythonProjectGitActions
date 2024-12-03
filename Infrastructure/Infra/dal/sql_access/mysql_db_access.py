from typing import TypeVar, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from Infrastructure.Infra.common.common_functionality import CommonFunctionality as CF
from Infrastructure.Infra.dal.data_reposetory.data_rep import DataRep
from Infrastructure.Infra.dal.sql_access import Base, Product


class MySqlDbAccess:
    T = TypeVar('T')

    @staticmethod
    def initialize_session() -> Session:
        engine = create_engine(DataRep.mysql_connection_string)
        Base.metadata.create_all(engine)
        # Create a session
        session_temp = sessionmaker(bind=engine)
        session = session_temp()
        return session

    @staticmethod
    def select_all_rows_by_table_name(table_name: str) -> List[T]:
        class_name = CF.find_class_by_name(table_name)
        # Query all rows using the Product model
        all_rows = MySqlDbAccess.initialize_session().query(class_name).all()



print("")
