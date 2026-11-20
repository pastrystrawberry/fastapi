import bcrypt
from security import hash_password, verify_password
password="@Captain@123"
hashed="$2b$12$ah23UQD0LmwSt699RIvzkeZZNy7uKvbYzdyM4uiCAz8TAmGvB1hEu"
print("original:",password)
print("hashed:",hashed)
print(verify_password(password,hashed))
print(verify_password("dsfdsfsdg",hashed))
