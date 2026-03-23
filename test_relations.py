import pytest
import datetime
from relations_manager import RelationsManager
from employee import Employee

@pytest.fixture
def manager() -> RelationsManager:
    return RelationsManager()

def test_john_doe(manager: RelationsManager):
    john : Employee | None = next(
        (emp for emp in manager.employee_list 
         if emp.first_name == 'John' and emp.last_name == 'Doe'),
         None
    )
    expected_birth = datetime.date(1970, 1, 31)

    assert john is not None, 'John Doe nem talalhato az alkalmazottak kozott'
    assert john.birth_date == expected_birth, f'Helytelen szuletesi datum, a helyes: {john.birth_date}'
    assert manager.is_leader(john) is True, "John-nak vezetonek kell lennie"

def test_team_members(manager: RelationsManager):
    john = next((emp for emp in manager.employee_list if emp.first_name == 'John' and emp.last_name == 'Doe'), None)
    team_ids: list[int] = manager.get_team_members(john)

    assert 2 in team_ids, "Myrta Torkelson-nek a csapatban kell lennie"
    assert 3 in team_ids, "Jettie Lynch-nek a csapatban kell lennie"
    assert 5 not in team_ids, "Tomas Andre-nak nem szabat a csapatban lennie"

def test_gretchen_salary(manager: RelationsManager):
    gretchen: Employee | None = next(
        (emp for emp in manager.employee_list
         if emp.first_name == 'Gretchen' and emp.last_name == 'Watford'), 
         None
    )
    expected_salary = 4000

    assert gretchen is not None, "Gretchen Watford nem talalhato az alkalmazottak kozott"
    assert gretchen.base_salary == expected_salary, (
        f"Gretchen fizetese helytelen, a helyes: {gretchen.base_salary}"
    )

def test_tomas_not_leader(manager: RelationsManager):
    tomas : Employee | None = next(
        (emp for emp in manager.employee_list 
         if emp.id == 5), None
    )

    assert tomas is not None, "Tomas Andre nem talalhato az alkalmazottak kozott"
    assert manager.is_leader(tomas) is False, "Tomas-nak nem szabad vezetonek lennie"

    team = manager.get_team_members(tomas)

    assert team is None, "Egy nem vezetonek a csapata None kellene legyen"

def test_jude_nonexistent(manager: RelationsManager):
    jude : Employee | None = next(
        (emp for emp in manager.employee_list
         if emp.first_name == "Jude" and emp.last_name == "Overcrash"),
         None
    )

    assert jude is None, "Jude Overcrash nem szabadna az adatbazisban benne legyen"