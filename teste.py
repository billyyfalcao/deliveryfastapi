import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzg1MTcwMzg0fQ.M0WsMuI_MHOG2seIWLLCw8IWrkJkK0LmYdmM0eCWJHY"
}

requisicao = requests.get ("http://127.0.0.1:8000/auth/refresh", headers=headers)
print (requisicao)
print (requisicao.json())