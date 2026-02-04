// Debug script to understand JSON parsing logic
function extractJsonFromOutput(output) {
  console.log("Processing output:", output);
  
  // First, try to parse the entire output as JSON
  try {
    console.log("Trying to parse entire output as JSON");
    const result = JSON.parse(output.trim());
    console.log("Success parsing entire output:", result);
    return result;
  } catch (e) {
    console.log("Failed to parse entire output as JSON");
    
    // If that fails, try to extract JSON from mixed content
    // Look for JSON objects in the output, handling potential API errors
    
    // First, try to find JSON ignoring error lines
    const lines = output.split('\n');
    let cleanedOutput = '';
    
    console.log("Processing", lines.length, "lines");
    
    // Process each line to find potential JSON responses
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmedLine = line.trim();
      console.log(`Line ${i}: "${trimmedLine}"`);
      
      // Skip lines that are clearly error messages
      if (trimmedLine.includes('Error parsing user request') || 
          trimmedLine.includes('RESOURCE_EXHAUSTED') ||
          trimmedLine.includes('rate-limits') ||
          trimmedLine.startsWith('Error:') ||
          (trimmedLine.includes('error') && trimmedLine.includes('RESOURCE_EXHAUSTED'))) {
        console.log(`Skipping error line ${i}`);
        continue;
      } else {
        // Keep lines that might contain JSON
        console.log(`Keeping line ${i} for JSON extraction`);
        cleanedOutput += line + '\n';
      }
    }
    
    console.log("Cleaned output:", cleanedOutput);
    
    // Try to extract JSON from the cleaned output
    const jsonRegex = /\{[\s\S]*?\}(?=\s*$|,\s*|\s*[}\]]|$)/g;
    const matches = cleanedOutput.match(jsonRegex);
    
    console.log("Matches from cleaned output:", matches);
    
    if (matches) {
      // Try to parse each match, starting with the last one (most likely to be the actual response)
      for (let i = matches.length - 1; i >= 0; i--) {
        try {
          const parsed = JSON.parse(matches[i].trim());
          console.log("Parsed match:", parsed);
          // Check if this looks like a valid response from our Python script
          if (parsed.hasOwnProperty('response') || parsed.hasOwnProperty('error')) {
            console.log("Found valid response/error object:", parsed);
            return parsed;
          }
        } catch (parseError) {
          console.log("Failed to parse match:", matches[i], "Error:", parseError.message);
          continue; // Try the next match
        }
      }
    }
    
    // If the above didn't work, try the original approach on the full output
    const fullOutputMatches = output.match(/\{[\s\S]*\}/g);
    console.log("Full output matches:", fullOutputMatches);

    if (fullOutputMatches) {
      // Try to parse each match, starting with the last one (most likely to be the actual response)
      for (let i = fullOutputMatches.length - 1; i >= 0; i--) {
        try {
          const parsed = JSON.parse(fullOutputMatches[i].trim());
          console.log("Parsed full match:", parsed);
          // Check if this looks like a valid response from our Python script
          if (parsed.hasOwnProperty('response') || parsed.hasOwnProperty('error')) {
            console.log("Found valid response/error object in full matches:", parsed);
            return parsed;
          }
        } catch (e) {
          console.log("Failed to parse full match:", fullOutputMatches[i], "Error:", e.message);
          continue; // Try the next match
        }
      }
    }

    console.log("Returning null - no valid JSON found");
    return null;
  }
}

// Test case that was failing
const test2 = `Error parsing user request: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details.', 'status': 'RESOURCE_EXHAUSTED'}}
{"response": "Error processing general query: 429 RESOURCE_EXHAUSTED."}`;

console.log("Test 2 - Mixed output with error:", extractJsonFromOutput(test2));