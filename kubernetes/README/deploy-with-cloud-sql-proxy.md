1. Create GCP Service Account
2. Activate Cloud SQL Admin API 
3. Create and download Service Account.

---

4. Create a Kubernetes Secret for a Service Account

```
kubectl create secret generic cloud-sql-proxy-secrets \
  --from-file=service_account.json=./key.json
```

5. Create a Kubernetes Secret for a database credentials (password is stored in GCP Secret Manager)

```
kubectl create secret generic database-credentials \
  --from-literal=db-user=users_db_user \
  --from-literal=db-password=$(gcloud secrets versions access 1 --secret=db-password) \
  --from-literal=db-name=users_db
```

6. Create Kubernetes Secret for the application:
```
kubectl create secret generic users-api-secrets \
  --from-literal=jwt-secret-key=$(gcloud secrets versions access 1 --secret=jwt-secret-key)
```

7. Create a Kubernetes configMap for the application 

```
kubectl create configmap users-api-config \
  --from-literal=jwt-algorithm=HS256 \
  --from-literal=access-token-expire-minutes="30"
```

8. Create a Kubernetes configMap for the database configuration (now only db-host is stored)

```
kubectl create configmap database-config \
    --from-literal=db-host=127.0.0.1
```


9. Create a Kubernetes configMap for the database connection name which is used by Cloud SQL Auth Proxy container:

```
kubectl create configmap cloud-sql-proxy-config \
    --from-literal=connection-name=$(gcloud sql instances describe users-db --format json | jq -r '.connectionName')
```

10. Apply the deployment

11. Run the migration
```
kubectl exec -it <POD_NAME> -c users-api -- /bin/bash -c "/scripts/migrate.sh"
```

Usefull commands:
```
kubectl get secret database-creds -o jsonpath="{.data.password}" | base64 --decode
gcloud sql instances describe users-db --format json | jq -r '.connectionName'
gcloud secrets versions access 1 --secret=db-password
```


