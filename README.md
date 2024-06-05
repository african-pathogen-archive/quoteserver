### Quoteserver

This is not a server project, but rather a testbed for technologies deployed on Kubernetes.

### Deployment


To deploy the database used by quoteserver, first set up a db_values.yml file:

```
postgresqlDatabase: quoteserver
global:
  storageClass: "cinder-csi"
```

Then: 

```
helm upgrade --install quoteserver-db bitnami/postgresql -f db_values.yml -n apa
```

```
helm upgrade --install quoteserver apa/quoteserver --debug -f values.yml -n apa
```

