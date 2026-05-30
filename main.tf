# GOOGLE CLOUD PROVIDER CONFIGURATION
provider "google" {
    project = "lending-platform-2026"
    region = "asia-south2"
}

# 1. VPC
resource "google_compute_network" "vpc_network" {
    name = "secure-lending-vpc"
    auto_create_subnetworks = false # Turn off auto-routes to enforce tight security controls
}

# 2. Create private subnet for data and DB
resource "google_compute_subnetwork" "private_subnet" {
    name = "private-database-subnet" 
    ip_cidr_range = "10.0.1.0/24"
    region = "asia-south2"
    ntwork = google_compute_network.vpc_network.id 
    private_ip_google_access = true
}

# 3. Create public subnet for compliance consumption API
resource 'google_compute_subnetwork" "public_subnet" {
    name = "public-api-subnet"
    ip_cidr_range = "10.0.2.0/24"
    region = "asia-south2"
    network = google_compute_network.vpc_network.id
}

# 4. Cloud armor firewall protection ruleset
resource 'google_compute_firewall" "allow_http" {
    name = "allow-monitored-api-traffic"
    network = google_compute_network.vpc_network.name
    allow {
        protocol = "tcp"
        ports  = ["8000"]
    }
    source_ranges = ["0.0.0.0./0"]
}