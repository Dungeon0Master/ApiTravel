"""
manage.py — Entry point de comandos Django.
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamificacion.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se puede importar Django. ¿Está el entorno virtual activo "
            "y Django instalado?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
