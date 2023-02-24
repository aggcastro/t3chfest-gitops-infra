# Este script despliega toda la infraestructura necesaria en el clúster de k8s.

import subprocess
import sys

# Función que despliega el clúster de K8S.
def login_k8s():
    try:
        # Configuro Kubectl para el acceso al clúster.
        subprocess.run("cd terraform && gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)", shell=True, check=True)
        print("\nSe configura el acceso al clúster de k8s.\n")
    except subprocess.CalledProcessError:
        sys.exit("Ha habido un error, por favor, revisa el código y vuelve a intentarlo.") 

# Función que despliega ArgoCD.
def deploy_argocd():
    try:
        subprocess.run("kubectl create namespace argocd", shell=True, check=True)
        subprocess.run("kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml", shell=True, check=True)        
        subprocess.run("kubectl rollout -n argocd status deployment argocd-server", shell=True, check=True)
        subprocess.run("kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo", shell=True, check=True)
        # Si queremos ver el interfaz web
        # subprocess.run("kubectl port-forward svc/argocd-server -n argocd 8080:443", shell=True, check=True)
        print("\nDespliegue de argocd completado.\n")
    except subprocess.CalledProcessError:
        sys.exit("Ha habido un error, por favor, revisa el código y vuelve a intentarlo.") 
        
# Inicio el despliegue de Kubernetes y ArgoCD.
login_k8s()
deploy_argocd()