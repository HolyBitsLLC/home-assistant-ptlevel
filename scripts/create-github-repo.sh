#!/usr/bin/env bash
# Run these commands locally (or in your environment authenticated to GitHub)
# to create the repo under holybitsllc and grant the 'agents' team write access.

set -euo pipefail

ORG="holybitsllc"
REPO="home-assistant-ptlevel"
TEAM="agents"

echo "==> Creating repo ${ORG}/${REPO} ..."
gh repo create "${ORG}/${REPO}" \
  --public \
  --description "Home Assistant custom integration for PTLevel wireless tank monitors" \
  --homepage "https://github.com/${ORG}/${REPO}"

echo "==> Granting team '${TEAM}' push (write) access ..."
# The team must already exist in the org.
gh api \
  --method PUT \
  "repos/${ORG}/${REPO}/teams/${TEAM}" \
  -f permission=push

echo "==> Done. Verify at https://github.com/${ORG}/${REPO}/settings/access"
