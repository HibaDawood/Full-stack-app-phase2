// frontend/src/app/api/agent/route.ts
import { NextRequest } from 'next/server';
import { pythonApiService } from '@/lib/python-executor';

export async function POST(request: NextRequest): Promise<Response> {
  try {
    const { userInput } = await request.json();

    if (!userInput) {
      return jsonResponse({ response: 'Missing user input' }, 400);
    }

    // Use HTTP API approach (recommended for production/serverless)
    // This communicates with the main backend service which now includes the chat endpoint
    // For local development, use localhost:8000
    const pythonApiBaseUrl = process.env.PYTHON_API_URL || 'https://hiba-05-todoapp-phase-2.hf.space';
    const pythonApiUrl = `${pythonApiBaseUrl}/api/chat`;  // The chat endpoint is now part of the main backend

    console.log('Using HTTP API approach:', pythonApiUrl);
    const result = await pythonApiService.executeViaHttpApi(pythonApiUrl, { userInput });

    // Handle the result
    if (!result.success) {
      console.error('Python API error:', result.error);

      // Check if it's a rate limit error
      if (result.error?.includes('429') ||
          result.error?.toLowerCase().includes('rate limit') ||
          result.error?.toLowerCase().includes('quota')) {
        return jsonResponse({
          response: "I've reached my API usage limit. Please try again later when more capacity is available."
        }, 200);
      }

      // For other errors, return a generic message
      return jsonResponse({
        response: "You have reached your API request limit. Try again later or upgrade your plan."
      }, 200);
    }

    return jsonResponse(result.data, 200);
  } catch (error: any) {
    console.error('Agent API error:', error);
    return jsonResponse({
      response: "You have reached your API request limit. Try again later or upgrade your plan."
    }, 200);
  }
}

/* ---------------- HELPERS ---------------- */

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}