resource "google_project_iam_member" "project_editors" {
  for_each = toset(var.gcp_project_editors)
  project  = var.gcp_project_id
  role     = "roles/editor"
  member   = "user:${each.value}"
}

locals {
  service_account_ids = {
    "website"               = "Digital membership frontend website"
    # "worker-pubsub-invoker" = "Digital membership pubsub to worker invoker"
    # "worker"                = "Digital membership background worker"
  }
}

resource "time_rotating" "mykey_rotation" {
  rotation_days = 30
}

resource "google_service_account" "omatic" {
  for_each     = local.service_account_ids
  account_id   = each.key
  display_name = each.value
}

# resource "google_service_account_key" "omatic" {
#   for_each = toset([
#     "website",
#     # "worker",
#   ])
#   service_account_id = google_service_account.omatic[each.value].name

#   keepers = {
#     rotation_time = time_rotating.mykey_rotation.rotation_rfc3339
#   }

#   lifecycle {
#     create_before_destroy = true
#   }
# }

resource "google_cloud_run_service_iam_policy" "omatic" {
  for_each = google_cloud_run_service.omatic
  location = each.value.location
  project  = each.value.project
  service  = each.value.name

  policy_data = data.google_iam_policy.omatic[each.key].policy_data
}

data "google_iam_policy" "omatic" {
  for_each = local.cloud_run_services
  binding {
    role    = "roles/run.invoker"
    members = each.value.invokers
  }
}

data "google_iam_policy" "omatic_secret_access" {
  binding {
    role = "roles/secretmanager.secretAccessor"
    members = [
      "serviceAccount:${google_service_account.omatic["website"].email}",
      # "serviceAccount:${google_service_account.omatic["worker"].email}",
    ]
  }
}

# resource "google_project_iam_member" "worker_pubsub_invoker_token_creator" {
#   #ts:skip=accurics.gcp.IAM.137 Unable to figure out how this is suppose to work otherwise...
#   project = var.gcp_project_id
#   role    = "roles/iam.serviceAccountTokenCreator"
#   member  = "serviceAccount:${google_service_account.omatic["worker-pubsub-invoker"].email}"
# }

# resource "google_project_service_identity" "pubsub" {
#   provider = google-beta

#   project = google_project.omatic.project_id
#   service = "pubsub.googleapis.com"
# }

# resource "google_service_account_iam_member" "worker_pubsub_invoker_token_creator" {
#   provider           = google-beta
#   service_account_id = google_project_service_identity.pubsub.id
#   role               = "roles/iam.serviceAccountTokenCreator"
#   member             = "serviceAccount:${google_service_account.omatic["worker-pubsub-invoker"].email}"
# }

resource "google_project_iam_binding" "omatic_cloudsql_clients" {
  project = var.gcp_project_id
  for_each = toset([
    "roles/cloudsql.instanceUser",
    "roles/cloudsql.client",
  ])
  role = each.value
  members = [
    "serviceAccount:${google_service_account.omatic["website"].email}",
    # "serviceAccount:${google_service_account.omatic["worker"].email}",

  ]
}

resource "google_project_iam_binding" "omatic_trace_agents" {
  project = var.gcp_project_id
  role    = "roles/cloudtrace.agent"
  members = [
    "serviceAccount:${google_service_account.omatic["website"].email}",
    # "serviceAccount:${google_service_account.omatic["worker"].email}",
  ]
}
# resource "google_project_iam_member" "omatic_log_writer" {
#   project = var.gcp_project_id
#   role    = "roles/logging.logWriter"
#   member  = "serviceAccount:${google_service_account.omatic["website"].email}"
# }

# resource "google_project_iam_member" "omatic_trace_agent" {
#   project = var.gcp_project_id
#   role    = "roles/cloudtrace.agent"
#   member  = "serviceAccount:${google_service_account.omatic["website"].email}"
# }
resource "google_service_account_iam_binding" "allow_sa_impersonation_tokens" {
  service_account_id = google_service_account.omatic["website"].name
  role               = "roles/iam.serviceAccountTokenCreator"
  members            = [for u in var.gcp_project_editors : "user:${u}"]
}

resource "google_service_account_iam_binding" "allow_sa_impersonation" {
  service_account_id = google_service_account.omatic["website"].name
  role               = "roles/iam.serviceAccountUser"
  members            = [for u in var.gcp_project_editors : "user:${u}"]
}
