import yaml
from kubernetes import config
from openshift.dynamic import DynamicClient


DNS_SUFFIX = "192.168.42.25.nip.io"

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)


def create_deploy(ns, app, image, rep):
    v1_services = dyn_client.resources.get(api_version='v1', kind='Deployment')
    deployment = f"""
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: {app['name']}
    spec:
      selector:
        matchLabels:
          app: {app.label}
      replicas: {rep} # tells deployment to run 2 pods matching the template
      template:
        metadata:
          labels:
            app: {app.label}
        spec:
          containers:
          - name: {image.name}
            image: {image.name}:{image.ver}
            ports:
            - containerPort: {app['port']}
    """
    dep_data = yaml.load(deployment)
    v1_services.create(body=dep_data, namespace=ns)


def create_image_stream(namespace, app_name):
    client = dyn_client.resources.get(api_version='image.openshift.io/v1', kind='ImageStream')
    image_stream = f"""
    apiVersion: image.openshift.io/v1
    kind: ImageStream
    metadata:
      creationTimestamp: null
      name: s2i-{app_name}-container
    spec:
      lookupPolicy:
        local: false
    status:
      dockerImageRepository: ""
    """
    data = yaml.load(image_stream)
    client.create(body=data, namespace=namespace)


def create_build_conf(namespace, app_name, source, builder):
    build_conn = dyn_client.resources.get(api_version='build.openshift.io/v1', kind='BuildConfig')
    build_config = f"""
  apiVersion: build.openshift.io/v1
  kind: BuildConfig
  metadata:
    annotations:
      openshift.io/generated-by: HakunahMatata
    labels:
      app: s2i-{app_name}-container
      app.kubernetes.io/component: s2i-{app_name}-container
      app.kubernetes.io/instance: s2i-{app_name}-container
    name: s2i-{app_name}-container
  spec:
    output:
      to:
        kind: ImageStreamTag
        name: s2i-{app_name}-container:latest
    source:
      git:
        uri: {source}
      type: Git
    strategy:
      sourceStrategy:
        from:
          kind: ImageStreamTag
          name: {builder}
          namespace: openshift
      type: Source
    triggers:
    - github:
        secret: "oiehat385ok24jbGewlkb!"
      type: GitHub
    - type: ConfigChange
    - imageChange: {{}}
      type: ImageChange
    """
    build_data = yaml.load(build_config)
    print(build_data)
    build_conn.create(body=build_data, namespace=namespace)


def create_deployment_conf(namespace, app_name, replicas=1, port=8080):
    build_conn = dyn_client.resources.get(api_version='apps.openshift.io/v1', kind='DeploymentConfig')
    build_config = f"""
  apiVersion: apps.openshift.io/v1
  kind: DeploymentConfig
  metadata:
    annotations:
      openshift.io/generated-by: OpenShiftNewApp
    creationTimestamp: null
    labels:
      app: s2i-{app_name}-container
      app.kubernetes.io/component: s2i-{app_name}-container
      app.kubernetes.io/instance: s2i-{app_name}-container
    name: s2i-{app_name}-container
  spec:
    replicas: {replicas}
    selector:
      deploymentconfig: s2i-{app_name}-container
    strategy:
      resources: {{}}
    template:
      metadata:
        annotations:
          openshift.io/generated-by: OpenShiftNewApp
        creationTimestamp: null
        labels:
          deploymentconfig: s2i-{app_name}-container
      spec:
        containers:
        - image: s2i-{app_name}-container:latest
          name: s2i-{app_name}-container
          ports:
          - containerPort: {port}
            protocol: TCP
            name: exposed
          resources: {{}}
    test: false
    triggers:
    - type: ConfigChange
    - imageChangeParams:
        automatic: true
        containerNames:
        - s2i-{app_name}-container
        from:
          kind: ImageStreamTag
          name: s2i-{app_name}-container:latest
      type: ImageChange
        """
    dep_conf = yaml.load(build_config)
    build_conn.create(body=dep_conf, namespace=namespace)


def create_service(namespace, app_name, port):
    services = dyn_client.resources.get(api_version='v1', kind='Service')
    spec = f"""
  apiVersion: v1
  kind: Service
  metadata:
    annotations:
      openshift.io/generated-by: OpenShiftNewApp
    creationTimestamp: null
    labels:
      app: s2i-{app_name}-container
      app.kubernetes.io/component: s2i-{app_name}-container
      app.kubernetes.io/instance: s2i-{app_name}-container
    name: s2i-{app_name}-container
  spec:
    ports:
    - name: exposed
      port: {port}
      protocol: TCP
      targetPort: {port}
    selector:
      deploymentconfig: s2i-{app_name}-container
    """
    service_data = yaml.load(spec)
    services.create(body=service_data, namespace=namespace)


def create_route(namespace, app_name):
    client = dyn_client.resources.get(api_version='route.openshift.io/v1', kind='Route')
    route = f"""
    apiVersion: route.openshift.io/v1
    kind: Route
    metadata:
      annotations:
      labels:
        app: s2i-{app_name}-container
        app.kubernetes.io/component: s2i-{app_name}-container
        app.kubernetes.io/instance: s2i-{app_name}-container
      name: s2i-{app_name}-container
    spec:
      host: {app_name}-{namespace}.{DNS_SUFFIX}
      port:
        targetPort: exposed
      to:
        kind: Service
        name: s2i-{app_name}-container
    """
    data = yaml.load(route)
    client.create(body=data, namespace=namespace)


def create_s2i(name, source, port):
    namespace = "myproject"
    builder = "python:3.6"

    create_image_stream(namespace=namespace, app_name=name)
    create_build_conf(namespace=namespace, app_name=name, source=source, builder=builder)
    create_deployment_conf(namespace=namespace, app_name=name, port=port)
    create_service(namespace=namespace, app_name=name, port=port)
    create_route(namespace=namespace, app_name=name)
