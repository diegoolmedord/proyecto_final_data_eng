import os
import subprocess
from dotenv import load_dotenv
from prefect import flow, task

# Cargar las variables de entorno desde el archivo .env de la raíz
load_dotenv()

@task(name="Validar Entorno y Credenciales", retries=1)
def check_environment():
    """Valida que el token de MotherDuck esté disponible en la sesión."""
    token = os.getenv("motherduck_token")
    if not token:
        raise ValueError("ERROR: No se encontró la variable 'motherduck_token' en el archivo .env")
    print("Variable 'motherduck_token' detectada correctamente para dbt.")
    return token

@task(name="Limpiar Caché de dbt", log_prints=True)
def dbt_clean():
    """Ejecuta dbt clean para eliminar artefactos antiguos."""
    print("Borrando artefactos temporales y carpetas target de dbt...")
    result = subprocess.run("dbt clean", shell=True, capture_output=True, text=True, env=os.environ)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("Falló la ejecución de dbt clean")

@task(name="Instalar Dependencias (dbt deps)", log_prints=True)
def dbt_deps():
    """Descarga e instala los paquetes declarados en packages.yml."""
    print("Instalando paquetes y dependencias (dbt-expectations)...")
    result = subprocess.run("dbt deps", shell=True, capture_output=True, text=True, env=os.environ)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("Falló la ejecución de dbt deps")

@task(name="Ejecutar Transformaciones y Tests (dbt build)", log_prints=True)
def dbt_build():
    """Ejecuta el build completo de los modelos y data tests en MotherDuck."""
    print("Iniciando la compilación y ejecución del linaje en MotherDuck...")
    result = subprocess.run("dbt build", shell=True, capture_output=True, text=True, env=os.environ)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("Falló la ejecución de dbt build. Revisar errores de compilación o fallos de tests.")

@flow(name="Pipeline Analítico: dbt + MotherDuck", log_prints=True)
def fuzzy_factory_pipeline():
    """Flujo principal de Prefect que coordina la ejecución analítica."""
    print("Iniciando el Orquestador Prefect...")
    
    # 1. Validar entorno
    check_environment()
    
    # 2. Borrado preventivo
    dbt_clean()
    
    # 3. Rehidratar los paquetes eliminados (¡La pieza que faltaba!)
    dbt_deps()
    
    # 4. Compilación, carga y validación final
    dbt_build()
    
    print("¡Pipeline ejecutado con éxito! Los modelos y tests están sincronizados en MotherDuck.")

if __name__ == "__main__":
    fuzzy_factory_pipeline()