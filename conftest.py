URL_BOOKS = "https://restful-booker.herokuapp.com"

HEADERS = {

    "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="

}

data_create_method = {
    "firstname": "Michael",
    "lastname": "Astapov",
    "totalprice": 999,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2024-01-01",
        "checkout": "2025-01-01"
    },
    "additionalneeds": "Breakfast"
}

data_put_method = {
    "firstname": "James",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"
}

data_patch_method = {"firstname": "TEST NAME",
                     "lastname": "TEST SURNAME"}
