# loggen Helm Chart

This Helm chart deploys the `loggen` log generator application with best security and production practices.

## Usage

Add the Helm repository (GitHub Pages):

```sh
helm repo add loggen https://smana.github.io/loggen/helm/loggen
helm repo update
```

Install the chart:

```sh
helm install loggen loggen/loggen
```

Upgrade the release:

```sh
helm upgrade loggen loggen/loggen
```

Uninstall the release:

```sh
helm uninstall loggen
```

## Configuration

See `values.yaml` for all configurable options, including:

- `replicaCount`: Number of pod replicas
- `image.repository` and `image.tag`: Container image settings
- `resources`: CPU/memory requests and limits
- `securityContext` and `containerSecurityContext`: Pod/container security settings
- `affinity`, `tolerations`, `topologySpreadConstraints`: Advanced scheduling
- `serviceAccount.create`, `serviceAccount.name`: ServiceAccount management
- `podDisruptionBudget`: PDB settings
- `service`: Service type and port

### Example: Override values

```sh
helm install loggen ./helm/loggen \
  --set replicaCount=3 \
  --set image.tag=v0.2.0 \
```

## Security

This chart applies the following security best practices:

- Runs as a non-root user (UID/GID 10001)
- Disables privilege escalation
- Drops all Linux capabilities
- Uses a read-only root filesystem

You can further customize security settings in `values.yaml` as needed.

## Advanced Scheduling

- **affinity**: Control pod placement (e.g., anti-affinity, node affinity)
- **tolerations**: Allow scheduling on tainted nodes
- **topologySpreadConstraints**: Distribute pods across zones/nodes

## PodDisruptionBudget

Enable and configure a PDB to ensure high availability during voluntary disruptions.

---

This project is licensed under the Apache-2.0 License.
