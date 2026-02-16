#!/usr/bin/env python3
"""
CLI pour gérer et exécuter les playbooks Ansible de façon simple et flexible.
Supporte l'exécution parallèle et la découverte automatique des playbooks.
"""

import click
import concurrent.futures
import json
import os
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


class Colors:
    """Codes ANSI pour colorer la sortie terminal"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class AnsibleCLI:
    """Classe principale pour gérer l'exécution des playbooks Ansible"""

    def __init__(self, base_dir: str | None = None):
        """
        Initialise le CLI

        Args:
            base_dir: Répertoire de base (par défaut: répertoire du script)
        """
        self.base_dir = Path(base_dir or os.path.dirname(os.path.abspath(__file__)))
        self.playbooks_dir = self.base_dir / "ansible" / "playbooks"
        self.config_file = self.base_dir / "ansible" / "playbooks.yaml"
        self.playbooks = self._discover_playbooks()

    def _discover_playbooks(self) -> Dict[str, Dict]:
        """
        Découvre automatiquement les playbooks disponibles

        Returns:
            Dictionnaire des playbooks avec leurs métadonnées
        """
        playbooks = {}

        # Charger la config si elle existe
        config = {}
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f) or {}

        # Scanner tous les fichiers .yaml/.yml dans le répertoire playbooks
        if self.playbooks_dir.exists():
            for pattern in ["*.yaml", "*.yml"]:
                for pb_path in self.playbooks_dir.glob(pattern):
                    name = pb_path.stem
                    playbooks[name] = {
                        "path": str(pb_path.relative_to(self.base_dir)),
                        "description": config.get("playbooks", {})
                        .get(name, {})
                        .get("description", ""),
                        "tags": config.get("playbooks", {})
                        .get(name, {})
                        .get("tags", []),
                        "requires": config.get("playbooks", {})
                        .get(name, {})
                        .get("requires", []),
                        "order": config.get("playbooks", {})
                        .get(name, {})
                        .get("order", 999),
                    }

        return dict(sorted(playbooks.items(), key=lambda x: x[1]["order"]))

    def list_playbooks(self, verbose: bool = False):
        """
        Liste tous les playbooks disponibles

        Args:
            verbose: Affiche les détails complets
        """
        print(f"{Colors.HEADER}{Colors.BOLD}Playbooks disponibles:{Colors.ENDC}\n")

        if not self.playbooks:
            print(
                f"{Colors.WARNING}Aucun playbook trouvé dans {self.playbooks_dir}{Colors.ENDC}"
            )
            return

        for name, info in self.playbooks.items():
            print(f"{Colors.OKBLUE}{Colors.BOLD}{name}{Colors.ENDC}")
            if verbose or info["description"]:
                print(f"  Description: {info['description'] or 'N/A'}")
                print(f"  Chemin: {info['path']}")
                if info["tags"]:
                    print(f"  Tags: {', '.join(info['tags'])}")
                if info["requires"]:
                    print(f"  Dépendances: {', '.join(info['requires'])}")
            print()

    def duplicate_example_files(self):
        """Duplique les fichiers example.main.yaml vers main.yaml"""
        print(f"{Colors.OKCYAN}Duplication des fichiers d'exemple...{Colors.ENDC}")

        count = 0
        for example_file in self.base_dir.rglob("example.main.yaml"):
            target = example_file.parent / "main.yaml"
            if not target.exists():
                import shutil

                shutil.copy2(example_file, target)
                print(
                    f"{Colors.OKGREEN}✓{Colors.ENDC} Créé: {target.relative_to(self.base_dir)}"
                )
                count += 1
            else:
                print(
                    f"{Colors.WARNING}→{Colors.ENDC} Existe déjà: {target.relative_to(self.base_dir)}"  # noqa
                )

        print(f"\n{Colors.OKGREEN}{count} fichier(s) créé(s){Colors.ENDC}\n")

    def _run_playbook(
        self,
        playbook_name: str,
        inventory: str = "localhost",
        extra_vars: Dict | None = None,
        tags: List[str] | None = None,
        skip_tags: List[str] | None = None,
        dry_run: bool = False,
        verbose: int = 0,
    ) -> Tuple[str, int, str, str]:
        """
        Exécute un playbook Ansible

        Args:
            playbook_name: Nom du playbook
            inventory: Fichier d'inventaire ou hôte
            extra_vars: Variables supplémentaires
            tags: Tags à exécuter
            skip_tags: Tags à ignorer
            dry_run: Mode simulation (--check)
            verbose: Niveau de verbosité (0-3)

        Returns:
            Tuple (playbook_name, return_code, stdout, stderr)
        """
        if playbook_name not in self.playbooks:
            return (playbook_name, 1, "", f"Playbook '{playbook_name}' non trouvé")

        playbook_path = self.base_dir / self.playbooks[playbook_name]["path"]

        cmd = ["ansible-playbook", "-i", inventory, str(playbook_path)]

        if dry_run:
            cmd.append("--check")

        if verbose > 0:
            cmd.append("-" + "v" * min(verbose, 4))

        if extra_vars:
            cmd.extend(["--extra-vars", json.dumps(extra_vars)])

        if tags:
            cmd.extend(["--tags", ",".join(tags)])

        if skip_tags:
            cmd.extend(["--skip-tags", ",".join(skip_tags)])

        start_time = datetime.now()
        print(
            f"{Colors.OKCYAN}[{start_time.strftime('%H:%M:%S')}] Démarrage: {playbook_name}{Colors.ENDC}"  # noqa
        )

        try:
            result = subprocess.run(
                cmd, cwd=self.base_dir, capture_output=True, text=True
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            if result.returncode == 0:
                print(
                    f"{Colors.OKGREEN}[{end_time.strftime('%H:%M:%S')}] ✓ Succès: {playbook_name} ({duration:.1f}s){Colors.ENDC}"  # noqa
                )
            else:
                print(
                    f"{Colors.FAIL}[{end_time.strftime('%H:%M:%S')}] ✗ Échec: {playbook_name} ({duration:.1f}s){Colors.ENDC}"  # noqa
                )

            return (playbook_name, result.returncode, result.stdout, result.stderr)

        except Exception as e:
            end_time = datetime.now()
            print(
                f"{Colors.FAIL}[{end_time.strftime('%H:%M:%S')}] ✗ Erreur: {playbook_name} - {str(e)}{Colors.ENDC}"  # noqa
            )
            return (playbook_name, 1, "", str(e))

    def run_playbooks(
        self,
        playbook_names: List[str],
        parallel: bool = False,
        max_workers: int = 4,
        **kwargs,
    ) -> List[Tuple[str, int, str, str]]:
        """
        Exécute un ou plusieurs playbooks

        Args:
            playbook_names: Liste des noms de playbooks
            parallel: Exécution parallèle
            max_workers: Nombre de workers pour l'exécution parallèle
            **kwargs: Arguments passés à _run_playbook

        Returns:
            Liste des résultats (playbook_name, return_code, stdout, stderr)
        """
        # Résoudre les dépendances et l'ordre
        ordered_playbooks = self._resolve_dependencies(playbook_names)

        print(f"\n{Colors.HEADER}{Colors.BOLD}Plan d'exécution:{Colors.ENDC}")
        for i, name in enumerate(ordered_playbooks, 1):
            print(f"  {i}. {name}")
        print()

        results = []

        if parallel and len(ordered_playbooks) > 1:
            print(
                f"{Colors.BOLD}Mode parallèle activé (max {max_workers} workers){Colors.ENDC}\n"
            )
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                futures = {
                    executor.submit(self._run_playbook, name, **kwargs): name
                    for name in ordered_playbooks
                }
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
        else:
            print(f"{Colors.BOLD}Mode séquentiel{Colors.ENDC}\n")
            for name in ordered_playbooks:
                print(kwargs)
                results.append(self._run_playbook(name, **kwargs))

        return results

    def _resolve_dependencies(self, playbook_names: List[str]) -> List[str]:
        """
        Résout les dépendances et ordonne les playbooks

        Args:
            playbook_names: Liste des playbooks demandés

        Returns:
            Liste ordonnée avec dépendances
        """
        resolved = []
        seen = set()

        def add_with_deps(name: str):
            if name in seen or name not in self.playbooks:
                return

            # Ajouter d'abord les dépendances
            for dep in self.playbooks[name].get("requires", []):
                add_with_deps(dep)

            if name not in seen:
                resolved.append(name)
                seen.add(name)

        for name in playbook_names:
            add_with_deps(name)

        return resolved

    def print_summary(self, results: List[Tuple[str, int, str, str]]):
        """
        Affiche un résumé des exécutions

        Args:
            results: Liste des résultats d'exécution
        """
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}RÉSUMÉ{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

        success_count = sum(1 for _, rc, _, _ in results if rc == 0)
        fail_count = len(results) - success_count

        for name, return_code, stdout, stderr in results:
            status = (
                f"{Colors.OKGREEN}✓ SUCCÈS{Colors.ENDC}"
                if return_code == 0
                else f"{Colors.FAIL}✗ ÉCHEC{Colors.ENDC}"
            )
            print(f"  {status} - {name}")

            if return_code != 0 and stderr:
                print(f"{Colors.FAIL}  Erreur: {stderr}{Colors.ENDC}")

        print(
            f"\n{Colors.BOLD}Total: {len(results)} | Succès: {Colors.OKGREEN}{success_count}{Colors.ENDC} | Échecs: {Colors.FAIL}{fail_count}{Colors.ENDC}\n"  # noqa
        )


# Contexte global pour partager l'instance CLI
pass_cli = click.make_pass_decorator(AnsibleCLI, ensure=True)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """CLI pour gérer et exécuter les playbooks Ansible.

    Supporte l'exécution parallèle, la gestion des dépendances et
    la découverte automatique des playbooks.
    """
    # Initialiser le CLI et le stocker dans le contexte
    ctx.obj = AnsibleCLI()

    # Si aucune commande n'est fournie, afficher l'aide
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="Affichage détaillé")
@pass_cli
def ls(cli_obj, verbose):
    """Liste les playbooks disponibles."""
    cli_obj.list_playbooks(verbose=verbose)


