### How to secure your endpoints

1. Make sure your router is included in app.py with `JWTBearer` dependency
2. Make sure your router's route decorators have `Permissions` dependency, e.g. `@router.get("/users", response_model=User, dependencies=[Depends(Permissions("read_users"))])`
3. When implementing new routes, update `users_api/security/role_permissions.csv` accordingly. It's loaded to the database on the application startup.
4. When deploying, make sure you load the `users_api/security/role_permissions.csv` file to the database. 
