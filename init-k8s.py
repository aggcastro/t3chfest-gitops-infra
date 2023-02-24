# Este script despliega toda la infraestructura necesaria en el clúster de k8s.

import subprocess
import sys

# Función que despliega el clúster de K8S.
def deploy_k8s():
    try:
        subprocess.run("cd terraform && terraform init", shell=True, check=True)
        subprocess.run("cd terraform && terraform validate", shell=True, check=True)
        subprocess.run('cd terraform && echo "yes" | terraform apply', shell=True, check=True)
        print("\nDespliegue del clúster terminado.\n")

        # Configuro Kubectl para el acceso al clúster.
        subprocess.run("cd terraform && gcloud container clusters get-credentials $(terraform output -raw kubernetes_cluster_name) --region $(terraform output -raw region)", shell=True, check=True)
        print("\nSe configura el acceso al clúster de k8s.\n")
    except subprocess.CalledProcessError:
        sys.exit("Ha habido un error, por favor, revisa el código y vuelve a intentarlo.") 

# Inicio el despliegue de Kubernetes.
deploy_k8s()