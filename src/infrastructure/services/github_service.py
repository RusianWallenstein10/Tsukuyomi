import requests
import os
from typing import Dict, Any

class GitHubMetricsService:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Obtiene un resumen de métricas del usuario autenticado."""
        if not self.token:
            return {"error": "No GitHub Token found"}
            
        try:
            # Info de usuario
            user_response = requests.get(f"{self.base_url}/user", headers=self.headers)
            user_response.raise_for_status()
            user_data = user_response.json()
            
            # Repositorios (para contar estrellas y forks de forma precisa)
            repos_response = requests.get(f"{self.base_url}/user/repos?per_page=100&type=owner", headers=self.headers)
            repos_response.raise_for_status()
            repos = repos_response.json()
            
            total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
            total_forks = sum(repo.get("forks_count", 0) for repo in repos)
            
            return {
                "username": user_data.get("login"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "public_repos": user_data.get("public_repos"),
                "private_repos": user_data.get("total_private_repos", 0),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "followers": user_data.get("followers")
            }
        except Exception as e:
            return {"error": str(e)}
