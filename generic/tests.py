from rest_framework.test import APITestCase
from rest_framework import status


class RouterEndpointsTestCase(APITestCase):
    def test_message_viewset(self):
        response = self.client.get("/messages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sm_account_viewset(self):
        response = self.client.get("/sm-accounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_viewset(self):
        response = self.client.get("/companies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_agency_viewset(self):
        response = self.client.get("/agencies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_viewset(self):
        response = self.client.get("/projects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genai_viewset(self):
        response = self.client.get("/gen-ai/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_role_viewset(self):
        response = self.client.get("/employee-roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_viewset(self):
        response = self.client.get("/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itinerary_viewset(self):
        response = self.client.get("/itineraries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_itinerary_history_viewset(self):
        response = self.client.get("/itinerary-histories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
