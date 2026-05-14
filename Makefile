# Variables
PYTHON_VERSION := 3.13
ENV_NAME := env

# OS detection
ifeq ($(OS),Windows_NT)
    PYTHON := python
    VENV_BIN := $(ENV_NAME)/Scripts
else
    PYTHON := python3
    VENV_BIN := $(ENV_NAME)/bin
endif

UV_PIP := $(VENV_BIN)/uv pip install --python $(VENV_BIN)/python

# Makefile pour faciliter l'utilisation du CLI Ansible
.PHONY: help install clean


help: ## Affiche cette aide
	@echo "Commandes disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Pour plus d'options, utilisez: ./cli.py --help"

create-py-env: ## Créer un nouvel environnement python
	@echo "Création d'un environnement"
	$(PYTHON) -m venv $(ENV_NAME)
	@echo "L'environnement a été créé"
	@echo "Exécuter dans votre terminal: source $(VENV_BIN)/activate"

install-packages: ## Installer les packages python complémentaires
	@echo "Installation de uv"
	$(VENV_BIN)/python -m pip install uv
	$(UV_PIP) -r requirements.txt --prerelease=allow
	@echo "✓ Installation des packages terminée"


install-pre-commit: ## Installer les pre-commits
	@echo "Installation des pre-commits"
	$(VENV_BIN)/pre-commit install


install-collections: ## Installe les collections Ansible requises
	@echo "Installation des collections Ansible ..."
	ansible-galaxy collection install -r requirements.yaml
	@echo "✓ Installation des collections terminée"

setup-dev-env: create-py-env install-packages install-pre-commit ## Installer tout l'environnement de développement

duplicate: ## Duplique les fichiers example.main.yaml vers main.yaml
	echo "Needs to be refactored"

# Nettoyage
clean: ## Nettoie les fichiers temporaires Python
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Nettoyage terminé"
