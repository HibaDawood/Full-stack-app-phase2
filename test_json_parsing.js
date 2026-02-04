// Test script to verify JSON parsing logic
function safeJsonParse(str) {
  try {
    return JSON.parse(str);
  } catch (e) {
    // If standard JSON parsing fails, try to convert single quotes to double quotes
    // This is a simplified conversion - only handles basic cases
    try {
      // Replace single quotes with double quotes, but be careful not to replace
      // quotes inside string values
      const convertedStr = str.replace(/'/g, '"');
      return JSON.parse(convertedStr);
    } catch (conversionError) {
      // If conversion also fails, return null
      return null;
    }
  }
}

function extractJsonFromOutput(output) {
  // First, try to parse the entire output as JSON
  let result = safeJsonParse(output.trim());
  if (result !== null) {
    return result;
  }

  // If that fails, try to extract JSON from mixed content
  // Look for JSON objects in the output, handling potential API errors

  // First, try to find JSON ignoring error lines
  const lines = output.split('\n');
  let cleanedOutput = '';

  // Process each line to find potential JSON responses
  for (const line of lines) {
    const trimmedLine = line.trim();

    // Skip lines that are clearly error messages (but not JSON responses that might contain similar terms)
    if (trimmedLine.startsWith('Error parsing user request') ||
        (trimmedLine.startsWith('Error:') && !trimmedLine.includes('"response"') && !trimmedLine.includes('"error"')) ||
        (trimmedLine.includes('RESOURCE_EXHAUSTED') && !trimmedLine.includes('"response"') && !trimmedLine.includes('"error"')) ||
        (trimmedLine.includes('rate-limits') && !trimmedLine.includes('"response"') && !trimmedLine.includes('"error"'))) {
      continue;
    } else {
      // Keep lines that might contain JSON
      cleanedOutput += line + '\n';
    }
  }

  // Try to extract JSON from the cleaned output
  const jsonRegex = /\{[\s\S]*?\}(?=\s*$|,\s*|\s*[}\]]|$)/g;
  const matches = cleanedOutput.match(jsonRegex);

  if (matches) {
    // Try to parse each match, starting with the last one (most likely to be the actual response)
    for (let i = matches.length - 1; i >= 0; i--) {
      const parsed = safeJsonParse(matches[i].trim());
      if (parsed !== null && (parsed.hasOwnProperty('response') || parsed.hasOwnProperty('error'))) {
        return parsed;
      }
    }
  }

  // If the above didn't work, try the original approach on the full output
  const fullOutputMatches = output.match(/\{[\s\S]*\}/g);

  if (fullOutputMatches) {
    // Try to parse each match, starting with the last one (most likely to be the actual response)
    for (let i = fullOutputMatches.length - 1; i >= 0; i--) {
      const parsed = safeJsonParse(fullOutputMatches[i].trim());
      if (parsed !== null && (parsed.hasOwnProperty('response') || parsed.hasOwnProperty('error'))) {
        return parsed;
      }
    }
  }

  return null;
}

// Test cases
console.log("Testing JSON parsing logic...\n");

// Test 1: Normal response
const test1 = '{"response": "Task deleted successfully."}';
console.log("Test 1 - Normal response:", extractJsonFromOutput(test1));

// Test 2: Mixed output with error
const test2 = `Error parsing user request: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details.', 'status': 'RESOURCE_EXHAUSTED'}}
{"response": "Error processing general query: 429 RESOURCE_EXHAUSTED."}`;
console.log("Test 2 - Mixed output with error:", extractJsonFromOutput(test2));

// Test 3: Multiple JSON objects
const test3 = `{"response": "Some response"}
Error parsing user request: 429 RESOURCE_EXHAUSTED.
{"error": "Rate limit exceeded"}`;
console.log("Test 3 - Multiple JSON objects:", extractJsonFromOutput(test3));

// Test 4: Only error messages
const test4 = `Error parsing user request: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'Quota exceeded.'}}`;
console.log("Test 4 - Only error messages:", extractJsonFromOutput(test4));

// Test 5: Mixed output with single quotes
const test5 = `Error parsing user request: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details.', 'status': 'RESOURCE_EXHAUSTED'}}
{"response": "Error processing general query: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details.', 'status': 'RESOURCE_EXHAUSTED'}}"}`;
console.log("Test 5 - Mixed output with single quotes:", extractJsonFromOutput(test5));

console.log("\nAll tests completed.");