#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

# test data
TEST_URL="https://www.example.com/"
UPDATED_URL="https://www.updated-example.com/"
SHORTCODE="test123"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # no color

# check response
check_response() {
  local response="$1"
  local expected="$2"
  local message="$3"

  if [[ "$response" == *"$expected"* ]]; then
    echo -e "${GREEN}PASS:${NC} $message"
  else
    echo -e "${RED}FAIL:${NC} $message"
    echo "Expected: $expected"
    echo "Got: $response"
    exit 1
  fi
}

# test /shorten endpoint
echo "1. Testing /shorten endpoint..."
shorten_response=$(curl -s -X POST "$BASE_URL/shorten" -H "Content-Type: application/json" \
  -d "{\"url\": \"$TEST_URL\", \"shortcode\": \"$SHORTCODE\"}")
echo "Response: $shorten_response" # Debugging output
check_response "$shorten_response" "\"shortcode\":\"$SHORTCODE\"" "Shorten URL with shortcode"

# extract update_id from response
UPDATE_ID=$(echo "$shorten_response" | jq -r '.update_id')
if [[ -z "$UPDATE_ID" || "$UPDATE_ID" == "null" ]]; then
  echo -e "${RED}FAIL:${NC} Update ID not returned from /shorten"
  exit 1
fi

# test /{shortcode} redirect
echo "2. Testing /{shortcode} redirect endpoint..."
redirect_response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$SHORTCODE")
check_response "$redirect_response" "302" "Redirect using shortcode"

# test /update/{update_id}
echo "3. Testing /update/{update_id} endpoint..."
update_response=$(curl -s -X POST "$BASE_URL/update/$UPDATE_ID" -H "Content-Type: application/json" \
  -d "{\"url\": \"$UPDATED_URL\"}")
echo "Response: $update_response" # Debugging output
check_response "$update_response" "\"shortcode\":\"$SHORTCODE\"" "Update URL"

# test /{shortcode} redirect again after update
echo "4. Testing /{shortcode} redirect after update..."
redirect_updated_response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$SHORTCODE")
check_response "$redirect_updated_response" "302" "Redirect to updated URL"

# test /{shortcode}/stats
echo "5. Testing /{shortcode}/stats endpoint..."
stats_response=$(curl -s "$BASE_URL/$SHORTCODE/stats")
echo "Response: $stats_response" # Debugging output
check_response "$stats_response" "\"shortcode\":\"$SHORTCODE\"" "Fetch statistics"
check_response "$stats_response" "\"redirectCount\":2" "Verify redirect count in stats"

# done
echo -e "${GREEN}All endpoint tests passed successfully!${NC}"
