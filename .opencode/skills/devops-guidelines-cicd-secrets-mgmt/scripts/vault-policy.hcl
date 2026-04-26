path "secret/data/mobile/android" {
  capabilities = ["read"]
  allowed_parameters = {
    "fields" = ["signing-keystore-password", "signing-key-alias", "signing-key-password"]
  }
}
path "secret/data/mobile/production/*" {
  capabilities = ["deny"]
}