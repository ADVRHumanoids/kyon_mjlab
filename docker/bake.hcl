group "default" {
  targets = ["kyon_mjlab"]
}

target "kyon_mjlab" {
  context    = ".."
  dockerfile = "docker/Dockerfile"
  tags       = ["ghcr.io/advrhumanoids/kyon_mjlab"]
  secret = ["id=netrc,env=NETRC_CONTENT"]
  args = {
    NPROC = "8"
  }
}


