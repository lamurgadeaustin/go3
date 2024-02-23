terraform {
  backend "gcs" {
    bucket = "murga-o-matic-tfstate"
    prefix = "bootstrap"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 3.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.8.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.4.3"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = "us-central1"
}

# resource "google_app_engine_application" "murga_o_matic" {
#   project     = google_project.murga_o_matic.project_id
#   location_id = regexall("[-a-z]+", var.gcp_region)[0]
# }

# TODO: hook this up with a bot user's oauth creds (not jeffwecan...)
# resource "google_sourcerepo_repository" "murga_o_matic" {
#   name = "github_${replace(var.github_repo, "/", "_")}"
# }
