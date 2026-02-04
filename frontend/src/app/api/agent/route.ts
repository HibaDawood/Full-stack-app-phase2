// frontend/src/app/api/agent/route.ts
import { NextRequest } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request: NextRequest): Promise<Response> {
  try {
    const { userInput } = await request.json();

    if (!userInput) {
      return jsonResponse({ error: 'Missing userInput' }, 400);
    }

    const pythonScriptPath = path.join(
      process.cwd(),
      '../mcp/gemini_agent.py'
    );

    const result = await runPythonScript(pythonScriptPath, userInput);

    if (result.error) {
      return jsonResponse(result, 500);
    }

    return jsonResponse(result, 200);
  } catch (error) {
    console.error('Agent API error:', error);
    return jsonResponse({ error: 'Internal server error' }, 500);
  }
}

/* ---------------- HELPERS ---------------- */

function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function runPythonScript(
  scriptPath: string,
  userInput: string
): Promise<any> {
  return new Promise((resolve) => {
    const pythonProcess = spawn('python', [
      scriptPath,
      JSON.stringify({ userInput }),
    ]);

    let stdoutData = '';
    let stderrData = '';

    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        resolve({
          error: stderrData || 'Python script failed',
          code,
        });
      } else {
        const parsed = extractJsonFromOutput(stdoutData);
        resolve(parsed ?? { error: 'Invalid Python response' });
      }
    });
  });
}

/* -------- JSON EXTRACTION -------- */

function safeJsonParse(str: string): any | null {
  try {
    return JSON.parse(str);
  } catch {
    try {
      return JSON.parse(str.replace(/'/g, '"'));
    } catch {
      return null;
    }
  }
}

function extractJsonFromOutput(output: string): any | null {
  const cleaned = output.trim();
  return safeJsonParse(cleaned);
}
