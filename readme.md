mkdir BACKOFFICE
cd BACKOFFICE
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

docker-compose up -d
docker ps


Checklist Login Staff:

Endpoint POST /api/staff/login implementado en FastAPI.
Validación de staffId + pin.
Retorno de datos correctos (staffId, displayName, role, gateId?, zoneCheckpointId?).
Probado con PowerShell (Invoke-RestMethod) → vimos que responde 200 OK y 401 Unauthorized en los casos correctos.
(Pendiente, pero opcional ahora) Hash de PINs con bcrypt.