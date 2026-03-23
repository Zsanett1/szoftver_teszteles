import pytest
import datetime
from relations_manager import RelationsManager
from employee import Employee

def test_john_doe():
    rm = RelationsManager()
    john = next((emp for emp in rm.employee_list if emp.first_name == "John" and emp.last_name == "Doe"), None)
    expected_birth = datetime.date(1970, 1, 31)
    assert john is not None, "John Doe nincs az alkalmazottak kozott"
    assert john.birth_date == expected_birth, f"John Doe szuletesnapi datuma nem helyes, a valodi: {john.birth_date}"
    assert rm.is_leader(john) == True, "John Doe-nak vezetonek kell lennie"

