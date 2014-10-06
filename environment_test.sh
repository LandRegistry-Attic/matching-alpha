export SETTINGS='config.Config'
# Here we'll create a test database, and override the database to the test values.
set +o errexit
createuser -s matching_test
createdb -U matching_test -O matching_test matching_test -T template0
set -e

export DATABASE_URL="postgresql://localhost/matching_test"
