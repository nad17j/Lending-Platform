# --- ENTERPRISE HARDENED CLOUD BOUNDARY NETWORK ---
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "srilanka-lending-core-2026"
  region  = "asia-south1" # Closest low-latency zone to Sri Lanka
}

# 1. THE PRODUCTION CASTLE WALLS (VPC Network)
resource "google_compute_network" "production_vpc" {
  name                    = "prod-lending-vpc"
  auto_create_subnetworks = false
}

# 2. THE PUBLIC DRAWBRIDGE SUBNET (For Frontend & API Gateway Load Balancer)
resource "google_compute_subnetwork" "public_subnet" {
  name          = "prod-public-ingress-subnet"
  ip_cidr_range = "10.0.1.0/24"
  network       = google_compute_network.production_vpc.id
  region        = "asia-south1"
}

# 3. THE PRIVATE KEEP SUBNET (Isolated Database with NO Public IP)
resource "google_compute_subnetwork" "private_subnet" {
  name          = "prod-private-database-subnet"
  ip_cidr_range = "10.0.2.0/24"
  network       = google_compute_network.production_vpc.id
  region        = "asia-south1"
  private_ip_google_access = true
}

# 4. FIREWALL PROTECTION RULES (Strict Internals Only)
resource "google_compute_firewall" "allow_internal_app_to_db" {
  name    = "allow-internal-app-to-db-traffic"
  network = google_compute_network.production_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["5432"] # Isolated PostgreSQL Port
  }

  source_ranges = ["10.0.1.0/24"] # Trust ONLY traffic originating from the public subnet
  target_tags   = ["database-node"]
}