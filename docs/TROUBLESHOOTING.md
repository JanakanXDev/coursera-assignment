# Troubleshooting

## Application not reachable

Check the deployment and route:

```bash
oc get deployment product-catalogue -n <project>
oc get pods -n <project>
oc get route product-catalogue -n <project>
```

## Pipeline fails

Inspect the task logs:

```bash
tkn pipelinerun list -n <project>
tkn pipelinerun logs oc-pipelines-oc-green -n <project> --all
```

## Buildah permission issues

If the build fails with a security context or SCC error, grant the pipeline service account the appropriate permission as a cluster administrator.

```bash
oc adm policy add-scc-to-user privileged -z tekton-pipeline -n <project>
```

## Database or health issues

Use:

```bash
oc logs deployment/product-catalogue -n <project>
oc get pod -n <project>
```

and verify that the `/health` endpoint returns a successful HTTP response.
