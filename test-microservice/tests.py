from fastapi.testclient import TestClient
from fastapi import File

from app.main import app

client = TestClient(app)

test_file1 = 'test_files/test1.csv'
test_file2 = File('/test_files/test2.xlsx')


# def test_create_upload_file():
#     response = client.post("/uploadfile/", files={"file": ("filename", open(test_file1, "rb"), "application/vnd.ms-excel")})
#     assert response.status_code == 200
#     assert response.json() == 'test1'
#
#     response2 = client.post(test_file2, names = ["'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'"], index_col = ["'A', 'C'"], header = 1)
#     assert response2.status_code == 200
#     assert response2.json() == 'test2'



def test_get_tables_names():
    response = client.get("/")
    assert response.status_code == 200
#    assert 'test1' in response.json() and 'test2' in response.json()