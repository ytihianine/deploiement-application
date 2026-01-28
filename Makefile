# Makefile pour faciliter l'utilisation du CLI Ansible
.PHONY: help install list duplicate run-all test clean

# Variables
CLI = python3 cli.py
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

list: ## Liste tous les playbooks disponibles
	$(CLI) list

list-verbose: ## Liste les playbooks avec détails complets
	$(CLI) list -v

duplicate: ## Duplique les fichiers example.main.yaml vers main.yaml
	$(CLI) duplicate

# Exécution des playbooks
run-postgres: ## Déploie PostgreSQL (service + users)
	$(CLI) run postgresql-service postgresql-users

run-airflow: ## Déploie Airflow
	$(CLI) run airflow

run-chartsgouv: ## Déploie Charts Gouv (Superset)
	$(CLI) run chartsgouv

run-n8n: ## Déploie n8n
	$(CLI) run n8n

run-all: ## Déploie tous les playbooks en séquentiel
	$(CLI) run --all

run-all-parallel: ## Déploie tous les playbooks en parallèle
	$(CLI) run --all --parallel

# Commandes de test
dry-run-all: ## Teste tous les playbooks en mode dry-run
	$(CLI) run --all --dry-run

test: dry-run-all ## Alias pour dry-run-all

# Déploiement complet
deploy: duplicate run-all ## Setup complet: duplique les fichiers et déploie tout

# Nettoyage
clean: ## Nettoie les fichiers temporaires Python
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Nettoyage terminé"
