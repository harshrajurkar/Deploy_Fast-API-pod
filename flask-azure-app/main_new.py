from fastapi import FastAPI
from kubernetes import client, config
from prometheus_client import PrometheusClient

app = FastAPI()

# Load Kubernetes config
config.load_kube_config()

# Initialize Prometheus client
prom = PrometheusClient()

@app.post("/createDeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    apps_v1 = client.AppsV1Api()
    
    # Define the deployment
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector={'matchLabels': {'app': deployment_name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': deployment_name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name=deployment_name,
                        image="nginx",  # Example image
                        ports=[client.V1ContainerPort(container_port=80)]
                    )]
                )
            )
        )
    )
    
    # Create the deployment
    apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    return {"message": f"Deployment {deployment_name} created"}

@app.get("/getPromdetails")
async def get_prom_details():
    response = prom.get('http://prometheus-server.default.svc.cluster.local/api/v1/query?query=kube_pod_info')
    return response.json()



#################################################################

from fastapi import FastAPI
from kubernetes import client, config
import requests

app = FastAPI()

# Load Kubernetes config
config.load_kube_config()

@app.post("/createDeployment/{deployment_name}")
async def create_deployment(deployment_name: str):
    apps_v1 = client.AppsV1Api()
    
    # Define the deployment
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={'app': deployment_name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': deployment_name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name=deployment_name,
                        image="nginx",  # Example image
                        ports=[client.V1ContainerPort(container_port=80)]
                    )]
                )
            )
        )
    )
    
    # Create the deployment
    apps_v1.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    return {"message": f"Deployment {deployment_name} created"}

@app.get("/getPromdetails")
async def get_prom_details():
    prometheus_url ='http://prometheus-operated.monitoring.svc.cluster.local:9090/api/v1/query?query=kube_pod_info'
    response = requests.get(prometheus_url)
    return response.json()