@cli.command()
@pass_cli
def duplicate(cli_obj):
    """Duplique les fichiers example.main.yaml vers main.yaml."""
    cli_obj.duplicate_example_files()


@cli.command()
@click.argument("playbooks", nargs=-1)
@click.option("--all", is_flag=True, help="Exécuter tous les playbooks")
@click.option(
    "-i",
    "--inventory",
    default="localhost",
    help="Fichier d'inventaire (défaut: localhost)",
)
@click.option(
    "-e", "--extra-vars", type=str, help="Variables supplémentaires (format JSON)"
)
@click.option("-t", "--tags", help="Tags à exécuter (séparés par des virgules)")
@click.option("--skip-tags", help="Tags à ignorer (séparés par des virgules)")
@click.option("-p", "--parallel", is_flag=True, help="Exécution parallèle")
@click.option(
    "--max-workers",
    type=int,
    default=4,
    help="Nombre de workers parallèles (défaut: 4)",
)
@click.option("-c", "--dry-run", is_flag=True, help="Mode simulation (--check)")
@click.option("-v", "--verbose", count=True, help="Niveau de verbosité (-v, -vv, -vvv)")
@click.option("--show-output", is_flag=True, help="Afficher la sortie complète")
@pass_cli
def run(
    cli_obj: AnsibleCLI,
    playbooks,
    all,
    inventory,
    extra_vars,
    tags,
    skip_tags,
    parallel,
    max_workers,
    dry_run,
    verbose,
    show_output: bool = True,
):
    """Exécute un ou plusieurs playbooks.

    Exemples:

    \b
      # Exécuter un playbook
      ansible_cli.py run postgresql-service

    \b
      # Exécuter plusieurs playbooks en parallèle
      ansible_cli.py run airflow n8n --parallel

    \b
      # Exécuter tous les playbooks
      ansible_cli.py run --all

    \b
      # Mode dry-run avec verbosité
      ansible_cli.py run airflow --dry-run -vv

    \b
      # Avec variables supplémentaires
      ansible_cli.py run airflow -e '{"version": "2.0"}'
    """
    if not playbooks and not all:
        click.secho(
            "Erreur: Spécifiez des playbooks ou utilisez --all", fg="red", err=True
        )
        raise click.Abort()

    playbook_names = list(cli_obj.playbooks.keys()) if all else list(playbooks)

    # Valider que tous les playbooks existent
    invalid = [name for name in playbook_names if name not in cli_obj.playbooks]
    if invalid:
        click.secho(
            f"Erreur: Playbooks non trouvés: {', '.join(invalid)}", fg="red", err=True
        )
        click.echo(f"\nPlaybooks disponibles: {', '.join(cli_obj.playbooks.keys())}")
        raise click.Abort()

    # Parser les extra-vars si fournies
    parsed_extra_vars = None
    if extra_vars:
        try:
            parsed_extra_vars = json.loads(extra_vars)
        except json.JSONDecodeError as e:
            click.secho(
                f"Erreur: Format JSON invalide pour --extra-vars: {e}",
                fg="red",
                err=True,
            )
            raise click.Abort()

    # Exécuter
    results = cli_obj.run_playbooks(
        playbook_names,
        parallel=parallel,
        max_workers=max_workers,
        inventory=inventory,
        extra_vars=parsed_extra_vars,
        tags=tags.split(",") if tags else None,
        skip_tags=skip_tags.split(",") if skip_tags else None,
        dry_run=dry_run,
        verbose=verbose,
    )

    # Afficher les sorties si demandé
    if show_output:
        print(f"\n{Colors.HEADER}{Colors.BOLD}SORTIE DÉTAILLÉE{Colors.ENDC}\n")
        for name, rc, stdout, stderr in results:
            print(f"\n{Colors.BOLD}=== {name} ==={Colors.ENDC}")
            if stdout:
                print(stdout)
            if stderr:
                print(f"{Colors.FAIL}{stderr}{Colors.ENDC}")

    # Afficher le résumé
    cli_obj.print_summary(results)

    # Code de sortie
    if any(rc != 0 for _, rc, _, _ in results):
        sys.exit(1)


def main():
    """Point d'entrée principal du CLI"""
    cli()


if __name__ == "__main__":
    main()
