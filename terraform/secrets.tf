locals {
  website_postgres_connection_url = join(
    "",
    [
      "postgres://",
      google_sql_user.website.name,
      ":",
      google_sql_user.website.password,
      "@",
      "//cloudsql/${var.gcp_project_id}:${var.gcp_region}",
      ":",
      google_sql_database_instance.omatic.name,
      "/",
      google_sql_database.database.name,
    ]
  )
}

resource "random_password" "secret_key" {
  length  = 64
  special = false
}

resource "google_secret_manager_secret" "django_settings" {
  secret_id = "django-settings"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "django_settings" {
  secret      = google_secret_manager_secret.django_settings.id
  secret_data = <<-SECRET
    DATABASE_URL=${local.website_postgres_connection_url}
    GS_BUCKET_NAME=${google_storage_bucket.statics.name}
    SECRET_KEY=${random_password.secret_key.result}
    SECRET

  lifecycle {
    create_before_destroy = true
  }
}

# resource "google_secret_manager_secret" "service_accounts" {
#   for_each = toset([
#     "website",
#     # "worker",
#   ])
#   secret_id = "${each.key}-service_account_key"

#   replication {
#     auto {}
#   }
# }

# resource "google_secret_manager_secret_version" "service_accounts" {
#   for_each    = google_secret_manager_secret.service_accounts
#   secret      = each.value.id
#   secret_data = base64decode(google_service_account_key.omatic[each.key].private_key)

#   lifecycle {
#     create_before_destroy = true
#   }
# }
