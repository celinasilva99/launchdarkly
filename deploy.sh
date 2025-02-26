#!/bin/bash
set -e

echo "Deploying with LaunchDarkly Project Key: ${PROJECT_KEY} and Feature Flag Key: ${FEATURE_FLAG_KEY}"

# Example API call to LaunchDarkly
curl -H "Authorization: Bearer $LAUNCHDARKLY_API_KEY" \
     -X POST "https://app.launchdarkly.com/api/v2/flags/$PROJECT_KEY/$FEATURE_FLAG_KEY"
