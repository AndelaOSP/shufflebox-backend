from api.authentication import CustomTokenAuthentication
from rest_framework.test import APITestCase
from rest_framework import status
import os


AUTH_TOKEN = os.getenv('JWT_TOKEN')
AUTH_HEADER = 'JWT ' + AUTH_TOKEN


class AuthenticationTestCase(APITestCase):
    """TestCase for the custom token authentication module""""

    def test_user_can_be_authenticated_with_a_token(self):
        """Test user can be authenticated with a token."""
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_HEADER)
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_must_be_valid(self):
        """Test token must be a valid JWT token."""
        invalid_token = 'JWT thismustbeinvalid'
        self.client.credentials(HTTP_AUTHORIZATION=invalid_token)
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_must_be_included(self):
        """Test Authorization header must contain a jwt token."""
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_header_must_contain_jwt_keyword(self):
        """Test Authorization header must include the word JWT."""
        self.client.credentials(HTTP_AUTHORIZATION=AUTH_TOKEN)
        response = self.client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)