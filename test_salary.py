import pytest
import datetime
from employee import Employee
from relations_manager import RelationsManager
from employee_manager import EmployeeManager
from unittest.mock import Mock, patch

@pytest.fixture
def emp() -> EmployeeManager:
    rm = RelationsManager()
    return EmployeeManager(rm)

def test_non_leader_salary(emp: EmployeeManager):
    test_employee = Employee(
        id=99,
        first_name='Teszt',
        last_name='Elek',
        base_salary=1000,
        birth_date=datetime.date(1970, 1, 1),
        hire_date=datetime.date(1998, 10, 10)
    )
    salary = emp.calculate_salary(test_employee)
    expected_years = datetime.date.today().year - 1998
    expected_salary = test_employee.base_salary + (expected_years * 100)

    assert salary == expected_salary, f"Vart fizetes: {expected_salary}, kapott: {salary}"


def test_leader_salary_with_team():
    rm = Mock()
    em = EmployeeManager(rm)
    
    leader = Employee(
        id=1,
        first_name='Vezeto',
        last_name='Ember',
        base_salary=2000,
        birth_date=datetime.date(1980, 5, 15),
        hire_date=datetime.date(2008, 10, 10)
    )
    
    team_member_1 = Employee(
        id=2,
        first_name='Csapattag',
        last_name='Elso',
        base_salary=1500,
        birth_date=datetime.date(1990, 3, 20),
        hire_date=datetime.date(2010, 1, 15)
    )
    
    team_member_2 = Employee(
        id=3,
        first_name='Csapattag',
        last_name='Masodik',
        base_salary=1500,
        birth_date=datetime.date(1991, 7, 22),
        hire_date=datetime.date(2010, 6, 1)
    )
    
    team_member_3 = Employee(
        id=4,
        first_name='Csapattag',
        last_name='Harmadik',
        base_salary=1500,
        birth_date=datetime.date(1992, 11, 10),
        hire_date=datetime.date(2011, 2, 14)
    )
    
    rm.is_leader.return_value = True
    rm.get_team_members.return_value = [team_member_1, team_member_2, team_member_3]
    
    salary = em.calculate_salary(leader)
    expected_years = datetime.date.today().year - 2008
    expected_salary = leader.base_salary + (expected_years * 100) + (3 * 200)
    
    assert salary == expected_salary, f"Vart fizetes: {expected_salary}, kapott: {salary}"


def test_salary_with_email_notification(emp: EmployeeManager):
    test_employee = Employee(
        id=99,
        first_name='Teszt',
        last_name='Elek',
        base_salary=1000,
        birth_date=datetime.date(1970, 1, 1),
        hire_date=datetime.date(1998, 10, 10)
    )
    
    with patch('builtins.print') as mock_print:
        emp.calculate_salary_and_send_email(test_employee)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert 'Teszt' in call_args
        assert 'Elek' in call_args
        assert 'salary' in call_args
    