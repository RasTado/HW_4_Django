import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name='Ivan')


@pytest.fixture
def course(student):
    course = Course.objects.create(name='SQL')
    course.students.add(student)
    return course


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_create_student(client, student):
    response = client.post(BASE_URL, data={'name': 'Python', 'students': [student.id]})
    assert response.json()['id'] == 32
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    course_name = 'SQL'
    url = reverse('courses-list')
    response = client.post(url, data={'name': course_name})
    assert response.status_code == 201
    answer = response.json()
    assert answer['name'] == course_name


@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    for c in courses:
        check_data = {'id': str(c.id)}
        response = client.get(url, check_data)
        assert response.status_code == 200
        data = response.json()
        assert data[0]['id'] == c.id


@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    for c in courses:
        check_data = {'name': c.name}
        response = client.get(url, check_data)
        assert response.status_code == 200
        data = response.json()
        assert data[0]['name'] == c.name


@pytest.mark.django_db
def test_update_courses(client, course_factory):
    course = course_factory(_quantity=1)
    updated_course_name = 'SQL'
    data = {'name': updated_course_name}
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])
    response = client.patch(url, data=data)
    answer = response.json()

    assert response.status_code == 200
    assert answer['name'] == updated_course_name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    delete_url = reverse('courses-detail', args=[course_id])
    response = client.delete(delete_url)
    assert response.status_code == 204
    course = Course.objects.filter(id=course_id)
    assert len(course) == 0
