# Makefile pour faciliter l'utilisation du CLI Ansible
.PHONY: help install clean

# Variables
VENV = env

help: ## Affiche cette aide
	@echo "Commandes disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Pour plus d'options, utilisez: ./cli.py --help"

install-packages: ## Installe les dépendances Python uniquement
	@echo "Installation des packages Python ..."
	pip install -r requirements.txt
	@echo "✓ Installation des packages terminée"

install-collections: ## Installe les collections Ansible requises
	@echo "Installation des collections Ansible ..."
	ansible-galaxy collection install -r requirements.yaml
	@echo "✓ Installation des collections terminée"

install: install-packages install-collections ## Installe les dépendances Python et les collections Ansible

setup-env: install-packages ## Installe les dépendances et les pre-commits
	# Installer les pre-commits
	pre-commit install

duplicate: ## Duplique les fichiers example.main.yaml vers main.yaml
	echo "Needs to be refactored"

# Nettoyage
clean: ## Nettoie les fichiers temporaires Python
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Nettoyage terminé"
