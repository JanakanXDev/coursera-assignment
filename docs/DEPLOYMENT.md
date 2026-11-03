# Deployment Guide

This project is designed to run as a Flask REST API inside OpenShift using port 8080.

## OpenShift project and namespace

Use `oc project` to inspect or switch namespaces:

```bash
oc project
oc project <namespace>
```

If you run more than one project, confirm the active namespace with:

```bash
oc project -q
```

## Applying resources

```bash
oc apply -f openshift/pvc.yaml -n <project>
oc apply -f openshift/rbac.yaml -n <project>
oc apply -f openshift/deployment.yaml -n <project>
oc apply -f openshift/service.yaml -n <project>
oc apply -f openshift/route.yaml -n <project>
```

## Tekton pipeline workspace

The shared pipeline workspace is backed by the `oc-pipelines-pvc` claim. Validate it before running the pipeline:

```bash
oc get pvc oc-pipelines-pvc -n <project>
oc describe pvc oc-pipelines-pvc -n <project>
```

## Image updates

The Tekton buildah task pushes the image to the OpenShift internal registry. Update the deployment by setting the image in the Deployment manifest or by allowing the `deploy` Tekton task to update it.

## Buildah permissions

On restricted OpenShift clusters, the pipeline service account may need a privileged SCC. The cluster administrator can grant it with:

```bash
oc adm policy add-scc-to-user privileged -z tekton-pipeline -n <project>
```

This is required only when the Buildah task runs in privileged mode.
