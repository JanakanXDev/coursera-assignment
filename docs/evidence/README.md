# Evidence

This folder documents the validation performed for the course project.

## PVC validation commands

```bash
oc get storageclass skills-network-learner
oc apply -f openshift/pvc.yaml
oc get pvc oc-pipelines-pvc
oc describe pvc oc-pipelines-pvc
```

Check that:

- The storage class is `skills-network-learner`.
- The requested size is `1Gi`.
- The status is `Bound`.

If an existing `oc-pipelines-pvc` claim has different settings, verify whether it contains important data before deleting or recreating it.

## Local validation

- `flake8 app tests` for lint validation
- `nosetests -v tests` for unit test execution
- Docker build verification via `docker build .`

Keep the generated logs and output in the CI/CD evidence folder when using a grading environment.
